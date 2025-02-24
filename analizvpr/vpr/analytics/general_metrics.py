from collections import Counter
from typing import List, Dict, Any, Set

from vpr.analytics.base_metric import BaseMetric, MarkType, BaseVerification
from vpr.analytics.student import Students
from vpr.analytics.utils import calculate_exam_points, get_percentage, get_task_keys


class TotalStudentsMetric(BaseMetric):
    """
    Metric for calculating the total number of students in a class.
    Метрика для расчёта количества всех учеников в классе.
    """
    metric_name = "total_students"

    def calculate(self, students_data: Students) -> int:
        return len(students_data.get_all)


class StudentsPresentExamMetric(BaseMetric):
    """
    Metric for calculating the number of students present at the exam.
    Метрика для расчёта количества присутствующих на экзамене учеников.
    """
    metric_name = "students_present_exam"

    def calculate(self, student_data: Students) -> int:
        return len(student_data.get_present)


class ListStudentsAndMarksMetric(BaseMetric):
    """
    Metric for generating a list of student names with marks for the third quarter and exam.
    Метрика для формирования списка имен учеников с оценками за 3-ю четверть и экзамен.
    """
    metric_name = "list_students_and_marks"

    def calculate(self, students_data: Students) -> List[Dict[str, Any]]:
        student_list = []

        for student in students_data.get_all:
            student_data = {
                "student_name": student.get("student_name", "Неизвестный"),
                "exam_mark": student.get("exam_mark", "-"),
                "exam_points": calculate_exam_points(student) if student.get("is_present") is True else "-",
            }
            student_list.append(student_data)
        return student_list


class BaseCounterMarksMetric(BaseMetric):
    """
    Base class for counting the number of marks.
    Базовый класс для подсчёта количества оценок.
    """
    def calculate(self, students_data: Students) -> Counter:
        return Counter(student.get(self.mark_type.value, 0) for student in students_data)


class CounterMarksThirdQuarterMetric(BaseCounterMarksMetric):
    """
    Metric for counting the number of each mark for the third quarter.
    Метрика для расчёта количества каждой оценки за 3-ю четверть.
    """
    metric_name = "marks_3rd_quarter"
    mark_type = MarkType.THIRD_QUARTER


class CounterMarksExamMetric(BaseCounterMarksMetric):
    """
    Metric for counting the number of each mark for the exam.
    Метрика для расчёта количества каждой оценки за экзамен.
    """
    metric_name = "marks_exam"
    mark_type = MarkType.EXAM


class BaseRateMetric(BaseMetric):
    """
    Base class for metrics calculating the percentage of good marks compared to bad ones.
    Базовый класс метрики, процентное отношение хороших оценок к плохим.
    """
    metric_name: str = None
    mark_type: MarkType = None
    good_marks: Set = None

    def calculate(self, students_data: Students) -> float:
        good_marks = sum(1 for student in students_data if student.get(self.mark_type.value) in self.good_marks)
        return get_percentage(good_marks, len(students_data.get_present))


class QualityThirdQuarterMetric(BaseRateMetric):
    """
    Metric for calculating the quality percentage for the third quarter.
    Метрика для расчёта процента качества, 3-я четверть.
    """
    metric_name = "quality_third_quarter"
    mark_type = MarkType.THIRD_QUARTER
    good_marks = {4, 5}


class QualityExamMetric(BaseRateMetric):
    """
    Metric for calculating the quality percentage for the exam.
    Метрика для расчёта процента качества, экзамен.
    """
    metric_name = "quality_exam"
    mark_type = MarkType.EXAM
    good_marks = {4, 5}


class SuccessThirdQuarterMetric(BaseRateMetric):
    """
    Metric for calculating the success rate for the third quarter.
    Метрика для расчёта процента успеваемости, 3-я четверть.
    """
    metric_name = "success_third_quarter"
    mark_type = MarkType.THIRD_QUARTER
    good_marks = {3, 4, 5}


class SuccessExamMetric(BaseRateMetric):
    """
    Metric for calculating the success rate for the exam.
    Метрика для расчёта процента успеваемости, экзамен.
    """
    metric_name = "success_exam"
    mark_type = MarkType.EXAM
    good_marks = {3, 4, 5}


class BaseAverageMarkMetric(BaseMetric):
    """
    Base class for metrics that calculate the average mark.
    Базовый класс для метрик, вычисляющих среднюю оценку.
    """

    def calculate(self, students_data: Students) -> float:
        sum_marks = sum(student.get(self.mark_type.value, 0) for student in students_data)
        if sum_marks == 0:
            return 0
        return round(sum_marks / len(students_data.get_present), 2)


class AverageMarkThirdQuarterMetric(BaseAverageMarkMetric):
    """
    Metric for calculating the average mark for the 3rd quarter.
    Метрика для вычисления средней оценки за 3-ю четверть.
    """
    metric_name = "average_mark_third_quarter"
    mark_type = MarkType.THIRD_QUARTER


class AverageMarkExamMetric(BaseAverageMarkMetric):
    """
    Metric for calculating the average exam mark.
    Метрика для вычисления средней оценки за экзамен.
    """
    metric_name = "average_mark_exam"
    mark_type = MarkType.EXAM


class AverageSolvedExamTasks(BaseMetric):
    """
    Metric for calculating the average number of solved exam tasks.
    Метрика для вычисления среднего количества решенных задач на экзамене.
    """
    metric_name = "average_solved_exam_tasks"

    def calculate(self, students_data: Students) -> float:
        sum_solved_tasks = self.__get_sum_solved_tasks(students_data)
        if sum_solved_tasks == 0:
            return 0
        return round(sum_solved_tasks / len(students_data.get_present), 2)

    @staticmethod
    def __get_sum_solved_tasks(students_data: Students) -> int:
        sum_solved_tasks = 0
        for student in students_data:
            for item in student:
                if item.startswith('task_') and student.get(item, 0) > 0:
                    sum_solved_tasks += 1
        return sum_solved_tasks


class ImproveMarkMetric(BaseMetric):
    """
    Metric for calculating the number and percentage of students who improved their mark.
    Метрика для определения количества и процента учеников, улучшивших свою оценку.
    """
    metric_name = "improve_mark"
    mark_exam = MarkType.EXAM
    mark_third_quarter = MarkType.THIRD_QUARTER

    def calculate(self, students_data: Students) -> str:
        count_changes = sum(1 for student in students_data if self.__verify_improve(student))
        percentage_changes = get_percentage(count_changes, len(students_data.get_present))
        return f"{percentage_changes}% ({count_changes} чел.)"

    @classmethod
    def __verify_improve(cls, student: Dict[str, Any]) -> bool:
        return student.get(cls.mark_exam.value, 0) > student.get(cls.mark_third_quarter.value, 0)


class ReduceMarkMetric(BaseMetric):
    """
    Metric for calculating the number and percentage of students who lowered their mark.
    Метрика для определения количества и процента учеников, ухудшивших свою оценку.
    """
    metric_name = "reduce_mark"
    mark_exam = MarkType.EXAM
    mark_third_quarter = MarkType.THIRD_QUARTER

    def calculate(self, students_data: Students) -> str:
        count_changes = sum(1 for student in students_data if self.__verify_reduce(student))
        percentage_changes = get_percentage(count_changes, len(students_data.get_present))
        return f"{percentage_changes}% ({count_changes} чел.)"

    @classmethod
    def __verify_reduce(cls, student: Dict[str, Any]) -> bool:
        return student.get(cls.mark_exam.value, 0) < student.get(cls.mark_third_quarter.value, 0)


class VerificationResults(BaseMetric):
    """
    Metric for verifying the reliability of results.
    Метрика для проверки достоверности результатов.
    """
    metric_name = "verification_results"
    good_result = "результат достоверный"
    bad_result = "результат недостоверный"

    def __init__(self, verifications: List):
        self.verifications = [v for v in verifications if isinstance(v, BaseVerification)]

    def calculate(self, students_data: Students) -> str:
        verifications_bad_result = self.__get_bad_verifications(students_data)
        if verifications_bad_result:
            return self.bad_result + ", так как " + '; '.join([v for v in verifications_bad_result])
        return self.good_result

    def __get_bad_verifications(self, students_data: Students) -> List:
        bad_verifications = []
        for verification in self.verifications:
            check = verification.get_verification(students_data)
            if check is False:
                bad_verifications.append(verification.bad_message)
        return bad_verifications


class PopularMistakes(BaseMetric):
    """
    Metric for identifying the most common mistakes.
    Метрика для выявления самых распространенных ошибок.
    """
    metric_name = "popular_mistakes"
    CRITICAL_MISTAKE_PERCENTAGE = 20

    def calculate(self, students_data: Students) -> str:
        count_tasks_mistakes = self.__get_count_tasks_mistakes(students_data)
        popular_mistakes = self.__get_popular_mistakes(students_data, count_tasks_mistakes)
        return popular_mistakes if popular_mistakes else "отсутствуют"

    @classmethod
    def __get_popular_mistakes(cls, students_data: Students, count_tasks_mistakes: Counter) -> Dict[str, str]:
        popular_mistakes = {}

        for task_name, count_mistakes in count_tasks_mistakes.items():
            students_mistakes_percentage = get_percentage(count_mistakes, len(students_data.get_present))
            if students_mistakes_percentage >= cls.CRITICAL_MISTAKE_PERCENTAGE:
                task_name = task_name.replace("task_", "Задание ")
                popular_mistakes[task_name] = f"{count_mistakes} / {students_mistakes_percentage}%"
        return popular_mistakes

    @staticmethod
    def __get_count_tasks_mistakes(students_data: Students) -> Counter:
        count_mistakes = Counter()
        task_keys = get_task_keys(student=students_data.get_present[0])

        for task in task_keys:
            count_mistakes[task] = sum(1 for student in students_data if student.get(task, 0) == 0)

        return count_mistakes
