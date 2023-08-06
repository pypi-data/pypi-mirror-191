import os
import zipfile
import io
import yaml
import pickle
import copy
import imageio


from pyrateshield.constants import CONSTANTS
from pyrateshield import model_items
from pyrateshield.model_sequences import (ClearanceItemSequence, 
                                          ModelItemSequence, 
                                          NamedModelItemSequence, 
                                          ShieldingItemSequence,
                                          MaterialItemSequence)

from pyrateshield.floorplan_and_dosemap import Dosemap, Floorplan, DosemapStyle
from pyrateshield import labels, Observable, GLOBAL_LOG_LEVEL



LOG_LEVEL = GLOBAL_LOG_LEVEL
#LOG_LEVEL = 10

class Defaults:
    def __init__(self):
        try:
            wdir = os.path.split(__file__)[0] 
        except:
            wdir = os.getcwd()
            
        self._defaults = yaml.safe_load(open(os.path.join(wdir, 'defaults.yml')))
        
        clearances = self._defaults[labels.CLEARANCE]
        clearances = [model_items.Clearance.from_dict(item) for item in clearances]
        self.clearances = clearances
        
        materials = self._defaults[labels.MATERIALS]
        materials = [model_items.Material.from_dict(item) for item in materials]
        self.materials = materials
        
        shieldings = self._defaults[labels.SHIELDINGS]
        shieldings = [model_items.Shielding.from_dict(item) for item in shieldings]
        self.shieldings = shieldings
        

DEFAULTS = Defaults()


class Model(Observable):
    filename            = None
    
    _floorplan          = None
    _selected_item      = None    
    _sources_nm         = None
    _sources_ct         = None
    _sources_xray       = None
    _walls              = None
    _clearances         = None
    _shieldings         = None
    _critical_points    = None
    _floorplan          = None
    _dosemap            = None
    _dosemap_style      = None
    _materials          = None
    
    EVENT_UPDATE_FLOORPLAN = 'event_update_floorplan'    
    
    def __init__(self, 
                 floorplan          =None, 
                 dosemap            =None, 
                 dosemap_style      =None, 
                 shieldings         =None, 
                 walls              =None, 
                 critical_points    =None, 
                 sources_ct         =None, 
                 sources_nm         =None, 
                 sources_xray       =None,
                 clearances         =None, 
                 materials          =None):  
        

        Observable.__init__(self, log_level=LOG_LEVEL)
        # create empty model possibility for gui
        
        
        self.constants = CONSTANTS
        
        self._floorplan = floorplan
        self._dosemap = dosemap
        self._dosemap_style = dosemap_style
        
        if walls is not None:
            self.walls.extend(walls)
            
        if critical_points is not None:
            self.critical_points.extend(critical_points)
        
        if sources_ct is not None:
            self.sources_ct.extend(sources_ct)
            
        if sources_xray is not None:
            self.sources_xray.extend(sources_xray)

        if sources_nm is not None:
            self.sources_nm.extend(sources_nm)
            
        if clearances is not None:
            self.clearances.extend(clearances)
        else:
            self.clearances.extend(DEFAULTS.clearances)
            
        if materials is not None:
            self.materials.extend(materials)
        else:
            self.materials.extend(DEFAULTS.materials)
        
        if shieldings is not None:
            self.shieldings.extend(shieldings)
        else:
            self.shieldings.extend(DEFAULTS.shieldings)
            
        # force origin at (0, 0), shift older pyrateshield models
        self.zero_origin()
        self.match_extent_to_floorplan()
        self.set_callbacks()
        
        self.item_selector = ModelItemSelector(self)
        
    @property
    def floorplan(self):
        if self._floorplan is None:
            self._floorplan = Floorplan()
        return self._floorplan
    
    @floorplan.setter
    def floorplan(self, floorplan):
        self._floorplan = floorplan
    
    @property
    def dosemap(self):
        if self._dosemap is None:
            self._dosemap = Dosemap()
        return self._dosemap
            
    @property
    def dosemap_style(self):
        if self._dosemap_style is None:
            self._dosemap_style = DosemapStyle()
        return self._dosemap_style
        
    @property
    def walls(self):
        if self._walls is None:
            self._walls = ModelItemSequence(item_class=model_items.Wall)
        return self._walls
    
    @property
    def shieldings(self):
        if self._shieldings is None:
            self._shieldings = ShieldingItemSequence(item_class=model_items.Shielding)
        return self._shieldings
    
    @property
    def critical_points(self):
        if self._critical_points is None:
            self._critical_points = NamedModelItemSequence(item_class=model_items.CriticalPoint)
        return self._critical_points
    
    @property
    def sources_nm(self):
        if self._sources_nm is None:
            self._sources_nm = NamedModelItemSequence(item_class=model_items.SourceNM)
        return self._sources_nm
    
    @property
    def clearances(self):
        if self._clearances is None:
            self._clearances = ClearanceItemSequence(item_class=model_items.Clearance)
        return self._clearances
    
  
    
   
    @property
    def materials(self):
        if self._materials is None:
            self._materials = MaterialItemSequence(item_class=model_items.Material)
        return self._materials
    
    

    @property
    def sources_ct(self):
        if self._sources_ct is None:
            self._sources_ct = NamedModelItemSequence(item_class=model_items.SourceCT)
        return self._sources_ct
            
    @property
    def sources_xray(self):
        if self._sources_xray is None:
            self._sources_xray = NamedModelItemSequence(item_class=model_items.SourceXray)
        return self._sources_xray
    
            
        
    def zero_origin(self):
        # old psp files had an origin option, origin is now always at (0, 0)
        
        origin = self.floorplan.geometry.origin_cm
        
        if origin[0] != 0 or origin[1] != 0:
            self.shift_cm(origin[0], origin[1])
            self.floorplan.geometry.origin_cm = [0, 0]
            
        
    def __str__(self):
        return yaml.dump(self.to_dict())
        
        
    def set_callbacks(self):

        self.shieldings.connect(self, self.shieldings.EVENT_UPDATE_ITEM,
                                self.update_shielding)
        
        self.clearances.connect(self, self.clearances.EVENT_UPDATE_ITEM,
                                self.update_clearance)
        
        self.materials.connect(self, self.materials.EVENT_UPDATE_ITEM,
                               self.update_material)
        
    def remove_item(self, item):
        container = self.sequence_for_item(item)
        container.remove(item)
        
    def update_material(self, event_data):
        # called when a material is changed. Check for change in name
        # and update the references for all walls
        self.logger.debug(f'Update material with event_data {str(event_data)}')
        item, label, old_value, value = event_data
        if label == labels.NAME:
            for shielding in self.shieldings:
                materials = shielding.materials
                update = False
                if len(materials) > 0 and old_value == materials[0][0]:
                    update = True
                    materials[0][0] = value
                if len(materials) > 1 and old_value == materials[1][0]:
                    update = True
                    materials[1][0] = value
                
                if update:
                    shielding.materials = materials
                
        
    def update_shielding(self, event_data):
        # called when a shielding is changed. Check for change in name
        # and update the references for all walls
        self.logger.debug(f'Update shielding with event_data {str(event_data)}')
        item, label, old_value, value = event_data

        
            
        if label == labels.NAME:
            # name of shielding changed!
            
            #update references in walls to ensure a consistent model
            for wall in self.walls:
                if wall.shielding == old_value:                    
                    wall.shielding = value
    
        # If shielding color or linewidth changed generate event for walls
        elif label == labels.COLOR:
            
            for wall in self.walls:
                if wall.shielding == item.name:
                    event_data = (wall, labels.COLOR, item.color, item.color)
                    wall.emit(wall.EVENT_UPDATE, event_data)
                    
        elif label == labels.LINEWIDTH:
         
            for wall in self.walls:
                if wall.shielding == item.name:
                    event_data = (wall, labels.LINEWIDTH, item.linewidth, item.linewidth)
                    wall.emit(wall.EVENT_UPDATE, event_data)
                    
    def update_clearance(self, event_data):
        self.logger.debug(f'Update shielding with event_data {str(event_data)}')
        item, label, old_value, value = event_data

        if label == labels.NAME:
            # name of shielding changed!
            
            #update references in sources nm to ensure a consistent model
            for item in self.sources_nm:
                if item.clearance == old_value:                    
                    item.clearance = value
                    
    def add_item(self, item):
        # add a item of any type used by gui
        sequence = self.sequence_for_item(item)
        sequence.append(item)
            
        
    def shift_cm(self, dx_cm, dy_cm):

         self._shift_walls_cm(dx_cm, dy_cm)
         self._shift_sources_cm(dx_cm, dy_cm)
         
    def _shift_walls_cm(self, shiftx, shifty):
         for wall in self.walls:
             vertices = copy.deepcopy(wall.vertices)
             vertices[0][0] += shiftx
             vertices[1][0] += shiftx
             vertices[0][1] += shifty
             vertices[1][1] += shifty
             
             self.logger.debug('Shift Wall form {wall.vertices}')
             wall.vertices = vertices
             
    def _shift_sources_cm(self, shiftx, shifty):
        
        
         containers = [self.critical_points, self.sources_nm,
                       self.sources_xray, self.sources_ct]
         
         for container in containers:
             for item in container:
                 position = item.position.copy()
                 position[0] += shiftx   
                 position[1] += shifty
                 item.position = position
                 
    def get_sequence_by_label(self, label):
        if label == labels.SOURCES_CT:
            return self.sources_ct
        elif label == labels.SOURCES_XRAY:
            return self.sources_xray
        elif label == labels.SOURCES_NM:
            return self.sources_nm
        elif label == labels.CRITICAL_POINTS:
            return self.critical_points
        elif label == labels.SHIELDINGS:
            return self.shieldings
        elif label == labels.WALLS:
            return self.walls
        elif label == labels.FLOORPLAN:
            return self.floorplan
        elif label == labels.DOSEMAP:
            return self.dosemap
        elif label == labels.CLEARANCE:
            return self.clearances
        elif label == labels.MATERIALS:
            return self.materials
        else:
            raise KeyError(label)

    def sequence_for_item(self, item):
        return self.get_sequence_by_label(item.label)
    
    def match_extent_to_floorplan(self):
        self.dosemap.extent = self.floorplan.extent
        
    @classmethod
    def from_dict(cls, dct): 
        floorplan = Floorplan.from_dict(dct[labels.FLOORPLAN])

        dosemap_dct = dct.get(labels.DOSEMAP, None)
        
        if dosemap_dct is not None:
            dosemap = Dosemap.from_dict(dosemap_dct)
        else:
            dosemap = None
            
        material_lst = dct.get(labels.MATERIALS, None)
        if material_lst is not None:
            materials = [model_items.Material.from_dict(item) for item in material_lst]
        else:
            materials = None
            
        
        
        dosemap_style = DosemapStyle.from_dict(
                                        dct.get(labels.DOSEMAP_STYLE, None))
        
        
        
        shieldings = [model_items.Shielding.from_dict(item)\
                      for item in dct[labels.SHIELDINGS]]
            
            
        walls = [model_items.Wall.from_dict(item)\
                 for item in dct[labels.WALLS]]
            
            
        critical_points = [model_items.CriticalPoint.from_dict(item)\
                           for item in dct[labels.CRITICAL_POINTS]]
            
        # clearances are not present in older versions (psp files)
        # ClearanceItemSequence.from_dict resolves compatability and must
        # be called before loading sources_nm
        
        clearances = ClearanceItemSequence.from_dict(dct)
        
            
        sources_ct = [model_items.SourceCT.from_dict(item)\
                      for item in dct[labels.SOURCES_CT]]
            
        sources_nm = [model_items.SourceNM.from_dict(item)\
                      for item in dct[labels.SOURCES_NM]]

        sources_xray = [model_items.SourceXray.from_dict(item)\
                        for item in dct[labels.SOURCES_XRAY]]
            
        
            
            
       
            
            
        
        model = cls(floorplan=floorplan, 
                    dosemap=dosemap, 
                    dosemap_style=dosemap_style, 
                    shieldings=shieldings, 
                    walls=walls, 
                    critical_points=critical_points, 
                    sources_ct=sources_ct, 
                    sources_nm=sources_nm, 
                    sources_xray=sources_xray, 
                    clearances=clearances,
                    materials=materials)

        return model
    
        
    def to_dict(self):
        floorplan = self.floorplan.to_dict()
        dosemap = self.dosemap.to_dict()
        dosemap_style = self.dosemap_style.to_dict()
        
    
        
        walls           = [wall.to_dict()   for wall    in self.walls]        
        critical_points = [item.to_dict()   for item    in self.critical_points]        
        sources_ct      = [source.to_dict() for source  in self.sources_ct]
        sources_nm      = [source.to_dict() for source  in self.sources_nm]
        sources_xray    = [source.to_dict() for source  in self.sources_xray]
        
        # remove the default / empty item
        shieldings      = [item.to_dict()   for item    in self.shieldings[1:]]
        clearances      = [item.to_dict()   for item    in self.clearances[1:]]
        materials       = [item.to_dict()   for item    in self.materials[1:]]
        
            
        return {labels.FLOORPLAN:           floorplan,
                labels.DOSEMAP:             dosemap,
                labels.DOSEMAP_STYLE:       dosemap_style,
                labels.SHIELDINGS:          shieldings,
                labels.WALLS:               walls,
                labels.SOURCES_NM:          sources_nm,
                labels.SOURCES_XRAY:        sources_xray,
                labels.SOURCES_CT:          sources_ct,
                labels.CRITICAL_POINTS:     critical_points,
                labels.CLEARANCE:           clearances,
                labels.MATERIALS:           materials}
    
    


    def save_to_project_file(self, filename):    
        file, ext = os.path.splitext(filename)
        if ext.lower() != '.zip':
            filename = file + '.zip' # force saving old projects to ext zip
        
        self.filename = filename
                        
        project_dict = self.to_dict()
        image = project_dict[labels.FLOORPLAN].pop(labels.IMAGE)
        
        temp_yml = io.StringIO()
        yaml.dump(project_dict, temp_yml, default_flow_style=None)
        
        temp_img = io.BytesIO()
        imageio.imwrite(temp_img, image, format=".png")

        with zipfile.ZipFile(filename, "w") as zf:
            zf.writestr("project.yml", temp_yml.getvalue())
            zf.writestr("floorplan.png", temp_img.getvalue())
    
    
    @classmethod
    def load_from_project_file(cls, filename):
        try:
            with zipfile.ZipFile(filename) as zf:
                with zf.open("floorplan.png", "r") as f:
                    image = imageio.imread(f)
                with zf.open("project.yml", "r") as f:
                    dct = yaml.safe_load(f)
                 
                
                dct[labels.FLOORPLAN][labels.IMAGE] = image
                model = cls.from_dict(dct)
                
        
        except zipfile.BadZipFile:
            ### For backwards compatibility:
            success = False
            if filename.endswith(".psp"):
                try:
                    model = cls.load_old_psp_file(filename)
                    success = True
                except:
                    pass
                
            if not success:
                # IOError is picked up by GUI to show error dlg
                raise IOError(f'Could not read {filename}')
    
        model.filename = filename
        return model
    
    @classmethod
    def load_old_psp_file(cls, filename):
        ### For backwards compatibility:
        with open(filename, 'rb') as fp:
            dct = pickle.load(fp)
        
        image = dct.pop("IMAGE_DATA")   
        dct[labels.FLOORPLAN][labels.IMAGE] = image
        dct[labels.FLOORPLAN].pop('Filename', None)
        
        # ugly code to remove invalid key from older versions
        dct[labels.FLOORPLAN][labels.GEOMETRY].pop(False, False)
        
        return cls.from_dict(dct)
        

class ModelItemSelector(Observable):
    model = None
    EVENT_SELECT_ITEM = 'event_select_item'
    _selected_item = None
    
    
    def __init__(self, model=None):
        Observable.__init__(self)
        self.connect_model(model)
        
    def disconnect_model(self):
        for container in (self.model.shieldings, 
                          self.model.walls, 
                          self.model.critical_points,
                          self.model.sources_nm, 
                          self.model.sources_ct, 
                          self.model.sources_xray,
                          self.model.clearances):
            
            container.disconnect(self)
    
    def connect_model(self, model):
        if self.model is not None:
            self.disconnect_model()
        
        self.model = model
        

        for container in (self.model.shieldings, 
                          self.model.walls, 
                          self.model.critical_points,
                          self.model.sources_nm, 
                          self.model.sources_ct, 
                          self.model.sources_xray,
                          self.model.clearances):
            
            container.connect(self, container.EVENT_ADD_ITEM, self.item_added)
            
            container.connect(self, container.EVENT_WILL_REMOVE_ITEM, 
                              self.will_remove_item)
    
    def item_added(self, item):
        # make new item the selected item always
        self.select_item(item)
        
        
    def will_remove_item(self, item):
        # called just before removal of item
        if self.selected_item is item:
            # change selected item to something sensible
            container = self.model.sequence_for_item(item)
            index = container.index(item)
            if len(container) > 1:
                if index == 0:
                    new_selected_item = container[1]
                else:
                    new_selected_item = container[index-1]
            else:
                new_selected_item = None 
            
            self.select_item(new_selected_item)
            
    def select_item(self, item):
        # if item is self._selected_item:
        #     return
        self._selected_item = item
        self.emit(self.EVENT_SELECT_ITEM, self.selected_item)   
        
        
        
    @property
    def selected_item(self):
        return self._selected_item


if __name__ == "__main__":
    # import yaml
    # with open('test_model_in.yml') as file:
    #     dct = yaml.safe_load(file)
    # model = Model.from_dict(dct)
    file = '../example_projects/LargeProject/project.zip'
    # file = 'C:/Users/757021/git/pyrateshield/example_projects/Nucleaire Geneeskunde.psp'
    model = Model.load_from_project_file(file)
    
