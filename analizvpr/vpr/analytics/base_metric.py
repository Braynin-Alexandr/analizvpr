from abc import ABC, abstractmethod
from enum import Enum

from vpr.analytics.student import Students


class MarkType(Enum):
    """
    Class for defining mark types used in child classes of BaseMetric.
    Класс для типизации оценок в дочерних классах BaseMetric.
    """
    EXAM = "exam_mark"
    THIRD_QUARTER = "third_quarter"


class BaseMetric(ABC):
    """
    Base class for all metrics.
    Базовый класс для всех метрик.
    """
    metric_name: str = None
    mark_type: MarkType = None

    @abstractmethod
    def calculate(self, students_data: Students):
        pass


class BaseVerification(ABC):
    """
    Base class for data verification.
    Базовый класс для верификации данных.
    """
    bad_message: str = None

    @abstractmethod
    def get_verification(self, students_data: Students) -> bool:
        """
        Returns True if the object has passed verification.
        Возвращает True, если объект прошел верификацию.
        """
        pass
