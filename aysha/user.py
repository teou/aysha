#-*- coding:utf-8 -*-

from eventbus import event_bus,EVENT_CAST_SPELL,EVENT_SPEAK

class User(object):

    def __init__(self, name, room=None, blood=100):
        self.name = name
        self.join(room)
        self.blood = blood

    def join(self, room):
        self.room = room

    def quit(self, room):
        self.room = None

    def cast_spell(self, spell, targets=None):
        spell.caster = self
        event_bus.pub(EVENT_CAST_SPELL, self, spell, targets)

    def damaged(self, spell):
        self.blood = self.blood - spell.damage

    def speak_to(words, targets=None):
        event_bus.pub(EVENT_SPEAK, self, words, targets)
        pass

    def spoken(self, frm, msg, callback=None):
        if callback:
            callback(self.room, frm, self, msg)

