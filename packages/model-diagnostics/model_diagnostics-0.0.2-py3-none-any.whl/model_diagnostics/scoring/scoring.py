from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
import numpy.typing as npt
import polars as pl
from scipy import special

from .._utils.array import (
    validate_2_arrays,
)


class BaseScoringFunction(ABC):
    """A base class for scoring functions."""
    @property
    def functional(self):
        return ""

    @abstractmethod
    def __call__(
        self,
        y_obs: npt.ArrayLike,
        y_pred: npt.ArrayLike,
    ) -> npt.ArrayLike:
        """Score per observation."""
        pass

    def mean(self,
        y_obs: npt.ArrayLike,
        y_pred: npt.ArrayLike,
        weights: Optional[npt.ArrayLike] = None,        
    ) -> float:
        """Mean or average score."""
        np.average(self.__call__(y_obs, y_pred), weights=weights)

class HomogeneousScoringFunction(BaseScoringFunction):
    """Homogeneous scoring function of degree h.

    Parameters
    ----------
    degree : float

    Attributes
    ----------
    functional: "mean"
    
    Notes
    -----
    The homogeneous score of degree \(h\) is given by

    \[
    S_h(y, z) = 2\frac{\abs{y}^h - \abs{z}^h}{h(h-1)} - 2\frac{\abs{z}^{h-1}}{h-1}(y-z)\)
    \]
    
    There are important domain restrictions and limits.
        - \(h>1\): All real numbers \(y\) and \(z\) are allowed. Note, for \(h=2\) this
          equals the squared error, aka Normal deviance.
        - \(0 < h \leq 1\): Only \(y \geq 0\), \(z>0\). In the special case of \(h=1\),
          \(S_h(y, z) = 2(y\log\frac{y}{z} - y + z)\) is the Poisson deviance.
        - \(h \leq 0\): Only \(y>0\), \(z>0\). In the special case of \(h=0\),
          \(S_h(y, z) = 2(\frac{y}{z} -\log\frac{y}{z} - 1)\) is the Gamma deviance.

    This degree of homogeneity \(h = 2-p\) with Tweedie power \(p\) for common domains
    of the arguments.
    """
    def __init__(self, degree: float) -> None:
        self.degree = degree
    
    @property
    def functional(self):
        return "mean"

    def __call__(
        self,
        y_obs: npt.ArrayLike,
        y_pred: npt.ArrayLike,
    ) -> npt.ArrayLike:
        """Score per observation."""
        y: np.ndarray
        y: np.ndarray
        y, z = validate_2_arrays(y_obs, y_pred)
        if self.degree == 2:
            # Fast path
            return np.square(z - y)
        elif self.degree > 1:
            z_abs = np.abs(z)
            return 2 * (
                (np.power(np.abs(y), self.degree) - np.power(z_abs, self.degree)) / (self.degree * (self.degree - 1))
                -  np.sign(z) / (self.degree - 1) * np.power(z_abs, self.degree - 1) * (y - z)
            )
        elif self.degree == 1:
            # Should error when y<0 or x<=0.
            return 2 * (special.xlogy(y, y / z) - z + y)
        elif self.degree == 0:
            # Should error when y<0 or x<0.
            y_z = y/z
            return 2 * (np.log(y_z) - y_z - 1)
        else:  # self.degree < 1
            # Should error when y<0 or x<0.
            return 2 * (
                (np.power(y, self.degree) - np.power(z, self.degree)) / (self.degree * (self.degree - 1))
                -  1 / (self.degree - 1) * np.power(z, self.degree - 1) * (y - z)
            )


class SquaredError(HomogeneousScoringFunction):
    """Squared error.""" 
    def __init__(self) -> None:
        super().__init__(degree=2)
