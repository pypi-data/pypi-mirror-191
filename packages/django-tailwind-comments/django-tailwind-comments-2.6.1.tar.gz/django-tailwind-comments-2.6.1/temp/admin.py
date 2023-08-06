from django.contrib import admin

from . import models


class QuestionAdmin(admin.StackedInline):
    model = models.Question.exam.through


@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'field')
    list_filter = ('grade', 'field')
    search_fields = ('title',)

    inlines = [QuestionAdmin]

    class Meta:
        model = models.Exam


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('id',)
    search_fields = ('name',)


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    ordering = ('id',)
    list_filter = ('province',)
    search_fields = ('name', 'province')


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'city', 'established_year')
    search_fields = ('name',)


@admin.register(models.Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree')
    search_fields = ('name',)
    list_filter = ('degree',)


@admin.register(models.Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'major', 'gpa', 'year')
    search_fields = ('user', 'university', 'major')
    list_filter = ('university', 'major')


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nid', 'birth', 'gender', 'phone', 'email', 'city')
    search_fields = ('first_name', 'last_name')
    list_filter = ('gender',)


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nid', 'grade', 'field', 'gpa', 'birth', 'gender', 'phone', 'email', 'city')
    search_fields = ('first_name', 'last_name')
    list_filter = ('gender', 'grade', 'field')


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nid', 'salary', 'birth', 'gender', 'phone', 'email', 'city')
    search_fields = ('first_name', 'last_name')
    list_filter = ('gender',)


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'factor', 'field')
    search_fields = ('name',)
    list_filter = ('field',)


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'subject')
    search_fields = ('name',)
    list_filter = ('grade',)


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'hardness', 'provider')
    search_fields = ('question_text', 'answer_text')
    list_filter = ('hardness', 'provider', 'lesson')


@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score')
    search_fields = ('student', 'exam')

# admin.site.register(models.Participant)
