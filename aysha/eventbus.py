#-*- coding:utf-8 -*-

from gevent import spawn

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

        #the key and value of the callbacks map are the same, redundency here?
        callbacks[callback] = callback

    """
    TODO doing a event bus @subscribe annotation
    seems much more difficult in python than in 
    java since there is not a applicationContext
    in python :).
    def subscribe(self, event, callback):
        def __decorated(func):
            def __docall(*args, **kwargs):
                func(*args, **kwargs)
            return __docall
        return __decorated
    """

    def inner_subscribe(self, event):
        def __decorated(f):
            self.sub(event, f)
            def __replacement(*args, **kwargs):
                f(*args, **kwargs)
            return __replacement
        return __decorated

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
        greenlets = []
        if callbacks:
            for k, v in callbacks.items():
                greenlets.append(spawn(v, *args, **kwargs))
        return greenlets


def outer_subscribe(event_bus, event):
    def wrap_callback(f):
        callbacks = event_bus.subs.get(event)
        if callbacks is None:
            callbacks = {}
            event_bus.subs[event] = callbacks
        callbacks[f] = f

        def wrapped(*args, **kwargs):
            f(*args, **kwargs)
        return wrapped
    return wrap_callback


if __name__ == '__main__':
    eb = EventBus()
    def testSub(test):
        print "testSub:", test
    event = "testSub"
    eb.sub(event, testSub)
    greenlets = eb.pub(event, "test word haha")
    from gevent import joinall
    joinall(greenlets)
    
    eb.unsub_all(event, testSub)
    greenlets2 = eb.pub(event, "2 haha 2")
    joinall(greenlets2)
    #######################################
    eb1 = EventBus()
    event1 = "event_1"

    @outer_subscribe(eb1, event1)
    def callback1(test):
        print 'test callback', test

    greenlets = eb1.pub(event1, "this is argument to callback1")
    joinall(greenlets)
    ########################################
    eb2 = EventBus()
    event2 = "event_2"

    @eb2.inner_subscribe(event2)
    def callback2(test):
        print 'test callback', test
    greenlets = eb2.pub(event2, "this is argument to callback2")
    joinall(greenlets)

