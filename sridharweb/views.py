from django.template import RequestContext, loader
from django.http import HttpResponse

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'latest_question_list': 'asd',
    })
    return HttpResponse(template.render(context))