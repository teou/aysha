from __future__ import division, print_function

import time
import datetime


class ChatMsg(object):
    def __init__(self, ts, content, source):
        self.ts = ts
        self.content = content
        self.source = source

    @staticmethod
    def to_readable_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return self.source + ': ' + self.content + " at " + ChatMsg.to_readable_timestamp(self.ts)


class User(object):
    def __init__(self, name):
        self.name = name
        self.chat_history = []

    def join(self, room):
        room.add_user(self)

    def __repr__(self):
        return self.name

    def update_msg(self, msg):
        self.chat_history.append(msg)

    def talk(self, msg, room):
        msg = ChatMsg(time.time(), msg, self.name)
        room.publish_msg(msg)


class Room(object):
    def __init__(self):
        self.user = []
        self.chat_msg = []
        self._user_name = set()

    def notify(self, msg):
        for user in self.user:
            user.update_msg(msg)

    def add_user(self, user):
        if user.name not in self._user_name:
            self.user.append(user)
            self._user_name.add(user.name)
            msg = ChatMsg(time.time(), 'user %s joined the channel' % user.name, 'system')
            self.publish_msg(msg)

    def publish_msg(self, msg):
        self.notify(msg)
        self.chat_msg.append(msg)


if __name__ == '__main__':
    room = Room()
    user1 = User('liuhuo1')
    user2 = User('liuhuo2')
    user1.join(room)
    user2.join(room)
    print(user1.chat_history)
    print(user2.chat_history)
    user1.talk("I speak for the truth", room)
    print(user1.chat_history)
    print(user2.chat_history)
