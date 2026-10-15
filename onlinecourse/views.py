from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

# Course list view
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:5]

# Course detail view
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.total_enrollment += 1
    course.save()
    return HttpResponseRedirect(reverse(f'onlinecourse:course_details', args=(course.id,)))

# Submit exam view (Task 5)
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        
        selected_ids = []
        for key, value in request.POST.lists():
            if key.startswith('choice_'):
                for choice_id in value:
                    selected_ids.append(int(choice_id))
                    
        for choice_id in selected_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
            
        submission.save()
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))
        
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))

# Show exam result view (Task 5)
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    max_score = 0
    
    for question in course.question_set.all():
        max_score += question.grade
        correct_choices = set(question.choice_set.filter(is_correct=True).values_list('id', flat=True))
        user_choices = set(submission.choices.filter(question=question).values_list('id', flat=True))
        
        if correct_choices == user_choices:
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'grade': total_score,
        'max_score': max_score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
