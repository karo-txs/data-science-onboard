from dataclasses import dataclass, field

@dataclass
class Model:
    model: any = field(default=None)
    params: dict = field(default=None)
    name: str = field(default="")
    