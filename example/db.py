import os
from datetime import datetime
from pony.orm import *


db = Database()


class Device(db.Entity):
    name = PrimaryKey(str)
    data_channels = Set('DataChannel')


class ChannelEntry(db.Entity):
    id = PrimaryKey(int, auto=True)
    time = Required(datetime,default=lambda:datetime.utcnow())
    numeric_value = Optional(float)
    metadata = Optional(Json)
    data_channel = Required('DataChannel')


class DataChannel(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    device = Required(Device)
    device_time_entrys = Set(ChannelEntry)
    data_type = Required(str)

