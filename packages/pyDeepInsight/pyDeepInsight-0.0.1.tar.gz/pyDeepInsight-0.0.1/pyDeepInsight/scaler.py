import numpy as np


class LogScaler:
    """Log normalize and scale data

    Log normalization and scaling procedure as described as norm-2 in the
    DeepInsight paper supplementary information.
    """

    def __init__(self):
        self._min0 = None
        self._max = None
        pass

    def fit(self, X, y=None):
        self._min0 = X.min(axis=0)
        self._max = np.log(X + np.abs(self._min0) + 1).max()

    def fit_transform(self, X, y=None):
        self._min0 = X.min(axis=0)
        X_norm = np.log(X + np.abs(self._min0) + 1)
        self._max = X_norm.max()
        return X_norm / self._max

    def transform(self, X, y=None):
        X_norm = np.log(X + np.abs(self._min0) + 1).clip(0, None)
        return (X_norm / self._max).clip(0, 1)


class insightMinMaxScaler:
    """Scaler for MinMaxScaler that clips the values to 0 and 1 when above.
    Does the same as a MinMaxScaler from scikit learn but clips some values."""

    def __init__(self):
        self._min0 = None
        self._max0 = None
        pass

    def fit(self, X, y=None):
        self._min0 = X.min(axis=0)
        self._max0 = X.max(axis=0)

    def fit_transform(self, X, y=None):
        self._min0 = X.min(axis=0)
        self._max0 = X.max(axis=0)
        return ((X - self._min0) / (self._max0 - self._min0)).clip(0, 1)

    def transform(self, X, y=None):
        return ((X - self._min0) / (self._max0 - self._min0)).clip(0, 1)
