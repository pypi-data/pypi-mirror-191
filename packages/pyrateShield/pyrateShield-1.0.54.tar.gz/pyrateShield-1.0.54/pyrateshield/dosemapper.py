import multiprocessing
from multiprocessing.sharedctypes import Value as mpValue
import ctypes
import queue
import time
import psutil
from pyrateshield.constants import CONSTANTS
from pyrateshield import labels, Logger, GLOBAL_LOG_LEVEL
from pyrateshield.radtracer import radtracer
from pyrateshield.pyshield.engine import Engine
import pandas as pd

LOG_LEVEL = GLOBAL_LOG_LEVEL

UNSUPPORTED_PYSHIELD_ISOTOPES = ['Y-90']
CRITICAL_POINT_NAME         = 'Critical Point Name'
RADTRACER_DOSE              = 'RadTracer Dose [mSv]'
PYSHIELD_DOSE               = 'PyShield Dose [mSv]'
OCCUPANCY_FACTOR            = 'Occupancy factor'
RADTRACER_DOSE_CORRECTED    = 'RadTracer Dose corrected for occupancy [mSv]'
PYSHIELD_DOSE_CORRECTED     = 'PyShield Dose corrected for occupancy [mSv]'
SOURCE_NAME                 = 'Source Name'

COLUMNS = [CRITICAL_POINT_NAME, PYSHIELD_DOSE, RADTRACER_DOSE, 
           OCCUPANCY_FACTOR, PYSHIELD_DOSE_CORRECTED, RADTRACER_DOSE_CORRECTED]

SPLIT_COLUMNS = [CRITICAL_POINT_NAME, SOURCE_NAME, PYSHIELD_DOSE, 
                 RADTRACER_DOSE, OCCUPANCY_FACTOR, 
                 RADTRACER_DOSE_CORRECTED, PYSHIELD_DOSE_CORRECTED]



def is_supported_by_pyshield(src):
    supported = CONSTANTS.pyshield_supported_isotopes
    return src.label == labels.SOURCES_NM and src.isotope in supported


def is_supported_by_radtracer(src):
    supported = CONSTANTS.radtracer_supported_isotopes
    return src.label != labels.SOURCES_NM or src.isotope in supported



class Worker(multiprocessing.Process, Logger):
    def __init__(self, project_queue, source_queue, dosemap_queue, update_flag, stop_flag):
        multiprocessing.Process.__init__(self)
        Logger.__init__(self, log_level=LOG_LEVEL)
        
        self.project_queue = project_queue
        self.source_queue = source_queue
        self.dosemap_queue = dosemap_queue
        self.update_flag = update_flag
        self.stop_flag = stop_flag        
    
    def update_project(self):        
        # MS: To use dosemapper when radtracer does not (yet) support all
        # isotopes, alwayse prepare the engine regardless of engine settings.
        # sources not (yet) supported by radtracer will go through the engine
        self.pyshield_engine = Engine.from_pyrateshield(self.project)
    
       
    def get_radtracer_dosemap(self, source):
        if is_supported_by_radtracer(source):
            return radtracer.dosemap_single_source(source, self.project)
        elif is_supported_by_pyshield(source): # fallback to pyshield
            print(f'Source {source.name} not supported by radtracer, will use pyshield')   
            return self.pyshield_engine.source_dosemap(source)

    def get_pyshield_dosemap(self, source):
        if is_supported_by_pyshield(source):    
            return self.pyshield_engine.source_dosemap(source)
        elif is_supported_by_radtracer(source): # fallback to radtracer
            # Xray will go through radtracer any how no need to warn
            if source.label == labels.SOURCES_NM:
                print(f'Source {source.name} not supported by pyshield, will use radtracer')
            return radtracer.dosemap_single_source(source, self.project)
    
    def get_dosemap(self, source):
        # Pyshield set as engine
        if self.project.dosemap.engine == labels.PYSHIELD:
            return self.get_pyshield_dosemap(source)
        # Radtracer set as engine
        elif self.project.dosemap.engine == labels.RADTRACER:
            return self.get_radtracer_dosemap(source)
            
            
    
    def get_dosemap2(self, source):
        if self.project.dosemap.engine == labels.PYSHIELD:
            return self.pyshield_engine.source_dosemap(source)
        elif self.project.dosemap.engine == labels.RADTRACER:
            return radtracer.dosemap_single_source(source, self.project)
            
    def run(self):
        while not self.stop_flag.value:            
            try:
                sources = self.source_queue.get(timeout=0.1)
            except queue.Empty:
                sources = None
            
            if self.update_flag.value:
                self.project = self.project_queue.get()
                self.update_project()
                self.update_flag.value = False
                self.logger.info(f'{self.name}, Updated project')
        
            if sources is not None:                
                for source in sources:                    
                    self.dosemap_queue.put( self.get_dosemap(source) )
                    
        self.logger.info(f'{self.name}, Stopped')


class Dosemapper(Logger):
    def __init__(self, processes=None, multi_cpu=True):
        Logger.__init__(self, log_level=LOG_LEVEL)
        
        self.multi_cpu = multi_cpu
        
        if self.multi_cpu:
            self.source_queue = multiprocessing.Queue()
            self.dosemap_queue = multiprocessing.Queue()
            self._workers = []
            
            self.max_cpu_count = 4 #psutil.cpu_count(logical=True)
            if processes is None:
                processes = psutil.cpu_count(logical=False)
            self.set_workers(processes)
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._stop_workers()
    
    def update_project(self, project):
        # Make sure all worker processes are done updating from a previous call
        # to this method before updating again.
        while any( w.update_flag.value for w in self._workers ):
            time.sleep(0.1)
        
        for w in self._workers:
            w.project_queue.put(project)
            w.update_flag.value = True

    @staticmethod
    def get_single_cpu_dosemap(project, sources=None):
        # DEBUGGING Purpuses
        if sources is None:
            sources = list(project.sources_nm) + list(project.sources_ct)\
                + list(project.sources_xray)
                
        dosemap = None        
        update_dosemap = lambda dm: dm if dosemap is None else (dosemap + dm)
            
        
        pyshield_engine = Engine.from_pyrateshield(project)
         
        for source in sources:
            if not source.enabled:
                continue
            if project.dosemap.engine == labels.PYSHIELD:
                if  is_supported_by_pyshield(source):                
                    source_dosemap = pyshield_engine.source_dosemap(source)
                else:
                    source_dosemap = radtracer.dosemap_single_source(source, project)
                    
            elif project.dosemap.engine == labels.RADTRACER:
                if is_supported_by_radtracer(source):
                    source_dosemap = radtracer.dosemap_single_source(source, project)
                else:
                    source_dosemap = pyshield_engine.source_dosemap(source)
        
            dosemap = update_dosemap(source_dosemap)
        return dosemap
 
    def get_dosemap(self, project, sources=None):

        if not self.multi_cpu:
            return self.get_single_cpu_dosemap(project, sources)
        # Process all sources by default
        if sources is None:
            sources = list(project.sources_nm) + list(project.sources_ct) + list(project.sources_xray)
        
        # Exclude sources which are not set to Enabled
        sources = [src for src in sources if src.enabled]
        
        # Check if there is any work to be done
        if not len(sources):
            return None

        
        # Sources with the same position are processed by the same worker.
        # This allows PyShield to benefit from caching.
        # MS: Group sources by default won't affect radtracer
            
        src_pos_dct = {}

        for source in sources:
            # Make a dictionary of source_positions and group the corresponding sources
            # I.e.: { (x,y,z): [src1, src2, src3 ], (x,y,z): [src4, src5, ... ] }
            src_pos_dct.setdefault(tuple(source.position), []).append(source)
            
        sources_grouped = [srcs for srcs in src_pos_dct.values()]
        
        
                       
        self.update_project(project)
        
        for grp in sources_grouped:
            self.source_queue.put(grp)
        
        # Collect the results. Make sure to get as many results from the queue
        # as the number of sources
        nr_of_sources = sum(len(grp) for grp in sources_grouped)
                
        dosemap = None        
        update_dosemap = lambda dm: dm if dosemap is None else (dosemap + dm)
        
        for i in range(nr_of_sources):
            dosemap = update_dosemap( self.dosemap_queue.get() )        
        
        return dosemap        
    
    
    @staticmethod
    def empty_critical_point_result():
        return pd.DataFrame([{CRITICAL_POINT_NAME:      None,
                              SOURCE_NAME:              None,
                              RADTRACER_DOSE:           None,
                              PYSHIELD_DOSE:            None,
                              OCCUPANCY_FACTOR:         None,
                              RADTRACER_DOSE_CORRECTED: None,
                              PYSHIELD_DOSE_CORRECTED:  None
                              }])
    @staticmethod
    def get_source_critical_point_result(source, 
                                         critical_point, 
                                         dose_radtracer, 
                                         dose_pyshield):
        
        factor = critical_point.occupancy_factor
        
        return {CRITICAL_POINT_NAME:        critical_point.name,
                SOURCE_NAME:                source.name,
                RADTRACER_DOSE:             dose_radtracer,
                PYSHIELD_DOSE:              dose_pyshield,
                OCCUPANCY_FACTOR:           factor,
                RADTRACER_DOSE_CORRECTED:   factor * dose_radtracer,
                PYSHIELD_DOSE_CORRECTED:    factor * dose_pyshield}
                              
        
    @staticmethod
    def get_sources_critical_points(project):
        sources = list(project.sources_nm) + list(project.sources_ct) + list(project.sources_xray)
        
        # Exclude sources which are not set to Enabled
        sources = [src for src in sources if src.enabled]
        
        # Exclude points which are not set to Enabled
        crit_points = [crp for crp in project.critical_points if crp.enabled]
                
        if len(crit_points) == 0 or len(sources) == 0:            
            return Dosemapper.empty_critical_point_result()
        
        reports = []        
        
        pyshield_engine = Engine.from_pyrateshield(project)
        
        for crit_point in crit_points:            
            for source in sources:
                if is_supported_by_radtracer(source):
                    dose_radtracer = radtracer.pointdose_single_source(
                        crit_point.position, source, project)
                else:
                    # At least one isotope not supported by radtracer
                    dose_radtracer = None
                
                if is_supported_by_pyshield(source):
                    dose_pyshield = pyshield_engine.dose_at_point(crit_point.position,
                                                         sources=[source])
                else:
                    dose_pyshield = None
                    
                if dose_radtracer is None and dose_pyshield is None:
                    raise RuntimeError
                elif dose_radtracer is None:
                    dose_radtracer = dose_pyshield
                elif dose_pyshield is None:
                    dose_pyshield = dose_radtracer
                    
                
                reports += [Dosemapper.get_source_critical_point_result(
                    source, crit_point, dose_radtracer, dose_pyshield)]
        report = pd.DataFrame(reports)[SPLIT_COLUMNS]
        
        return report
        
    @staticmethod
    def get_critical_points(project):
        
        
        if len(project.sources_nm) + len(project.sources_ct) + len(project.sources_xray) == 0\
            or len(project.critical_points) == 0:
                return Dosemapper.empty_critical_point_result()
            
        report = Dosemapper.get_sources_critical_points(project)
        
        aggfunc = {RADTRACER_DOSE: sum, RADTRACER_DOSE_CORRECTED: sum,
                   PYSHIELD_DOSE: sum, PYSHIELD_DOSE_CORRECTED: sum,
                   OCCUPANCY_FACTOR: max}
        
        summed_report = pd.pivot_table(report, index=CRITICAL_POINT_NAME, 
                                       aggfunc=aggfunc)
        
        # preserve order
        pnames = [crit_point.name for crit_point in project.critical_points\
                  if crit_point.enabled]
            
        summed_report = summed_report.reindex(pnames)
        
        summed_report = summed_report.reset_index()
       
        summed_report = summed_report[COLUMNS]
        return summed_report

    @property
    def n_workers(self):
        return len(self._workers)
    
    
    def set_workers(self, processes):
        if processes > self.max_cpu_count:
            self.logger.info(f"Max nr of parallel processes: {self.max_cpu_count}")
            processes = self.max_cpu_count
        if processes < 0:
            processes = 0
        
        
        if processes > self.n_workers:
            self._start_workers(processes - self.n_workers)
        elif processes < self.n_workers:
            self._stop_workers(self.n_workers - processes)
    
    
    def _start_workers(self, processes=None):
        self.logger.info(f"Starting {processes} workers")
        
        for i in range(processes):
            project_queue = multiprocessing.Queue()
            stop_flag = mpValue(ctypes.c_bool, False)
            update_flag = mpValue(ctypes.c_bool, False)
            args = (
                project_queue,
                self.source_queue,
                self.dosemap_queue,
                update_flag,
                stop_flag,
            )
            p = Worker(*args)            
            self._workers.append(p)
            p.start()
        
        
    def _stop_workers(self, processes=None):
        if processes is None:
            processes = self.n_workers
        
        stopworkers = [self._workers.pop() for i in range(processes)]
                    
        for w in stopworkers:
            w.stop_flag.value = True
        for w in stopworkers: 
            w.join()
        time.sleep(0.1)
        for w in stopworkers:
            if w.is_alive():
                self.logger.info("Stil alive")
            w.close()
        
            
if __name__ == "__main__":
    from pyrateshield.model import Model
    import timeit
    import time
    #model = Model.load_from_project_file('/Users/marcel/git/pyrateshield/example_projects/LargeProject/large_project.psp')
    #model = Model.load_from_project_file('../example_projects/LargeProject/large_project.psp')
    #model = Model.load_from_project_file('../example_projects/SmallProject/project.zip')
    model = Model.load_from_project_file('../example_projects/Stabin/Tb-161.zip')
    #model = Model.load_from_project_file('../example_projects/Lu-177.psp')
    model.dosemap.grid_matrix_size = 120
    
    # with Dosemapper() as dm:        
    #     model.dosemap.engine = labels.PYSHIELD
    #     print("PyShield", timeit.timeit(lambda: dm.get_dosemap(model), number=1) )
    
    #     time.sleep(1) 
    #     print()
        
    #     model.dosemap.engine = labels.RADTRACER
    #     print("Radtracer", timeit.timeit(lambda: dm.get_dosemap(model), number=1) )
        
    report = Dosemapper.get_critical_points(model)

    # from pyshield import Sources
    # sources = Sources.from_pyrateshield(model)
    # print("Pyshield single CPU:", end=" ", flush=True)
    # print(timeit.timeit(lambda: sources.get_dosemap(), number=1) )
    
    
    
    

