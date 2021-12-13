import os
from django import forms
from django.core.validators import RegexValidator
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')

CONTENT = {
    "select_configs": {
        "page_name": "Deploy AnyLog",
        "preset_config_file": {
            "label": "Config File",
            "type": forms.FilePathField,
            "required": False,
            "path": CONFIG_FILE_PATH,
            "match": r'^.*?\.ini$',
            "help": "List of configuration files in %s" % CONFIG_FILE_PATH
        },
        "external_config_file": {
            "label": "External Config File",
            "type": forms.CharField,
            "required": False,
            "widget": None,
            "help": "Manually input a configuration file"
    }
  }
}


class GenericForm(forms.Form):
    LOCAL_PARAMS = CONTENT["select_configs"]
    del LOCAL_PARAMS["page_name"]
    content = {}
    for param in LOCAL_PARAMS:
        if LOCAL_PARAMS[param]["type"] is forms.FilePathField:
            content[param] = forms.FilePathField(label=LOCAL_PARAMS[param]["label"], path=LOCAL_PARAMS[param]["path"],
                                                 required=LOCAL_PARAMS[param]["required"],
                                                 match=LOCAL_PARAMS[param]["match"],
                                                 help_text=LOCAL_PARAMS[param]["help"])
        elif LOCAL_PARAMS[param] is forms.CharField:
            content[param] = forms.CharField(label=LOCAL_PARAMS[param]["label"], widget=LOCAL_PARAMS[param]["widget"],
                                                 required=LOCAL_PARAMS[param]["required"],
                                                 match=LOCAL_PARAMS[param]["match"],
                                                 help_text=LOCAL_PARAMS[param]["help"])

