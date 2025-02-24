from django import forms


class GradeAndExamForm(forms.Form):

    grade = forms.IntegerField(
        label='Номер класса',
        min_value=1,
        max_value=11,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "7"}))

    students_count = forms.IntegerField(
        label="Количество учеников в классе",
        min_value=1,
        max_value=40,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "30"}))

    exercises_count = forms.IntegerField(
        label="Количество заданий",
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "15"}))

    points_for_3 = forms.IntegerField(
        label=f'Нижняя граница баллов для 3-ки ',
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "6"}))

    points_for_4 = forms.IntegerField(
        label=f'Нижняя граница баллов для 4-ки',
        min_value=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "9"}))

    points_for_5 = forms.IntegerField(
        label=f'Нижняя граница баллов для 5-ки',
        min_value=3,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "13"}))

    def clean(self):
        cd = super().clean()
        marks = [3, 4]
        for m in marks:
            current_mark = cd.get(f"points_for_{m}")
            next_mark = cd.get(f"points_for_{m+1}")
            if current_mark is not None and next_mark is not None:
                if current_mark >= next_mark:
                    self.add_error(f"points_for_{m+1}",
                                   f"Баллы для оценки {m+1} должны быть выше, чем для оценки {m}")
        return cd


class StudentsDataForm(forms.Form):

    student_name = forms.CharField(
        label='Имя ученика',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 200px;'}))

    is_present = forms.BooleanField(
        label=f"Присутствие на экзамене",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    third_quarter = forms.IntegerField(
        label=f'Оценка за 3-ю четверть',
        required=False,
        min_value=2,
        max_value=5,
        widget=forms.NumberInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with dynamically created fields for exercises.
        Инициализирует форму с динамически создаваемыми полями для заданий.
        """
        self.exercises_count = kwargs.pop('exercises_count', 0)
        super().__init__(*args, **kwargs)
        for i in range(self.exercises_count):
            self.fields[f'task_{i+1}'] = forms.IntegerField(
                label=f'Задание {i+1}',
                required=False,
                initial=0,
                min_value=0,
                max_value=2,
                widget=forms.NumberInput(attrs={"class": "form-control", "style": "width: 100px;"}))

    def clean(self):
        cleaned_data = super().clean()

        student_name = cleaned_data.get('student_name', False)
        if not student_name:
            cleaned_data['student_name'] = 'Неизвестно'

        is_present = cleaned_data.get('is_present')
        if is_present:
            third_quarter = cleaned_data.get('third_quarter', None)
            if third_quarter is None:
                self.add_error('third_quarter', 'Укажите оценку')

            for i in range(self.exercises_count):
                task = cleaned_data.get(f'task_{i+1}', None)
                if task is None:
                    self.add_error(f'task_{i+1}', 'Укажите балл')

        return cleaned_data


class EmailForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "необязательное поле"}))

    email = forms.EmailField(
        label='Ваш email',
        max_length=100,
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "необязательное поле"}))

    message = forms.CharField(
        label='Сообщение',
        required=True,
        max_length=1000,
        widget=forms.Textarea(attrs={"class": "form-control"}))
