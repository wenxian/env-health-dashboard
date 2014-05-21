import django
from django.test.utils import setup_test_environment
from mock import MagicMock
from env_health_dashboard.alexandria_services import AlexandriaServices
from env_health_dashboard.server_locations import ALEXANDRIA_SERVER
import json


class AlexandriaServicesTests(django.test.testcases.TestCase):

    def setUp(self):
        self.alexandria_services = AlexandriaServices(ALEXANDRIA_SERVER)

    def test_get_job_status(self):
        self.alexandria_services._get_url_content = MagicMock(return_value="SUCCESS")

        content = self.alexandria_services.get_job_status("job_name_test", "job_repository_test")

        self.alexandria_services._get_url_content.assert_called_with(
            "http://test-results.internal.shutterfly.com/job/status?job_name=job_name_test&"
            "job_repository=job_repository_test")

        self.assertEqual(content, "SUCCESS")

    def test_get_failure_test_result(self):
        failure_test_result_json = \
            '[{"url": "url", "job_repository": "job_repository", ' \
            '"test_name": "test_name", ' \
            '"class_name": "class_name", "module_name": "module_name", ' \
            '"error_message": "error_msg", ' \
            '"job_name": "job_name", "last_build_number": "build_number"}]'
        self.alexandria_services._get_url_content = MagicMock(return_value=failure_test_result_json)

        content = self.alexandria_services.get_last_job_test_result_failures(
            "job_name_test", "job_repository_test")

        failure_test_result = json.loads(failure_test_result_json)
        self.alexandria_services._get_url_content.assert_called_with(
            "http://test-results.internal.shutterfly.com/job/"
            "last_build_failed_test_results?job_name=job_name_test&"
            "job_repository=job_repository_test")

        self.assertEqual(content, failure_test_result)
