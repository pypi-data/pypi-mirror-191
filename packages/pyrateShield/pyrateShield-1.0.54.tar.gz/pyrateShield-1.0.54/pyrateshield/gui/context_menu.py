from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtGui import QCursor
from pyrateshield import labels, Logger, GLOBAL_LOG_LEVEL
from functools import partial
import pyperclip
import yaml
from copy import copy

from pyrateshield.model_items import Wall
from pyrateshield.gui.mpl_items_controller import PixelSizeLine
import qtawesome as qta
SNAP_RADIUS_POINTS = 100

LOG_LEVEL = GLOBAL_LOG_LEVEL
#LOG_LEVEL = 10

class ContextMenuController(Logger):
    to_copy = None
    
    def __init__(self, model=None, view=None, mpl_controller=None,
                 main_controller=None):
        Logger.__init__(self, log_level=LOG_LEVEL)
        
        self.view = view
        self.model = model
        self.main_controller = main_controller
        self.mpl_controller = mpl_controller
        
        self.mpl_controller.connect(self, mpl_controller.EVENT_RIGHT_CLICK,
                                    self.right_click)
    
    @property
    def snap_radius_cm(self):
        T =  self.mpl_controller.axes.transData.inverted().transform
        snap_radius_cm = (T([SNAP_RADIUS_POINTS, 0]) - T([0, 0]))[0]
        return snap_radius_cm
    
    def right_click(self, event_data):
        self.logger.debug('Right click event triggered')
        model_item, vertex_index, position = event_data
        self.logger.debug(f'At position {position}')
        
        if model_item is None:
            self.logger.debug('Show canvas context menu')
            self.show_canvas_context_menu(position)
        else:
            self.logger.debug(f'Show context menu for {type(model_item)}')
            self.show_pick_context_menu(model_item, vertex_index, position)
    
    def show_canvas_context_menu(self, position=None):
        context_menu = QMenu(self.view)
       
        for label in [labels.SOURCES_CT, labels.SOURCES_XRAY,
                      labels.SOURCES_NM, labels.CRITICAL_POINTS]:
            
            title = 'Add ' + label + ' item'
            action = context_menu.addAction(title)
            callback = partial(self.add_item, label, position)
            
            action.triggered.connect(callback)
            
        action = context_menu.addAction('Start wall here')
        callback = partial(self.mpl_controller.add_wall_by_mouse, position)
        action.triggered.connect(callback)
        
            
        action = context_menu.addAction('Paste item')
        callback = partial(self.paste_item, position)
        action.triggered.connect(callback)
        
        
        if self.to_copy is None or isinstance(self.to_copy, Wall):
            # pasting walls doesnt make sense
            action.setEnabled(False)
        
        context_menu.exec_(QCursor.pos())
            
    def add_item(self, label, position):
        self.mpl_controller.view.toolbar.button_checked(label, True)
        self.mpl_controller.add_model_item(label, position)                
  
                    
    def get_snap_action(self, model_item, vertex_index, position):
        
        self.logger.debug(f'Get snap action At position {position}')
        
        get_closest = self.mpl_controller.mpl_picker.get_closest_vertex
        
        walls = [wall for wall in self.model.walls if wall is not model_item]
        wall, closest_vertex_index, distance = get_closest(position, walls=walls)
        
        if distance is not None and distance <= self.snap_radius_cm:
                
            closest_vertex = wall.vertices[closest_vertex_index]
        
            disp_vv = str([round(vi) for vi in closest_vertex])
        
            shielding = self.model.shieldings.get_item_by_name(wall.shielding)
            
            action = "Snap to: " + shielding.name + ' at ' + disp_vv
            snap_action = QAction(action)
        
            callback = partial(self.snap_wall, model_item, 
                               vertex_index, closest_vertex)
                               
        
            snap_action.triggered.connect(callback)
        
            icon = qta.icon('fa5s.circle', color=shielding.color)
            snap_action.setIcon(icon)

        else:
            snap_action = QAction('Snap to: ')
            snap_action.setEnabled(False)
        return snap_action
        
    
    def show_pick_context_menu(self, model_item, vertex_index, position):
        context_menu = QMenu(self.view)
        self.logger.debug(f'Generate contextmenu At position {position}')
        if isinstance(model_item, PixelSizeLine):
            return
        
        if not isinstance(model_item, Wall):
            enabled_action = context_menu.addAction("Enabled")
            enabled_action.setCheckable(True)            
            enabled_action.setChecked(model_item.enabled)            
            enabled_action.triggered.connect(model_item.enable)
            
            cut_action = context_menu.addAction("Cut")
            callback = lambda: self.cut_item(model_item)
            cut_action.triggered.connect(callback)
                
        copy_action = context_menu.addAction("Copy")
        callback = lambda: self.copy_item(model_item)
        copy_action.triggered.connect(callback)
            
                    
        delete_action = context_menu.addAction("Delete")
        callback = model_item.delete
        delete_action.triggered.connect(callback)
                
        if isinstance(model_item, Wall) and vertex_index is not None:
            wall_draw_action = context_menu.addAction("Continue wall here")
            callback = partial(self.mpl_controller.add_wall_by_mouse, model_item.vertices[vertex_index])
            wall_draw_action.triggered.connect(callback)
            
            snap_action = self.get_snap_action(model_item, vertex_index, 
                                               position)
                                               
            context_menu.addAction(snap_action)

            
        context_menu.exec_(QCursor.pos())
    
        
    def snap_wall(self, wall, vertex_index, closest_vertex):
        self.logger.debug(f'Snapping wall {wall.vertices}, index {vertex_index} to {closest_vertex}')
        wall.set_vertex(vertex_index, closest_vertex)
     
        

        
        
    def copy_item(self, item):
        self.to_copy = copy(item)
        
        # copies yaml definition of object to clipboard :)
        yaml_text = yaml.dump(self.to_copy.to_dict(), default_flow_style=None)
        pyperclip.copy(yaml_text)
        
        
    def paste_item(self, pos):
        self.to_copy.position = pos
        self.model.add_item(self.to_copy)
        self.model.item_selector.select_item(self.to_copy)
        self.to_copy = None
        
    
    def cut_item(self, item):
        self.copy_item(item)
        sequence = self.model.sequence_for_item(item)
        sequence.remove(item)
        
        
    def delete_item(self, item):
        self.model.delete_item(item)