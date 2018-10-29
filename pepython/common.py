# Logging TODO: use python's logging module
class Logger(object):
    def set_verbose(self,verbose=True):
        self._verbose = verbose

    def log(self, message):
        print(message)

    def log_verbose(self, message):
        if not self._verbose:
            return
        self.log(message)

logger = Logger()


def fail(message):
    logger.log(message)
    exit(1)


def list_get(list, index, default=None):
    return list[index] if len(list) > index else default


class Result(object):

    def __init__(self, value=None):
        self.value = value


class OkResult(Result):

    def __init__(self, *a, **kwa):
        super(OkResult, self).__init__(*a, **kwa)
        self.ok = True


class ErrorResult(Result):

    def __init__(self, *a, **kwa):
        super(ErrorResult, self).__init__(*a, **kwa)
        self.ok = False
        self.error = self.value
