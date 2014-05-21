import django
from django.test.utils import setup_test_environment
from env_health_dashboard.server_locations import *
from env_health_dashboard.models import PortletAssignment, Portlet
from mock import MagicMock
from datetime import datetime
from dateutil import tz
from env_health_dashboard import portlet_services
from env_health_dashboard.version_service import VersionService
from env_health_dashboard.server_locations import *


class PortletServiceTest(django.test.testcases.TestCase):

    def test_LastDeployTimePortletService(self):
        config = dict()
        config["server"] = "{SFLY_CHINA_JENKINS}"
        config["jobname"] = "Test Job"
        nextDeployTimePortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.NextDeployTimePortletService")
        envPortlet = PortletAssignment(
            title="Next scheduled deployment", portlet=nextDeployTimePortlet, config=config)
        service = portlet_services.LastDeployTimePortletService(envPortlet)
        date_object_utc = datetime.strptime("2014/03/19 22:27:46", "%Y/%m/%d %H:%M:%S")
        utc_object = date_object_utc.replace(tzinfo=tz.tzutc())

        mocked_jenkins = MagicMock()
        portlet_services._get_jenkins = MagicMock(return_value=mocked_jenkins)
        mocked_jenkins.get_last_build_timestamp = MagicMock(return_value=utc_object)
        service.execute()

        portlet_services._get_jenkins.assert_called_with(SFLY_CHINA_JENKINS)
        mocked_jenkins.get_last_build_timestamp.assert_called_with('Test Job')
        self.assertEqual(service.textContent, "2014/03/19 15:27 (PDT)")

    def test_BrandPortletService(self):
        config = dict()
        config["brand"] = "sfly"
        config["jobs"] = "jobs"
        brandPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.brandPortletService")
        envPortlet = PortletAssignment(portlet=brandPortlet, config=config)
        service = portlet_services.BrandPortletService(envPortlet)

        env_list_config = [
            {
                'job_name': "job1_name",
                'job_repository': "job1_repository",
            },
            {
                'job_name': "job2_name",
                'job_repository': "job2_repository",
            },
        ]
        queue_config = {
            'job_name': "job_queue_name",
            'job_repository': "job_queue_repository",
        }
        service._get_env_status_config_list_from_env = MagicMock(return_value=env_list_config)
        service._get_job_status_config_list_from_env = MagicMock(return_value=env_list_config)
        service._get_queue_status_config_list_from_env = MagicMock(return_value=queue_config)
        service.alexandria_services = MagicMock()
        service.alexandria_services.get_job_status = MagicMock(return_value="SUCCESS")
        service.execute()

        env_check_list = service.env_check_list
        self.assertEqual(len(env_check_list), 5)
        for each_check in env_check_list:
            self.assertEqual(each_check['env_status'].status['description'], "All OK")
            self.assertEqual(each_check['job_status'].status['description'], "All OK")
            self.assertEqual(each_check['web_sanity'].status['description'], "All OK")
            self.assertEqual(each_check['test_job_queue'].status['description'], "Test Job Queue: Enabled")

        service.alexandria_services.get_job_status = MagicMock(side_effect=Exception('Exception!'))
        service.execute()
        env_check_list = service.env_check_list
        self.assertEqual(len(env_check_list), 5)
        for each_check in env_check_list:
            self.assertEqual(each_check['env_status'].status['description'], 'Failed to get status')
            self.assertEqual(each_check['job_status'].status['description'], 'Failed to get status')
            self.assertEqual(each_check['web_sanity'].status['description'], 'Failed to get status')
            self.assertEqual(each_check['test_job_queue'].status['description'], 'Test Job Queue: Non-supported feature')

    def test_JobStatusPortletService(self):
        config = dict()
        config['env'] = "test_env"
        job = {
            "job_description": "job_description",
            'view_name': "view_name",
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': "job_name",
                    'job_repository': "tre-jenkins",
                }
            ]
        }
        config["job"] = job
        jobStatusPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.JobStatusPortletService")
        envPortlet = PortletAssignment(portlet=jobStatusPortlet, config=config)
        service = portlet_services.JobStatusPortletService(envPortlet)

        service.alexandria_services = MagicMock()
        service.alexandria_services.get_job_status = MagicMock(return_value="SUCCESS")
        service.execute()

        self.assertEqual(service.job['link'], SFLY_TRE_JENKINS + "/view/view_name")
        self.assertEqual(service.status_dict['description'], "job_description")
        self.assertEqual(service.status_dict['status'].status['description'], "All OK")

        job = {
            "job_description": "job_description",
            'job_name': "job_name",
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': "job_name",
                    'job_repository': "tre-jenkins",
                    }
            ]
        }
        config["job"] = job
        jobStatusPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.JobStatusPortletService")
        envPortlet = PortletAssignment(portlet=jobStatusPortlet, config=config)
        service = portlet_services.JobStatusPortletService(envPortlet)

        service.alexandria_services = MagicMock()
        service.alexandria_services.get_job_status = MagicMock(return_value="SUCCESS")
        service.execute()

        self.assertEqual(service.job['link'], SFLY_TRE_JENKINS + "/job/job_name")


    def test_QueueStatusPortletService(self):
        config = dict()
        config['env'] = "test_env"
        config['job_name'] = 'queue_job_name'
        config['job_repository'] = 'tre-jenkins'
        queueStatusPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.QueueStatusPortletService")
        envPortlet = PortletAssignment(portlet=queueStatusPortlet, config=config)
        service = portlet_services.QueueStatusPortletService(envPortlet)

        service.alexandria_services = MagicMock()
        service.alexandria_services.get_job_status = MagicMock(return_value="SUCCESS")
        service.execute()

        self.assertEqual(service.link, SFLY_TRE_JENKINS + "/job/queue_job_name")
        self.assertEqual(service.queue_status.status['description'], "Test Job Queue: Enabled")

        service.alexandria_services.get_job_status = MagicMock(return_value="FAILED")
        service.execute()

        self.assertEqual(service.queue_status.status['description'], "Test Job Queue: Disabled")

    def test_EnvStatusPortletService(self):
        config = dict()
        config['env'] = "test_env"
        job = {
            "job_description": "job_description",
            'view_name': "view_name",
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Test',
                    'job_repository': "tre-jenkins",
                },
                {
                    'job_name': 'Env_Availability_Check-Test',
                    'job_repository': "tre-jenkins",
                },
            ]
        }
        config["job"] = job
        envStatusPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.EnvStatusPortletService")
        envPortlet = PortletAssignment(portlet=envStatusPortlet, config=config)
        service = portlet_services.EnvStatusPortletService(envPortlet)

        service.alexandria_services = MagicMock()
        service.alexandria_services.get_job_status = MagicMock(return_value="SUCCESS")
        service.execute()

        self.assertEqual(service.env, "test_env")
        self.assertEqual(service.status_dict['description'], "job_description")
        self.assertEqual(service.status_dict['status'].status['description'], "All OK")

        failure_test_result = \
            [
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
        service.alexandria_services.get_job_status = MagicMock(return_value="FAILED")
        service.alexandria_services.get_last_job_test_result_failures = MagicMock(
            return_value=failure_test_result)
        service.execute()

        self.assertEqual(service.env, "test_env")
        self.assertEqual(len(service.status_dict['failure_job_list']), 2)
        self.assertEqual(len(service.status_dict['env_status_failure_job_list']), 2)
        self.assertEqual(service.status_dict['status'].status['description'], "Critical failures detected; testing may be impeded")
        failure_job = service.status_dict['env_status_failure_job_list'][0]
        failure_test_list = failure_job['env_status_failure_test_list']
        self.assertEqual(failure_job['link'], SFLY_TRE_JENKINS + "/job/Env_Health_Check-Test")
        self.assertEqual(failure_test_list[0]['test_result_description'], "pool-server")
        self.assertEqual(failure_test_list[0]['test_result_level_url'],
                         "http://job_repository/job/jobname/jobnumber/testReport/healthchecks.testify/AdminServerTest/")

    def test_ChangelistPortletService_With_Same_Version(self):
        config = dict()
        config['env'] = "foxtrot"
        changelistStatusPortlet = Portlet(serviceClass="env_health_dashboard.portlet_services.ChangelistPortletService")
        envPortlet = PortletAssignment(portlet=changelistStatusPortlet, config=config)
        service = portlet_services.ChangelistPortletService(envPortlet)

        test_env_list = {
            "pool_1": [
                {
                    "host": "host_1_of_pool_1.com"
                },
                {
                    "host": "host_2_of_pool_1.com"
                },

            ],
            "pool_2": [
                {
                    "host": "host_1_of_pool_2.com"
                },
                {
                    "host": "host_2_of_pool_2.com"
                },
            ]
        }
        service.ackbar_service = MagicMock()
        service.ackbar_service.get_server_list_from_env = MagicMock(return_value=test_env_list)
        mocked_version_service = VersionService(test_env_list)
        mocked_version_service._get_url_content = MagicMock(return_value="test_key")
        service._get_version_service = MagicMock(return_value=mocked_version_service)
        service.execute()

        self.assertEqual(len(service.pool_server_version_dict), 1)
        self.assertEqual(service.pool_server_version_dict["test_key"], {'pools': ' pool_2, pool_1', 'hosts': ''})

    def test_ChangelistPortletService_With_Unknown_Version(self):
        config = dict()
        config['env'] = "foxtrot"
        changelistStatusPortlet = Portlet(serviceClass="env_health_dashboard.portlet_services.ChangelistPortletService")
        envPortlet = PortletAssignment(portlet=changelistStatusPortlet, config=config)
        service = portlet_services.ChangelistPortletService(envPortlet)

        test_env_list = {
            "pool_1": [
                {
                    "host": "host_1_of_pool_1.com"
                },
                {
                    "host": "host_2_of_pool_1.com"
                },
            ],
            "pool_2": [
                {
                    "host": "host_1_of_pool_2.com"
                },
                {
                    "host": "host_2_of_pool_2.com"
                },
            ]
        }
        service.ackbar_service = MagicMock()
        service.ackbar_service.get_server_list_from_env = MagicMock(return_value=test_env_list)
        mocked_version_service = VersionService(test_env_list)
        mocked_version_service._get_url_content = MagicMock(return_value="")
        service._get_version_service = MagicMock(return_value=mocked_version_service)
        service.execute()

        self.assertEqual(len(service.pool_server_version_dict), 1)
        self.assertEqual(service.pool_server_version_dict["unknown"], {'pools': ' pool_2, pool_1', 'hosts': ''})

    def test_ChangelistPortletService_With_Different_Version(self):
        config = dict()
        config['env'] = "foxtrot"
        changelistStatusPortlet = Portlet(serviceClass="env_health_dashboard.portlet_services.ChangelistPortletService")
        envPortlet = PortletAssignment(portlet=changelistStatusPortlet, config=config)
        service = portlet_services.ChangelistPortletService(envPortlet)

        test_env_list = {
            "pool_1": [
                {
                    "host": "host_1_of_pool_1.com"
                },
                {
                    "host": "host_2_of_pool_1.com"
                },

            ],
            "pool_2": [
                {
                    "host": "host_1_of_pool_2.com"
                },
                {
                    "host": "host_2_of_pool_2.com"
                },
            ]
        }
        service.ackbar_service = MagicMock()
        service.ackbar_service.get_server_list_from_env = MagicMock(return_value=test_env_list)
        server_version = {
            "key_1": "host1, host2",
            "key_2": "host3"
        }
        mocked_version_service = VersionService(test_env_list)
        mocked_version_service._get_server_version = MagicMock(return_value=server_version)
        service._get_version_service = MagicMock(return_value=mocked_version_service)
        service.execute()

        self.assertEqual(len(service.pool_server_version_dict), 2)
        self.assertEqual(service.pool_server_version_dict["key_1"], {'pools': '', 'hosts': ' host1, host1'})
        self.assertEqual(service.pool_server_version_dict["key_2"], {'pools': '', 'hosts': ' host3, host3'})

    def test_time_format(self):
        time_now = datetime(2015, 5, 13, 12, 30, 50)
        expect_time_string = "2015/05/13 12:30 (PDT)"
        rtn_time = portlet_services.format_time(time_now)
        self.assertEqual(str(rtn_time), expect_time_string)