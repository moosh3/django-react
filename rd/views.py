import json
from django.shortcuts import render
from django.views.generic import View
from react.render import render_component
from django.core.urlresolvers import reverse
# Create your views here.

comments = []

def comment_box(request):
    rendered = render_component(
        path='bundles/main.server.js',
        to_static_markup=True,
        props={
            'comments': comments,
            'url': reverse('comment')
        }
    )
    context = {
        'rendered': rendered,
    }
    return render(request, 'index.html', context)

def comment(request):
    if request.POST:
        comments.append({
            'author': request.POST.get('author', None),
            'text': request.POST.get('text', None),
        })
    return render(
        json.dumps(comments),
        content_type='application/json'
    )
