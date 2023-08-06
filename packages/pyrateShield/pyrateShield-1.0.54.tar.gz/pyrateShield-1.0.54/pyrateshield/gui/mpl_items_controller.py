import numpy as np
from pyrateshield.model_items import Wall
from pyrateshield.floorplan_and_dosemap import Geometry
                                     
from pyrateshield import labels
from pyrateshield.gui import styles
from pyrateshield import Logger, GLOBAL_LOG_LEVEL

LOG_LEVEL = GLOBAL_LOG_LEVEL



class PixelSizeLine(Wall):
    label = labels.PIXEL_SIZE_CM
    
    _attr_dct = {
        "vertices": labels.VERTICES, 
    }
    

class MplItemsPlotter(Logger):
    _model = None
    pixel_size = None
    def __init__(self, axes=None, model=None):
        Logger.__init__(self, log_level=LOG_LEVEL)
        self.plotted_items = []
        self.axes = axes
        self.model = model
        self.pixel_size = self.get_pixel_size()
        self.plotted_items += [self.pixel_size]
        
    def get_pixel_size(self):
        vertices = self.model.floorplan.geometry.vertices
        model_item = PixelSizeLine(vertices=vertices)
        return MPLPixelSize(model_item=model_item,
                                       axes=self.axes)
        
    @property
    def model_items(self):
        return [*self.model.sources_ct, 
                *self.model.sources_nm,
                *self.model.sources_xray, 
                *self.model.critical_points,
                *self.model.walls]
    
    def set_callbacks(self):
        for container in [self.model.sources_ct, 
                          self.model.sources_nm,
                          self.model.sources_xray, 
                          self.model.critical_points,
                          self.model.walls]:
            
            container.connect(self, container.EVENT_ADD_ITEM,
                              self.add_mpl_item)
            
            container.connect(self, container.EVENT_WILL_REMOVE_ITEM,
                              self.remove_model_item)
            
        self.model.item_selector.connect(self, self.model.item_selector.EVENT_SELECT_ITEM, self.select)
    
    def find_item_by_matplotlib(self, matplotlib_item):
        mpl_item = None
        for item in self.plotted_items:
            if item.contains_matplotlib_item(matplotlib_item):
                mpl_item = item
        return mpl_item
    
    def mpl_item(self, model_item):
        mpl_item = None
        for item in self.plotted_items:
            if item.model_item is model_item:
                mpl_item = item                
        return mpl_item
    
               
        
    def disconnect(self):
        if self.model is None: return
        
        for container in (self.model.sources_nm, 
                          self.model.sources_ct,
                          self.model.sources_xray, 
                          self.model.walls,
                          self.model.critical_points,
                          self.model.item_selector):
            container.disconnect(self)
        
    def select(self, model_item):
        self.logger.debug(f'Will Select Model Item of type {type(model_item)}!')
        
        
        for mpl_item in self.plotted_items:
            if mpl_item.model_item is not model_item:
                mpl_item.deselect()
            else:
                self.logger.debug('Item Selected!')
                mpl_item.select()
        
    
    def clear(self):
        for item in self.plotted_items:
            item.remove()

        self.pixel_size = None
        self.plotted_items = []

        
    def refresh(self):
        self.clear()
        for model_item in self.model_items:
            self.add_mpl_item(model_item)
        self.pixel_size = self.get_pixel_size()
        self.plotted_items += [self.pixel_size]
            
        
    def remove_model_item(self, model_item):
        for mpl_item in self.plotted_items:
            if mpl_item.model_item is model_item:
                mpl_item.remove()
                self.plotted_items.remove(mpl_item)
                
    
    def add_mpl_item(self, model_item):
        if isinstance(model_item, Wall):
            mpl_item = MPLWall(model_item=model_item, 
                               shieldings=self.model.shieldings,
                               axes=self.axes)
        else:
            mpl_item = MPLPoint(model_item=model_item, axes=self.axes)
        
        if model_item == self.model.item_selector.select_item:
            mpl_item.select()
        
        self.plotted_items += [mpl_item]
        
    
                         
            
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        if model is self.model:
            return
        if self._model is not None:
            self.disconnect()
            
        self._model = model
        self.set_callbacks()
        self.refresh()
        self.pixel_size.deselect()
        
    
class MPLPoint(Logger):
    selected = False
    enabled = False
    _pick_enabled = True
    
    def __init__(self, model_item=None, axes=None):
        Logger.__init__(self)
        self.axes = axes
        self.model_item = model_item
        self.plot()
        
        self.model_item.connect(self, self.model_item.EVENT_UPDATE,
                                self.update)
    def get_pick_enabled(self):
        return self._pick_enabled
    
    def enable_pick(self):
        self._pick_enabled = True

    def disable_pick(self):
        self._pick_enabled = False
    
    def remove(self):
        self.model_item.disconnect(self)
        self.mpl_item.remove()
        self.draw()
    
    def plot(self):
        if self.model_item.enabled:
            style = styles.STYLES[self.model_item.label][styles.DEFAULT]
            self.enabled = True
        else:
            style = styles.STYLES[self.model_item.label][styles.DISABLED]
            self.enabled = False
        
        X, Y = self.model_item.position
        
        self.mpl_item = self.axes.plot(X, Y, **style)[0]
        self.draw()
        
    def update(self, event_data):
        model_item, label, old_value, value = event_data
        
        if label == labels.POSITION:
            self.mpl_item.set_xdata(value[0])
            self.mpl_item.set_ydata(value[1])
            
        if label == labels.ENABLED:
            if value:
                self.enable()
            else:
                self.disable()
        self.draw()
                
    def select(self):
        if self.selected:
            return
        
        style = styles.STYLES[self.model_item.label][styles.SELECTED]
        self.mpl_item.update(style)
        self.selected = True
        self.logger.debug(f'Selected Point Item: {self.model_item.name}')
        self.draw()
        
    def deselect(self):
        if not self.selected:
            return
        
        if self.model_item.enabled:
            style = styles.STYLES[self.model_item.label][styles.DEFAULT]
            self.mpl_item.update(style)
        else:
            style = styles.STYLES[self.model_item.label][styles.DISABLED]
            self.mpl_item.update(style)
        self.enabled = self.model_item.enabled
        self.selected = False
        self.draw()
                
    def enable(self):
        if self.enabled:
            return
        
        style = styles.STYLES[self.model_item.label][styles.DEFAULT]
        self.mpl_item.update(style)
        self.enabled = True
        self.draw()
        
    def disable(self):
        if not self.enabled:
            return
        style = styles.STYLES[self.model_item.label][styles.DISABLED]
        self.mpl_item.update(style)
        self.enabled = False
        self.draw()
    
    def contains_matplotlib_item(self, mpl_item):
        return mpl_item == self.mpl_item
        
    
    def draw(self):
        self.axes.figure.canvas.draw_idle()    
        
class MPLLine(Logger):
    selected = False
    _pick_enabled = True
    def __init__(self, model_item=None, axes=None):
        Logger.__init__(self, log_level=LOG_LEVEL)
        self.axes = axes
        
        self.model_item = model_item
        self.plot()
        self.model_item.connect(self, self.model_item.EVENT_UPDATE,
                                self.update)
    def get_pick_enabled(self):
        return self._pick_enabled
    
    def enable_pick(self):
        self._pick_enabled = True

    def disable_pick(self):
        self._pick_enabled = False
        
    def update(self, event_data):
         
         model_item, label, old_value, value = event_data
         self.logger.debug(f'Event: {str(event_data)}')
         if label == labels.VERTICES:
             self.move(value)         
             self.draw()
             
    def remove(self):
        self.model_item.disconnect(self)
        self.mpl_item.remove()
        self.draw()
        
    def plot(self):
        self.plot_line()
        self.plot_markers()
        self.draw()
        
    def plot_line(self, style=None):
        if style is None:
            style = styles.STYLES[self.LINE_LABEL][styles.DEFAULT]
        
        # Plot Line on Axes
 
        X = (self.model_item.vertices[0][0], self.model_item.vertices[1][0])
        Y = (self.model_item.vertices[0][1], self.model_item.vertices[1][1])   
            
        self.mpl_item = self.axes.plot(X, Y, **style)[0]
    
    def plot_markers(self, style=None):
        if style is None:
            style = styles.STYLES[self.MARKER_LABEL][styles.DEFAULT]
            
        X = (self.model_item.vertices[0][0], self.model_item.vertices[1][0])
        Y = (self.model_item.vertices[0][1], self.model_item.vertices[1][1])
        
        marker1 = self.axes.plot(X[0], Y[0], **style)[0]
        marker2 = self.axes.plot(X[1], Y[1], **style)[0]
        self.markers = (marker1, marker2)
        
    def move(self, value):
        self.move_line(value)
        self.move_markers(value)
        self.draw()
        
    def move_line(self, value):
        self.mpl_item.set_xdata((value[0][0], value[1][0]))
        self.mpl_item.set_ydata((value[0][1], value[1][1]))
        
    def move_markers(self, value):
        self.markers[0].set_xdata(value[0][0],)
        self.markers[0].set_ydata(value[0][1],)
        
        self.markers[1].set_xdata(value[1][0],)
        self.markers[1].set_ydata(value[1][1],)
    
    def select(self):
        self.logger.debug('MPLWall Item Selected!')
        
        # if self.selected:
        #     return
        
        style = styles.STYLES[self.LINE_LABEL][styles.SELECTED]
        self.mpl_item.update(style)
         
        style = styles.STYLES[self.MARKER_LABEL][styles.SELECTED]
        self.markers[0].update(style)
        self.markers[1].update(style)
        self.selected = True
        
        
        self.draw()
        
    def deselect(self):
        if not self.selected:
            return
        self.logger.debug('MPLWall Item Selected!')
        style = styles.STYLES[self.LINE_LABEL][styles.DEFAULT]
        self.mpl_item.update(style)
        
        style = styles.STYLES[self.MARKER_LABEL][styles.DEFAULT]
        self.markers[0].update(style)
        self.markers[1].update(style)
        self.selected=False
        self.draw()
        
        
    def contains_matplotlib_item(self, mpl_item):
        return mpl_item is self.mpl_item or mpl_item in self.markers
        
    def draw(self):
        self.axes.figure.canvas.draw_idle()
        
    
    def get_vertex_index_at_position(self, position, tolerance_cm=0):
        # needed by gui
        if tolerance_cm == 0:
            if position not in self.model_item.vertices:
                return None
            else:
                return self.model_item.vertices.index(position)
        else:
            # check if position is close enough to vertices
            v1, v2 = self.model_item.vertices
            d1 = np.linalg.norm(np.asarray(v1) - np.asarray(position))
            d2 = np.linalg.norm(np.asarray(v2) - np.asarray(position))
            
            if d1 > tolerance_cm and d2 > tolerance_cm:
                # vertices to far away from position
                return None
            else:
                # return vertex index with closest distance
                return [d1, d2].index(min([d1, d2]))
            
        

class MPLWall(MPLLine):
    LINE_LABEL = labels.WALLS
    MARKER_LABEL = labels.WALL_MARKER
    
    def __init__(self, model_item=None, shieldings=None, axes=None):
        self.shieldings = shieldings
        super().__init__(model_item=model_item, axes=axes)
        
    def update(self, event_data):
        model_item, label, old_value, value = event_data
        if label in (labels.SHIELDING, labels.COLOR, labels.LINEWIDTH):
       
            fm = {'color': self.shielding.color, 
                 'linewidth': self.shielding.linewidth}
            self.mpl_item.update(fm)
        
            if label == labels.SHIELDING or label == labels.COLOR:
                self.markers[0].update({'color': self.shielding.color})
                self.markers[1].update({'color': self.shielding.color})
            
            self.draw()
            
        super().update(event_data)
    
    @property
    def shielding(self):
        name = self.model_item.shielding
        return self.shieldings.get_item_by_name(name)
        
    def plot_line(self, _=None):
        style = styles.STYLES[labels.WALLS][styles.DEFAULT].copy()
        style['color'] = self.shielding.color
        style['linewidth'] = self.shielding.linewidth
        super().plot_line(style=style)
        
    def plot_markers(self, _=None):
        # Plot Selection Markers, only visible when item is selected
        style = styles.STYLES[labels.WALL_MARKER][styles.DEFAULT].copy()
        style['color'] = self.shielding.color
        super().plot_markers(style=style)
        
   


            
class MPLPixelSize(MPLLine):
    LINE_LABEL = labels.PIXEL_SIZE_CM
    MARKER_LABEL = labels.PIXEL_SIZE_MARKER
    



    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from pyrateshield.model import Model
    axes = plt.axes()
    project = '/Users/marcel/git/pyrateshield/example_projects/SmallProject/project.psp'
    model = Model.load_from_project_file(project)
    
    items = MplItemsPlotter(model=model, axes=axes)
    
    
       
                
   
                       
   
            
            
   

    
    
    
       
            
    
    
            
        
        

        

