from django.shortcuts import render
from django.views.generic import View
from react.render import render_component
from django.shortcuts import render
# Create your views here.

def rendered_index(request):
    rendered = render_component(
        path='assets/components/CommentBox.jsx',
        to_static_markup=False,
    )
    return render('index.html', rendered)
