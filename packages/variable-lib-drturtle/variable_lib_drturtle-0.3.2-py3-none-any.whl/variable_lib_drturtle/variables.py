import matplotlib.pyplot as plt
import re
from functools import total_ordering

U_RE = re.compile(r"^(?P<name>.+?)(?:\((?P<unit>.+)\))?$", flags=re.MULTILINE)


class Variable(float):
    def __new__(self, value, name: str):
        return float.__new__(self, value)

    def __init__(self, value, name: str):
        float.__init__(value)
        match = U_RE.match(name)
        self.unit = (match.group("unit") or "").strip()
        self.var_name = match.group("name").strip()
        self.name = f'{self.var_name}{f" ({self.unit})" if self.unit else ""}'.strip()

    @property
    def with_unit(self):
        return f"{self:.3f} {self.unit}"

    @property
    def name_val(self):
        return f"{self.var_name}: {self.with_unit}"

    def __iadd__(self, other):
        return Variable(self + other, self.name)

    def __isub__(self, other):
        return Variable(self - other, self.name)

    def __imul__(self, other):
        return Variable(self * other, self.name)

    def __idiv__(self, other):
        return Variable(self / other, self.name)


@total_ordering
class VariableList:
    def __init__(self, initial: Variable):
        self.name = initial.name
        self.vals = [initial]

    @classmethod
    def new(cls, initial_value, name):
        init = Variable(initial_value, name)
        return cls(init)

    @classmethod
    def empty(cls, name):
        i = Variable(0, name)
        inst = cls(i)
        inst.vars = []
        return inst

    @property
    def value(self):
        return self.vals[-1]

    def __getitem__(self, key: int):
        return self.vals[key]

    def __setitem__(self, key: int, val: Variable):
        self.vals[key] = val

    def __delitem__(self, key: int):
        del self.vals[key]

    def __iadd__(self, val):
        new = Variable(self.vals[-1] + val, self.name)
        self.append(new)
        return self

    def __imul__(self, val):
        new = Variable(self.vals[-1] * val, self.name)
        self.append(new)
        return self

    def append(self, val: Variable):
        if val.name != self.name:
            print(val.name, self.name)
            raise ValueError("Variables must be of the same name.")
        self.vals.append(val)

    def add(self, val):
        new = Variable(val, self.name)
        self.vals.append(new)

    def __len__(self):
        return len(self.vals)

    def __str__(self):
        return f"List ({self.name}): " + str(self.vals)

    def __lt__(self, other):
        return self.value < other

    def __eq__(self, other):
        if not isinstance(other, VariableList):
            return False
        return self.vals == other.vals

    def last_element_equals(self, other):
        return self.value == other


def scatter(x: VariableList, y: VariableList, x_name=None, y_name=None):
    plt.scatter(x, y)
    plt.xlabel(x.name)
    plt.ylabel(y.name)
    plt.title(f"{x.name} vs {y.name}")

    return plt


def drag_force(rho, v, C, A):
    """Caculates the drag force for an object at a speed

    :param rho: Density of fluid/air. Standard is 1.204 kg/m^3
    :param v: Velocity of object (m/s)
    :param C: Coefficient of Drag
    :param A: Cross-sectional Area (m^2)
    """
    return (1 / 2) * rho * (v**2) * C * A


def print_all(*args):
    out = []
    for arg in args:
        out.append(arg.value.name_val)
    print(", ".join(out))
