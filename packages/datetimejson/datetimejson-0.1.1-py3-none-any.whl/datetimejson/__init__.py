"""
Handle datetime objects in json format
"""

from datetime import datetime
import json
from typing import Any, Union


class DateTimeDecoder(json.JSONDecoder):
    """A class to decode datetime objects from json"""

    def __init__(self, *args, **kargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                                  *args, **kargs)

    def dict_to_object(self, d: dict) -> Union[dict, datetime]:
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except TypeError:
            d['__type__'] = type
            return d


class DateTimeEncoder(json.JSONEncoder):
    """
    Instead of letting the default encoder convert datetime to string,
    convert datetime objects into a dict, which can be decoded by the
    DateTimeDecoder
    """

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
            }
        else:
            return json.JSONEncoder.default(self, obj)


def loads(*args, **kwargs) -> Any:
    """Load json string and return python object"""
    kwargs['cls'] = DateTimeDecoder
    return json.loads(*args, **kwargs)


def load(*args, **kwargs) -> Any:
    """Load json file and return python object"""
    kwargs['cls'] = DateTimeDecoder
    return json.load(*args, **kwargs)


def dumps(*args, **kwargs) -> str:
    """Return json string from object"""
    kwargs['cls'] = DateTimeEncoder
    return json.dumps(*args, **kwargs)


def dump(*args, **kwargs):
    """Export object to json file"""
    kwargs['cls'] = DateTimeEncoder
    json.dump(*args, **kwargs)
