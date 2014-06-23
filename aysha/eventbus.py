#-*- coding:utf-8 -*-

"""
a simple event bus
"""
class EventBus(object):

    def __init__(self):
        self.subs = {}

    #TODO create a decorator for this : @subscribe on functions
    def sub(self, event, callback):
        callbacks = self.subs.get(event)
        if callbacks is None:
            callbacks = {}
            self.subs[event] = callbacks
        callbacks[callback] = callback

    """
    TODO doing a event bus @subscribe annotation
    seems much more difficult in python than in 
    java.
    def subscribe(self, event, callback):
        def __decorated(func):
            
            def __docall(*args, **kwargs):
                func(*args, **kwargs)
            return __docall
        return __decorated
    """

    def unsub_all(self, event=None, callback=None):
        if event is None:
            self.subs.clear()
        else:
            callbacks = self.subs.get(event)
            if callbacks is None:
                return
            if callback:
                callbacks.pop(callback, None)
            else:
                callbacks.clear()

    def pub(self, event, *args, **kwargs):
        callbacks = self.subs.get(event)
        if callbacks:
            for k,v in callbacks.items():
                callbacks[v](*args, **kwargs)

