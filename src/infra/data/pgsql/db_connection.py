from dataclasses import dataclass, field


@dataclass
class DbConnection:
    dbname: str
    host: str
    user: str = field(repr=False)
    password: str = field(repr=False)
    port: str
