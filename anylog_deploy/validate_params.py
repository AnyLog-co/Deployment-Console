def format_content(env_params:dict)->dict:
    """
    Given the generated environment params, convert to usable params
    :sample-content:
    {
        'general':
            {'build': 'predevelop', 'node_type': 'rest', 'node_name': 'anylog-rest', 'company_name': 'AnyLog Co.'},
        'authentication':
            {'authentication': 'false', 'auth_type': 'admin'},
        'networking':
            {'anylog_tcp_port': '2048', 'anylog_rest_port': '2049', 'master_node_ip': '10.0.0.228',
            'master_node_port': '2048'},
        'database':
            {'db_type': 'sqlite', 'db_port': '5432', 'default_dbms': 'test_db', 'db_user': 'anylog@127.0.0.1:demo'},
        'cluster':
            {'enable_cluster': 'true', 'cluster_name': 'anylog-cluster'},
        'partition':
            {'enable_partition': 'true', 'partition_column': 'timestamp', 'partition_interval_value': '2',
            'partition_interval_period': 'day'},
        'mqtt':
            {'mqtt_enable': 'true', 'broker': 'driver.cloudmqtt.com', 'mqtt_port': '18785', 'mqtt_user': 'ibglowct',
            'mqtt_password': 'test', 'mqtt_log': 'false', 'mqtt_topic_name': 'anylogedgex',
            'mqtt_topic_dbms': 'bring [dbms]', 'mqtt_topic_table': 'bring [table]', 'mqtt_column_timestamp': 'now',
            'mqtt_column_value_type': 'float', 'mqtt_column_value': 'bring [readings][][value]'}
    }
    :args:
        env_params:dict - user inputted parameters
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
            if env_params[key]['authentication'] is 'true' and ('username' not in env_params[key] or
                                                                'password' not in env_params[key]):
                env_params[key]['authentication'] = 'false'

        if key == 'networking':
            '''
            1. merge master node params into a single value 
            2. validate ports are not the same - if they are change them
            '''
            env_params[key]['master_node'] = '%s:%s' % (env_params[key]['master_node_ip'],
                                                        env_params[key]['master_node_port'])
            for param in ['master_node_ip', 'master_node_port']:
                del env_params[key][param]

            if env_params[key]['anylog_tcp_port'] == env_params[key]['anylog_rest_port']:
                env_params[key]['anylog_rest_port'] += 1
            if env_params[key]['anylog_tcp_port'] == env_params[key]['anylog_broker_port']:
                env_params[key]['anylog_broker_port'] += 1
            if env_params[key]['anylog_rest_port'] == env_params[key]['anylog_broker_port']:
                env_params[key]['anylog_broker_port'] += 1

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
            if env_params[key]['enable_cluster'] == 'true' and 'cluster_name'  not in env_params[key]:
                env_params[key]['cluster_name'] = '%s-cluster' % (env_params['general']['comapny'].replace(' ', '-'))

        if key == 'partition':
            '''
            1. validate column and interval value, if not set to False
            2. create partition interval  
            '''
            if not env_params[key]['partition_column'] or not env_params[key]['partition_interval_value']:
                env_params[key]['enable_partition'] = 'false'

            if env_params[key]['enable_partition'] == 'true':
                env_params[key]['partition_interval'] = '%s %s' % (env_params[key]['partition_interval_value'],
                                                                   env_params[key]['partition_interval_period'])
                for param in ['partition_interval_value', 'partition_interval_period']:
                    del env_params[key][param]

        if key == 'mqtt':
            '''
            1. validate broker & port are set if MQTT is enabled
            2. if MQTT is enabled and topic is missing, set to *
            '''
            if env_params[key]['mqtt_enable'] == 'true' and (not env_params[key]['broker'] or
                                                             not env_params[key]['port']):
                env_params[key]['mqtt_enable'] = 'false'
            if env_params[key]['mqtt_enable'] == 'true' and not env_params[key]['mqtt_topic_name']:
                env_params[key]['mqtt_topic_name'] = '*'

    return env_params
