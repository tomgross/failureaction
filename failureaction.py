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

    locals = None

    def __call__(self, func):
        def probe_func(frame, event, arg):
            if event == 'return':
                self.locals = frame.f_locals
                self.locals.pop('self', None)
                sys.settrace(None)
            return probe_func
        def wrapper(*args, **kwargs):
            try:
                sys.settrace(probe_func)
                return func(*args, **kwargs)
            except (ConflictError, KeyboardInterrupt), e:
                raise
            except Exception, e:
                context = args[0]
                self._doaction(context, e)
        self.func = func
        wrapper.__name__ = func.__name__
        wrapper.__dict__.update(func.__dict__)
        wrapper.__doc__ = func.__doc__
        return wrapper

    def _doaction(self, context, e):
        raise NotImplementedError


class MailOnFailure(ActionOnFailure):
    """ Send a mail in case of an exception.
    """

    def __init__(self, subject='foo'):
        self.subject = subject

    def _doaction(self, context, e):
        print self.locals
        pass

class LogOnFailure(ActionOnFailure):
    """ Log to event-log in case of an exception.
    """

    def _doaction(self, context, e):
        pass

# Selftest

class TestOb(object):

    @MailOnFailure(subject='foo bar')
    def withmail(self):
        data = 42
        1/0

    @MailOnFailure()
    def raiseerror(self):
        raise ConflictError

if __name__ == '__main__':
    ob = TestOb()
    ob.withmail()
    ob.raiseerror()
