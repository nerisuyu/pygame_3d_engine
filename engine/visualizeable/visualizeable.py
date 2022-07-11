from abc import ABC, abstractmethod
import weakref

class Visualizeable(ABC):
    @abstractmethod
    def __init__(self, parent):
        self.__parent = weakref.ref(parent) if parent else parent

    @abstractmethod
    def draw(self, camera, renderBuffer, globalLight, localLights): ...

    @property
    def parent(self):
        if not self.__parent:
            return self.__parent
        __parent = self.__parent()
        if __parent:
            return __parent
        else:
            raise LookupError("Parent was destroyed")

    def set_parent(self,parent):
        self.__parent = weakref.ref(parent) if parent else parent

    def __del__(self):
        print("deleted", self)


