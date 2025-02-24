from typing import Dict, Any, List

from vpr.analytics.base_metric import BaseMetric
from vpr.analytics.general_metrics import TotalStudentsMetric, CounterMarksThirdQuarterMetric, \
    StudentsPresentExamMetric, ListStudentsAndMarksMetric, CounterMarksExamMetric, QualityThirdQuarterMetric, \
    QualityExamMetric, SuccessThirdQuarterMetric, SuccessExamMetric, AverageMarkThirdQuarterMetric, \
    AverageMarkExamMetric, AverageSolvedExamTasks, ImproveMarkMetric, ReduceMarkMetric, PopularMistakes, \
    VerificationResults
from vpr.analytics.student import Students
from vpr.analytics.utils import translate_russian
from vpr.analytics.verification_metrics import VerificationPresent, VerificationMarkThreshold, VerificationAverageMarks


class MetricsController:
    """
    Class for calculating all general_metrics.
    Класс для расчета всех general_metrics.
    """
    def __init__(self, students_data: Students, metrics: List):
        self.students = students_data if isinstance(students_data, Students) else None
        self.metrics = [m for m in metrics if isinstance(m, BaseMetric)]

    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Generates calculation results for general_metrics.
        Генерирует результаты расчетов general_metrics.
        """
        calculations = {}
        for metric in self.metrics:
            calculations[metric.metric_name] = metric.calculate(self.students)
        return calculations


@translate_russian
def get_report(data) -> Dict[str, Any]:
    students_data = data.get("students_data")
    mark_threshold = data.get('mark_3')

    metrics = [
        TotalStudentsMetric(),
        StudentsPresentExamMetric(),
        ListStudentsAndMarksMetric(),
        CounterMarksThirdQuarterMetric(),
        CounterMarksExamMetric(),
        QualityThirdQuarterMetric(),
        QualityExamMetric(),
        SuccessThirdQuarterMetric(),
        SuccessExamMetric(),
        AverageMarkThirdQuarterMetric(),
        AverageMarkExamMetric(),
        AverageSolvedExamTasks(),
        ImproveMarkMetric(),
        ReduceMarkMetric(),
        PopularMistakes(),
        VerificationResults(
            [VerificationPresent(),
             VerificationAverageMarks(),
             VerificationMarkThreshold(mark_threshold=mark_threshold)
             ]),
    ]

    students = Students(students_data)
    mc = MetricsController(students_data=students, metrics=metrics)
    return mc.calculate_metrics()
