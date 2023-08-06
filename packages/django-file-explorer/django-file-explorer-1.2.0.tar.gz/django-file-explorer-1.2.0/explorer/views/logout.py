""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-02-12 12:22:27
Project:	 Explorer App
Description: Provide class for login.
"""

from django.views.generic.base import TemplateView
from django.contrib.auth import logout

class Logout(TemplateView):
    template_name = 'explorer/logout.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        # GETTING CONTEXT
        context = self.get_context_data()
        
        # LOGOUT USER
        logout(request)
        return self.render_to_response(context)