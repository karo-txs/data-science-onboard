from dataclasses import dataclass
from typing import List


@dataclass(eq=False)
class DbConnection:
    def __init__(
        self,
        tables: List[str],
        env: str,
        host: str = None,
        port: int = None,
        access_key_id: str = None,
        secret_access_key=None,
    ):

        self.env = env
        self.host = host
        self.port = port
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.tables = tables
