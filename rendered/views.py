import os
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from react_render.django import render_component

comments = []

def index(request):
    no_js = 'no_js' in request.GET 
    
    comment_box = render_component(
        'js/main.server.js',
        props={
            'comments': comments,
            'url': reverse('comment'),
            'pollInterval': 2000,
        },
        to_static_markup=no_js
    )
    
    button = render_component(
        ''
    )

    return render(request, 'rendered/index.html')

def comment(request):
    if request.POST:
        comments.append({
            'author': request.POST.get('author', None),
            'text': request.POST.get('text', None),
        }) 
    return HttpResponse(
        json.dumps(comments),
        content_type='application/json'
    ) 
