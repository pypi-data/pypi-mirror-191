# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 14:41:18 2022

@author: 757021
"""
import yaml
from collections.abc import MutableSequence
from pyrateshield import labels, Observable, GLOBAL_LOG_LEVEL
from pyrateshield.model_items import Clearance


LOG_LEVEL = GLOBAL_LOG_LEVEL

class ModelItemSequence(MutableSequence, Observable):
    # Sequence for Walls
    #
    # Sequence emulates a list. Items can be appended, inserted or set.
    # 
    # Sequences contain classes derived from ModelItem
    # Each model item can trigger an 'event_update'. THese events are 
    # catched by the sequence and resend as an 'event_update_item' by the
    # sequence. THe GUI only needs to connect to the sequence to receive all
    # events form each ModelItem.
    #
    # In Addition 'event_remove_item' will be emmitted when a ModelItem is 
    # removed. 'event_will_remove_item' just prior to removal.
    #'event_add_item' is emmitted when a new model item is added to the 
    # sequence.

    
    EVENT_REMOVE_ITEM       = 'event_remove_item'
    EVENT_WILL_REMOVE_ITEM  = 'event_will_remove_item' 
    EVENT_ADD_ITEM          = 'event_add_item'
    EVENT_UPDATE_ITEM       = 'event_update_item'
    
    def __init__(self, items=None, item_class=None):
       
        
        if items is None:
            items = []
        
        self.items = items
        
        MutableSequence.__init__(self)
        Observable.__init__(self, log_level=LOG_LEVEL)
        
        # Each container has a item_clas property which holds the
        # class of the type of ModelItem that is gathered in the sequence.
        # self.item_class() will return a new instance of the exact ModelItem
        # class.
        
        self.item_class = item_class

        for item in items:
            self.connect_to_item(item)
    

    # nice commandline output for easy debugging    
    def __str__(self):
        return yaml.dump(list(self))
    
    def __repr__(self):
        return self.__str__()
        
    # implementation of necessary abstract methods of MutableSequence
    # ---------------------------------------------------------------
    def __len__(self):
        return len(self.items)
                
    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, item):
        # if item in self: # all items must be unique
        #     raise IndexError()
        if not isinstance(item, self.item_class):
            raise TypeError(f'Item must be type {self.item_class.__name__}')
        
        self[index].disconnect(id(self))
        self.items[index] = item        
        self.connect_to_item(self[index])
    
    def __delitem__(self, index):        
        item = self[index]
        self.emit(self.EVENT_WILL_REMOVE_ITEM, item)
        
        item.disconnect(id(self))
        
        del self.items[index]

        self.emit(self.EVENT_REMOVE_ITEM, (index, item))
    
    def insert(self, index, item):
        # if item in self: # all items must be unique
        #     raise IndexError()
        if not isinstance(item, self.item_class):
            raise TypeError(f'Item must be type {self.item_class.__name__}')
            
        self.items.insert(index, item)
        self.connect_to_item(item)
        self.emit(self.EVENT_ADD_ITEM, item)
    #-----------------------------------------------------------------

    # methods for handling events
    def emit_update(self, event_data):
        # EVENT_UPDATE_ITEM is always emitted when a model item in the
        # sequence emits 'event_update'
        self.emit(self.EVENT_UPDATE_ITEM, event_data=event_data)
    
    def connect_to_item(self, item):
        # Connect to events of a ModelItem
        
        # mutable sequence is not hashable and cannot be used as a key in 
        # dictionary that maps the callbacks. Therefore use id which is unique
        item.connect(id(self), item.EVENT_UPDATE, self.emit_update)
        item.connect(id(self), item.EVENT_DELETE, self.delete_callback)
        
    def delete_callback(self, model_item):
        # A model item can be deleted by the del command. If a model item
        # will be deleted it will also be removed from the sequence
        if model_item not in self:
            pass
            # already taken care of
        else:
            # remove item from self and generate events for gui
            self.remove(model_item)

    def add_new_item(self, **kwargs): 
        # used by gui
        new_item = self.item_class(**kwargs)
        
        # note append will trigger insert and the insert method takes
        # care of connectint to the new model item
        self.append(new_item)
        
        return new_item
    
class NamedModelItemSequence(ModelItemSequence):    
    # Sequence for SourceNM, SourceXray, SourceCT, CriticalPoint
    #
    # The name attribute is somewhat special. The name attribute should be
    # unique for all items in the sequence. This object will call the
    # force_unique_name method on a item each time a ModelItem is added tot the 
    # sequence with a duplicate name
    
    def __setitem__(self, index, item):
        if not isinstance(item, self.item_class):
            raise TypeError(f'Item must be type {self.item_class.__name__}')
        item = self.force_unique_name(item)
        super().__setitem__(index, item)
    
    def insert(self, index, item):
        self.logger.debug(f'Adding item {item}')
        if not isinstance(item, self.item_class):
            raise TypeError(f'Item must be type {self.item_class.__name__}')
        self.force_unique_name(item)
        super().insert(index, item)

    @property
    def names(self):
        # convenient for gui to get all names easily
        return [item.name for item in self]
    
    def emit_update(self, event_data):
        # If a model item changes it names. Catch the name change here
        # and rename to a new unique name. 
        
        model_item, label, old_value, value = event_data
        
        if label == labels.NAME:
            names = [item.name for item in self]
            if names.count(value) > 1: # model item was assigned duplicate name
                self.force_unique_name(model_item)
                return  # renaming will trigger new update
            
        super().emit_update(event_data)
                
    def get_item_by_name(self, name):
        # convenient for gui to get item easily
        if name not in self.names:
            msg = f'No ModelItem exists with name: {name}'
        if self.names.count(name) > 1:
            # should not be possible, debugging only
            msg = f'Multiple ModelItems exists with name: {name}'
            raise KeyError(msg)
        return self[self.names.index(name)]
        
    def get_new_name(self):
        # Just add a counter to the defualt name for the new name. If new name 
        # already in self.names then the counter is increased until the
        # new name is not already in self.names
        new_name =  self.item_class.default_name + ' 1'
        i = 1
        while new_name in [item.name for item in self]:
            i += 1
            new_name = self.item_class.default_name + ' ' + str(i)
        return new_name     
    
    def force_unique_name(self, model_item):
        # rename model_item if model_item.name already in model_item.names
        for item in self:
            # if item is model_item:
            #     continue
            if model_item.name == item.name:
                model_item.name = self.get_new_name()
    
        return model_item
    
class DefaultNamedModelItemSequence(NamedModelItemSequence):
    # shieldings and clearance must always have an 'empty' or 
    # default item. THis object takes care that the item at index 0 cannot
    # be deleted. Deletion should be prevented by gui.
    
    empty_item_label = 'DefaultEmptyItemLabel'
    
    def __init__(self, items=None, item_class=None):
        super().__init__(items=items, item_class=item_class)
        
        # Always set the empty item at index zero
        if self.empty_item_label not in self.names:
           self.insert(0, self.get_empty_item())
        elif self.names.index(self.empty_item_label) != 0:
            # probably wont happen
            
            msg = 'ModelItem {self.empty_item_label} should be at index 0'
            raise IndexError(msg)
        
    def get_empty_item(self):
        return self.item_class(name=self.empty_item_label)
        
    def __delitem__(self, index):
          if index == 0:
              # Should be prevented by gui, raise error for debugging
              raise IndexError()
          else:
              super().__delitem__(index)

class MaterialItemSequence(DefaultNamedModelItemSequence):
    empty_item_label = labels.EMPTY_MATERIAL
    
    
class ShieldingItemSequence(DefaultNamedModelItemSequence):
    empty_item_label = labels.EMPTY_SHIELDING

    # get_shielding by name can be renamed to get_item_by_name in all code
    # keep for now
    def get_shielding_by_name(self, shielding_name):
        return super().get_item_by_name(shielding_name)
    
    @property
    def used_materials(self):
        # return all material names that are in this sequence
        materials = [labels.EMPTY_MATERIAL]
        for shielding in self:
            if len(shielding.materials) > 0:
                materials += [shielding.materials[0][0]]
            if len(shielding.materials) > 1:
                materials += [shielding.materials[1][0]]
        return list(set(materials))
    
    

class ClearanceItemSequence(DefaultNamedModelItemSequence):
    empty_item_label = labels.EMPTY_CLEARANCE
    
    # Legacy 
    # Ugly code to be compatible with old psp files
    @staticmethod
    def from_dict(project_dct):
        if labels.CLEARANCE in project_dct.keys():
            # Read new  clearance model
            lst = project_dct[labels.CLEARANCE]
            items = [Clearance.from_dict(item)\
                     for item in lst]
            
        else:
            # Read old biological half_life and convert to 1 fraction 
            # clearance model
            items = []
            for source in project_dct[labels.SOURCES_NM]:
                apply = source.pop(labels.APPLY_BIOLOGICAL_DECAY, False)
                half_life = source.pop(labels.BIOLOGICAL_HALFLIFE, False)
                
                if apply:
                    item = Clearance(apply_fraction1=apply,
                                                 half_life1=half_life,
                                                 fraction1=1)
                
                    if not(any([item.is_equal(other) for other in items])):
                        items += [item]
                    
                    source[labels.CLEARANCE] = item.name
                else:
                    source[labels.CLEARANCE] = labels.EMPTY_CLEARANCE
               
            
        return items