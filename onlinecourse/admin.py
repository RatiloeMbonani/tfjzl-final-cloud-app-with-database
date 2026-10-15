from django.contrib import admin
# Import the seven required models
from .models import Course, Lesson, Instructor, Learner, Enrollment, Question, Choice

# Inline for Choice model inside QuestionAdmin
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

# Inline for Question model inside CourseAdmin (optional but helpful, or registered separately)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('content', 'grade')

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

# Registering models with the admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
