class DummyProcess(object):
    def start(self, target):
        target()

class DummyLock(object):
    pass

class DummyProcessing(object):
    def __init__(self):
        pass

    @staticmethod
    def Lock():
        return DummyLock()

    @staticmethod
    def RLock():
        return DummyLock()

    @staticmethod
    def Process(target):
        return DummyProcess(target)

    @staticmethod
    def Queue():
        return Queue()
