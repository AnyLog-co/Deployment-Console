import os
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

FIRST_PAGE_KEY = "base_configs"      # First page ID

PAGE_COUNTER = 0                    # Number of pages process
PAGES_LIST = []                     # An array with pages visited

'''
Form options:
    name - the name of the form which appears on the title
    next - the key of the page, None - ends the page inputs and writes the file
    fields - a list of input fields for every form
        type -  "selection", "input_text", "input_ip", "input_password", "input_number", "button_submit", "checkbox"
        label - text before the input field
        print_before - list of text strings printed before the label and the input including "&nbsp;" and "<br/>"
        print_after - list of text strings printed before the label and the input including "&nbsp;" and "<br/>"
        options - selection options in selection field
        config - True/False - if included and set to False, is not included in the config file
        help - text with mouse hover
        required - Optional for "input_text" and "input_number"
        min - min value for number field
        max - max value for number field
'''

al_forms = {
    "base_configs" : { # Basic node type & build configuration
        "name" : "Base Configs",
        "next" : "general_info",
        "fields" : [
            {
                "section": "general",
                "required": True,
                "key" : "build",
                "label" : "Build",
                "type" : "selection",
                "options" : ["", "predevelop"],
                "print_after" : ["&nbsp;","&nbsp;"],
                "help" : "AnyLog version to download from Docker Hub",
                "config" : True,
            },
            {
                "section": "general",
                "required": True,
                "key": "node_type",
                "label": "Node Type",
                "type": "selection",
                "options": ["", "none", "rest", "master", "operator", "publisher",
                            "query", "single-node", "single-node-publisher"],
                "next": ["", "network_configs", "operator_params", "operator_params", "operator_params", "", "", "", ""],

                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Type of node AnyLog should run",
                "config": True,
            }
        ]
    },
    "general_info": { # General information & authentication params
        "name": "General Information",
        "next": "base_configs.node_type",
        "fields" : [
            {
                "section": "general",
                "required": True,
                "key" : "node_name",
                "label" : "Node Name",
                "type" : "input_text",
                "print_after": ["&nbsp;","&nbsp;"],
                "help" : "Name correlated with the node",
                "config" : True,
            },
            {
                "section": "general",
                "required": True,
                "key": "company_name",
                "label": "Company Name",
                "type": "input_text",
                "print_after": ["&nbsp;","&nbsp;"],
                "help": "Company correlated with policies declared via this node",
                "config": True
            },
            { # Optional
                "section": "general",
                "key": "location",
                "label": "Location",
                "type": "input_text",
                "print_after": ["&nbsp;","&nbsp;"],
                "help": "Machine location - coordinates location is accessible via Grafana Map visualization",
                "config": True
            },
            {
                "section": "authentication",
                "required": True,
                "key": "authentication",
                "label": "Authentication",
                "type": "selection",
                "options": ["false", "true"],
                "print_after": ["&nbsp;","&nbsp;"],
                "help": "Whether or not to enable authentication",
                "config": True
            },
            {
                "section": "authentication",
                "key": "username",
                "label": "Authentication User",
                "type": "input_text",
                "print_after": ["&nbsp;","&nbsp;"],
                "help": "Authentication username",
                "config": True
            },
            {
                "section": "authentication",
                "key": "password",
                "label": "Authentication Password",
                "type": "input_password",
                "print_after": ["&nbsp;","&nbsp;"],
                "help": "Authentication password correlated to user",
                "protected": True,
                "config": True
            },
            {
                "section": "authentication",
                "key": "auth_type",
                "label": "Authentication Type",
                "type": "selection",
                "options": ["admin", "user"],
                "print_after": ["&nbsp;","&nbsp;"],
                "help": "Authentication user type",
                "config": True
            }
        ]
    },
    "network_configs": { # network configurations
        "name": "Network Configurations",
        "next": "database_configs",
        "fields": [
            {
                "section": "networking",
                "required": True,
                "key": "anylog_tcp_port",
                "label": "TCP Port",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "min": 2048, "max": 65535,
                "help": "TCP port for node used to communicate with other nodes in the network",
                "config": True,
            },
            {
                "section": "networking",
                "required": True,
                "key": "anylog_rest_port",
                "label": "REST Port",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "min": 2048, "max": 65535,
                "help": "REST port to communicate against with the AnyLog instance",
                "config": True,
            },
            {
                "section": "networking",
                "required": True,
                "key": "master_node",
                "label": "Master Node",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "TCP connection information for master node",
                "config": True,
            },

            # Optional params
            {
                "section": "networking",
                "key": "anylog_broker_port",
                "label": "Local Broker Port",
                "type":"input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "AnyLog broker port",
                "config": True
            },
            {
                "section": "networking",
                "key": "external_ip",
                "label": "External IP",
                "type": "input_ip",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "IP address to be used as the external ip",
                "config": True
            },
            {
                "section": "networking",
                "key": "local_ip",
                "label": "Local IP",
                "type": "input_ip",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "IP address to be used as the local ip",
                "config": True
            }
       ]
    },
    "database_configs": { # database params
        "name": "Database Configurations",
        "next": "operator_params",
        "fields": [
            {
                "section": "database",
                "required": True,
                "key": "db_type",
                "label": "Database Type",
                "type": "selection",
                "options": ["", "sqlite", "psql"],
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Type of database to be used by the AnyLog node",
                "config": True,
            },
            {
                "section": "database",
                "required": True,
                "key": "db_user",
                "label": "Database Credentials",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Database credentials (ex. ${USER}@${IP}:${PASSWORD})",
                "config": True,
            },
            {
                "section": "database",
                "required": True,
                "key": "db_port",
                "label": "Database Port",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Database access port",
                "config": True,
            }
        ]
    },
    "operator_params": { # operator params - default dbms, cluster, partitioning
        "name": "Operator Params",
        "next": "mqtt_params",
        "node_type": ["rest", "operator", "single-node"],
        "fields": [
            {
                "section": "database",
                "required": True,
                "key": "default_dbms",
                "label": "Default Database",
                "type": "input_text",
                "options": ["true", "false"],
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Database correlated to the operator",
                "config": True
            },
            {
                "section": "cluster",
                "required": True,
                "key": "enable_cluster",
                "label": "Enable Cluster",
                "type": "selection",
                "options": ["true", "false"],
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Whether or not the operator is correlated to a cluster",
                "config": True
            },
            {
                "section": "cluster",
                "required": False,
                "key": "cluster_name",
                "label": "Cluster Name",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Cluster name",
                "config": True
            },
            {
                "section": "partition",
                "required": True,
                "key": "enable_partition",
                "label": "Enable Partitioning",
                "type": "selection",
                "options": ["false", "true"],
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Whether or not to enable partitioning",
                "config": True
            },
            {
                "section": "partition",
                "required": False,
                "key": "partition_column",
                "label": "Partition Column",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Timestamp column to partition by",
                "config": True
            },
            {
                "section": "partition",
                "required": False,
                "key": "partition_interval",
                "label": "Partition Interval",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Partition interval",
                "config": True
            }
        ]
    },
    "mqtt_params": { # MQTT params - should only be available for nodes of type publisher || operator
        "name": "MQTT Parameters",
        "next": "",
        "node_type": ["rest", "publisher", "operator", "single-node", "single-node-publisher"],
        "fields": [
            {
                "section": "mqtt",
                "required": True,
                "key": "mqtt_enable",
                "label": "Enable MQTT",
                "type": "selection",
                "options": ["false", "true"],
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Whether to enable MQTT",
                "config": True
            },
            {
                "section": "mqtt",
                "required": False, # required if mqtt_enable == "true"
                "key": "broker",
                "label": "Broker",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Whether to enable MQTT",
                "config": True
            },
            {
                "section": "mqtt",
                "required": False,  # required if mqtt_enable == "true"
                "key": "mqtt_port",
                "label": "MQTT Port",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT port",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_user",
                "label": "MQTT Username",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT username",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_password",
                "label": "MQTT Password",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT password",
                "config": True,
                "protected": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_log",
                "label": "MQTT Logging",
                "type": "selection",
                "options": ["false", "true"],
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "Whether to enable MQTT logging or not",
                "config": True
            },
            {
                "section": "mqtt",
                "required": False, # required if mqtt_enable == "true"
                "key": "mqtt_topic_name",
                "label": "Topic Name",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT topic name",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_topic_dbms",
                "label": "MQTT Topic Database",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT topic database",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_topic_table",
                "label": "MQTT Topic Name",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT topic table",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_column_timestamp",
                "label": "MQTT Timestamp Column",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT timestamp column name",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_column_value_type",
                "label": "MQTT Value Column Type",
                "type": "selection",
                "options": ["str", "int", "float", "bool", "timestamp"],
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT value column type",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_column_value",
                "label": "MQTT Value Column Value",
                "type": "input_text",
                "print_after": ["&nbsp;", "&nbsp;"],
                "help": "MQTT value column name",
                "config": True
            }
        ]
    }
}


class Example:
    def front_page(self, request)->HttpResponse:
        global FIRST_PAGE_KEY
        global PAGE_COUNTER
        global PAGES_LIST
        global al_forms

        selection_list = None
        save_button = False

        if request.method == 'POST':
            current_page = request.POST.get('page_name')

            if request.POST.get('show_selections'):
                # Keep the same page + show selections
                update_config(request)
                next_page_name = current_page
                selection_list = set_selection()         # This list is used to print the selection on the web page

            elif request.POST.get('previous_web_page'):
                next_page_name = set_previous()  # Set on the previous page or the first page

            elif request.POST.get('first_web_page'):
                next_page_name = FIRST_PAGE_KEY  # Set on the previous page or the first page
                PAGE_COUNTER = 0

            elif request.POST.get('save_config'):
                update_config(request)  # go to the last page
                write_config_file()
                next_page_name = current_page  # repeat page with option to save data
            else:
                # get next page
                next_page_name = update_config(request)
                if not next_page_name or next_page_name == "None":
                    # No more pages
                    next_page_name = current_page # repeat page with option to save data
                    save_button = True      # add save button
        else:
            next_page_name = set_previous()             # Set on the previous page or the first page

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

        al_forms[next_page_name]["save_button"] = save_button
        if selection_list:
            # add selection
            al_forms[next_page_name]["selection_header"] = ("Page", "Field", "Key", "Value")
            al_forms[next_page_name]["selection_list"] = selection_list
        else:
            # delete the selection
            if "selection_list" in al_forms[next_page_name]:
                del al_forms[next_page_name]["selection_list"]

        return render(request, 'generic.html', al_forms[next_page_name])

# ------------------------------------------------------------------------------------------------------
# Update the form info with the user selections on the form page
# ------------------------------------------------------------------------------------------------------
def update_config(request):
    '''
    Use the keys from al_forms to retrieve the values set on th eforms
    '''
    global al_forms

    post_data = request.POST
    page_name = post_data.get('page_name')
    next_page = post_data.get('next_page')
    if '.' in next_page:
        # get next page using an option list - example: "base_configs.node_type"
        next_page_info = next_page.split('.')
        page_key = next_page_info[0]        # The page with the options
        column_name = next_page_info[1]     # The column with the options
        form_defs = al_forms[page_key]
        fields = form_defs["fields"]
        for field in fields:
            if field["key"] == column_name:
                value = field["value"]
                index = field["options"].index(value)
                if field["next"][index]:
                    next_page = field["next"][index]    # Get the page name as a f(option selected)
                break;

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
# Update a list of selections
# ------------------------------------------------------------------------------------------------------
def set_selection():

    global FIRST_PAGE_KEY
    global PAGE_COUNTER
    global PAGES_LIST
    global al_forms

    selections_list = []

    for page_id in range (PAGE_COUNTER):

        page_key = PAGES_LIST[page_id]
        # get field values
        form_defs = al_forms[page_key]
        fields = form_defs["fields"]

        for index, field in enumerate(fields):

            if not index:
                page_name = form_defs["name"]
            else:
                page_name = ""

            if "key" in field and "value" in field and "type" in field:
                if "label" in field:
                    label = field["label"]
                else:
                    label = ""

                if field["type"] == "input_password":
                    value = '*' * len(field["value"])       # not showing value on screen
                else:
                    value = field["value"]

                selections_list.append((page_name, label, field["key"], value))

    return selections_list

# ------------------------------------------------------------------------------------------------------
# Return and set status on the previous page or on the first page if no previous
# ------------------------------------------------------------------------------------------------------
def set_previous():
    global FIRST_PAGE_KEY
    global PAGE_COUNTER
    global PAGES_LIST

    if PAGE_COUNTER > 1:
        PAGE_COUNTER -= 2  # Go back
        previous_page_name = PAGES_LIST[PAGE_COUNTER]
    else:
        previous_page_name = FIRST_PAGE_KEY  # First page to display
        PAGE_COUNTER = 0

    return previous_page_name
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