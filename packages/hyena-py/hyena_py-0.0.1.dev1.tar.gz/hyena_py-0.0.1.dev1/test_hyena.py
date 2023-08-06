from unittest import TestCase

from hyena import Hyena, PurifyActionException, skip


def test_validation1(value, **kwargs):
    if type(value) is not list:
        return False
    return len(value) >= 1


def test_validation2(value, **kwargs):
    if type(value) is not dict:
        return False
    return 'field' in value


class TestInspector(TestCase):
    def test_unknown(self):
        target = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
        }
        schema = {
            'one': {},
            'three': {},
            'four': {}
        }
        expected = {
            'one': 1,
            'three': 3,
            'four': 4,
        }
        hyn = Hyena(schema)
        result = hyn.purify(target)
        self.assertEqual(expected, result)

    def test_required(self):
        def _required_checker(key='three'):
            with self.assertRaises(PurifyActionException) as res:
                hyn.purify(target)
            self.assertEqual(key, res.exception.key)
            self.assertEqual('required', res.exception.action)

        target = {
            'one': 0,
            'two': False,
            'three': 3,
            'four': 4,
        }
        schema = {
            'one': {'required': True},
            'two': {'required': True},
            'three': {'required': True},
            'four': {},
        }
        hyn = Hyena(schema)

        for i in ['', None, [], {}, ()]:
            target.update({'three': i})
            _required_checker()

        target.pop('three')
        _required_checker()

        target.update({'three': 3})
        result = hyn.purify(target)
        self.assertEqual(target, result)

    def test_convert(self):
        def _inner_convertor(value):
            return value.split(',')

        target = {
            'one': 123,
            'two': '1234',
            'three': 'one,two,three',
            'four': 0,
            'five': None,
        }
        schema = {
            'one': {'convert': str},
            'two': {'convert': int},
            'three': {'convert': _inner_convertor},
            'four': {'convert': bool},
            'five': {'default': skip, 'convert': int},  # if skip not work, error raised.
        }
        expected = {
            'one': '123',
            'two': 1234,
            'three': ['one', 'two', 'three'],
            'four': False,
        }

        hyn = Hyena(schema)
        result = hyn.purify(target)
        self.assertEqual(expected, result)

    def test_type(self):
        def _type_checker(_key):
            with self.assertRaises(PurifyActionException) as res:
                hyn.purify(target)
            self.assertEqual(_key, res.exception.key)
            self.assertEqual('type', res.exception.action)
            self.assertEqual(_key, res.exception.param)

        target = {
            'int': 123,
            'str': '123',
            'float': 0.123,
            'number': 123,
            'bool': False,
            'list': [1, 2, 3],
            'dict': {'key': 'value'}
        }
        schema = {
            'int': {'type': 'int'},
            'str': {'type': 'str'},
            'float': {'type': 'float'},
            'number': {'type': 'number'},
            'bool': {'type': 'bool'},
            'list': {'type': 'list'},
            'dict': {'type': 'dict'},
        }
        hyn = Hyena(schema)
        result = hyn.purify(target)
        self.assertEqual(target, result)

        check_list = [
            ('int', 'string'),
            ('str', 123),
            ('float', 'string'),
            ('number', 'string'),
            ('bool', [1, 2, 3]),
            ('list', {'key': 'value'}),
            ('dict', 123),
        ]

        for key, value in check_list:
            target.update({key: value})
            _type_checker(key)
            target.pop(key)

    def test_default(self):
        target = {
            'one': '',
            'two': None,
            'three': {},
            'four': [],
            'five': 'value',
        }
        schema = {
            'one': {'default': skip},
            'two': {'default': None},
            'three': {'default': 'default'},
            'four': {'default': 100},
            'five': {},
            'six': {'default': 'NOT_EXISTS_DATA'},
        }
        expected = {
            'two': None,
            'three': 'default',
            'four': 100,
            'five': 'value',
            'six': 'NOT_EXISTS_DATA'
        }

        hyn = Hyena(schema)
        result = hyn.purify(target)
        self.assertEqual(expected, result)

    def test_valid(self):
        def _check_raise(_target, key):
            with self.assertRaises(PurifyActionException) as e:
                hyn.purify(_target)
                exc = e.exception
                self.assertEqual(exc.action, 'valid')
                self.assertEqual(exc.key, key)

        schema = {
            'one': {'valid': test_validation1},
            'two': {'valid': test_validation2},
        }
        target = {'one': 'NOT_VALID'}

        hyn = Hyena(schema)
        _check_raise(target, 'one')

        target['one'] = []
        _check_raise(target, 'one')

        target['one'].append(1)
        target['two'] = {}
        _check_raise(target, 'two')

        # Success
        target['two']['field'] = 1
        hyn.purify(target)

    def test_rename(self):
        def rename_func(value, original):
            return value + '_' + original

        schema = {
            'oneChanged': {'rename': 'one_changed'},
            'with_func': {'rename': rename_func}
        }
        target = {
            'oneChanged': 'value',
            'with_func': 'rename',
        }
        expect = {
            'one_changed': 'value',
            'rename_with_func': 'rename',
        }

        hyn = Hyena(schema)
        result = hyn.purify(target)
        self.assertEqual(expect, result)

    def test_purify(self):
        target = {
            'one': 123,
            'two': None,
            'three': 123,
        }
        schema = {
            'one': {'required': True, 'type': 'int'},
            'two': {'type': 'str', 'default': 'default_str'},
            'three': {'required': True, 'convert': str},
        }
        expected = {
            'one': 123,
            'two': 'default_str',
            'three': '123',
        }

        hyn = Hyena(schema)
        result = hyn.purify(target)
        self.assertEqual(expected, result)
