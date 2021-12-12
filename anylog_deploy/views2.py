import os
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect


al_forms = {

    "deploy_node" : {

        "name" : "Deploy Node",
        "next" : "set_connections",         # Next page
        "fields" :
        [
            {
                "key" : "config_file",
                "label" : "Config File",
                "type" : "selection",
                "options" : ["option 1", "option 2"],
                "print_after" : ["&nbsp;","&nbsp;"],
            },
            {
                "key": "my_text",
                "label": "My Text",
                "type": "input_text",
                "size" : 80,
            },

            {
                "print_before" : ["<br/>","<br/>","<br/>"],
                "label": "External Config File",
                "key": "external_config_file",
                "type": "button_submit",
            },
            {
                "label": "Deploy Node",
                "key": "deploy_node",
                "type": "button_submit",
            },

        ]
    },

    "set_connections" : {

        "name" : "Set Connections",
        "next" : "deploy_node",         # Next page
        "fields":
            [
                {
                    "label": "Config File",
                    "key": "config_file",
                    "type": "selection",
                    "options": os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')
                },
            ]
    }

}


class Example:
    def front_page(self, request)->HttpResponse:

        if request.method == 'POST':
            next_page_name = update_config(request)

        else:
            next_page_name = "deploy_node"      # First page to display

        al_forms[next_page_name]["page_name"] = next_page_name      # store the page key to analyze the data
        return render(request, 'generic.html', al_forms[next_page_name])


def update_config(request):
    '''
    Use the keys from al_forms to retrieve the values set on th eforms
    '''

    post_data = request.POST
    page_name = post_data.get('page_name')
    next_page = post_data.get('next_page')

    # get field values
    form_defs = al_forms[page_name]
    fields = form_defs["fields"]

    for field in fields:
        field_type = field["type"]
        key =  field["key"]
        value = post_data.get(key)

        if field_type == "button_submit":
            if value:
                value = True
            else:
                value = False

        field["value"] = value

    return next_page