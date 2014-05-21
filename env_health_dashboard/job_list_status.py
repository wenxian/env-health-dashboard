ALL_JOB_STATUS = {
    'PASS': {
        'description': 'All OK',
        'url': "/static/images/up.png",
    },
    'FAIL': {
        'description': 'Warning: Build failures detected',
        'url': "/static/images/down.png",
    },
    'UNREACHABLE': {
        'description': 'Failed to get status',
    }
}


class JobListStatus():

    def __init__(self, failure_job_list, exception):
        self.failure_job_list = failure_job_list
        self.exception = exception

    def determine_job_status(self):
        if not self.exception:
            if self.failure_job_list:
                self.status = ALL_JOB_STATUS['FAIL']
            else:
                self.status = ALL_JOB_STATUS['PASS']
        else:
            self.status = ALL_JOB_STATUS['UNREACHABLE']
