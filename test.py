import numpy as np
from io import BytesIO

class Foo(object):
    def setup(self):
        print('This is setup')

    @classmethod
    def setup_class(cls):
        print('This is setup_class')


def fake_setup(obj):
    print('It is fake, {}'.format(obj))


def fake_setup_class(clz):
    print('It is fake from clz, {}'.format(clz))


def test_fake_instance_method():
    foo = Foo()
    print('before: {}'.format(foo.setup))
    foo.setup()

    foo2 = Foo()
    foo2.setup = fake_setup.__get__(foo2)
    print('after: {}'.format(foo2.setup))
    foo2.setup()


def test_fake_class_method():
    foo = Foo()
    print('before: {}'.format(foo.setup_class))
    foo.setup_class()

    foo2 = Foo()
    foo2.setup_class = fake_setup_class.__get__(foo2.__class__)
    print('after: {}'.format(foo2.setup_class))
    foo2.setup_class()


def test_io():
    # a = np.array([[1, 2], [3, 4]], dtype=int)
    # # fmt = '%.18e'
    # c = BytesIO()
    # np.savetxt(c, a, delimiter=',', fmt='%d')
    # c.seek(0)
    # print(c.readlines())

    # fmt = '%.18e'
    # fmt2 = '.18e'
    # line = (fmt + ' ' + fmt + '\n') % (1, 2)
    # line2 = '{:{fmt}} {:{fmt}}'.format(1, 2, fmt=fmt2)
    # print(line)
    # print(line2)

    c = BytesIO()
    c.write('0,0,0\n1,1,1')
    c.seek(0)
    print(c.readlines())


if __name__ == '__main__':
    test_io()
