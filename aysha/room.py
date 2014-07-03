#-*- coding:utf-8 -*-

from eventbus import event_bus, EVENT_CAST_SPELL, EVENT_SPEAK

"""
class as a room
"""
class Room(object):
    
    def __init__(self, name):
        self.name = name
        self.users = {}
        event_bus.sub(EVENT_SPEAK, self._user_speak)
        event_bus.sub(EVENT_CAST_SPELL, self._user_cast)
       
    def has_user(self, name):
        return name in self.users

    def get_user(self, name):
        return self.users.get(name, None)

    """
    callback=function(room, frm, reciever, msg)
    """
    def broadcast(self, msg, callback=None):
        for user in self.users.values():
            user.spoken(self, msg, callback)

    def _user_cast(self, frm, spell, targets=None):
        if targets is None:
            targets = self.users.values()
        spell.caster = frm
        for user in targets:
            user.damaged(spell)

    def _user_speak(self, frm, msg, targets=None):
        if targets is None:
            targets = self.users.values()
        for user in targets:
            user.spoken(frm, msg)

    """
    join the game
    called only when first login to a room
    """
    def join(self, user, callback=None):
        self.users[user.name] = user
        user.join(self)
        self.broadcast(user.name+' joined game '+self.name, callback)

    """
    quit the game.
    logout does not call quit
    """
    def quit(self, name, callback=None):
        user = self.users.pop(name, None)
        if(user):
            user.quit(self)
            self.broadcast(user.name+' quit game '+self.name, callback)

