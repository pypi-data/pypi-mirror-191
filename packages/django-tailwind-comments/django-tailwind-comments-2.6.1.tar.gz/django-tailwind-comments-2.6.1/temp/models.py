# CHANGE APP NAME TO TABLE
from django.core.validators import MinLengthValidator
from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f'{self.name} [{self.province.name}]'

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class University(models.Model):
    name = models.CharField(max_length=100)
    rank = models.PositiveIntegerField()
    established_year = models.DateField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='universities')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'


class Major(models.Model):
    name = models.CharField(max_length=100)
    DEGREE_CHOICES = (
        ('a', 'Associate’s degree'),
        ('b', 'Bachelor’s degree'),
        ('m', 'Master’s Degree'),
        ('d', 'Doctorate'),
    )
    degree = models.CharField(max_length=1, choices=DEGREE_CHOICES)

    def __str__(self):
        return f'{self.get_degree_display()} of {self.name}'


class User(models.Model):
    nid = models.CharField(primary_key=True, max_length=10, unique=True, validators=[MinLengthValidator(10)])
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth = models.DateField()
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='users')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(User):
    GRADE_CHOICES = (
        (10, '10th'),
        (11, '11th'),
        (12, '12th')
    )
    grade = models.IntegerField(choices=GRADE_CHOICES)
    FIELD_CHOICES = (
        ('m', 'Mathematics & Physics'),
        ('e', 'Experimental Sciences'),
        ('l', 'Literature & Humanities')
    )
    field = models.CharField(max_length=1, choices=FIELD_CHOICES)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=10)


class Teacher(User):
    salary = models.IntegerField(default=0)


class Certification(models.Model):
    user = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='certifications')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='certifications')
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='certifications')
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=10)
    year = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.user} - {self.university} - {self.major}'

    class Meta:
        unique_together = ('user', 'university', 'major')


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration = models.TimeField(default='00:00:00')
    GRADE_CHOICES = (
        (10, '10th'),
        (11, '11th'),
        (12, '12th')
    )
    grade = models.IntegerField(choices=GRADE_CHOICES)
    FIELD_CHOICES = (
        ('m', 'Mathematics & Physics'),
        ('e', 'Experimental Sciences'),
        ('l', 'Literature & Humanities')
    )
    field = models.CharField(max_length=1, choices=FIELD_CHOICES)

    def __str__(self):
        return f'{self.title} , {self.get_grade_display()} - {self.get_field_display()}'


class Subject(models.Model):
    name = models.CharField(max_length=100)
    factor = models.IntegerField(default=1)
    FIELD_CHOICES = (
        ('g', 'General'),
        ('m', 'Mathematics & Physics'),
        ('e', 'Experimental Sciences'),
        ('l', 'Literature & Humanities')
    )
    field = models.CharField(max_length=1, choices=FIELD_CHOICES)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    GRADE_CHOICES = (
        (10, '10th'),
        (11, '11th'),
        (12, '12th')
    )
    grade = models.IntegerField(choices=GRADE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ManyToManyField(Exam, blank=True, null=True, related_name='questions')

    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True, related_name='questions')

    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    ANSWER_CHOICES = ((1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4'))
    answer = models.IntegerField(choices=ANSWER_CHOICES)

    HARDNESS_CHOICES = ((0, 'None'), (1, 'Very Easy'), (2, 'Easy'), (3, 'Medium'), (4, 'Hard'), (5, 'Very Hard'))
    hardness = models.IntegerField(choices=HARDNESS_CHOICES, default=0)

    provider = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.SET_NULL, related_name='exams')

    def __str__(self):
        if self.lesson:
            return f'{self.lesson.subject.name} - {self.lesson.name} | {self.get_hardness_display()}'
        else:
            return f'Unknown Reference | {self.get_hardness_display()}'


class Participant(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='participants')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='participants')
    score = models.IntegerField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.student} - {self.exam}'

    class Meta:
        unique_together = ('student', 'exam')
