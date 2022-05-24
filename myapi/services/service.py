from abc import ABC , abstractclassmethod , abstractmethod



class Service(ABC):
     
    @abstractclassmethod
    def get_by_id(id):
        pass

    @abstractclassmethod
    def create(**kwargs):
        pass

    @abstractclassmethod
    def update(**kwargs):
        pass