from dataclasses import dataclass
from typing import Any, List


@dataclass
class ColumnValuePair:
    column: str
    value: Any


@dataclass
class ColumnValuePairList:
    pairs: List[ColumnValuePair]

    def to_dict(self):
        output = dict()
        for pair in self.pairs:
            output[pair.column] = pair.value
        return output
