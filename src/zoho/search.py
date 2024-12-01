from typing import Any
from urllib.parse import quote


class Criterion:
    def __init__(self, key: str, operator: str, value: Any):
        self.key = key
        self.operator = operator
        self.value = value

    def __call__(self):
        return f"({self.key}:{self.operator}:{quote(self.escape_value())})"

    def escape(self, value) -> str:
        if isinstance(value, bool):
            value = str(value).lower()
        value = str(value).replace(",", "\\,").replace("(", "\\(").replace(")", "\\)")
        if value[-1] == "\\":
            value += "\\"
        return value

    def escape_value(self) -> str:
        return self.escape(self.value)


class InCriterion(Criterion):
    value: list[Any]

    def __init__(self, key: str, value: Any):
        if not isinstance(value, list):
            value = [value]
        super().__init__(key, "in", value)

    def escape_value(self) -> str:
        return ",".join(self.escape(v) for v in self.value)


class BetweenCriterion(Criterion):
    value: tuple[Any, Any]

    def __init__(self, key: str, value: tuple[Any, Any]):
        super().__init__(key, "between", value)

    def escape_value(self) -> str:
        return ",".join(self.escape(v) for v in self.value)


class Search:
    _criteria: list[Criterion]

    def __init__(self, **eq):
        self._criteria = []
        self.eq(**eq)

    def __call__(self):
        return f"({"and".join(c() for c in self._criteria)})"

    def _add_terms(self, operator: str, **terms):
        for key, value in terms.items():
            self._criteria.append(Criterion(key=key, operator=operator, value=value))
        return self

    def eq(self, **terms):
        return self._add_terms(operator="equals", **terms)

    def ne(self, **terms):
        return self._add_terms(operator="not_equal", **terms)

    def in_(self, **terms):
        for key, value in terms.items():
            try:
                criterion = [c for c in self._criteria if isinstance(c, InCriterion) and c.key == key][0]
                assert isinstance(criterion, InCriterion)
                if value not in criterion.value:
                    criterion.value.append(value)
            except IndexError:
                self._criteria.append(InCriterion(key=key, value=value))
        return self

    def gt(self, **terms):
        return self._add_terms(operator="greater_than", **terms)

    def gte(self, **terms):
        return self._add_terms(operator="greater_equal", **terms)

    def lt(self, **terms):
        return self._add_terms(operator="less_than", **terms)

    def lte(self, **terms):
        return self._add_terms(operator="less_equal", **terms)

    def startswith(self, **terms):
        return self._add_terms(operator="starts_with", **terms)

    def between(self, key: str, term1: Any, term2: Any):
        self._criteria.append(BetweenCriterion(key=key, value=(term1, term2)))
        return self
