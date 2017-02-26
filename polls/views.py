from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


# Create your views here.
class IndexView(generic.ListView):
    """ display list object of question models"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        :returns: published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """ display choices of each question """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """ display the result of the choices voted  """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """
    :param request:
    :param question_id:
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # redisplay the question voting from
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "you didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,)))


def about(request):
    """ return render to polls/about.html"""
    return render(request, 'polls/about.html')
