from typing import Dict, Any, List


translation_dictionary = {
    "total_students": "Учащихся по списку",
    "students_present_exam": "Учащиеся, присутствующие на экзамене",
    "students_absent_exam": "Отсутствующие учащиеся",
    "list_students_and_marks": "Список учеников с оценками",
    "marks_3rd_quarter": "Оценки за 3-ю четверть",
    "marks_exam": "Оценки за ВПР",
    "quality_third_quarter": "Процент качества, 3я четверть",
    "quality_exam": "Процент качества, экзамен",
    "success_third_quarter": "Процент успеваемости, 3-я четверть",
    "success_exam": "Процент успеваемости, экзамен",
    "average_mark_third_quarter": "Средний балл по предмету",
    "average_mark_exam": "Средний балл за ВПР",
    "average_solved_exam_tasks": "Среднее количество решенных задач",
    "improve_mark": "Процент учащихся, повысивших свой результат",
    "reduce_mark": "Процент учащихся, понизивших свой результат",
    "verification_results": "Проверка достоверности результатов",
    "popular_mistakes": "Cамые распространенные ошибки",
}


def translate_russian(function):
    """
    Decorator that translates dictionary keys from English to Russian using translation_dictionary.
    Декоратор, переводящий ключи словаря с английского на русский, используя translation_dictionary.
    """
    def wrapper(data: Dict[str, Any]) -> Dict[str, Any]:
        result = function(data)
        translated_result = {translation_dictionary.get(k, k): v
                             for k, v in result.items()}
        return translated_result
    return wrapper


def get_task_keys(student: Dict[str, Any]) -> List[str]:
    """
    Returns a list of task names from the student’s data.
    Возвращает список названий задач из данных ученика.
    """
    return [task for task in student if task.startswith("task_")]


def get_average_mark(students_data, mark_type) -> float:
    """
    Returns an average_mark of mark_type.
    Возвращает среднюю оценку, указанную mark_type.
    """
    return sum(student.get(mark_type) for student in students_data) / len(students_data.get_present)


def normalize_student_data(student: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a student's data to a standard format.
    Приводит данные ученика к стандартному виду.
    """
    student_presents = student.get("is_present", False)
    normalize_data = {
        "student_name": student.get("student_name", "Неизвестный"),
        "is_present": student_presents,
        "third_quarter": student.get("third_quarter", "-"),
        "exam_mark": student.get("exam_mark", "-")
    }

    if student_presents is False:
        return normalize_data

    task_keys = get_task_keys(student)
    for task in task_keys:
        normalize_data[task] = student.get(task)
    return normalize_data


def get_percentage(part: int, whole: int, decimal_places: int = 2) -> float:
    """
    Calculates the percentage based on a partial and total value, rounding to the specified decimal places.
    Высчитывает процент на основе частичного и общего значения, округляя до указанного количества знаков после запятой.
    """
    if part == 0:
        return 0.0
    return round(part / whole * 100, decimal_places)


def calculate_exam_points(student: Dict[str, Any]) -> int:
    """
    Calculates the total exam points based on task scores.
    Считает сумму экзаменационных баллов на основе оценок за задания.
    """
    if not isinstance(student, dict):
        raise ValueError
    return sum(value for task, value in student.items() if task.startswith("task_") and isinstance(value, int))


def add_marks_to_students(student_data: List[Dict[str, Any]], marks_data: Dict[str, int]) -> List[Dict[str, Any]]:
    """
    Assigns an exam mark to each student based on their exam points.
    Присваивает каждому ученику оценку за экзамен на основе набранных баллов.
    """

    updated_data = []
    for student in student_data:
        if not student.get('is_present', False):
            updated_data.append(student)
            continue

        exam_points = calculate_exam_points(student)

        exam_mark = 2
        for key in marks_data:
            if exam_points < marks_data[key]:
                break
            exam_mark += 1

        student['exam_mark'] = exam_mark
        updated_data.append(student)

    return updated_data
