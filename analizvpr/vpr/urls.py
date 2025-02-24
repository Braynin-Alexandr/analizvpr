from django.urls import path
from .views import (GradeAndExamInputView, StudentsDataInputView, ResultsAnalysisView, instructions_view, ContactsView,
                    about_view)

app_name = "vpr"

urlpatterns = [
    path('', GradeAndExamInputView.as_view(), name='grade_and_exam_settings'),
    path('students_data/', StudentsDataInputView.as_view(), name='students_data_input'),
    path('results/', ResultsAnalysisView.as_view(), name='results'),
    path('instructions/', instructions_view, name='instructions'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', about_view, name='about'),
]
