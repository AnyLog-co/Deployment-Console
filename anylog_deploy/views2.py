import os
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

FIRST_PAGE_KEY = "deploy_node"      # First page ID

PAGE_COUNTER = 0                    # Number of pages process
PAGES_LIST = []                     # An array with pages visited

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
                "help" : "Selection help ...",
                "config" : False,                   # not to include in the config file
            },
            {
                "key": "my_text",
                "label": "My Text",
                "type": "input_text",
                "size" : 80,
                "help" : "Description of input ...",
                "required" : True
            },

            {
                "print_before" : ["<br/>","<br/>","<br/>"],
                "label": "External Config File",
                "key": "external_config_file",
                "type": "button_submit",
                "help" : "HELP submit config ..."
            },
            {
                "label": "Deploy Node",
                "key": "deploy_node",
                "type": "button_submit",
                "help" : "HELP submit deploy ..."
            },
            {
                "label": "Checkbox",
                "key": "my_checkbox",
                "type": "checkbox",
                "help" : "HELP checkbox ..."
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
                    "options": ["----------", os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')]
                },
                {
                    "label": "submit Node",
                    "key": "submit_node",
                    "type": "button_submit",
                    "help": "HELP submit deploy ..."
                },

            ]
    }

}


class Example:
    def front_page(self, request)->HttpResponse:

        global FIRST_PAGE_KEY
        global PAGE_COUNTER
        global PAGES_LIST

        if request.method == 'POST':
            next_page_name = update_config(request)
            if not next_page_name:
                write_config_file()
                next_page_name = FIRST_PAGE_KEY     # FIRST form page
                PAGE_COUNTER = 0

        else:
            if PAGE_COUNTER > 1:
                PAGE_COUNTER -= 2       # Go back
                next_page_name = PAGES_LIST[PAGE_COUNTER]
            else:
                next_page_name = FIRST_PAGE_KEY      # First page to display
                PAGE_COUNTER = 0

        # Organize a list of pages to consider
        if next_page_name in PAGES_LIST:
            # The page exists - make this page the las page to consider
            PAGE_COUNTER = PAGES_LIST.index(next_page_name)
        else:
            if PAGE_COUNTER == len(PAGES_LIST):
                PAGES_LIST.append(next_page_name)
            else:
                PAGES_LIST[PAGE_COUNTER] = next_page_name
        PAGE_COUNTER += 1

        al_forms[next_page_name]["page_name"] = next_page_name      # store the page key to analyze the data
        return render(request, 'generic.html', al_forms[next_page_name])

# ------------------------------------------------------------------------------------------------------
# Update the form info with the user selections on the form page
# ------------------------------------------------------------------------------------------------------
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

        if field_type == "button_submit" or field_type == "checkbox":
            if value:
                value = True
            else:
                value = False

        field["value"] = value

    return next_page

# ------------------------------------------------------------------------------------------------------
# Create the config file + Output the info to a config file
# ------------------------------------------------------------------------------------------------------
def write_config_file():
    '''
    Write the config file
    '''
    global al_forms
    global PAGE_COUNTER
    global PAGES_LIST

    config_file = ""

    for counter in range(PAGE_COUNTER):

        page_name = PAGES_LIST[counter]
        form_defs = al_forms[page_name]
        fields = form_defs["fields"]

        for field in fields:

            if "key" in field and "value" in field:
                if not "config" in field or field["config"] == False:       # field["config"] set to false makes the value removed from the output file
                    config_file.append("\n\r" + field["key"] + '=' + field["value"])


    # write to file
    pass