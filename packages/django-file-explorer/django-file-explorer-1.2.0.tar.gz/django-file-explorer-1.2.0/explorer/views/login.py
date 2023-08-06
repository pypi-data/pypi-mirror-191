""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-02-12 12:22:27
Project:	 Explorer App
Description: Provide class for login.
"""
from django import http
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login


class Login(TemplateView):
    template_name = 'explorer/login.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        # GETTING CONTEXT
        context = self.get_context_data()
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return http.HttpResponseRedirect(redirect_to=request.GET.get('next'))
        return render(request, template_name='explorer/error.html', context={'message': 'Username or Password is incorrect.'})