from abc import ABC, abstractmethod

class Processor(ABC):

    def __init__(self,config=None):
        self.config = config
        super.__init__()

    @abstractmethod
    def process(self,data=None):
        pass
