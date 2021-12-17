import configparser
import os

ROOT_DIR_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('anylog_conn', 1)[0]
CONFIG_FILE = os.path.join(ROOT_DIR_PATH, 'config', 'new-config.ini')


def write_configs(config_file:str=CONFIG_FILE, config_data:dict={}):
    """
    Write configurations to file
    :args:
        config_data:dict - content to write to file
        config_file:str - file to write content into
    :params:
        parser:configparser.configparser.ConfigParser - configuration parser
    :return:
        error otherwise None
    """
    config_file = os.path.expandvars(os.path.expanduser(config_file))
    output = None
    # create file if DNE
    if not os.path.isfile(config_file):
        try:
            open(config_file, 'w').close()
        except Exception as e:
            print('Error: Unable to create file %s (Error: %s)' % (config_file, e))
    try:
        parser = configparser.ConfigParser()
    except Exception as e:
        print('Error: Unbale to set parser for setting configs (Error: %s)' % e)

    try:
        for section in config_data:
            parser.add_section(section)
            for key in config_data[section]:
                if config_data[section][key] != '' and config_data[section][key] != None:
                    parser.set(section, key, config_data[section][key])
    except Exception as e:
        print('Error: Failed to add content into file (Error: %s)' % e)

    try:
        with open(config_file, 'w') as configfile:
            try:
                parser.write(configfile)
            except Exception as e:
                print('Error: Failed to write content into %s (Error: %s)' % (config_file, e))
    except Exception as e:
        print('Error: Failed to open %s for content to be written (Error: %s)' % (config_file, e))




