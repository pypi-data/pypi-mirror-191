import numpy as np
from pyrateshield.gui.main_view import MainView, TOOLBOX_LAYOUT
from pyrateshield.model import Model
from PyQt5.QtWidgets import QApplication
from pyrateshield.gui.mpl_controller import MplController
from pyrateshield.dosemapper import Dosemapper
from pyrateshield.model_items import Wall
from pyrateshield.gui.context_menu import ContextMenuController
from pyrateshield.gui.critical_point_controller import CriticalPointReportController
from pyrateshield.floorplan_and_dosemap import Floorplan, Geometry
from pyrateshield.gui import io, calculator, dosemap_style, isotopes

from pyrateshield.gui.item_controllers import (EditSourceXrayController, 
                                               EditSourceCTController, 
                                               EditWallsController, 
                                               EditCriticalPointsController, 
                                               EditSourcesNMController, 
                                               EditShieldingController,
                                               EditClearanceModel,
                                               EditPixelSizeController,
                                               EditMaterialsController)
                                                                                              
from pyrateshield import labels
    
class MainController():
    _mpl_controller = None
    _critical_points_controller = None
    _calculator = None
    _dosemap_style = None
    
    def __init__(self, dosemapper=None, model=None, view=None):
        
        if dosemapper is None:
            dosemapper = Dosemapper(multi_cpu=True)
        
        if model is None:
            model = Model()
    
        if view is None:
            view = MainView()
        
        self.dosemapper = dosemapper
        self.view = view
        
        if model is None:
            model = self.get_empty_model()
        
        self._model = model
        self.connect_model()
        
        self.controllers = self.create_controllers()
        
        self.set_view_callbacks()
        
        self.context_menu_controller = ContextMenuController(view=self.view,
                             mpl_controller=self.mpl_controller,
                             model=model,
                             main_controller=self)
        
        self.controllers[labels.SHIELDINGS].view.setEnabled(True)
        
        
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        if model is self.model:
            return
        elif self.model is not None:
            self.disconnect_model()
            
        self._model = model
        self.load_model()
        self.connect_model()
        
    def disconnect_model(self):
        self._mpl_controller = None
        self.model.item_selector.disconnect(self)
    
    def load_model(self):
        for key, controller in self.controllers.items():
            controller.model = self.model

        self.mpl_controller.model = self.model
        self.context_menu_controller.model = self.model
        self.crit_point_controller.model = self.model
        
        
    def connect_model(self):
        self.model.item_selector.connect(self, 
                                         self.model.item_selector.EVENT_SELECT_ITEM,
                                         self.select_item_in_view)
        
    def select_item_in_view(self, model_item):
        if model_item is not None:
            self.view.set_focus(model_item.label)
        
    def set_view_callbacks(self):
        for label, tab in self.view.toolbox_tabs.items():            
            if len(TOOLBOX_LAYOUT[label]) > 1:                
                tab.currentChanged.connect(self.tab_selected)
                
        self.view.toolbox.currentChanged.connect(self.toolbox_selected)

        # {develop}
        mouse = self.mpl_controller.mouse
        mouse.connect(self, mouse.MOVE_EVENT, self.view.set_status_text)
        
        toolbar = self.view.views[labels.CANVAS].toolbar
        toolbar.connect(self, toolbar.EVENT_TOOLBUTTON_CLICK, 
                        self.toolbar_callback)    
        

      
    @property
    def controller_types(self):
        return {
                labels.SOURCES_CT:        EditSourceCTController,
                labels.SOURCES_XRAY:      EditSourceXrayController,
                labels.SOURCES_NM:        EditSourcesNMController,
                labels.CLEARANCE:         EditClearanceModel,
                labels.WALLS:             EditWallsController,
                labels.SHIELDINGS:        EditShieldingController,
                labels.CRITICAL_POINTS:   EditCriticalPointsController,
                labels.PIXEL_SIZE_CM:     EditPixelSizeController,
                labels.MATERIALS:         EditMaterialsController}       

        
    def create_controllers(self):
        self.mpl_controller = MplController(dosemapper=self.dosemapper,
                                            view=self.view.views[labels.CANVAS],
                                            model=self.model)
        
        self.crit_point_controller = CriticalPointReportController(
            view=self.view.views[labels.CRITICAL_POINT_REPORT_VIEW], model=self.model, 
            controller=self, dosemapper=self.dosemapper)
        
    
        controllers = {}
        for key in (labels.SOURCES_NM, labels.SOURCES_CT, 
                   labels.CLEARANCE, labels.SOURCES_XRAY, labels.WALLS, 
                   labels.CRITICAL_POINTS, labels.PIXEL_SIZE_CM, 
                   labels.SHIELDINGS, labels.MATERIALS):

            contr_type = self.controller_types[key]
            view = self.view.views[key]
            controllers[key] = contr_type(model=self.model, 
                                          view = view,
                                          mpl_controller=self.mpl_controller)
        return controllers

    
        
    def toolbox_selected(self, _=None):
        self.tab_selected()
        
        
    def tab_selected(self, _=None):
        label = self.view.get_active_tool_panel_name()
        selected_item = self.model.item_selector.selected_item
        
        if label in [labels.SHIELDINGS] and isinstance(selected_item, Wall):
            wall = self.controllers[labels.WALLS].get_item_in_view()
            if wall is not None:
                shielding = self.model.shieldings.get_shielding_by_name(
                    wall.shielding)
                self.controllers[label].model_to_view(shielding)
        
        if label in [labels.CLEARANCE]:
            source_nm = self.controllers[labels.SOURCES_NM].get_item_in_view()
            if source_nm is not None:
                clearance = self.model.clearances.get_item_by_name(
                    source_nm.clearance)
                self.controllers[label].model_to_view(clearance)
        
        if label != labels.PIXEL_SIZE_CM:
            model_item = self.controllers[label].get_item_in_view()

            self.controllers[labels.PIXEL_SIZE_CM].hide_pixelsize_line()
            self.model.item_selector.select_item(model_item)
            

        else:
            self.controllers[labels.PIXEL_SIZE_CM].show_pixelsize_line()
            
            
        self.controllers[label].refresh()
        



    def toolbar_callback(self, event_data):
        toolname, checked = event_data
    
        if toolname == 'side_panel':
            self.view.toolbox.setVisible(checked)
        elif toolname == 'save_project_as':
            self.save_as()
        elif toolname == 'load_project':
            self.load()
        elif toolname == 'save_project':
            self.save()
        elif toolname == 'load_image':
            self.load_image()
        elif toolname == 'new':
            self.new()
        elif toolname == 'calculator':
            self.show_calculator()
        elif toolname == 'dosemap_style':
            self.show_dosemap_style()
        elif toolname == labels.ISOTOPES:
            self.show_isotopes()
           
          
            
    def load_image(self):
       image = io.safe_load_image()
       if image is not None:
           # Load floorplan and reset pixel size (geometry)
           self.model.floorplan.image = image
                              
           
           # self.controllers[labels.PIXEL_SIZE_CM].refresh()
           self.view.set_focus(labels.PIXEL_SIZE_CM)
           
    def new(self):        
        confirm = io.confirm_new_project()
        if confirm:
            self.model = self.get_empty_model()
        self.view.set_focus(labels.SOURCES_NM)
        
            
    def save(self):
        io.safe_write_model(model=self.model, 
                                        filename=self.model.filename)
            
    def save_as(self):
        io.safe_write_model(model=self.model)
               
    def load(self):
        model = io.safe_load_model(self.model.filename)
        
        if model is not None:        
 
            self.model = model
   
            
    def show_calculator(self):
        self._calculator = calculator.Controller()
        self._calculator.view.show()
    
    def show_dosemap_style(self):
        self._dosemap_style = dosemap_style.Controller(self.model)
        self._dosemap_style.view.show() 
        
    def show_isotopes(self):
        self._isotopes = isotopes.Controller()
        self._isotopes.view.show()
        
        
    def get_empty_model(self):
        default_empty_size_y = 1E2 # empty canvas number of pixels in y
        default_empty_size_cm = (1E4, 1E4) # default new size in cm
        
        shape_cm = (default_empty_size_cm)
        
        
        pixel_size = shape_cm[1] / default_empty_size_y
        
              
        # rounds pixels in x down, should not matter for large arrays
        shape_pixels = (int(shape_cm[0] / pixel_size), 
                        int(shape_cm[1] / pixel_size), 3)

        empty_canvas = np.ones(shape_pixels)
        
        geometry = Geometry(pixel_size_cm=pixel_size,
                            locked=True)
    
        floorplan_model = Floorplan(image=empty_canvas, geometry=geometry)
                                    
        
        return Model(floorplan=floorplan_model)
        

       
def main(model=None, controller=None, dm=None):
        app = QApplication([])
        
        controller = MainController(model=model, dosemapper=dm)
        window = controller.view
        window.show()    
        app.exec_()
    
if __name__ == "__main__":  
    from pyrateshield.dosemapper import Dosemapper

    
    project = '../../example_projects/SmallProject/project.zip'
    
    #project = '../../example_projects/LargeProject/project.zip'
    
    model = Model.load_from_project_file(project)
    
    app = QApplication([])
    
    controller = MainController(model=model, dosemapper=None)
    window = controller.view
    window.show()    
    app.exec_()
        

