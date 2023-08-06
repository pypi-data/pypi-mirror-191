from datetimejson import loads, load, dumps, dump
from datetime import datetime
from faker import Faker  # type: ignore
from pathlib import Path
import filecmp
import pytest

json_test_path = Path(__file__).parents[0] / 'test.json'

# Build a list of random datetime objects
fake = Faker(['fr_FR'])
Faker.seed(4321)
start_date = datetime(1999, 1, 1, 0, 0, 0, 0)
end_date = datetime(2021, 8, 3, 0, 0, 0, 0)
dt_list = [fake.date_time_between(start_date=start_date,
                                  end_date=end_date)
           for _ in range(10)]


class Unserializable:
    """A mockup class to test non serializable objects"""
    pass


unser = Unserializable()


def test_dumps():
    # Test a single datetime object
    s = dumps(dt_list[0])
    assert s == """{"__type__": "datetime", "year": 2007, "month": 8, "day": 27, "hour": 2, "minute": 15, "second": 10, "microsecond": 0}"""
    # Test a classic object
    s = dumps({'a': 1, 'b': 2})
    assert s == """{"a": 1, "b": 2}"""
    # Test a non serializable object
    with pytest.raises(TypeError):
        s = dumps(unser)


def test_dump(tmp_path):
    with open(tmp_path / 'test.json', 'w') as f:
        dump(dt_list, f)
    assert filecmp.cmp(json_test_path, tmp_path / 'test.json')


def test_loads():
    # Test a single datetime object
    s = """{"__type__": "datetime", "year": 2007, "month": 8, "day": 27, "hour": 2, "minute": 15, "second": 10, "microsecond": 0}"""
    dt = loads(s)
    assert dt == datetime(2007, 8, 27, 2, 15, 10, 0)
    # Test a classic object
    s = """{"a": 1, "b": 2}"""
    assert loads(s) == {'a': 1, 'b': 2}
    # Test an object with a __type__ key but not a datetime
    s = """{"__type__": "foo", "bar": 1}"""
    assert loads(s) == {'__type__': 'foo', 'bar': 1}


def test_load():
    with open(json_test_path) as f:
        dt_list_read = load(f)
    assert dt_list == dt_list_read
