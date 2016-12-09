from django.shortcuts import render

from react_render.django.render import render_component

def index(request):
    demo = render_component('templates/components/Demo.js')

    return render(request, 'app/demo.html')
