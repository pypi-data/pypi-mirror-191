import inspect
from pyrateshield import labels, Observable, GLOBAL_LOG_LEVEL

LOG_LEVEL = GLOBAL_LOG_LEVEL

#LOG_LEVEL = 10

def equal_position(position1, position2):
    if  [position1, position2].count(None) == 1:
        return False
    elif [position1, position2].count(None) == 2:
        return True
    else:
        return position1[0] == position2[0]\
            and position1[1] == position2[1]
        
def equal_vertices(vertices1, vertices2):
    if  [vertices1, vertices2].count(None) == 1:
        return False
    elif [vertices1, vertices2].count(None) == 2:
        return True
    else:
        return equal_position(vertices1[0], vertices2[0])\
            and equal_position(vertices1[1], vertices2[1])

def equal_materials(materials1, materials2):
    if  [materials1, materials2].count(None) == 1:
        return False
    elif [materials1, materials2].count(None) == 2:
        return True
    elif len(materials1) != len(materials2):
            return False
    else:
        eq = True
        for material1, material2 in zip(materials1, materials2):
            eq = eq and material1[0] == material2[0] and material1[1] == material2[1]
        return eq
    

### Base class
class ModelItem(Observable):
    label = 'ModelItem'
    EVENT_UPDATE = 'event_update'
    EVENT_DELETE = 'event_delete'
    
    _attr_dct = {}
    _attr_defaults = {}   


    def __init__(self, **kwargs):        
        
        Observable.__init__(self, log_level=LOG_LEVEL)
        
        
        init_values = self._get_default_values()
        init_values.update(kwargs)
        self.logger.debug(f'Init with kwargs {str(init_values)}')
        for attr_name, value in init_values.items():
            setattr(self, attr_name, value)
            
    def delete(self):
        self.emit(self.EVENT_DELETE, self)
        self.disconnect()
        # will be picked up by garbage collector now
            
    def __copy__(self):
        return self.__class__.from_dict(self.to_dict())

    
    @classmethod
    def _get_default_value(cls, attr_name):
        if cls._attr_dct[attr_name] in cls._attr_defaults.keys():     
            # default value defined
            value = cls._attr_defaults[cls._attr_dct[attr_name]]

        elif attr_name in cls._attr_dct.keys(): 
            # No default value but is in the attribute dct
            value = None
        else:
            # Debug purpuses should not happen for a well defined ModelItem
            raise AttributeError(f'Unknown Attribute {attr_name}')
            
        if inspect.isclass(value) or inspect.isfunction(value):
            value = value() # call or create instance
        return value
    
    @classmethod
    def _get_default_values(self):
        values = {}
        for attr_name in self._attr_dct.keys():
            values[attr_name] = self._get_default_value(attr_name)
        return values
        
    def __setattr__(self, attr_name, value):
        
        if attr_name not in self._attr_dct.keys():
            return super().__setattr__(attr_name, value)
        
        
        if hasattr(self, attr_name):
            old_value = getattr(self, attr_name)
        else: 
            super().__setattr__(attr_name, None)
            old_value = None
        self.logger.debug(f'Setting Attribute {attr_name} from {str(old_value)} to {str(value)}')
        # Override None values to default values                
        if value is None:            
            value = self._get_default_value(attr_name)
            self.logger.debug(f'Overriding value with defualt {str(value)}')
        
        if attr_name == 'materials' and equal_materials(old_value, value):
                return # don't set and don't emit event
                
        elif attr_name == 'position':
            value = [float(value[0]), float(value[1])] # force list!
            if equal_position(old_value, value):
                return # don't set and don't emit event
                
        elif attr_name == 'vertices' :# force list!            
            value = [[float(value[0][0]), float(value[0][1])],
                     [float(value[1][0]), float(value[1][1])]]
                
            if equal_vertices(old_value, value):
                return # don't set and don't emit event
        elif attr_name == 'image': 
            if old_value is value:
                return
        else:
            if old_value == value:
                return  # don't set and don't emit event
    
        super().__setattr__(attr_name, value)
            
        if attr_name in self._attr_dct.keys():
            # gather event_data and emit event
            value = getattr(self, attr_name)
            label = self._attr_dct[attr_name]
            event_data = self, label, old_value, value
            self.emit(self.EVENT_UPDATE, event_data=event_data)
            
    def update_by_dict(self, dct):
        for key, value in dct.items():
            attr_name = self.attr_name_from_label(key)
            setattr(self, attr_name, value)
          
    @classmethod
    def from_dict(cls, dct):
        kwargs = {}
        for label, value in dct.items():
            # older pyshield version had a key apply biological decay
            # this is now included in the Clearance model, ignore keys
            if label in (labels.APPLY_BIOLOGICAL_DECAY, labels.BIOLOGICAL_HALFLIFE):
                continue
            
            if label in cls._attr_dct.values():
                kwargs[cls.attr_name_from_label(label)] = value
            elif label == labels.ENABLED or label == 'enable' or label=='show':
                # Tricky part here 
                # Some older psp / zip files contain model_items with the
                # enabled tag while it is not used. This would now error in 
                # code. Ignore the enabled flag below to ignore
                continue
            else:
                raise KeyError(f'{label} not a valid setting for {cls.__name__}')
                
            
        return cls(**kwargs)
    
    def enable(self, value):
        if labels.ENABLED in self._attr_dct.values():
            self.enabled = value
        else:
            raise AttributeError

    def to_dict(self):
        dct = {label: getattr(self, var)\
               for var, label in self._attr_dct.items()}
        return dct
    
    @classmethod
    def attr_name_from_label(cls, label):        
        index = list(cls._attr_dct.values()).index(label)
        return list(cls._attr_dct.keys())[index]
    
    
    def __str__(self):
        return "\n".join([f"{k}: {v}" for k, v in self.to_dict().items()])
    
    def __repr__(self):
        return self.__str__()
    
    

