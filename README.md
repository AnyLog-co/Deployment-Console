# Deployment Console 

The Deployment Console is a GUI based interface (using [Django](https://www.djangoproject.com/)) to easily create a 
configuration file. The actual deployment process is then done using the [AnyLog-API](https://github.com/AnyLog-co/AnyLog-API). 

The deployment console provides support for the following node types: 
* Generic -  clean node with nothing on it
* REST - node with a TCP/REST and authentication configuration, but no other processes running on it
* Master - notary node that manages and shares the content in blockchain 
* Operator - node containing data that comes in from device(s) 
* Publisher - node responsible for distributing the data 
* Query - node dedicated for querying data, though all nodes can query data
* Single-Node -  A node containing both _master_ and _operator_ process respectively
* Single-Node-Publisher -  A node containing both _master_ and _publisher_ process respectively


### Requirements
* Python3
  * [django](https://pypi.org/project/Django/)
  * [cryptography](https://pypi.org/project/cryptography/)  

### Deployment
```
cd $HOME/Deployment-Console
python3 $HOME/Deployment-Console/manage.py ${IP}:${PORT}
```

## For Developers

### Adding Forms
Unlike a regular Django form, the [views.py](anylog_deploy/views.py) contains a dictionary object (`al_forms`) which 
contains a dictionary of forms, which are formatted as shown bellow.   

**Full List of Support Option Types**: 
* selection - list of options to select from 
* input_text - generic text box
* input_ip - input of type IP
* input_password - An encrypted textbox 
* input_number - input of integer type, which supports min & max 
* checkbox - When checked sets valjue to _True_, else _False_ 

````python
# Sample form with a single field
al_forms = {
  "form_id": {
    "name": "Form Name",
    "next": "next_form", # the following form to go to
    "fields": [ # list of objects in form 
      {
        "section": "section_name", # ini config file section
        "required": False, # whether the field is required (boolean)
        "key": "value_key", # variable name within ini config file
        "label": "Value Key", # field label
        "type": "input_text", # expected valuee type
        "print_after": ["<br/>","<br/>"], # what to print after field
        "help": "help information", # help information
        "config": True # whether to save param or not
      }
    ]
  }
}
````

### Password Encryption
When setting the form value type to `input_password` the code recognizes to hide the content inputted by a user. 
Once all the forms are completed, the code finds all the passwords and encrypts them using the `cryptography.fernet` 
protocol.

The [password_encryption.py](anylog_deploy/password_encryption.py) works as follows:
1. Creates a new directory named [anylog_api/keys] if it doesn't exit (done in `__init__` process)
2. If a file named `encryption_key.txt` doesn't exist within said file create it, and store a key of type `Fernet` within it (`create_keys`)
3. Using the created key, encrypt the passwords(s) using the `encrypt_string` command. 



    
`





