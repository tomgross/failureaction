import sys
try:
    from ZODB.POSException import ConflictError
except ImportError:
    # we don't want to depend on Zope here, this package is generally usable

    class ConflictError(Exception):
        """ A dummy ConflictError """

class ActionOnFailure(object):
    """ A decorator for doing an action in case of an exception.
    """

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ConflictError, KeyboardInterrupt), e:
                raise
            except Exception, e:
                context = args[0]
                return self._doaction(context, e)
        self.func = func
        wrapper.__name__ = func.__name__
        wrapper.__dict__.update(func.__dict__)
        wrapper.__doc__ = func.__doc__
        return wrapper

    def _doaction(self, context, e):
        raise NotImplementedError


class PrintOnFailure(ActionOnFailure):
    """ Print something in case of an exception.
    """

    def __init__(self, msg='foo'):
        self.msg = msg

    def _doaction(self, context, e):
        print self.msg

# Selftest

class TestOb(object):

    @PrintOnFailure(msg='foo bar')
    def doaction(self):
        1/0

    @PrintOnFailure()
    def doraise(self):
        raise ConflictError

if __name__ == '__main__':
    ob = TestOb()
    ob.doaction()
    ob.doraise()
