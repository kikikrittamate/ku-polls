"""Views for ku polls."""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """View for index."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions \
        (not including those set to be published in the future).

        Returns: latest 5 questions
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """View for detail."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """View for result."""

    model = Question
    template_name = 'polls/results.html'
    

@login_required()
def vote(request, question_id):
    """Vote page for the selected question."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.vote_set.filter(user=request.user).exists():
            the_vote = question.vote_set.get(user=request.user)
            the_vote.choice = selected_choice
            the_vote.save()
        else:
            selected_choice.vote_set.create(user=request.user, question=question)
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def detail(request, question_id=None):
    """Return poll not available or go to detail page."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, f'{"Poll not available"}')
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request, 'polls/detail.html', {'question': question, })
