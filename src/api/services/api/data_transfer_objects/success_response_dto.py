from dataclasses import field, dataclass


@dataclass(eq=False)
class SuccessResponseDto:
    state: str
    message: str = field(default="ok")
