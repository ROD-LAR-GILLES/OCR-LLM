from abc import ABC, abstractmethod

class LlmPort(ABC):
    @abstractmethod
    def refine(self, markdown: str) -> str: ...

class StoragePort(ABC):
    @abstractmethod
    def read(self, filename: str) -> str: ...
    @abstractmethod
    def write(self, filename: str, content: str) -> str: ...
