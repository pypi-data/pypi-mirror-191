import time
import numpy as np
import copy
from matplotlib.cm import get_cmap
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from pyrateshield.model_items import Wall, Shielding
from pyrateshield.gui.mpl_items_controller import PixelSizeLine
from pyrateshield.floorplan_and_dosemap import MeasuredGeometry
from pyrateshield.gui.mpl_view import PointClicker, MovePointByMouse, Mouse
from pyrateshield.gui.mpl_items_controller import MplItemsPlotter, MPLPixelSize
from pyrateshield.gui.mpl_picker import MPLPicker
from pyrateshield import labels, Observable, GLOBAL_LOG_LEVEL


LOG_LEVEL = GLOBAL_LOG_LEVEL
#LOG_LEVEL = 10


def plot_dosemap(ax, model, dosemap):
    extent = model.dosemap.extent        
    style = model.dosemap_style
    
    cmap = copy.copy(get_cmap(style.cmap_name))
    if style.alpha_gradient:
        alphas = np.linspace(0, 1, cmap.N)
        cmap._init()
        cmap._lut[:len(alphas), -1] = alphas            
    cmap.set_under(alpha=0)
    
    img = ax.imshow(dosemap, interpolation="bilinear")
    img.set_extent(extent)
    img.set_cmap(cmap)
    img.set_alpha(style.alpha)
    img.set_clim([style.vmin, style.vmax])
    img.set_norm(LogNorm(vmin=style.vmin, vmax=style.vmax))
            
    levels, colors, linestyles, linewidths, active = zip(*[cl for cl in style.contour_lines if cl[4]])
    CS = ax.contour(dosemap, extent=extent, levels=levels, 
                                colors=colors, linestyles=linestyles,
                                linewidths=linewidths, origin="upper")
    h,_ = CS.legend_elements()        
    leg = ax.legend(h, levels, handlelength=3, 
                                title="Contours [mSv]", framealpha=0.7)

    return img, CS, leg

            
class MplController(Observable):
    _dosemap_image = None
    _contour_lines = None
    _legend = None
    _floorplan_image = None
    
    _scale_line = None
    _origin_point = None

    _model = None
    lock_mouse = False
    
    _point_clicker = None
    
    EVENT_PICK_LEFT_CLICK = 'event_pick_left_click'
    EVENT_RIGHT_CLICK = 'event_right_click'
    EVENT_REFRESH = 'event_refresh'

    def __init__(self, dosemapper=None, view=None, model=None):       
        Observable.__init__(self, log_level=LOG_LEVEL)
        self.dosemapper = dosemapper
        self.view = view

        self.mouse = Mouse(self.view.canvas)
        
        self.mpl_items = MplItemsPlotter(model=model, axes=self.axes)
       
        self.mpl_picker = MPLPicker(mpl_items=self.mpl_items,
                                   item_selector=model.item_selector,
                                   axes = self.axes)
        self._enable_pick = True
        self.model = model
        
        self.set_callbacks()   
        
        self.refresh()
    
    
    def enable_picking(self):
        self._enable_pick = True
    
    def disable_picking(self):
        self._disable_pick = True
    
    
    @property
    def model(self):
       return self._model
   
    @model.setter
    def model(self, model):
       if self.model is model:
           return
       if self.model is not None:
           self.model.disconnect(self)
           self.model.item_selector.disconnect(self)
           
       self._model = model
       
       self.mpl_items.model = model       
     
       self.mpl_picker.item_selector = model.item_selector
       
       callback = self.select_item_callback
       self.model.item_selector.connect(self, 
                                    self.model.item_selector.EVENT_SELECT_ITEM, 
                                    callback)
              
       callback = self.new_floorplan
       
       self.model.connect(self,
                          self.model.EVENT_UPDATE_FLOORPLAN,
                          callback)
       self.refresh()

       
    def set_callbacks(self):
        # button callbacks
        button = self.view.buttons[self.view.dosemap_button_pyshield_label]
        button.clicked.connect(self.show_dosemap_pyshield)
        
        button = self.view.buttons[self.view.dosemap_button_radtracer_label]
        button.clicked.connect(self.show_dosemap_radtracer)
        
        button = self.view.buttons[self.view.refresh_button_label]
        button.clicked.connect(self.refresh)
        
        #self.axes.figure.canvas.mpl_connect('pick_event', self.pick_event)
        
        self.mouse.connect(self, self.mouse.LEFT_CLICK_EVENT, 
                           self.left_mouse_click)
        
        self.mouse.connect(self, self.mouse.RIGHT_CLICK_EVENT, 
                           self.right_mouse_click)
        
        
        event = self.view.toolbar.EVENT_TOOLBUTTON_CLICK
        self.view.toolbar.connect(self, event, self.toolbar_callback)
    
    
    def draw(self):        
        self.axes.figure.canvas.draw_idle()
    
    
    def left_mouse_click(self, position):
        self.logger.debug('Left Mouse Click')
        # check toolbar what to do
        toolname = self.view.toolbar.selected_tool
        
        self.logger.debug(f'Tool selected: {str(toolname)}')
        
        if toolname is None: # select, and drag items
            self.logger.debug('Start picking objects')
            # note vertex_index is None for point items
            model_item, vertex_index = self.mpl_picker.pick_model_item(position)
            
            if model_item is None:
                self.logger.debug('Nothing close to the mouse position')
                # nothing selected random click
                return
            self.logger.debug(f'Item of type {type(model_item)} picked')
                
            if model_item is self.model.item_selector.selected_item:
                if isinstance(model_item, Wall):
                    if vertex_index is not None:
                        # selected item clicked, start mouse interaction / drag
                        MovePointByMouse(mouse=self.mouse, 
                                         model_item=model_item,
                                         vertex_index=vertex_index)
                else:
                    MovePointByMouse(mouse=self.mouse, model_item=model_item)
                                     
            else:
                # select picked model_item, make active
                self.model.item_selector.select_item(model_item)
        
        
        elif toolname in (labels.SOURCES_CT, labels.SOURCES_NM, 
                          labels.SOURCES_XRAY, labels.CRITICAL_POINTS):
            # create point item
            self.add_model_item(label=toolname, position=position)
        elif toolname == labels.WALLS:
            self.add_wall_by_mouse(position)
        elif toolname == labels.FLOORPLAN:
            self.move_items(position)
    
    
    def right_mouse_click(self, position):
        # check toolbar what to do
        toolname = self.view.toolbar.selected_tool
        
        self.logger.debug(f'Position!: {position}')
        if toolname is None:
            model_item, vertex_index = self.mpl_picker.pick_model_item(position)
            event_data = (model_item, vertex_index, position)
            # note model item can be None if no item was in radius
            self.emit(self.EVENT_RIGHT_CLICK, event_data)
 
 
    @property
    def floorplan_image(self):
        if self._floorplan_image is None:
            self._floorplan_image = self.axes.imshow(((0,0), (0,0)))
        return self._floorplan_image
        
        
    def select_item_callback(self, item):
        self.toggle_delete()


    def toggle_delete(self):
        if self.model.item_selector.selected_item is not None:
            self.view.toolbar.button_enabled('delete', True)
        else:
            self.view.toolbar.button_enabled('delete', False)
        
        
    def clear(self):
        self.axes.cla()
        self._floorplan_image = None
        self.mpl_items.clear()
        
        
    @property
    def axes(self):
        return self.view.canvas.ax
        
        
    def refresh(self, _=None):
        self.clear()
        self.model.floorplan.disconnect(self)
        self.new_floorplan()
        self.mpl_items.refresh()
        #self.mpl_items_selector.refresh()
        self.toggle_delete()
        self.draw()


    def update_floorplan(self, event_data=None):
        model_item, label, old_value, value = event_data
        if label == labels.IMAGE:
            self.floorplan_image.set_data(self.model.floorplan.image)
            self.model.match_extent_to_floorplan()
            self.refresh()
            
        elif label == labels.GEOMETRY:
            self.floorplan_image.set_extent(self.model.floorplan.extent)
        self.draw()
        #self.plot_floorplan()
    
    
    def new_floorplan(self, _=None):
        self.logger.debug('Plotting new floorplan')
        self.floorplan_image.set_data(self.model.floorplan.image)
        self.floorplan_image.set_extent(self.model.floorplan.extent)
        
        self.axes.set_xlim(self.model.dosemap.extent[:2])
        self.axes.set_ylim(self.model.dosemap.extent[2:])
                
        # callback for changes in geometry
        callback = self.update_floorplan
        self.model.floorplan.connect(self, 
                                     self.model.floorplan.EVENT_UPDATE,
                                     callback)
        
        self.draw()
    
   
    def get_dosemap(self):
        start = time.time()
        self.model.dosemap.extent = self.axes.get_xlim() + self.axes.get_ylim()
        dosemap = self.dosemapper.get_dosemap(self.model)          
        end = time.time()        
        exec_time = round(end-start, 2)
        self.logger.info(f'Dosemap calculated in {exec_time}s')
        return dosemap
    
    
    def show_dosemap_pyshield(self):
        engine = self.model.dosemap.engine
        self.model.dosemap.engine = labels.PYSHIELD
        self.show_dosemap()
        self.model.dosemap.engine = engine
    
    
    def show_dosemap_radtracer(self):
        engine = self.model.dosemap.engine
        self.model.dosemap.engine = labels.RADTRACER
        self.show_dosemap()
        self.model.dosemap.engine = engine
    
    
    def show_dosemap(self):
        # Remove all dosemap related elements from the current axes
        clear_elements = [self._dosemap_image, self._legend]
        if self._contour_lines is not None:
            clear_elements += self._contour_lines.collections
        
        ax_elements = self.axes.get_children()
        for element in clear_elements:
            if element in ax_elements:
                element.remove()
        
        # Calculate new dosemap and plot elements
        dosemap = self.get_dosemap()
        if dosemap is not None:            
            img, CS, leg = plot_dosemap(self.axes, self.model, dosemap)            
            self._dosemap_image = img
            self._contour_lines = CS
            self._legend = leg
            
        self.draw()


    def add_model_item(self, label, position):
        model_items = self.model.get_sequence_by_label(label)
        new_item = model_items.add_new_item(position=position)
        
        self.model.item_selector.select_item(new_item)
        
        self.view.toolbar.select_checkable_tool(toolname=None)
    
    
    def add_wall_by_mouse(self, position=None):       

        vertices = [position.copy(), position.copy()]
        
        # Find active shielding
        if isinstance(self.model.item_selector.selected_item, PixelSizeLine):
            shielding = labels.EMPTY_SHIELDING
        elif isinstance(self.model.item_selector.selected_item, Wall):
            shielding = self.model.item_selector.selected_item.shielding
        elif isinstance(self.model.item_selector.selected_item, Shielding):
            shielding = self.model.item_selector.selected_item.name
        else:
            shielding = labels.EMPTY_SHIELDING
            
            
        # Create new empyt wall
        new_item = self.model.walls.add_new_item(vertices=vertices,
                                                 shielding=shielding)
        
        self.model.item_selector.select_item(new_item)
        
        # Move second vertex by mouse
        def finished(_=None):
            self.view.toolbar.select_checkable_tool(toolname=None)
        
        mover = MovePointByMouse(mouse=self.mouse, model_item=new_item,
                                 vertex_index=1, hold=True)
        
        mover.connect(self, mover.EVENT_FINISHED, finished)
        
        #ugly fix for small displacement of first vertex 
        new_item.set_vertex(0, [*position])
        
        self.draw()

    
    def move_items(self, event_data):
        self.temp_data = None
        self.logger.debug('Start Moving!')
        def move_model(position):
            if self.temp_data is None:
                self.temp_data = self.mouse.click_position
            
            dx_cm =  position[0] - self.temp_data[0]
            dy_cm = position[1] - self.temp_data[1] 
            
            self.logger.debug(f'Shifting {dx_cm}, {dy_cm}')
            
            self.model.shift_cm(dx_cm, dy_cm)
            self.temp_data = position
        
        def release(_):
            self.mouse.disconnect(self, self.mouse.MOVE_EVENT)
            self.mouse.disconnect(self, self.mouse.RELEASE_EVENT)
        
        
        self.mouse.connect(self, self.mouse.MOVE_EVENT, move_model)
        self.mouse.connect(self, self.mouse.RELEASE_EVENT, release)


    def toolbar_callback(self, event_data):
        toolname, checked = event_data
        
        if toolname == labels.PYSHIELD:
            self.show_dosemap_pyshield()
        elif toolname == labels.RADTRACER:
            self.show_dosemap_radtracer()
        elif toolname == labels.FLOORPLAN:
            self.move_items(event_data)
        elif toolname == 'refresh':
            self.refresh()
        elif toolname == 'delete':
            if self.model.item_selector.selected_item is not None:
                self.model.remove_item(self.model.item_selector.selected_item)

