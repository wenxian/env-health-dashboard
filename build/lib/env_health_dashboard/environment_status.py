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


class EnvironmentStatus():

    def __init__(self, env, failure_job_list, exception):
        self.env = env
        self.failure_job_list = failure_job_list
        self.exception = exception

    def determine_env_status(self):
        if not self.exception:
            if self.failure_job_list:
                self.status = ALL_NODE_STATUS['DOWN']
            else:
                self.status = ALL_NODE_STATUS['UP']
        else:
            self.status = ALL_NODE_STATUS['UNREACHABLE']
