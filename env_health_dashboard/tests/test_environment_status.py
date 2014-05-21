import django
from django.test.utils import setup_test_environment
from env_health_dashboard.environment_status import EnvironmentStatus


class EnvironmentStatusTests(django.test.testcases.TestCase):

    def test_envrionment_status_success(self):
        env_status = EnvironmentStatus("env", [], None)
        env_status.determine_env_status()
        self.assertEqual(env_status.status['description'], 'All OK')

    def test_envrionment_status_down_with_failure_job(self):
        failure_job_list = [
            {
                "url": "http://job_repository/job/jobname/jobnumber/testReport/healthchecks.testify/AdminServerTest/test_name",
                "job_repository": "job_repository",
                "test_name": "env--pool--server--test_name",
                "class_name": "class_name",
                "module_name": "module_name",
                "error_message": "error_msg",
                "job_name": "Env_Availability_Check-Test",
                "last_build_number": "build_number"
            }
        ]
        env_status = EnvironmentStatus("env", failure_job_list, None)
        env_status.determine_env_status()
        self.assertEqual(env_status.status['description'], 'Critical failures detected; testing may be impeded')

    def test_envrionment_status_down_with_unstable_job(self):
        failure_job_list = [
            {
                "url": "http://job_repository/job/jobname/jobnumber/testReport/healthchecks.testify/AdminServerTest/test_name",
                "job_repository": "job_repository",
                "test_name": "env--pool--server--test_name",
                "class_name": "class_name",
                "module_name": "module_name",
                "error_message": "error_msg",
                "job_name": "Env_Health_Check-Test",
                "last_build_number": "build_number"
            }
        ]
        env_status = EnvironmentStatus("env", failure_job_list, None)
        env_status.determine_env_status()
        self.assertEqual(env_status.status['description'], 'Minor failures detected; testing should be unaffected')

    def test_envrionment_status_unreachable(self):
        env_status = EnvironmentStatus("env", ['UNSTABLE'], "Exception")
        env_status.determine_env_status()
        self.assertEqual(env_status.status['description'], 'Failed to get status')
