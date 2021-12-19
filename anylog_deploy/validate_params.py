def format_content(env_params:dict)->dict:
    """
    Given the generated environment params, convert to usable params
    :sample-content:
        * anylog-rest.ini provides a completed form as an example
    :args:
        env_params:dict - user inputted parameters
    :params:
        encrypt_password:password_encryption.EncryptPasswords - class call to encrypt password(s)
    :return:
        updated env_params
    """

    for key in env_params:
        if key == 'general' and env_params[key]['node_type'] == 'generic':
            '''
            Convert node_type from generic to none   
            '''
            env_params[key]['node_type'] = 'none'

        if key == 'authentication':
            '''
            if username or password is missing set authentication to false
            '''
            if env_params[key]['authentication'] == 'true' and ('username' not in env_params[key] or
                                                                'password' not in env_params[key]):
                env_params[key]['authentication'] = 'false'

        if key == 'networking':
            '''
            1. merge master node params into a single value 
            '''
            env_params[key]['master_node'] = '%s:%s' % (env_params[key]['master_node_ip'],
                                                        env_params[key]['master_node_port'])
            for param in ['master_node_ip', 'master_node_port']:
                del env_params[key][param]

        if key == 'database':
            '''
            merge database credential information into a single value
            '''
            env_params[key]['db_user'] = '%s@%s:%s' % (env_params[key]['db_username'], env_params[key]['db_ip'],
                                                       env_params[key]['db_password'])
            for param in ['db_username', 'db_ip', 'db_password']:
                del env_params[key][param]

        if key == 'cluster':
            '''
            validate cluster name if cluster is valid, if not generate name
            '''
            if env_params[key]['enable_cluster'] == 'true' and 'cluster_name' not in env_params[key]:
                env_params[key]['cluster_name'] = '%s-cluster' % (env_params['general']['company'].replace(' ', '-'))

        if key == 'partition':
            '''
            1. validate column and interval value, if not set to False
            2. (if enable_partition is true) create partition interval  
            '''
            if env_params[key]['enable_partition'] == 'true' and ('partition_column' not in env_params[key]
                                                                  or 'partition_interval_value' not in env_params[key]
                                                                  or  'partition_interval_period' not in env_params[key]):
                env_params[key]['enable_partition'] = 'false'
            elif env_params[key]['enable_partition'] == 'true':
                env_params[key]['partition_interval'] = '%s %s' % (env_params[key]['partition_interval_value'],
                                                                   env_params[key]['partition_interval_period'])
                for param in ['partition_interval_value', 'partition_interval_period']:
                    del env_params[key][param]

        if key == 'data_monitor':
            '''
            1. validate time_value and time_interval are set
            2. (if enable_data_monitor == true) declare  data_monitor_interval
            '''
            if env_params[key]["enable_data_monitor"] == 'true' and ('time_interval' not in env_params[key]
                                                                     or 'time_value' not in env_params[key]):
                env_params[key]["enable_data_monitor"] = 'false'
            elif env_params[key]["enable_data_monitor"] == "true":
                env_params[key]["data_monitor_interval"] = "%s %s" % (env_params[key]["time_value"],
                                                                      env_params[key]["time_interval"])
                for param in ["time_value", "time_interval"]:
                    del env_params[key][param]

        if key == 'mqtt':
            '''
            1. validate broker & port are set if MQTT is enabled
            '''
            if env_params[key]['mqtt_enable'] == 'true' and (not env_params[key]['broker'] or
                                                             not env_params[key]['mqtt_port']):
                env_params[key]['mqtt_enable'] = 'false'


    return env_params
