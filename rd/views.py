import json
from django.shortcuts import render
from django.core.urlresolvers import reverse
from react.render import render_component
# Create your views here.
comments = []
def index(request):
    comment_box = render_component(
        path='js/components/app.jsx', 
        to_static_markup=True
    )
    context = {
        'app': app,
    }
    return render(request, 'index.html', app)
