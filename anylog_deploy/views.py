import os
import socket

import django.core.handlers.wsgi
import anylog_api.io_config as io_config
from django.http.response import HttpResponse
from django.shortcuts import render

from anylog_deploy.validate_params import format_content

FIRST_PAGE_KEY = "base_configs"      # First page ID

PAGE_COUNTER = 0                    # Number of pages process
PAGES_LIST = []                     # An array with pages visited

# Config directory params
CONFIG_DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')
if not os.path.isdir(CONFIG_DIR_PATH):
    os.makedirs(CONFIG_DIR_PATH)

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
    # Basic node type & build configuration
    "base_configs" : {
        "name" : "Base Configs",
        "next" : "general_info",
        "fields" : [
            {
                "section": "general",
                "required": True,
                "key" : "build",
                "label" : "Build",
                "type" : "selection",
                "options" : ["predevelop"],
                "print_after" : ["<br/>","<br/>"],
                "help" : "AnyLog version to download from Docker Hub",
                "config" : True,
            },
            {
                "section": "general",
                "required": True,
                "key": "node_type",
                "label": "Node Type",
                "type": "selection",
                "options": ["generic", "rest", "master", "operator", "publisher", "query", "single-node",
                            "single-node-publisher"],
                "next1": ["database_configs", "network_configs", "network_configs", "network_configs", "network_configs",
                         "network_configs", "network_configs", "network_configs"],
                "next2": [None, "database_configs", "database_configs", "database_configs", "database_configs",
                         "database_configs", "database_configs", "database_configs"],
                "next3": [None, "operator_params", None, "operator_params", "mqtt_params",
                          None, "operator_params", "mqtt_params"],
                "print_after" : ["<br/>","<br/>"],
                "help": "Type of node AnyLog should run",
                "config": True,
            }
        ]
    },
    # General information & authentication params
    "general_info": {
        "name": "General Information",
        "next": "base_configs.node_type.next1",      # 3 sections: page + field + key in field showing destination pages
        "fields" : [
            {
                "section": "general",
                "required": True,
                "key" : "node_name",
                "label" : "Node Name",
                "value": "new-node",
                "type" : "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help" : "Name correlated with the node",
                "config" : True,
            },
            {
                "section": "general",
                "required": True,
                "key": "company_name",
                "label": "Company Name",
                "value": "Your Company Name",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "Company correlated with policies declared via this node",
                "config": True
            },
            { # Optional
                "section": "general",
                "key": "location",
                "label": "Location",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "Machine location - coordinates location is accessible via Grafana Map visualization",
                "config": True
            },
            {
                "section": "authentication",
                "required": True,
                "key": "authentication",
                "label": "Authentication",
                "type": "checkbox",
                "print_after" : ["<br/>","<br/>"],
                "help": "Whether or not to enable authentication",
                "config": True
            },
            {
                "section": "authentication",
                "key": "username",
                "label": "Authentication User",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "Authentication username",
                "config": True
            },
            {
                "section": "authentication",
                "key": "password",
                "label": "Authentication Password",
                "type": "input_password",
                "print_after" : ["<br/>","<br/>"],
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
                "print_after" : ["<br/>","<br/>"],
                "help": "Authentication user type",
                "config": True
            }
        ]
    },
    # network configurations
    "network_configs": {
        "name": "Network Configurations",
        "next": "base_configs.node_type.next2",
        "fields": [
            {
                "section": "networking",
                "required": True,
                "key": "anylog_tcp_port",
                "label": "TCP Port",
                "type": "input_number",
                "value": 2048,
                "min": 2048, "max": 65535,
                "print_after" : ["<br/>","<br/>"],
                "help": "TCP port for node used to communicate with other nodes in the network",
                "config": True,
            },
            {
                "section": "networking",
                "required": True,
                "key": "anylog_rest_port",
                "label": "REST Port",
                "type": "input_number",
                "value": 2049,
                "min": 2048, "max": 65535,
                "print_after" : ["<br/>","<br/>"],
                "help": "REST port to communicate against with the AnyLog instance",
                "config": True,
            },
            {
                "section": "networking",
                "required": True,
                "key": "master_node_ip",
                "label": "Master Node",
                "type": "input_ip",
                "value": socket.gethostbyname(socket.gethostname()),
                "print_after" : ["",":"],
                "help": "TCP IP connection information for master node",
                "config": True,
            },
            {
                "section": "networking",
                "required": True,
                "key": "master_node_port",
                "type": "input_number",
                "value": 2048,
                "min": 2048, "max": 65535,
                "print_after" : ["<br/>","<br/>"],
                "help": "TCP port connection information for master node",
                "config": True,
            },
            # Optional params
            {
                "section": "networking",
                "key": "external_ip",
                "label": "External IP",
                "type": "input_ip",
                "print_after" : ["<br/>","<br/>"],
                "help": "IP address to be used as the external ip",
                "config": True
            },
            {
                "section": "networking",
                "key": "local_ip",
                "label": "Local IP",
                "type": "input_ip",
                "print_after" : ["<br/>","<br/>"],
                "help": "IP address to be used as the local ip",
                "config": True
            },
            {
                "section": "networking",
                "key": "anylog_broker_port",
                "label": "Local Broker Port",
                "type":"input_number",
                "min": 2048, "max": 65535,
                "print_after" : ["<br/>","<br/>"],
                "help": "AnyLog broker port",
                "config": True
            }
       ]
    },
    # database params
    "database_configs": {
        "name": "Database Configurations",
        "next": "base_configs.node_type.next3",
        "fields": [
            {
                "section": "database",
                "required": True,
                "key": "db_type",
                "label": "Database Type",
                "type": "selection",
                "options": ["", "sqlite", "psql"],
                "print_after": ["<br/>","<br/>"],
                "help": "Type of database to be used by the AnyLog node",
                "config": True,
            },
            {
                "section": "database",
                "required": True,
                "key": "db_username",
                "label": "Database Credentials",
                "type": "input_text",
                "value": "db_user",
                "print_after" : ["","@"],
                "help": "Database username",
                "config": True,
            },
            {
                "section": "database",
                "required": True,
                "key": "db_ip",
                "type": "input_ip",
                "value": "127.0.0.1",
                "print_after" : ["",":"],
                "help": "IP address of database",
                "config": True,
            },
            {
                "section": "database",
                "required": True,
                "key": "db_password",
                "type": "input_password",
                "print_after" : ["<br/>","<br/>"],
                "help": "Database password correlated to user",
                "config": True,
            },
            {
                "section": "database",
                "required": True,
                "key": "db_port",
                "label": "Database Port",
                "type": "input_number",
                "value": 5432,
                "min": 2048, "max": 65535,
                "print_after" : ["<br/>","<br/>"],
                "help": "Database access port",
                "config": True,
            }
        ]
    },
    # operator params - default dbms, cluster, partitioning
    "operator_params": {
        "name": "Operator Params",
        "next": "data_monitor",
        "node_type": ["rest", "operator", "single-node"],
        "fields": [
            {
                "section": "database",
                "required": True,
                "key": "default_dbms",
                "label": "Default Database",
                "type": "input_text",
                "value": "test_db",
                "print_after" : ["<br/>","<br/>"],
                "help": "Logical Database correlated to the operator",
                "config": True
            },
            {
                "section": "cluster",
                "required": False,
                "key": "enable_cluster",
                "label": "Enable Cluster",
                "type": "checkbox",
                "print_after" : ["<br/>","<br/>"],
                "help": "Whether or not the operator is correlated to a cluster",
                "config": True
            },
            {
                "section": "cluster",
                "required": False,
                "key": "cluster_name",
                "label": "Cluster Name",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "Cluster name",
                "config": True
            },
            {
                "section": "partition",
                "required": False,
                "key": "enable_partition",
                "label": "Enable Partitioning",
                "type": "checkbox",
                "print_after": ["<br/>","<br/>"],
                "help": "Whether or not to enable partitioning",
                "config": True
            },
            {
                "section": "partition",
                "required": False,
                "key": "partition_column",
                "label": "Partition Column",
                "type": "input_text",
                "print_after": ["<br/>","<br/>"],
                "help": "Timestamp column to partition by",
                "config": True
            },
            {
                "section": "partition",
                "required": False,
                "key": "partition_interval_value",
                "label": "Partition Interval",
                "type": "input_text",
                "print_after": ["", "&nbsp;"],
                "help": "Partition interval",
                "config": True
            },
            {
                "section": "partition",
                "required": False,
                "key": "partition_interval_period",
                "type": "selection",
                "options": ["hour", "day", "month", "year"],
                "print_after": ["<br/>", "<br/>"],
                "help": "Partition interval",
                "config": True
            },
            {
                "section": "partition",
                "required": False,
                "key": "drop_partition",
                "label": "Enable Drop Partition",
                "type": "checkbox",
                "print_after": ["<br/>", "<br/>"],
                "help": "Whether or not to drop partitions",
                "config": True
            },
            {
                "section": "partition",
                "required": "False",
                "key": "partition_keep",
                "label": "Days",
                "type": "input_number",
                "print_after": ["<br/>", "<br/>"],
                "help": "Number of partition days to keep",
                "config": True
            }
        ]
    },
    # information for monitoring data on operator node
    "data_monitor": {
        "name": "Data Monitoring",
        "next": "mqtt_params",
        "node_type": ["rest", "operator", "single-node"],
        "fields": [
            {
                "section": "data_monitor",
                "required": False,
                "key": "enable_data_monitor",
                "label": "Enable Data Monitor",
                "type": "checkbox",
                "print_after" : ["<br/>","<br/>"],
                "help": "Whether to enable data monitoring",
                "config": True

            },
            {
                "section": "data_monitor",
                "required": False,
                "key": "table_name",
                "label": "Table Name",
                "type": "input_text",
                "value": "*",
                "print_after" : ["<br/>","<br/>"],
                "help": "Table(s) to monitor",
                "config": True
            },
            {
                "section": "data_monitor",
                "required": False,
                "key": "interval_value",
                "label": "Interval",
                "type": "input_number",
                "value": 10,
                "print_after" : ["<br/>","<br/>"],
                "help": "number of interval to keep",
                "config": True
            },
            {
                "section": "data_monitor",
                "required": False,
                "key": "time_value",
                "label": "Frequency",
                "type": "input_number",
                "print_after": ["", "&nbsp;"],
                "help": "Numeric amount of time",
                "config": True
            },
            {
                "section": "data_monitor",
                "required": False,
                "key": "time_interval",
                "type": "selection",
                "options": ["second", "minute", "hour", "day"],
                "print_after": ["<br/>", "<br/>"],
                "help": "Time interval period",
                "config": True
            }
        ]
    },
    # MQTT related params
    "mqtt_params": {
        "name": "MQTT Parameters",
        "next": None,
        "node_type": ["rest", "publisher", "operator", "single-node", "single-node-publisher"],
        "fields": [
            {
                "section": "mqtt",
                "required": True,
                "key": "mqtt_enable",
                "label": "Enable MQTT",
                "type": "checkbox",
                "print_after" : ["<br/>","<br/>"],
                "help": "Whether to enable MQTT",
                "config": True
            },
            {
                "section": "mqtt",
                "required": False, # required if mqtt_enable == "true"
                "key": "broker",
                "label": "Broker",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "Whether to enable MQTT",
                "config": True
            },
            {
                "section": "mqtt",
                "required": False,  # required if mqtt_enable == "true"
                "key": "mqtt_port",
                "label": "MQTT Port",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT port",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_user",
                "label": "MQTT Username",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT username",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_password",
                "label": "MQTT Password",
                "type": "input_password",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT password",
                "config": True,
                "protected": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_log",
                "label": "Enable MQTT Logging",
                "type": "checkbox",
                "print_after" : ["<br/>","<br/>"],
                "help": "Whether to enable MQTT logging or not",
                "config": True
            },
            {
                "section": "mqtt",
                "required": False, # required if mqtt_enable == "true"
                "key": "mqtt_topic_name",
                "label": "Topic Name",
                "type": "input_text",
                "value": "*",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT topic name",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_topic_dbms",
                "label": "MQTT Topic Database",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT topic database",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_topic_table",
                "label": "MQTT Topic Name",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT topic table",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_column_timestamp",
                "label": "MQTT Timestamp Column",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT timestamp column name",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_column_value_type",
                "label": "MQTT Value Column Type",
                "type": "selection",
                "options": ["", "str", "int", "float", "bool", "timestamp"],
                "print_after" : ["&nbsp;", "&nbsp;"],
                "help": "MQTT value column type",
                "config": True
            },
            {
                "section": "mqtt",
                "key": "mqtt_column_value",
                "label": "MQTT Value Column Value",
                "type": "input_text",
                "print_after" : ["<br/>","<br/>"],
                "help": "MQTT value column name",
                "config": True
            }
        ]
    }
}


class DeploymentConsole:
    def front_page(self, request:django.core.handlers.wsgi.WSGIRequest)->HttpResponse:
        """
        Call to the deployment website (default: 127.0.0.1:8000)
        :args:
            request:django.core.handlers.wsgi.WSGIRequest - type of request against the form
        :global params:
            FIRST_PAGE_KEY - initial page
            PAGE_COUNTER:int - number value of the page user is on
            PAGES_LIST:list - list of pages
            al_forms:dict - with configuration content by user
        :params:
            selection_list:list - print selections
            save_button:bool - save content
        :redirect:
            update generic.html based on the form information
        """
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


def update_config(request:django.core.handlers.wsgi.WSGIRequest):
    """
    Update the form info with the user selections on the form page - Use the keys from al_forms to retrieve the values
    set on the forms
    :args:
        request:django.core.handlers.wsgi.WSGIRequest - type of request against the form
    :global params:
        al_forms:dict - with configuration content by user
    :params:
        post_data:request.POST
        page_name:str - page being generated
        next_page:str - following page
        form_defs:dict - content inputted by user
        fields:list - form questions for section
    """
    global al_forms

    post_data = request.POST
    page_name = post_data.get('page_name')
    next_page = post_data.get('next_page')
    if '.' in next_page:
        # get next page using an option list - example: "base_configs.node_type"
        next_page_info = next_page.split('.')   # Need to be 3 sections:
                                                # page + field + key in field showing destination pages
        if len(next_page_info) == 3:
            page_key = next_page_info[0]        # The page with the options
            column_name = next_page_info[1]     # The column with the options
            column_key = next_page_info[2]      # The name of the key with the options

            form_defs = al_forms[page_key]
            fields = form_defs["fields"]

            # fnd the next page to use
            for field in fields:
                if column_key in field:
                    if field["key"] == column_name:
                        value = field["value"]
                        index = field["options"].index(value)
                        if column_key in field and len( field[column_key]) > index:
                            next_page = field[column_key][index]    # Get the page name as a f(option selected)
                        break

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


def set_selection():
    """
    Based on user input, updated selections
    :global params:
        FIRST_PAGE_KEY - initial page
        PAGE_COUNTER:int - number value of the page user is on
        PAGES_LIST:list - list of pages
        al_forms:dict - with configuration content by user
    :params:
        selections_list:list - content
        form_defs:dict - content inputted by user
    """
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


def set_previous()->str:
    """
    Return and set status on the previous page or on the first page if no previous
    :global params;
        FIRST_PAGE_KEY - initial page
        PAGE_COUNTER:int - number value of the page user is on
        PAGES_LIST:list - list of pages
    :params:
        previous_page_name:str - previous page name
    :return:
        previous_page_name
    """
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


def write_config_file():
    """
    Create the config file + Output the info to a config file
    :global params:
        FIRST_PAGE_KEY - initial page
        PAGE_COUNTER:int - number value of the page user is on
        PAGES_LIST:list - list of pages
        al_forms:dict - with configuration content by user
    :params:
        config_params:dict - params to write to file
        config_file:str - full file path
    """
    global al_forms
    global PAGE_COUNTER
    global PAGES_LIST

    config_params = {}

    for counter in range(PAGE_COUNTER):
        page_name = PAGES_LIST[counter]
        form_defs = al_forms[page_name]
        fields = form_defs["fields"]

        for field in fields:
            if "key" in field and "value" in field:
                if "config" in field and field["config"] is True:       # field["config"] set to false makes the value removed from the output file
                    if field['section'] not in config_params:
                        config_params[field['section']] = {}
                    if isinstance(field['value'], bool):
                        config_params[field['section']][field["key"]] = str(field['value']).lower()
                    elif field['value'] != '':
                        config_params[field['section']][field["key"]] = field['value']

        if counter == PAGE_COUNTER - 1:
            # write to config file
            print(config_params)
            config_params = format_content(env_params=config_params)
            print(config_params)
            config_file = os.path.join(CONFIG_DIR_PATH, '%s.ini' % config_params['general']['node_name'])
            io_config.write_configs(config_file=config_file, config_data=config_params)
