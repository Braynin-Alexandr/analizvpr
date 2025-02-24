from vpr.analytics.base_metric import BaseVerification, MarkType
from vpr.analytics.student import Students
from vpr.analytics.utils import get_percentage, get_average_mark, calculate_exam_points


class VerificationPresent(BaseVerification):
    """
    Verification that the number of absent students does not exceed 25% of all students.
    Проверка, что количество отсутствующих учеников не превышает 25% от общего числа.
    """
    bad_message = "кол-во неявившихся учеников > 25%"
    CRITICAL_PRESENT_PERCENTAGE = 25

    def get_verification(self, students_data: Students) -> bool:
        student_present_percentage = get_percentage(len(students_data.get_present), len(students_data.get_all))
        return not (student_present_percentage > self.CRITICAL_PRESENT_PERCENTAGE)


class VerificationAverageMarks(BaseVerification):
    """
    Verification that the difference between the average exam mark and the 3rd quarter mark is within the threshold.
    Проверка, что разница между средней оценкой за экзамен и 3-ю четверть находится в допустимых пределах.
    """
    bad_message = "отличие средних баллов и предыдущей четверти >= 0.5 баллов"
    CRITICAL_AVERAGE_DIFF = 0.5

    def get_verification(self, students_data: Students) -> bool:
        average_mark_exam = get_average_mark(students_data, MarkType.EXAM.value)
        average_mark_third_quarter = get_average_mark(students_data, MarkType.THIRD_QUARTER.value)
        return not (abs(average_mark_exam - average_mark_third_quarter) >= self.CRITICAL_AVERAGE_DIFF)


class VerificationMarkThreshold(BaseVerification):
    """
    Verification that the percentage of students at the lower boundary of mark 3 does not exceed the threshold.
    Проверка, что процент учеников на нижней границе 3-ки не превышает допустимый порог.
    """
    bad_message = "на нижней границе 3-ки >= 25% учеников"
    CRITICAL_STUDENTS_PERCENTAGE = 25

    def __init__(self, mark_threshold: int):
        self.mark_threshold = mark_threshold if mark_threshold and isinstance(mark_threshold, int) else None

    def get_verification(self, students_data) -> bool:
        if self.mark_threshold is None:
            return True

        count_students = sum(1 for student in students_data
                             if calculate_exam_points(student) == self.mark_threshold)

        students_percentage = get_percentage(count_students, len(students_data.get_present))
        return not (students_percentage >= self.CRITICAL_STUDENTS_PERCENTAGE)
