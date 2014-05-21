import django
from django.test.utils import setup_test_environment
from env_health_dashboard.job_list_status import JobListStatus


class JobStatusTests(django.test.testcases.TestCase):

    def test_job_status_success(self):
        job_status = JobListStatus([], None)
        job_status.determine_job_status()
        self.assertEqual(job_status.status['description'], 'All OK')

    def test_envrionment_status_down_with_failure_job(self):
        job_status = JobListStatus(['FAILURE'], None)
        job_status.determine_job_status()
        self.assertEqual(job_status.status['description'], 'Warning: Build failures detected')

    def test_envrionment_status_down_with_unstable_job(self):
        job_status = JobListStatus(['UNSTABLE'], None)
        job_status.determine_job_status()
        self.assertEqual(job_status.status['description'], 'Warning: Build failures detected')

    def test_envrionment_status_unreachable(self):
        job_status = JobListStatus(['UNSTABLE'], "Exception")
        job_status.determine_job_status()
        self.assertEqual(job_status.status['description'], 'Failed to get status')
