import numpy as np

from pyrateshield import labels
from pyrateshield.modelitem import ModelItem

from pyrateshield.constants import CONSTANTS


def ZERO_VERTICES():
    return [[0, 0], [0, 0]]

def ZERO_POSITION():
   return [0, 0]      

def EMPTY_MATERIALS():
    # default for shielding
    return [[labels.EMPTY_MATERIAL, 0], 
            [labels.EMPTY_MATERIAL, 0]]

class Material(ModelItem):
    # buildup table and attenuation table are used by pyshield only
    default_name = 'Material'
    label = labels.MATERIALS
    _attr_dct = {
        "name": labels.NAME,
        "density": labels.DENSITY,
        "attenuation_table": labels.ATTENUATION_TABLE,
        "buildup_table": labels.BUILDUP_TABLE,
        "radtracer_material": labels.RADTRACER_MATERIAL
    }
    
    _attr_defaults = {labels.NAME: default_name,
                      labels.DENSITY: 1,
                      labels.ATTENUATION_TABLE: labels.EMPTY_TABLE,
                      labels.BUILDUP_TABLE: labels.EMPTY_TABLE,
                      labels.RADTRACER_MATERIAL: labels.EMPTY_MATERIAL}
                      
    
class Shielding(ModelItem):
    default_name = 'Shielding'
    label = labels.SHIELDINGS

    _attr_dct = {
        "name": labels.NAME,
        "color": labels.COLOR,
        "linewidth": labels.LINEWIDTH,
        "materials": labels.MATERIALS,
        
    }
    
    _attr_defaults = {labels.NAME: default_name,
                      labels.COLOR: 'black',
                      labels.LINEWIDTH: 2,
                      labels.MATERIALS: EMPTY_MATERIALS}
                      
   
    
    
class Clearance(ModelItem):
    default_name = 'Clearance Model'
    label = labels.CLEARANCE
    
    _attr_dct = {
        "name": labels.NAME,
        'apply_fraction1': labels.APPLY_FRACTION1,
        'apply_fraction2': labels.APPLY_FRACTION2,
        "fraction1": labels.DECAY_FRACTION1,
        "fraction2": labels.DECAY_FRACTION2,
        "half_life1": labels.HALFLIFE1,
        'half_life2': labels.HALFLIFE2,    
        'apply_split_fractions': labels.ENABLE_SPLIT_FRACTIONS,
        'split_time': labels.SPLIT_FRACTION_TIME}
       
    
    
    _attr_defaults = {labels.NAME: default_name,
                      labels.APPLY_FRACTION1: False,
                      labels.DECAY_FRACTION1: 0,
                      labels.HALFLIFE2: 24,
                      labels.APPLY_FRACTION2: False,
                      labels.DECAY_FRACTION2: 0,
                      labels.HALFLIFE1: 24,          
                      labels.ENABLE_SPLIT_FRACTIONS: False,
                      labels.SPLIT_FRACTION_TIME: 24}
    
            
    
    def is_equal(self, other):
        if isinstance(other, Clearance):
            eq = True
            for attr in self._attr_dct.keys():
                if attr == 'name': continue
                eq = eq and (getattr(self, attr) == getattr(other, attr))
            return eq
        else:
            return False
        
    
    # LEGACY, Old psp files use single half_life
    @classmethod
    def from_half_life(cls, half_life):
        return cls(fraction1=1,
                   half_life1=half_life)
        


class Wall(ModelItem):
    label = labels.WALLS

    _attr_dct = {
        "vertices": labels.VERTICES, 
        "shielding": labels.SHIELDING,
    }
    
    _attr_defaults = {
        labels.VERTICES: ZERO_VERTICES,
        labels.SHIELDING: labels.EMPTY_SHIELDING
    }
        
    def set_vertex(self, index, vertex):
        self.logger.debug('Test!!!!!!!')
        # needed by gui
        vertices = self.vertices.copy()
        vertices[index] = vertex
        self.vertices = vertices # generates event for gui if copied first
        

        
class CriticalPoint(ModelItem):
    default_name = 'Critical Point'
    label = labels.CRITICAL_POINTS

    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "occupancy_factor": labels.OCCUPANCY_FACTOR,
        'enabled': labels.ENABLED
    }
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.OCCUPANCY_FACTOR: 1,
        labels.ENABLED: True
    }

class SourceNM(ModelItem):
    default_name = 'Source NM'
    label = labels.SOURCES_NM
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION,  
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "isotope": labels.ISOTOPE,
        "self_shielding": labels.SELF_SHIELDING,
        "activity": labels.ACTIVITY,
        "duration": labels.DURATION,
        "apply_decay_correction": labels.APPLY_DECAY_CORRECTION,
        'clearance': labels.CLEARANCE,
        'enabled': labels.ENABLED
    }
    
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.NUMBER_OF_EXAMS: 1,
        labels.ISOTOPE: 'F-18',
        labels.SELF_SHIELDING: 'None', # must be str 'None' or 'Body' 
        labels.ACTIVITY: 1,
        labels.DURATION: 1,
        labels.APPLY_DECAY_CORRECTION: True,
        labels.CLEARANCE: labels.EMPTY_CLEARANCE,
        labels.ENABLED: True}
                

    
    @property
    def tiac(self):
        return self.time_integrated_activity_coefficient_mbqh

class SourceXray(ModelItem):
    default_name = 'Source Xray'
    label = labels.SOURCES_XRAY
    _kvp = None
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "kvp": labels.KVP,
        "dap": labels.DAP,
        "enabled": labels.ENABLED,
    }
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.DAP: 1,
        labels.NUMBER_OF_EXAMS: 1,
        labels.ENABLED: True,
        labels.KVP: CONSTANTS.xray[0].kvp
        }

        

class SourceCT(ModelItem):
    default_name = 'Source CT'
    label = labels.SOURCES_CT
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "body_part": labels.CT_BODY_PART,
        "kvp": labels.KVP,
        "dlp": labels.DLP,
        'enabled': labels.ENABLED
    }
    
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.DLP: 1,
        labels.NUMBER_OF_EXAMS: 1,
        labels.CT_BODY_PART: 'Body',
        labels.KVP: CONSTANTS.ct[0].kvp,
        labels.ENABLED: True}
        
    
    @property
    def available_kvp(self):
        return list(set([item.kvp for item in CONSTANTS.ct]))
    
   
