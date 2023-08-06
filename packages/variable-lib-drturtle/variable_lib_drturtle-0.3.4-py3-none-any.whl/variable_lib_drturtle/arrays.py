import numpy as np
import re
import matplotlib.pyplot as plt
from variable_lib_drturtle.variables import *
from dataclasses import dataclass

U_RE = re.compile(r"^(?P<name>.+?)(?:\((?P<unit>.+)\))?$", flags=re.MULTILINE)


@dataclass
class Value1D:
    """Represents one dimension of a two-dimensional value.
    Should not be created manually, but gotten from a VariableList2D instance.
    Do not set these to a variable, but retrieve them from an instance.
    """

    name: str
    unit: str
    values: np.ndarray

    @property
    def with_unit(self):
        """Returns the current value of the variable, plus its unit.

        :rtype: str
        """
        return f"{self.value} {self.unit}"

    @property
    def name_val(self):
        """Returns the name, unit, and current value of the variable.

        :rtype: str
        """
        return f"{self.name}: {self.with_unit}"

    @property
    def value(self):
        """Returns the most recent value"""
        return self.values[-1]

    def __getitem__(self, key: int):
        return self.values[key]

    def __len__(self):
        return len(self.values)


class VariableList2D:
    """Represents a list of 2D values, like position or velocity."""

    def __init__(self, name: str, initial: np.ndarray):
        """Takes a variable name and a 1D array with the first value.

        :param name: Name of the variable (with unit)
        :type name: str
        :param initial: Initial value of the variable. ex `np.ndarray([0, 0])`
        :type initial: np.ndarray
        """
        match = U_RE.match(name)
        self.unit = (match.group("unit") or "").strip()
        self.var_name = match.group("name").strip()
        self.name = f'{self.var_name}{f" ({self.unit})" if self.unit else ""}'.strip()

        self.vals: np.ndarray[np.ndarray] = np.array([initial])

    @classmethod
    def from_array(cls, name, arr: np.ndarray):
        """Depricated"""
        return cls(name, arr)

    def append(self, x, y):
        """Creates a 1D array and appends it to the list."""
        arr = np.array([x, y])
        self.add(arr)

    def add(self, arr: np.ndarray):
        """Adds an x, y pair to the list.

        :param arr: A pair, like `np.array([1, 2])`
        :type arr: np.ndarray
        """
        if self.vals.size == np.array([]).size:
            self.vals = np.array([arr])
        else:
            self.vals = np.vstack((self.vals, arr))

    def __iadd__(self, other):
        """Adds other to the last value, then appends"""
        if not isinstance(other, np.ndarray):
            raise ValueError("Other must be ndarray")
        self.add(other + self.vals[-1])
        return self

    def __isub__(self, other):
        if not isinstance(other, np.ndarray):
            raise ValueError("Other must be ndarray")
        self.add(other + self.vals[-1])
        return self

    def __add__(self, other):
        return other + self.value

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __div__(self, other):
        return self.value / other

    def __pow__(self, other):
        return self.value**other

    def __getitem__(self, key: int):
        return self.vals[key]

    def __setitem__(self, key: int, val: np.ndarray):
        self.vals[key] = val

    def __delitem__(self, key: int):
        del self.vals[key]

    @property
    def value(self):
        """The current, most recent value in the list.

        :rtype: np.ndarray
        """
        return self.vals[-1]

    @property
    def x_values(self):
        return self.vals.T[0]

    @property
    def x_name(self):
        return f"X {self.name}"

    @property
    def y_values(self):
        return self.vals.T[1]

    @property
    def y_name(self):
        return f"Y {self.name}"

    @property
    def x(self):
        return Value1D(f"X {self.name}", self.unit, self.x_values)

    @property
    def y(self):
        return Value1D(f"Y {self.name}", self.unit, self.y_values)

    @property
    def magnitude(self):
        return np.linalg.norm(self.value)

    @property
    def with_unit(self):
        return f"{self.value} {self.unit}"

    @property
    def name_val(self):
        return f"{self.var_name}: {self.with_unit}"


def scatter_2d(x_list, y_list, do_x=False):
    """Deprecated"""
    if isinstance(x_list, VariableList):
        x_name = x_list.name
        x_vals = x_list
    elif isinstance(x_list, VariableList2D):
        x_name = x_list.x_name
        x_vals = x_list.x_values

    if isinstance(y_list, VariableList):
        y_name = y_list.name
        y_vals = y_vals
    elif isinstance(y_list, VariableList2D):
        y_name = y_list.y_name if not do_x else y_list.x_name
        y_vals = y_list.y_values if not do_x else y_list.x_values

    plt.scatter(x_vals, y_vals)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(f"{x_name} vs {y_name}")

    return plt


def drag_force_2d(velocity: VariableList2D, rho, C, A):
    vMag = velocity.magnitude
    vHat = velocity / vMag  # direction of velocity

    Fdrag = (1 / 2) * rho * (vMag**2) * C * A * vHat
    return Fdrag
