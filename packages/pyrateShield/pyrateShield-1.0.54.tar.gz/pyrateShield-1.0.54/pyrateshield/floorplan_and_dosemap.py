from pyrateshield import labels
from pyrateshield import model_items

import copy
import numpy as np



    

class Geometry(model_items.ModelItem):
    _origin_cm = None
    _pixel_size_cm = None
    _attr_dct = {
        "pixel_size_cm":     labels.PIXEL_SIZE_CM,
        "origin_cm":         labels.ORIGIN_CM,
        'locked':            labels.LOCKED}
    
    _attr_defaults = {
        labels.PIXEL_SIZE_CM: 1,
        labels.ORIGIN_CM: model_items.ZERO_POSITION,
        labels.LOCKED: False}

    
    def get_extent(self, image):
        if image is None or self.pixel_size_cm is None\
            or self.origin_cm is None:
                return (0, 1, 0, 1)
        else:
            extent = (-self.origin_cm[0],
                      image.shape[1] * self.pixel_size_cm - self.origin_cm[0],
                      -self.origin_cm[1],
                      image.shape[0] * self.pixel_size_cm - self.origin_cm[1])
        return extent
    
    @property
    def vertices(self):
        return ((0, 0), (0, 0))
    
    def pixels_to_cm(self, point):
        oo = self.origin_cm
        pp = self.pixel_size_cm
        return [point[0] * pp - oo[0], point[1] * pp - oo[1]]

    def cm_to_pixels(self, point):
        oo = self.origin_cm
        pp = self.pixel_size_cm
        return [(point[0] + oo[0])/ pp, (point[1] + oo[1]) / pp]
    
    
    def to_dict(self):
        # disable origin 
        dct = super().to_dict()        
        dct.pop(labels.ORIGIN_CM, None)
        return dct
        
        
class MeasuredGeometry(Geometry):
    _distance_cm = None
    
    _attr_dct = {
        
        "origin_cm":         labels.ORIGIN_CM,
        "vertices_pixels":   labels.VERTICES_PIXELS,
        "distance_cm":       labels.REAL_WORLD_DISTANCE_CM,
        'locked':            labels.LOCKED}
    
    _attr_defaults = {
        labels.REAL_WORLD_DISTANCE_CM: 1,
        labels.ORIGIN_CM: [0, 0],
        labels.VERTICES_PIXELS: [[0, 0], [1, 0]]}
    

    
    @property
    def vertices(self):
        vv = self.vertices_pixels
        return [self.pixels_to_cm(vv[0]), self.pixels_to_cm(vv[1])]

    @property
    def distance_pixels(self):
        vvp = self.vertices_pixels
        dpixels = np.sqrt((vvp[0][0]-vvp[1][0])**2\
                          + (vvp[0][1] - vvp[1][1])**2)

        dpixels =  float(dpixels) if dpixels > 0 else 1
        return dpixels
    
    @property
    def pixel_size_cm(self):
        return self.distance_cm / self.distance_pixels
  

    def to_dict(self):
        dct = super().to_dict()
        vvp = dct[labels.VERTICES_PIXELS]
        # sometimes numpy objects endup in yaml here, use explicit conversion 
        vvp = [[float(vvii) for vvii in vvi] for vvi in vvp]
        dct[labels.VERTICES_PIXELS] = vvp
        return dct



class DosemapStyle(model_items.ModelItem):
    _attr_dct = {
       "cmap_name": labels.CMAP_NAME,
       "vmin": labels.CMAP_MIN,
       "vmax": labels.CMAP_MAX,
       "alpha": labels.CMAP_ALPHA,
       "alpha_gradient": labels.CMAP_ALPHA_GRADIENT,
       "contour_lines": labels.CONTOUR_LINES,
    }
    _attr_defaults = {
                  labels.CMAP_NAME: "jet",
                  labels.CMAP_MIN: 0.01,
                  labels.CMAP_MAX: 10,
                  labels.CMAP_ALPHA: 0.5,
                  labels.CMAP_ALPHA_GRADIENT: True,
                  labels.CONTOUR_LINES: [
                        [0.1, "black", "dotted", 1.5, True],
                        [0.3, "black", "dashed", 1.5, True],
                        [1.0, "darkred", "solid", 1.5, True],
                        [3.0, "black", "dashdot", 1.5, True],
                        [10., "white", "dotted", 1.5, False],
                  ]
    }
    
    @classmethod
    def from_dict(cls, dct):
        ### Fix for backwards compatibility: add the is_active flag to the end
        ### of the contour_line list if it wasn't already present.
        ### #TODO: remove this classmethod after next release.

        # dct is None for older versions of pyshield files
        
        if dct is None:
            return cls()
        
        for cl in dct[labels.CONTOUR_LINES]:
            if len(cl) == 4:
                cl.append(True)
        return super().from_dict(dct)

        
            

class Dosemap(model_items.ModelItem):
    _grid = None
    _extent = None
    _grid_matrix_size = None
    _attr_dct = {
       "grid_matrix_size": labels.GRID_MATRIX_SIZE,
       "extent": labels.EXTENT,
       "engine": labels.ENGINE,
    }
    
    _attr_defaults = {labels.GRID_MATRIX_SIZE: 100,
                      labels.EXTENT: None,
                      labels.ENGINE: labels.RADTRACER} 
    
    @classmethod
    def from_dict(cls, dct):
        # HACK to be compatible with old files for now
        # engine is defined in dosemap and in Modlel ! FIX 
        dct[labels.ENGINE] = dct.pop(labels.ENGINE, labels.PYSHIELD)
        # Legacy old psp files have enabled item for all ModelItems
        dct.pop(labels.ENABLED, None)
        dct.pop('enable', None)
        dct.pop('show', None)
        return super().from_dict(dct)
                  
    def to_grid_coords(self, coords_cm):
        shape = self.shape
        x, y = coords_cm
        x0, x1, y0, y1 = self.extent
        j = (y1-y)/(y1-y0) * shape[0] - 0.5
        i = (x-x0)/(x1-x0) * shape[1] - 0.5
        return np.array((j, i))
        
    @property
    def extent(self):
        if self._extent is None:
            self._extent = [0 , self.grid_matrix_size, 0, self.grid_matrix_size]        
        return self._extent
    
    @extent.setter
    def extent(self, extent):
        self._extent = [float(ei) for ei in extent] if extent else None
        self._grid = None
        self._shape = None
        
    @property
    def grid_matrix_size(self):
        if self._grid_matrix_size is None:
            self._grid_matrix_size = self._attr_defaults[labels.GRID_MATRIX_SIZE]
        return self._grid_matrix_size
    
    @grid_matrix_size.setter
    def grid_matrix_size(self, grid_matrix_size):
        self._grid_matrix_size = grid_matrix_size
        self._shape = None
        self._grid = None
        
    @property
    def grid(self):  
        if self._grid is None:
            grid = Grid.make_grid(shape=self.shape, 
                                  extent=self.extent,
                                  grid_matrix_size=self.grid_matrix_size)
            self._grid = grid
        return self._grid
    
    @property
    def shape(self):
        if self._shape is None:
            x0, x1, y0, y1 = self.extent
            y_size = self.grid_matrix_size
            self._shape = (int(y_size), int(y_size * (x1-x0)/(y1-y0)))
        return self._shape
    

    
def empty_image():
    return np.ones((100, 100, 3))
        
        
    
class Floorplan(model_items.ModelItem):
    # EVENT_UPDATE_IMAGE     = 'event_update_image'
    # EVENT_UPDATE_GEOMETRY  = 'event_geometry_update'
   
    _attr_dct = {
        "geometry": labels.GEOMETRY,
        "image": labels.IMAGE}
    
    _attr_defaults = {labels.GEOMETRY: Geometry,
                      labels.IMAGE: empty_image}
        
    _image = None    


    @property
    def extent(self):
        return self.geometry.get_extent(self.image)


    def to_dict(self):
        dct = super().to_dict()
        dct[labels.GEOMETRY] = dct[labels.GEOMETRY].to_dict()
        return dct
    
    @classmethod
    def from_dict(cls, dct):
        if labels.PIXEL_SIZE_CM in dct[labels.GEOMETRY].keys():
            dct[labels.GEOMETRY] = Geometry.from_dict(dct[labels.GEOMETRY])
        else:
            dct[labels.GEOMETRY] = MeasuredGeometry.from_dict(dct[labels.GEOMETRY])
        return super().from_dict(dct)
        
        
    
    


class Grid:
    _distance_map = None
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        
    def distance_map_meters(self, x=0, y=0):
        x, y = (float(x), float(y))

        if self._distance_map is None:
            # cache results in dict when re-used
            self._distance_map = {}

        if (x, y) not in self._distance_map.keys():
            # no distance map yet calculated for point x, y
            distance_map = np.sqrt( ((self.X-x)/100)**2\
                                   + ((self.Y - y) / 100)**2)
            # add distance map for x, y to cache
            self._distance_map[(x, y)] = distance_map

        # return distance map
        return self._distance_map[(x, y)]
    
    @classmethod
    def make_grid(cls, shape=None, extent=None, grid_matrix_size=None):
        x0, x1, y0, y1 = extent
        xcoords = x0 + (np.arange(shape[1])+0.5)*(x1-x0)/shape[1]
        ycoords = y1 - (np.arange(shape[0])+0.5)*(y1-y0)/shape[0]
        return cls(*np.meshgrid(xcoords, ycoords, sparse=False))
    
    @staticmethod
    def multiply(*args):
        # used to multiple an iterable of arrays. Can be used safely if
        # iterable has just one element
        if len(args) == 1:
            return args[0]
        else:
            return np.prod(args, axis=0)
        
    @staticmethod
    def make_grid_pyshield(extent=None, grid_matrix_size=None):
        # Ga ik niet meer gebruiken maar laat er nog even in staan. Als ik
        # weer tegen rare problemen aanloop kan ik het nog gebruiken
        
        # onderstaant geeft 1 op 1 hetzelfde grid nu
        
        raise DeprecationWarning()
        def get_spaced_axis(xi_range, gi):
            start, stop = xi_range
            remainder = (stop - start) % grid_matrix_size
            offset = remainder / 2
            offset = 0
            start += 0.5 * gi
            p = np.arange(start+offset, stop, step=gi)
            return p
        
        yi_range = extent[3] - extent[2]
        xi_range = extent[1] - extent[0]
        
        grid_spacing_y = yi_range / grid_matrix_size
        
        
        grid_spacing_x = xi_range / (int(xi_range / grid_spacing_y))

        xi = get_spaced_axis(extent[0:2], grid_spacing_x)

        # why is y inverted ?? (probably because y-axis increases from bottom
        # to top instead of standard top to bottom).
        yi = get_spaced_axis(extent[2:],  grid_spacing_y)[::-1]

        X, Y = np.meshgrid(xi, yi)
        
        return Grid(X, Y)
    
