ALL_QUEUE_STATUS = {
    'ENABLED': {
        'description': 'Test Job Queue: Enabled',
        'url': "/static/images/up.png",
        'key': "enabled"
    },
    'DISABLED': {
        'description': 'Test Job Queue: Disabled',
        'url': "/static/images/gray.png",
        'key': "disabled"
    },
    'UNREACHABLE': {
        'description': 'Test Job Queue: Non-supported feature',
    }
}


class QueueStatus():

    def __init__(self, job_status, exception):
        self.job_status = job_status
        self.exception = exception

    def determine_queue_status(self):
        if not self.exception:
            if self.job_status == "SUCCESS":
                self.status = ALL_QUEUE_STATUS['ENABLED']
            else:
                self.status = ALL_QUEUE_STATUS['DISABLED']
        else:
            self.status = ALL_QUEUE_STATUS['UNREACHABLE']
