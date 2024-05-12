import dataclasses
from typing import Optional
from uuid import uuid4


@dataclasses.dataclass
class Order:
    user_id: int
    user_name: str
    user_language: str = "de"
    order_id: Optional[str] = dataclasses.field(
        default_factory=lambda: str(uuid4()))
    products: dict = dataclasses.field(default_factory=dict)
