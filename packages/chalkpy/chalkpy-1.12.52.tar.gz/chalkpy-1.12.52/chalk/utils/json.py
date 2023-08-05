from typing import Dict, List, Union

__all__ = ["TJSON"]

TJSON = Union[None, str, int, float, bool, List["TJSON"], Dict[str, "TJSON"]]
