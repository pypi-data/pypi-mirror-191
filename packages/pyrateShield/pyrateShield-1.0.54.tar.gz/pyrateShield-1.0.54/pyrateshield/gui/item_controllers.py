from pyrateshield import labels, Observable
from pyrateshield.gui.mpl_view import PointClicker, MovePointByMouse
from pyrateshield.logger import Logger, GLOBAL_LOG_LEVEL
from pyrateshield.floorplan_and_dosemap import Geometry, MeasuredGeometry
from pyrateshield.gui.item_views import safe_set_value_to_widget
from pyrateshield.model_items import Material
from pyrateshield.gui.io import pixelsize_error
import numpy as np

import qtawesome as qta
LOG_LEVEL = GLOBAL_LOG_LEVEL
#LOG_LEVEL = 10

class ModelUpdateController(Logger):
    _model = None
    def __init__(self, model=None, view=None, mpl_controller=None,
                 log_level=LOG_LEVEL):        
        super().__init__(log_level=LOG_LEVEL)
        self.view = view
        self.model = model        
        self.mpl_controller = mpl_controller
        self.set_view_callbacks()
         
    def set_view_callbacks(self):
        pass
        
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
        
        self.connect_model()
        
    def model_to_view(self, item=None):
        pass
    
    def connect_model(self):
        pass
    
    def disconnect_model(self):
        self.model.item_selector.disconnect(self)
        
class EditPixelSizeController(ModelUpdateController):
    _geometry = None
    distance_pixels = None
    
    
    def set_view_callbacks(self):
        self.view.measure_button.clicked.connect(self.measure)
        
        self.view.connect(self, self.view.EVENT_VIEW_UPDATE,
                          self.update_pixel_size)
        
        self.view.connect(self, self.view.EVENT_GEOMETRY_RADIO_BUTTON,
                          self.geometry_change)
        
        self.view.confirm_button.clicked.connect(self.confirm)
                                              
        self.refresh()
        
    def refresh(self):
        # HACK, line item may be renewed for new projects etc.
        # call this method before pixel size widget becomes active
        self.model_to_view()
        
        if self not in self.mpl_line_item.model_item.callbacks.keys():
            event = self.mpl_line_item.model_item.EVENT_UPDATE
            callback = self.update_distance_pixels
            self.mpl_line_item.model_item.connect(self, event, callback)

        
        self.logger.debug(self.model.floorplan.geometry.__class__.__name__)
    
    def show_pixelsize_line(self):
        if isinstance(self.model.floorplan.geometry, MeasuredGeometry):
            self.mpl_controller.mpl_items.pixel_size.select()
            self.mpl_controller.mpl_items.pixel_size.enable_pick()
        else:
            self.hide_pixelsize_line()
    
    def hide_pixelsize_line(self):
        self.mpl_controller.mpl_items.pixel_size.deselect()
        self.mpl_controller.mpl_items.pixel_size.disable_pick()
    
                
    def geometry_change(self, _=None):
        if self.view.choose_fixed.isChecked():
            self.hide_pixelsize_line()
        else:
            self.show_pixelsize_line()
    
    def update_pixel_size(self, event_data):
       
        if event_data == labels.REAL_WORLD_DISTANCE_CM:
            self.pixel_size_cm = self.get_measured_pixel_size()
        
    def update_distance_pixels(self, event_data):
        self.logger.debug('Update pixel distance!')
        model_item, label, old_value, value = event_data
        vv = np.asarray(model_item.vertices)
        distance_cm = np.linalg.norm(vv[0] - vv[1])
        distance_pixels = distance_cm / self.model.floorplan.geometry.pixel_size_cm
        
        self.distance_pixels = float(distance_pixels)
        
        
        self.pixel_size_cm = self.get_measured_pixel_size()
        
    @property
    def mpl_line_item(self):
        return self.mpl_controller.mpl_items.pixel_size
        
        
    @property
    def pixel_size_cm(self):
        if self.view.choose_fixed.isChecked():
            return self.view.pixel_size.value()
        else:
            return self.get_measured_pixel_size()
        
    def get_measured_pixel_size(self):
        try:
            return self.distance_cm / self.distance_pixels
        except (ZeroDivisionError, TypeError):
            return 1
            
    @pixel_size_cm.setter
    def pixel_size_cm(self, value):
        if self.view.choose_fixed.isChecked():
            safe_set_value_to_widget(self.view.pixel_size, value)
        else:
            safe_set_value_to_widget(self.view.pixel_size_measured, value)
        
    @property
    def distance_cm(self):
        try:
            return self.view.physical_distance.value()
        except ValueError:
            return None
    
    @distance_cm.setter
    def distance_cm(self, value):
        self.view.physical_distance.setValue(value)
        
    @property
    def distance_pixels(self):
        try:
            return float(self.view.pixel_distance.text())
        except ValueError:
            return 1
        
    @distance_pixels.setter
    def distance_pixels(self, value):
        safe_set_value_to_widget(self.view.pixel_distance, value)
        
        
    def model_to_view(self):
        geometry = self.model.floorplan.geometry
        if isinstance(geometry, MeasuredGeometry):
            #self.view.clear()
            self.view.set_choose_measured()
            self.distance_cm = geometry.distance_cm
            self.distance_pixels = geometry.distance_pixels
            self.pixel_size_cm = geometry.pixel_size_cm
            self.mpl_line_item.model_item.vertices = geometry.vertices            
        else:
            self.view.set_choose_fixed()
            self.pixel_size_cm = geometry.pixel_size_cm
            
            
      
   
    def measure(self, _=None):
        clicker = PointClicker(mpl_controller=self.mpl_controller)
        def draw_geometry_line(position):
            clicker.disconnect(self)
            vertices = [position, position]           
            self.mpl_line_item.model_item.vertices = vertices
            
            
        
            MovePointByMouse(mouse=self.mpl_controller.mouse, 
                             model_item=self.mpl_line_item.model_item,
                             vertex_index=1, hold=False)
            
    
        clicker.connect(self, clicker.EVENT_POINT_CLICKED, draw_geometry_line)
        return
        
    def confirm(self, _=None):
        self.logger.debug('Confirming!')
        geometry = self.model.floorplan.geometry
        if self.view.choose_fixed.isChecked():
            
            if geometry.pixel_size_cm == self.pixel_size_cm:
                return
            else:
                new_geometry = Geometry(pixel_size_cm=self.pixel_size_cm,
                                        origin_cm=geometry.origin_cm)
        else:
            if self.distance_cm <= 0:
                pixelsize_error()
                return
                
            vv = self.mpl_line_item.model_item.vertices
            vvp = [geometry.cm_to_pixels(vi) for vi in vv]
           
            if isinstance(geometry, MeasuredGeometry)\
                and (geometry.vertices_pixels == vvp and\
                    geometry.distance_cm == self.distance_cm):
                    self.logger.debug('Nothing to change!')
                    return
            else:
                self.logger.debug('New Geometry!')
                vvp = [[float(vi[0]), float(vi[1])] for vi in vvp]
                new_geometry = MeasuredGeometry(vertices_pixels=vvp,
                                                distance_cm=self.distance_cm,
                                                origin_cm=geometry.origin_cm)
               
                self.mpl_line_item.model_item.vertices = new_geometry.vertices
        self.model.floorplan.geometry = new_geometry
        
        # by large changes in pixel size matching is necessary
        self.model.match_extent_to_floorplan()
        # explicit refresh is necessary now, fix later with an event
        self.mpl_controller.refresh()
        
        self.show_pixelsize_line()
    
        self.logger.debug(f'New Pixel Vertices {self.mpl_line_item.model_item.vertices}')

    

class EditModelItemControllerBase(ModelUpdateController):
    ITEM_LABEL = 'None'

    def set_view_callbacks(self):
        super().set_view_callbacks()
        self.view.connect(self, self.view.EVENT_VIEW_UPDATE,
                          self.write_to_model)
        
        if len(self.sequence) > 0:
            self.model_to_view(self.sequence[0])
        
    def connect_model(self):
        super().connect_model()
           
        self.sequence.connect(self, 
                              self.sequence.EVENT_UPDATE_ITEM,
                              self.model_update_callback)   
        
        self.sequence.connect(self, 
                              self.sequence.EVENT_REMOVE_ITEM,
                              self.item_removed)
        
        self.sequence.connect(self, 
                              self.sequence.EVENT_ADD_ITEM,
                              self.item_added)
        
        self.model.item_selector.connect(self, 
                                         self.model.item_selector.EVENT_SELECT_ITEM,
                                         self.select_item_callback)
        
        if len(self.sequence) > 0:
            self.model_to_view(self.sequence[0])
            
    def disconnect_model(self):
        super().disconnect_model()
        self.sequence.disconnect(self)
        
        
    def item_added(self, item=None):
        self.model_to_view(item)
        self.refresh()
        
    def item_removed(self, item=None):
         if self.model.item_selector.selected_item in self.sequence:
             self.model_to_view(self.model.item_selector.selected_item)
         elif len(self.sequence) > 0:
             self.model_to_view(self.sequence[0])
         else:
             self.view.clear()
         self.refresh()
        
    
    def select_item_callback(self, item):
        self.logger.debug('Select Item Callback')
        if item in self.sequence:
            self.model_to_view(item)
            
    @property
    def sequence(self):
         return self.model.get_sequence_by_label(self.ITEM_LABEL)
     
     
    def write_to_model(self, event_data=None):
        item = self.get_item_in_view()
        if item is not None:
            item.update_by_dict(event_data)

            
            
    def model_to_view(self, item):
        self.view.disable_connection(self)
        self.logger.debug('Model to View')
        if item not in self.sequence:
            return
        
        if item is None:
            self.view.clear()
        else:
            self.logger.debug(f'Setting item of type {type(item)} to view')
            self.logger.debug(f'{str(item.to_dict())}')
            self.view.from_dict(item.to_dict())
        
        self.view.enable_connection(self)
        self.refresh()

        
    def refresh(self):
        # called by controller when view is selected by user
        self.logger.debug(f'Setting view status for n={len(self.sequence)}')
        if len(self.sequence) == 0:
            self.view.set_enabled(False)
        else:
            self.view.set_enabled(True)
        
        pass
    
    def new(self, **kwargs):
        self.mpl_controller.view.toolbar.deselect()
        self.sequence.add_new_item(**kwargs)

        
        
    def model_update_callback(self, event_data=None):
        self.logger.debug('model_update_callback event_data {str(event_data)}')
        #self.view.disable_connection(self)
        item, label, old_value, value = event_data
        
        if item is not self.model.item_selector.selected_item:
            return

        
        self.view.from_dict({label: value})
        
        
        
        self.logger.debug('model_update_callback finished')
        

class EditNamedModelItemController(EditModelItemControllerBase):  
 
    def set_view_callbacks(self):
        super().set_view_callbacks()            
        self.view.connect(self, self.view.EVENT_LIST_SELECTION, 
                          self.list_selection_callback)
    
    def model_update_callback(self, event_data=None):
        item, label, old_value, value = event_data
        if label == labels.NAME:
            self.update_list()
        
        super().model_update_callback(event_data=event_data)
        
    def connect_model(self):
        super().connect_model()
        self.update_list()
    
    def item_added(self, item=None):
        self.update_list()
        super().item_added(item=item)
       
    def item_removed(self, item=None):
        self.update_list()
        super().item_removed(item=item)
        
    def update_list(self):
        self.view.disable_connection(self)
        current_index = self.view.list.currentIndex()
        self.view.list.clear()
        
        for item in self.sequence:
            self.add_list_item(item)
        
        if self.view.list.count() >= current_index:
            self.view.list.setCurrentIndex(current_index)
            
        self.logger.debug(f'New selected list item: {self.view.list.currentText()}')
        self.view.enable_connection(self)
        
    def add_list_item(self, model_item):
        self.view.list.addItem(model_item.name)
        
    def add_model_item(self, _=None):
        super().add_model_item()
        self.update_list()
        
    def remove_model_item(self, _=None):
        super().remove_model_item()
        self.update_list()
        if len(self.sequence) == 0:
            self.view.set_enabled(False)
        else:
            self.view.set_enabled(True)
        
    def get_item_in_view(self):
        if len(self.sequence) == 0:
            return None
        else:
            name = self.view.list.currentText()
            item = self.get_item_by_name(name)
        return item
    
    @property
    def item_names(self):
        return [item.name for item in self.sequence] 
    
    
    def get_item_by_name(self, name):
        if name not in self.item_names:
            return None
        
        index = self.item_names.index(name) 
    
        return self.sequence[index]
            
    def model_to_view(self, item=None):
        self.view.disable_connection(self)
        if item not in self.sequence:
            return
        #self.view.disable_connection(self)
        self.view.list.setCurrentIndex(self.sequence.index(item))
        super().model_to_view(item)
        self.view.enable_connection(self)
        
    def list_selection_callback(self, index=None):
        self.model.item_selector.select_item(self.sequence[index])
        
    @property
    def list_items(self):
        return [self.view.list.itemText(i)\
                for i in range(self.view.list.count())]


class EditSourceCTController(EditNamedModelItemController):
    ITEM_LABEL = labels.SOURCES_CT
    
class EditSourceXrayController(EditNamedModelItemController):
    ITEM_LABEL = labels.SOURCES_XRAY

class EditCriticalPointsController(EditNamedModelItemController):
    ITEM_LABEL = labels.CRITICAL_POINTS
    
class EditSourcesNMController(EditNamedModelItemController):
    ITEM_LABEL = labels.SOURCES_NM
    
    def connect_model(self):
        super().connect_model()
        
        self.model.clearances.connect(self, 
                                      self.model.clearances.EVENT_UPDATE_ITEM,
                                      self.update_clearance_name)
        
        self.model.clearances.connect(self, 
                                      self.model.clearances.EVENT_ADD_ITEM,
                                      self.update_clearance_list)
        
        self.model.clearances.connect(self, 
                                      self.model.clearances.EVENT_REMOVE_ITEM,
                                      self.update_clearance_list)
        
        self.update_clearance_list()
        

    def disconnect_model(self):
        super().disconnect_model()
        self.model.clearances.disconnect(self)
        
    def update_clearance_name(self, event_data=None):
        model_item, label, old_value, value = event_data
        if label == labels.NAME:
            self.update_clearance_list()
    
    def update_clearance_list(self, event_data=None):
        self.logger.debug('Updating clearance list')
        
        item = self.get_item_in_view()
        
        if item is None:
            current_clearance = None
        else:
            current_clearance = item.clearance
        
        self.view.clearance_list.clear()
        
        for item in self.model.clearances:
            self.view.clearance_list.addItem(item.name)

        if current_clearance is not None:
            safe_set_value_to_widget(self.view.clearance_list, 
                                     current_clearance)
            
                  
    
class EditClearanceModel(EditNamedModelItemController):
    ITEM_LABEL = labels.CLEARANCE
    
    def set_view_callbacks(self):
        super().set_view_callbacks()
        self.view.new_button.clicked.connect(self.new)
        self.view.delete_button.clicked.connect(self.delete)
    
    def refresh(self):
        if len(self.sequence) <= 1 or self.view.list.currentIndex() == 0:
            self.view.set_enabled(False)
        else:
            self.view.set_enabled(True)
        
        self.toggle_delete()
        self.view.toggle_split_time()
        
    def delete(self, _=None):
        name = self.view.to_dict()[labels.NAME]
        index = self.item_names.index(name)
        self.logger.debug(f'Removing item: {index}')
        self.sequence.pop(index)
        self.refresh()
    
    @property
    def used_clearance_models(self):
        names = [labels.EMPTY_CLEARANCE]
        names += [source.clearance\
                       for source in self.model.sources_nm]
        
        return list(set(names))
    
    
    def toggle_delete(self, _=None):
        item = self.get_item_in_view()
        
        if item is None or item.name in self.used_clearance_models:
            self.view.delete_button.setEnabled(False)
        else:
           
            self.view.delete_button.setEnabled(True) 
            
    def select_item_callback(self, item):
        super().select_item_callback(item)
        
        if item in self.model.sources_nm:            
            clearance = self.model.clearances.get_item_by_name(item.clearance)
            self.logger.debug(f'!!! Type {type(self.model.item_selector.selected_item)}')
            self.model_to_view(clearance)
            self.logger.debug(f'!!! Type {type(self.model.item_selector.selected_item)}')

class EditMaterialsController(EditNamedModelItemController):
    ITEM_LABEL = labels.MATERIALS
    
    def set_view_callbacks(self):
        super().set_view_callbacks()
        self.view.new_button.clicked.connect(self.new)
        self.view.delete_button.clicked.connect(self.delete)
        
    def delete(self, _=None):
        item = self.sequence.get_item_by_name(self.view.to_dict()[labels.NAME])
        self.sequence.remove(item)
        self.refresh()
        
    def refresh(self):
        if len(self.sequence) <= 1 or self.view.list.currentIndex() == 0:
            self.view.set_enabled(False)
        else:
            self.view.set_enabled(True)
        
        self.toggle_delete()
    
    def connect_model(self):
        super().connect_model()
        
        
        self.model.materials.connect(self,
                                     self.model.materials.EVENT_ADD_ITEM,
                                     self.toggle_delete)
        
        self.model.materials.connect(self,
                                     self.model.materials.EVENT_REMOVE_ITEM,
                                     self.toggle_delete)
        
    
    
    def toggle_delete(self, _=None):
        item = self.get_item_in_view()
        
        if item is None or item.name in self.model.shieldings.used_materials:
            self.view.delete_button.setEnabled(False)
        else:
           
            self.view.delete_button.setEnabled(True)     
            
    
   
        
        

            
class EditShieldingController(EditNamedModelItemController):
    ITEM_LABEL = labels.SHIELDINGS
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_materials()
    
    def set_view_callbacks(self):
        super().set_view_callbacks()
        self.view.new_button.clicked.connect(self.new)
        self.view.delete_button.clicked.connect(self.delete)


    def refresh(self):
        super().refresh()
        if len(self.sequence) <= 1 or self.view.list.currentIndex() == 0:
            self.view.set_enabled(False)
        else:
            self.view.set_enabled(True)
        
        self.toggle_delete()
            
            
    def connect_model(self):
        super().connect_model()
        
        
        self.model.walls.connect(self,
                                  self.model.walls.EVENT_ADD_ITEM,
                                  self.toggle_delete)
        
        self.model.walls.connect(self,
                                  self.model.walls.EVENT_REMOVE_ITEM,
                                  self.toggle_delete)
        
        self.model.materials.connect(self,
                                     self.model.materials.EVENT_ADD_ITEM,
                                     lambda _: self.update_materials())
        
        self.model.materials.connect(self,
                                     self.model.materials.EVENT_REMOVE_ITEM,
                                     lambda _: self.update_materials())
        
        self.model.materials.connect(self,
                                     self.model.materials.EVENT_UPDATE_ITEM,
                                     self.update_materials)
        
    def update_materials(self, event_data=None):
        
        
        self.view.disable_connection(self)
        
        
        self.view.material1_list.clear()
        self.view.material1_list.addItems(self.model.materials.names)
        
        self.view.material2_list.clear()
        self.view.material2_list.addItems(self.model.materials.names)
            
        self.view.enable_connection()
            
    def disconnect_model(self):
        super().disconnect_model()
        self.model.walls.disconnect(self)
        
    
    def model_update_callback(self, event_data):
        super().model_update_callback(event_data)
        item, label, old_value, value = event_data
        if label == labels.COLOR or label == labels.NAME:
            # update color icons in list
            self.update_list()
        
    def delete(self, _=None):
        item = self.sequence.get_item_by_name(self.view.to_dict()[labels.NAME])
        self.sequence.remove(item)
        self.refresh()
      
    @property
    def used_shieldings(self):
        shieldings = [labels.EMPTY_SHIELDING]
        shieldings += [wall.shielding for wall in self.model.walls]
        return list(set(shieldings))
    
    
        
    def toggle_delete(self, _=None):
        item = self.get_item_in_view()
        
        if item is None or item.name in self.used_shieldings:
            self.view.delete_button.setEnabled(False)
        else:
           
            self.view.delete_button.setEnabled(True)     
    
    def select_item_callback(self, item):
        super().select_item_callback(item)
        
        if item in self.model.walls:            
            shielding = self.model.shieldings.get_item_by_name(item.shielding)
            self.logger.debug(f'!!! Type {type(self.model.item_selector.selected_item)}')
            self.model_to_view(shielding)
            self.logger.debug(f'!!! Type {type(self.model.item_selector.selected_item)}')

    
    def add_list_item(self, model_item):
        icon = qta.icon('fa5s.circle', color=model_item.color)
        self.view.list.addItem(icon, model_item.name)

class EditWallsController(EditModelItemControllerBase):
    ITEM_LABEL = labels.WALLS
   

    def set_view_callbacks(self):
        super().set_view_callbacks()            
        self.view.connect(self, self.view.EVENT_SCROLL, self.update_by_scroll)
        
        
    def get_item_in_view(self):
        if len(self.sequence) == 0:
            return None
        else:
            index = self.view.scroll_widget.value()
            if index < (len(self.sequence)):
                return self.sequence[index]
            else:
                raise IndexError()
    
    def item_added(self, item=None):
        index = self.sequence.index(item)
        self.logger.debug(f'New Wall Added {index}!')
        self.update_scroll_length()
        super().item_added(item)
        
    def item_removed(self, item=None):
        self.update_scroll_length()
        super().item_removed(item=item)
        
    def connect_model(self):

        super().connect_model()
        
        self.update_scroll_length()
        self.update_shielding_list()
        
        self.model.shieldings.connect(self, 
                                      self.model.shieldings.EVENT_UPDATE_ITEM,
                                      self.update_shielding)
        
        
        self.model.shieldings.connect(self, 
                                      self.model.shieldings.EVENT_ADD_ITEM,
                                      self.update_shielding_list)
        
        self.model.shieldings.connect(self, 
                                      self.model.shieldings.EVENT_REMOVE_ITEM,
                                      self.update_shielding_list)
    def disconnect_model(self):
        super().disconnect_model()
        self.model.shieldings.disconnect(self)
      
        
    def update_shielding(self, event_data):
        item, label, old_value, value = event_data
        if label == labels.COLOR or label == labels.NAME:
            self.update_shielding_list()
        

        
    def update_by_scroll(self, index):
        if index < len(self.sequence):
            self.model.item_selector.select_item(self.sequence[index])
    
  
    def update_scroll_length(self):
        
        self.view.scroll_widget.setMaximum(max(0, len(self.sequence)-1))
    
    def model_to_view(self, model=None):
        self.logger.debug('Will Add Wall!')
        self.view.disable_connection(self)
        super().model_to_view(model)
        if model is not None:
            index = self.sequence.index(model)
            safe_set_value_to_widget(self.view.scroll_widget, index)
            index_str = f'Wall index: {str(index)}'
            safe_set_value_to_widget(self.view.index_label, index_str)
        self.view.enable_connection(self)
   
        
    def update_shielding_list(self, event_data=None):
        self.view.disable_connection(self)
        item = self.get_item_in_view()
        
        if item is None:
            self.logger.debug('No item selected!')
            current_shielding = None
        else:
            current_shielding = item.shielding
        
        self.view.shielding_list.clear()
        
        for item in self.model.shieldings:
            icon = qta.icon('fa5s.circle', color=item.color)
            self.view.shielding_list.addItem(icon, item.name)

        self.view.enable_connection(self)        
        
        if current_shielding is not None:
            safe_set_value_to_widget(self.view.shielding_list, current_shielding)

        
          
        
   
      
        
        