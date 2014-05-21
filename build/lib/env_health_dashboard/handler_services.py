import alexandria_services
# icon name comes from http://getbootstrap.com/components/, class
ALL_NODE_STATUS = {
    'UP': {
        'description': 'All Ok',
        'url': "/static/images/up.png",
        },
    'DOWN': {
        'description': 'Warning: Issues found',
        'url': "/static/images/warning.png",
        },
    'UNREACHABLE': {
        'description': 'Failed to get status',
        'url': "/static/images/unreachable.png",
        }
}


def _get_status_from_env_config(env, env_config):
    status = "UNREACHABLE"
    if env == 'foxtrot':
        status_content = alexandria_services.get_site_status(env_config['job_name'],env_config['job_repository'])
        if status_content == "SUCCESS":
            status = "UP"
        elif status_content == "UNSTABLE":
            status = "DOWN"
        elif status_content == "FAILURE":
            status = "DOWN"
    else:
        raise Exception("Not Implemented")
    return status


def _get_env_site_status_list(env_list):
    env_status_list = []

    foxtrot_config = dict()
    foxtrot_config['job_name'] = "Env_Health_Check-Foxtrot"
    foxtrot_config['job_repository'] = "tre-jenkins"

    for env in env_list:
        env_dict = dict()
        env_dict['name'] = env
        try:
            status_key = _get_status_from_env_config(env, foxtrot_config)
        except Exception as ex:
            env_dict['exception'] = ex
            status_key = "UNREACHABLE"
        env_dict['status_key'] = status_key
        env_dict['status'] = ALL_NODE_STATUS[status_key]
        env_status_list.append(env_dict)

    return env_status_list

