from django.forms import formset_factory
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib import messages

from vpr.analytics.metrics_controller import get_report
from vpr.forms import GradeAndExamForm, StudentsDataForm, EmailForm
from vpr.utils import save_grade_exam_data, get_students_names, process_students_data, prepare_report_context


class GradeAndExamInputView(FormView):
    """
    Handles the input of grade and exam data.
    Обрабатывает ввод первичных данных о классе и экзамене.
    """
    form_class = GradeAndExamForm
    template_name = "vpr/index.html"
    extra_context = {'Title': 'Шаг 1. Введите данные'}
    success_url = reverse_lazy("vpr:students_data_input")

    def form_valid(self, form):
        """
        Saves the entered data to the session and goes to the next step.
        Сохраняет введенные данные в сессию и переходит к следующему шагу.
        """
        save_grade_exam_data(self.request.session, form.cleaned_data)
        return super().form_valid(form)


class StudentsDataInputView(FormView):
    """
    Handles the input of individual student data.
    Обрабатывает ввод данных каждого ученика.
    """
    form_class = StudentsDataForm
    template_name = "vpr/students_data_input.html"
    extra_context = {"Title": "Шаг 2. Заполните таблицу"}
    success_url = reverse_lazy("vpr:results")

    def get_context_data(self, **kwargs):
        """Adds a formset to the context_data.
        Добавляет formset в context_data.
        """
        context_data = super().get_context_data(**kwargs)
        context_data["formset"] = self.get_formset()
        return context_data

    def get_formset(self):
        """Creates and returns a formset for GET and POST requests.
        Создаёт и возвращает formset для GET и POST запросов.
        """
        StudentsDataFormSet = formset_factory(self.form_class, extra=0)
        exercises_count = self.request.session.get('exercises_count', 1)

        if self.request.method == 'POST':
            return StudentsDataFormSet(self.request.POST, form_kwargs={'exercises_count': exercises_count})

        return StudentsDataFormSet(
            initial=get_students_names(self.request.session),
            form_kwargs={'exercises_count': exercises_count})

    def form_valid(self, form):
        """
        Validates the formset, processes student data, and saves it to the session.
        Проверяет formset, обрабатывает данные учеников и сохраняет их в сессии.
        """
        formset = self.get_formset()
        if not formset.is_valid():
            return self.form_invalid(formset)

        students_data = process_students_data(self.request.session, formset)
        self.request.session["students_data"] = students_data
        return super().form_valid(form)


class ResultsAnalysisView(TemplateView):
    """
    Displays the "VPR analysis" report.
    Отображает отчет "Анализ ВПР"
    """
    template_name = "vpr/results_analysis.html"
    extra_context = {"Title": "Анализ ВПР"}

    def get_context_data(self, **kwargs):
        """
        Adds report data to the context.
        Добавляет данные отчета в контекст.
        """
        context = super().get_context_data(**kwargs)
        report = get_report(data=self.request.session)
        context.update(prepare_report_context(context, report))
        return context


def instructions_view(request):
    return render(request, template_name="vpr/instructions.html")


class ContactsView(FormView):
    form_class = EmailForm
    template_name = "vpr/contacts.html"
    success_url = reverse_lazy("vpr:contacts")

    def form_valid(self, form):
        cd = form.cleaned_data
        name = cd.get("name", "unknown")
        email = cd.get("email", "unknown")
        message = cd.get("message")

        send_mail(subject=f"Анализ ВПР, новое сообщене от {name}",
                  message=f"Email: {email}\n\n{message}",
                  from_email="braynin-alex@mail.ru",
                  recipient_list=["braynin-alex@mail.ru"],
                  fail_silently=False,
                  )
        messages.success(self.request, "Ваше сообщение отправлено!")
        return super().form_valid(form)


def about_view(request):
    return render(request, template_name="vpr/about.html")


def page_is_not_found(request, exception):
    return render(request, template_name="vpr/page_is_not_found.html")
