import json
from django.shortcuts import render
from react.render import render_component
# Create your views here.

def index(request):
    rendered = render_component(
        path='js/components/app.jsx',
        props={
            'items': 'Home'
        },
        to_static_markup=True,
    )
    context = {
        'rendered': rendered,
    }
    return render(request, 'index.html', context)
