from typing import Type, List
from .async_channel import AsyncChannel
from pika.channel import Channel
from random import randint
import logging


class ChannelPool:
    def __init__(self, factory: Type[AsyncChannel], count=1) -> None:
        self._limit = count
        self.free = count
        self._channels: List[AsyncChannel] = [ AsyncChannel() for i in range(0, self._limit)]
    
    def open(self, connection):
        [channel.open(connection) for channel in self._channels]
    
    def set_on_all(self, name, value):
        [setattr(channel, name, value) for channel in self._channels]
    
    def do_on_all(self, func):
        [func(channel) for channel in self._channels]

    def get_channel(self):
        if self.free>0:
            self.free-=1
        else:
            self.free=self._limit
        return self._channels[self.free-1]
    
    def is_open(self):
        return self._channels[0].is_open