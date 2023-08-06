from pyrateshield import Logger, GLOBAL_LOG_LEVEL, model_items
from pyrateshield.gui.mpl_items_controller import MPLPoint, MPLWall
import numpy as np
#from matplotlib.backend_bases import MouseButton
LOG_LEVEL = GLOBAL_LOG_LEVEL
#LOG_LEVEL = 10


class MPLPicker(Logger):
    # Used by MPL to select objects by mouse, objects within radius are selected
    
    # 2DO dont use points but pixels
    PICKRADIUS_POINTS = 10
    
    def __init__(self, axes=None, mpl_items=None, item_selector=None):
        Logger.__init__(self, log_level=LOG_LEVEL)
        self.axes = axes
        self.mpl_items = mpl_items
        self.item_selector = item_selector
        self.enable_pick()
        
    @staticmethod
    def is_point_item(item):
        return isinstance(item, (model_items.SourceNM,
                                 model_items.SourceCT,
                                 model_items.SourceXray,
                                 model_items.CriticalPoint))
        
    def disable_pick(self):
        for item in self.mpl_items.plotted_items:
            item.disable_pick()
    
    def enable_pick(self):
        for item in self.mpl_items.plotted_items:
            item.enable_pick()
        
    @property
    def point_mpl_items(self):
        # return all enabled point items that are plotted by mpl_items
        return [item for item in self.mpl_items.plotted_items\
                if isinstance(item, MPLPoint) and item.get_pick_enabled()]
            
    @property
    def point_model_items(self):
        return [item.model_item for item in self.point_mpl_items]
    
            
    @property
    def wall_mpl_items(self):
        # return all walls that are plotted by mpl_items
        items = [item for item in self.mpl_items.plotted_items\
                 if isinstance(item, MPLWall) and item.get_pick_enabled()]
        if self.mpl_items.pixel_size.get_pick_enabled:
            items += [self.mpl_items.pixel_size]
        return items
            
    @property
    def wall_model_items(self):
        return [item.model_item for item in self.wall_mpl_items]
    
    @staticmethod
    def lineseg_dists(p, a, b):
        """Cartesian distance from point to line segment
    
        Edited to support arguments as series, from:
        https://stackoverflow.com/a/54442561/11208892
    
        Args:
            - p: np.array of single point, shape (2,) or 2D array, shape (x, 2)
            - a: np.array of shape (x, 2)
            - b: np.array of shape (x, 2)
        """
        # normalized tangent vectors
        d_ba = b - a
        num = np.hypot(d_ba[:, 0], d_ba[:, 1]).reshape(-1, 1)
        d = np.divide(d_ba, num, where=num!=0)
    
        # signed parallel distance components
        # rowwise dot products of 2D vectors
        s = np.multiply(a - p, d).sum(axis=1)
        t = np.multiply(p - b, d).sum(axis=1)
    
        # clamped parallel distance
        h = np.maximum.reduce([s, t, np.zeros(len(s))])
    
        # perpendicular distance component
        # rowwise cross products of 2D vectors  
        d_pa = p - a
        c = d_pa[:, 0] * d[:, 1] - d_pa[:, 1] * d[:, 0]
        
        distance = np.hypot(h, c)
        
        # zero length line segments --> points
        points = a[num[:, 0]==0]
        dpoints = np.sqrt((points[:, 0] - p[0]) ** 2 + (points[:, 1] - p[1]) ** 2)
        
        
        distance[num[:, 0]==0] = dpoints
    
        return distance
    
    @property
    def pick_radius_cm(self):
        T =  self.axes.transData.inverted().transform
        pick_radius_cm = (T([self.PICKRADIUS_POINTS, 0]) - T([0, 0]))[0]
        return pick_radius_cm
    
    def pick_model_item(self, position):
        self.logger.debug(f'Pick event at position {position}')
        
        selected_item = self.item_selector.selected_item
        
        
        distance = self.selected_item_distance(position)
        
        if distance is not None and distance <= self.pick_radius_cm:
            self.logger.debug(f'Selected item selected at distance {distance}')
            item = selected_item
        else:
            wall, dw = self.get_closest_wall(position, 
                                                walls=self.wall_model_items)
            
            point, dp = self.get_closest_point(position, 
                                               points=self.point_model_items)
            
            
            self.logger.debug(f'Wall at distance {dw}')
            self.logger.debug(f'Point at distance {dp}')
            
            item = None
            
            if wall is not None and point is not None:
                if dp <= dw and dp <= self.pick_radius_cm:
                    item = point
                if dw < dp and dw <= self.pick_radius_cm:
                    item = wall
            elif point is not None:
                if dp <= self.pick_radius_cm:
                    item = point
            elif wall is not None:
                if dw <= self.pick_radius_cm:
                    item = wall
              
        vertex_index = None
        if isinstance(item, model_items.Wall):
            _, vi, di = self.get_closest_vertex(position, walls=[item])
            self.logger.debug(f'Closest vertex at : {di}')
            if di <= self.pick_radius_cm:
                self.logger.debug(f'Vertex selected index: {vi}')
                vertex_index = vi
        return item, vertex_index
        
        
    
    @staticmethod
    def get_closest_wall(position, walls=None):            
        
        
        if walls is None or len(walls) == 0:
            return None, None
        
        p = np.asarray(position, dtype=float)
        
        vertices = np.stack([wall.vertices for wall in walls])
        
        d = MPLPicker.lineseg_dists(p, vertices[:, 0, :], vertices[:, 1, :])
        
        distance = np.min(d)
        index = np.where(d==distance)[0][0]
                
        return walls[index], distance
    
    @staticmethod
    def get_closest_vertex(position, walls=None):
        if walls is None or len(walls) == 0:
            return None, None, None
        wall, _ = MPLPicker.get_closest_wall(position, walls=walls)
        vv = np.asarray(wall.vertices)
        p = position
        vd = np.sqrt((vv[:, 0] - p[0])**2 + (vv[:, 1] - p[1])**2)
        vi = np.where(vd==np.min(vd))[0][0]
        return wall, vi, np.min(vd)
    
    @staticmethod
    def get_closest_point(position, points=None):
        if points is None or len(points) == 0:
            return None, None
        
        p = position
        pp = np.asarray([point.position for point in points])
        
        d = np.sqrt((pp[:, 0]-p[0])**2 + (pp[:, 1]-p[1])**2)
        di = np.where(d==np.min(d))[0][0]
        
        return points[di], np.min(d)
        
        
    def selected_item_distance(self, position):
        selected_item = self.item_selector.selected_item
        if isinstance(selected_item, model_items.Wall):
            _, distance = self.get_closest_wall(position, [selected_item])

        elif self.is_point_item(selected_item):
            _, distance = self.get_closest_point(position, [selected_item])
   
        else:
            distance = None
        return distance
        
    
    def pick_point_item(self, position):
        if len(self.point_mpl_items) == 0:
            self.logger.debug('No point items in view')
            return None, None
        
        point_item, distance = self.get_closest_point(position, 
                                                      self.point_model_items)
        
        if distance <= self.pick_radius_cm:
            return point_item, distance
        else:
            return None, None
            
    def pick_wall_item(self, position):                
        if len(self.wall_mpl_items) == 0:
            self.logger.debug('No walls in view')
            return None, None, None

        wall, distance = self.get_closest_wall(position, self.wall_model_items)
        
        if distance > self.pick_radius_cm:
            return None, None, None
        else:
            return self.get_closest_vertex(position, walls=[wall])
       
        
            
            
          