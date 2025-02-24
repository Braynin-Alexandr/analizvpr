from typing import List, Dict, Any

from vpr.analytics.utils import normalize_student_data


class Students:
    """
    Class for managing a list of students.
    Класс для работы со списком учеников.
    """

    def __init__(self, students_data: List[Dict[str, Any]]):
        self._all_students = [normalize_student_data(student) for student in students_data]
        self._present_students = None

    @property
    def get_all(self):
        return self._all_students

    @property
    def get_present(self):
        if self._present_students is None:
            self._present_students = [student for student in self._all_students if student.get('is_present') is True]
        return self._present_students

    def __iter__(self):
        return iter(self.get_present)
