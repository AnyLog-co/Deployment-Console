import re


def validate_master_node(master_node:str)->bool:
    """
    Validate whether value set for master_node is valid
    :args:
        master_node:str - master node param
    :params:
        status:bool
        regex_param:str - master node address pattern
    :return:
        if success True, else, False
    """
    regex_param = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:[2-9][0-9][4-9][0-9]$'
    try:
        status = bool(re.match(regex_param, master_node))
    except:
        status = False
    else:
        if status is True:
            # validate IP address
            status = validate_ip_address(ip_address=master_node.split('@')[0])

    return status


def validate_ports(**kwargs)->bool:
    """
    Validate ports
    :args:
        kwargs:dict - "list" of ports
    :params:
        status:dict - statues for different cases
        unique_values:list - list of ports
    :return:
        if one or more cases fails return False, else return True
    """
    status = {}
    unqiue_values = []

    # validate port number(s) within range
    for key in kwargs:
        if isinstance(kwargs[key], int) and (kwargs[key] < 2048 or kwargs[key] > 65535):
            status[key] = False
        elif not isinstance(kwargs[key], int):
            status[key] = False
        else:
            status[key] = True

    # assert no 2 ports are the same
    if len(kwargs) > 1:
        for value in list(kwargs.values()):
            if value not in unqiue_values:
                unqiue_values.append(value)
            else:
                status['unique'] = False

    if False in list(status.values()):
        return False
    return True


def validate_ip_address(ip_address:str)->bool:
    """
    Validate whether input is a valid IP address of not
    :args:
        ip_address:str - IP address
    :params:
        status:bool
        regex_pattern:str - IP address pattern
    :return:
        if success True, else, False
    """
    regex_pattern = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
    status = True
    if ip_address != 'localhost':
        try:
            status = bool(re.match(regex_pattern, ip_address))
        except:
            status = False

    return status
