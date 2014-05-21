ALL_NODE_STATUS = {
    'UP': {
        'description': 'All OK',
        'url': "/static/images/up.png",
    },
    'TESTABLE': {
        'description': 'Minor failures detected; testing should be unaffected',
        'url': "/static/images/warning.png",
    },
    'UNTESTABLE': {
        'description': 'Critical failures detected; testing may be impeded',
        'url': "/static/images/down.png",
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
                self._set_status_if_has_failure_jobs()
            else:
                self.status = ALL_NODE_STATUS['UP']
        else:
            self.status = ALL_NODE_STATUS['UNREACHABLE']

    def _set_status_if_has_failure_jobs(self):
        self.status = ALL_NODE_STATUS['TESTABLE']
        for failure_job in self.failure_job_list:
            self._check_availability(failure_job)

    def _check_availability(self, failure_job):
        if failure_job['job_name'].find('Env_Availability_Check') != -1:
            self.status = ALL_NODE_STATUS['UNTESTABLE']
