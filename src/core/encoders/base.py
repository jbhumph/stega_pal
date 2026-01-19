from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class EncodeResult:
    success: bool
    data: Any          # PIL Image or similar
    message: str
    capacity_used: int = 0
    capacity_total: int = 0

class BaseEncoder(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def encode(self, carrier_path: str, payload: bytes, settings: dict) -> EncodeResult: ...
