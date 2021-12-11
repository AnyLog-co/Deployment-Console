import os
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect


al_forms = {

    "Deploy_Node" : {

        "name" : "Deploy Node",
        "fields" :
        [
            {
                "name" : "Config File",
                "type" : "selection",
                "options" : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')
            },
            {
                "name": "External Config File",
                "type": "text",
            },
            {
                "name": "Deploy Node",
                "type": "button",
            },

        ]
    }

}


class Example:
    def front_page(self, request)->HttpResponse:
        return render(request, 'generic.html', al_forms["Deploy_Node"])