from typing import List, Dict, Any

from vpr.analytics.utils import add_marks_to_students


def save_grade_exam_data(session, cleaned_data):
    """
    Saves grade and exam data to the session.
    Сохраняет в сессию данные о классе и экзамене.
    """
    session["grade"] = cleaned_data.get("grade")
    session["students_count"] = cleaned_data.get("students_count")
    session["exercises_count"] = cleaned_data.get("exercises_count")
    session["points_for_3"] = cleaned_data.get("points_for_3")
    session["points_for_4"] = cleaned_data.get("points_for_4")
    session["points_for_5"] = cleaned_data.get("points_for_5")


def process_students_data(session, formset) -> List[Dict[str, Any]]:
    """
    Processes student data and assigns marks.
    Обрабатывает данные учеников и назначает им оценки.
    """
    students_cleaned_data = [form.cleaned_data for form in formset]
    exam_marks = {f"points_for_{i}": session.get(f"points_for_{i}") for i in range(3, 6)}
    students_data = add_marks_to_students(students_cleaned_data, exam_marks)
    return students_data


def get_students_names(session) -> List[Dict[str, str]]:
    """
    Generates a list of student names based on grade and student count.
    Генерирует список имен на основе номера класса и количества учеников.
    """
    students_count = session.get('students_count', 0)
    grade = session.get('grade', 0) * 10000
    return [{'student_name': str(grade+i)} for i in range(1, students_count+1)]


def prepare_report_context(context, report):
    """
    Prepares report data for the template.
    Подготавливает данные отчета для шаблона.
    """
    context["chart_data"] = get_chart_data(report)
    context["table_marks"] = get_table_all_marks(report)
    context["table_students"] = report.pop("Список учеников с оценками", {})
    context["popular_mistakes"] = report.pop("Cамые распространенные ошибки", {})
    context["other_data"] = report
    return context

def get_chart_data(report: Dict[str, Any]) -> Dict[str, List[int]]:
    """
    Extracts chart data from the report.
    Извлекает данные для графика из отчета.
    """
    quarter_counter = report.get("Оценки за 3-ю четверть", {})
    exam_counter = report.get("Оценки за ВПР", {})

    all_marks = [2, 3, 4, 5]
    chart_data = {"quarter_grades": [quarter_counter.get(mark, 0) for mark in all_marks],
                  "exam_grades": [exam_counter.get(mark, 0) for mark in all_marks]}
    return chart_data


def get_table_all_marks(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates a table with student marks.
    Формирует таблицу с оценками учеников.
    """
    table_marks = []

    marks_third_quarter = report.pop("Оценки за 3-ю четверть", {})
    marks_exam = report.pop("Оценки за ВПР", {})
    quality_third_quarter = report.pop("Процент качества, 3я четверть", "-")
    quality_exam = report.pop("Процент качества, экзамен", "-")
    success_third_quarter = report.pop("Процент успеваемости, 3-я четверть", "-")
    success_exam = report.pop("Процент успеваемости, экзамен", "-")

    all_marks = [5, 4, 3, 2]
    for mark in all_marks:
        table_marks.append({
            "name": f"Кол-во «{mark}»",
            "quarter": marks_third_quarter.get(mark, "-"),
            "exam": marks_exam.get(mark, "-")
        })
    table_marks.append({"name": "Процент качества", "quarter": quality_third_quarter, "exam": quality_exam})
    table_marks.append({"name": "Процент успеваемости", "quarter": success_third_quarter, "exam": success_exam})
    return table_marks
