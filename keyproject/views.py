#coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RenderContext


def key(request):
    try:
        text = request.POST['textarea']
       
        return render_to_response('key.html', {'text':text})
    except:
        return render_to_response('key.html')