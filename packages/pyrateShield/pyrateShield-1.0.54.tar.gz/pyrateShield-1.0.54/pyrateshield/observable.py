
from pyrateshield import Logger, GLOBAL_LOG_LEVEL
LOG_LEVEL = GLOBAL_LOG_LEVEL

#LOG_LEVEL = 10

class Observable(Logger):
    
    """
    Superclass to generate events that can be observed externally.
    Used for a Model, View, Controller (MVC) GUI design
    """
    def __init__(self, log_level=None):
        if log_level is None:
            log_level = LOG_LEVEL
        super().__init__(log_level=log_level)
        
        self.callbacks = {}
        
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['callbacks']
        return state 

    def connect(self, listener, event_name, callback):
        """
        Add a listener for a specific event.

        Parameters
        ----------
        listener : Object
            Object that listens for event.
        event_name : string
            Name of event that is listent to.
        callback : function
            Function that is called when event is emitted/generated.
            A single positional argument is passed that contais specific data
            for the event.

        Returns
        -------
        None.

        """
        if self.log_level == Logger.LEVEL_DEBUG:
            if listener is not None:
                name_listener = listener.__class__.__name__
            else:
                name_listener = str(None)
            logstr = (f'Adding {name_listener} to event {event_name} of class '
                      f'{self.__class__.__name__} with callback '
                      f'{callback.__name__}')
            
            self.logger.debug(str(logstr))
            
        
        
        if listener not in self.callbacks.keys():
            self.callbacks[listener] = {}
        if event_name not in self.callbacks[listener].keys():
            self.callbacks[listener][event_name] = [True, callback]
        else:
            # connecting the same listener multiple times for the same callback
            # can lead to hard to debug errors
            # if LOG_LEVEL == Logger.LEVEL_DEBUG:
            #     raise KeyError(f'Listener already connected for {event_name}')
            # else:
            self.logger.debug(f'Listener already connected for {event_name}')

    def disconnect(self, listener=None, event_name=None):
        """
        Remove a specific listener/listener

        Parameters
        ----------
        listener : Object
            Object that listens for event.
        event_name : string, optional
            DIf specified only a specific event is removed for this listener.
            If None all events are unsubscribed. The default is None.

        Returns
        -------
        None.

        """
        # if len(self.callbacks) > 0:
        #     raise ValueError()
        if listener is None:
            for listener in self.callbacks.copy().keys():
                self.disconnect(listener=listener, event_name=event_name)
            return
        elif listener not in self.callbacks.keys():
            self.logger.debug(f"listener {listener.__class__.__name__} not connected")
            return
            
        elif event_name is None:
            for event_name in self.callbacks[listener].copy().keys():
                self.disconnect(listener=listener, event_name=event_name)

            return
        
        if listener not in self.callbacks.keys():
            return
        
        callback = self.callbacks[listener].pop(event_name)[1]
        
        if self.log_level == Logger.LEVEL_DEBUG:
            if listener is not None:
                name_listener = listener.__class__
            else:
                name_listener = str(None)
    
            
    
            logstr = f'Removing {name_listener} to event {event_name} of class {self.__class__.__name__} with callback {callback.__name__}'
            
            
            
            self.logger.debug(logstr)
        
        
            
                    

    def disable_connection(self, listener=None, event_name=None):
        """
        Disable a listener for events (temporarily).

        Parameters
        ----------
        listener : Object
            Object that listens for event.
        event_name : string, optional
            DIf specified only a specific event is disabled for this listener.
            If None all events are disabled. The default is None.

        Returns
        -------
        None.

        """
        if listener is None:
            for listener in self.callbacks.copy().keys():
                self.disable_connection(listener=listener, 
                                        event_name=event_name)

            return
            
        elif listener not in self.callbacks.keys():
            return
        
        if event_name is None:
            for event_name in self.callbacks[listener].copy().keys():
                self.disable_connection(listener=listener, 
                                        event_name=event_name)
 
            return

        if event_name in self.callbacks[listener].keys():
            self.callbacks[listener][event_name][0] = False
    
        if self.log_level == Logger.LEVEL_DEBUG:
        
            if listener is not None:
                name_listener = listener.__class__.__name__
            else:
                name_listener = str(None)
                    
            callback = self.callbacks[listener][event_name][1]
        
            logstr = f'Disabling {name_listener} to event {event_name} of class {self.__class__.__name__} with callback {callback.__name__}'        
            self.logger.debug(logstr)


    def enable_connection(self, listener=None, event_name=None):
        """
        Enable a listener for events (temporarily).

        Parameters
        ----------
        listener : Object
            Object that listens for event.
        event_name : string, optional
            DIf specified only a specific event is enabled for this listener.
            If None all events are enabled. The default is None.

        Returns
        -------
        None.

        """
        if listener is None:
            for listener in self.callbacks.copy().keys():
             
                self.enable_connection(listener=listener, 
                                        event_name=event_name)
            return
        
        elif listener not in self.callbacks.keys():
            return
            
        if event_name is None:
            for event_name in self.callbacks[listener].keys():
            
                self.enable_connection(listener=listener, 
                                        event_name=event_name)
            return
        
        if event_name in self.callbacks[listener].keys():
            self.callbacks[listener][event_name][0] = True
    
        if self.log_level == Logger.LEVEL_DEBUG:
        
            if listener is not None:
                name_listener = listener.__class__.__name__
            else:
                name_listener = str(None)
                    
            callback = self.callbacks[listener][event_name][1]
        
            logstr = f'Enabling {name_listener} to event {event_name} of class {self.__class__.__name__} with callback {callback.__name__}' 
            
            self.logger.debug(logstr)

    def emit(self, event_name, event_data=None):
        """
        Generate/Emit an event

        Parameters
        ----------
        event_name : string
            Name of the event that is generated/emitted.
        event_data : Object, optional
            Event data that is passed to listeners/listeners.
            The default is None.

        Returns
        -------
        None.

        """
        
        # mouse interactions add and remove callbacks quickly create copy
        # to prevent dictionary changes during iteration
        
        for listener, events in self.callbacks.copy().items():
            if event_name in events.keys():
                enabled, callback = self.callbacks[listener][event_name]
                

                if self.log_level == self.LEVEL_DEBUG:
                    if listener is not None:
                        name_listener = listener.__class__.__name__
                    else:
                        name_listener = str(None)
                

                    if enabled:
                        logstr = (f'Event {event_name} emitted, callback {callback.__name__} of {name_listener} is called') 
                    else:
                        logstr = (f'Event {event_name} emitted but disabled callback {callback.__name__} of {name_listener}') 
                        
                    self.logger.debug(logstr)
                if enabled:
                    callback(event_data)
                    
                    

