import json
from django.shortcuts import render
from django.core.urlresolvers import reverse
from react.render import render_component
# Create your views here.
comments = []
def index(request):
    comment_box = render_component(
        path='js/components/CommentBox.jsx',
        props={
            'comments': comments,
            'url': reverse('comment'),
            'pollInterval': 2000
        },
        to_static_markup=True,
    )
    context = {
        'comment_box': comment_box,
    }
    return render(request, 'index.html', context)

def comment(request):
    if request.method == 'POST':
        comments.append({
            'author': request.POST.get('author', None),
            'text': request.POST.get('text', None),
        })
    return HttpResponse(
        json.dumps(comments),
        content_type='application/json',
    )
