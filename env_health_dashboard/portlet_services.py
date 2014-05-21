from abc import ABCMeta
from urllib import quote

from jira.client import JIRA
from dateutil import parser
from dateutil import tz
from django.conf import settings

import server_locations
from server_locations import *
from jenkins_services import JenkinsService
from environment_status import EnvironmentStatus
from job_list_status import JobListStatus
from alexandria_services import AlexandriaServices
from ackbar_service import AckbarService
from version_service import VersionService
from collections import OrderedDict
from queue_status import QueueStatus


TIMEZONE = tz.tzlocal()


def _convert_timestamp_from_utc(utc_time):
    convert = utc_time.astimezone(TIMEZONE)
    return convert


def format_time(time):
    TIME_FORMAT = "%Y/%m/%d %H:%M (%Z)"
    return time.replace(tzinfo=TIMEZONE).strftime(TIME_FORMAT)


def _get_jenkins(server):
    return JenkinsService(server)


class PortletService():
    __metaclass__ = ABCMeta

    def __init__(self, envPortlet, template):
        self.envPortlet = envPortlet
        self.title = envPortlet.title
        self.viewTemplate = template
        self.error = ""

    def set_error(self, error):
        self.error = error


class TextPortletService(PortletService):

    def __init__(self, envPortlet):
        super(TextPortletService, self).__init__(
            envPortlet, "env_health_dashboard/text_portlet.html")

    def execute(self):
        self.textContent = self.envPortlet.config


class QuickLinkPortletService(PortletService):

    def __init__(self, envPortlet):
        super(QuickLinkPortletService, self).__init__(
            envPortlet, "env_health_dashboard/quick_link_template.html")

    def execute(self):
        self.link_list = self.envPortlet.config['link_list']


class DelayPortletService(PortletService):

    def __init__(self, envPortlet):
        super(DelayPortletService, self).__init__(
            envPortlet, "env_health_dashboard/text_portlet.html")
        self.delay = int(self.envPortlet.config)

    def execute(self):
        import time
        from datetime import datetime
        time.sleep(self.delay)
        self.textContent = "Delayed for " + str(self.delay) + \
                           " seconds -- current time " + str(datetime.now())


class JiraPortletService(PortletService):

    def __init__(self, envPortlet):
        super(JiraPortletService, self).__init__(
            envPortlet, "env_health_dashboard/jira_view_template.html")

    def execute(self):
        self.options = dict()
        self.options["server"] = self.envPortlet.config["server"]\
            .format(SFLY_JIRA=SFLY_JIRA)
        self.query = self.envPortlet.config["query"]
        self.columns = self.envPortlet.config["columns"]
        self.jira = JIRA(self.options)
        self.tickets = self.get_tickets()
        self.footlink = self.get_foot_link()

    def get_foot_link(self):
        base = self.options["server"]
        url = base + "/issues/?jql=" + self.query
        safeurl = quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        return safeurl

    def get_tickets(self):
        server = self.options["server"]
        issues = self.jira.search_issues(self.query)
        tickets = []

        for issue in issues:
            ticket = dict()
            ticket['key'] = issue.key
            ticket['link'] = server + "/browse/" + issue.key
            columns_value_list = []
            for column in self.columns:
                columns_value_list.append(self._get_field_value_with_key(column, issue))
            ticket['columns_value_list'] = columns_value_list
            tickets.append(ticket)
        return tickets

    def _get_field_value_with_key(self, key, issue):
        field_key_attribute = {
            'status': "status",
            'issue type': "issuetype",
            'priority': "priority",
            'summary': "summary",
            'reporter': "reporter",
            'assignee': "assignee",
            'creation time': "created",
            'last update time': "updated",
            'resolution': "resolution",
        }
        attribute_name = field_key_attribute[key]

        value = getattr(issue.fields, attribute_name)
        value = self._encode_value(value)
        value = self._format_time_value_if_have(key, value)
        return value

    def _encode_value(self, value):
        try:
            value = str(value)
        except:
            value = value
        return value

    def _format_time_value_if_have(self, key, value):
        if key.find('time') != -1:
            value = format_time(parser.parse(value))
        return value


class NextDeployTimePortletService(PortletService):

    def __init__(self, envPortlet):
        super(NextDeployTimePortletService, self).__init__(
            envPortlet, "env_health_dashboard/text_portlet.html")

    def execute(self):
        self.jobname = self.envPortlet.config['jobname']
        self.server = self.envPortlet.config['server']\
            .format(SFLY_CHINA_JENKINS=SFLY_CHINA_JENKINS)
        jenkins = _get_jenkins(self.server)
        nextbuild_local = jenkins.get_job_next_scheduled_build(self.jobname)
        nextbuild_local = format_time(nextbuild_local)
        self.textContent = nextbuild_local


class LastDeployTimePortletService(PortletService):

    def __init__(self, envPortlet):
        super(LastDeployTimePortletService, self).__init__(
            envPortlet, "env_health_dashboard/text_portlet.html")

    def execute(self):
        self.jobname = self.envPortlet.config['jobname']
        self.server = self.envPortlet.config['server'] \
            .format(SFLY_CHINA_JENKINS=SFLY_CHINA_JENKINS)
        jenkins = _get_jenkins(self.server)
        lastbuild_utc = jenkins.get_last_build_timestamp(self.jobname)
        lastbuild_local = _convert_timestamp_from_utc(lastbuild_utc)
        lastbuild_local = format_time(lastbuild_local)
        self.textContent = lastbuild_local


class ChangelistPortletService(PortletService):

    def __init__(self, envPortlet):
        super(ChangelistPortletService, self).__init__(
            envPortlet, "env_health_dashboard/changelist_view_template.html")
        self.ackbar_service = AckbarService()

    def execute(self):
        self.env = self.envPortlet.config['env']
        server_list = self.ackbar_service.get_server_list_from_env(self.env)
        version_service = self._get_version_service(server_list)
        version_service.get_pool_list_version()
        pool_server_version_dict = version_service.server_pool_version
        self.pool_server_version_dict = OrderedDict(sorted(pool_server_version_dict.items(), key=lambda t: t[0]))

    def _get_version_service(self, server_list):
        return VersionService(server_list)


class JobStatusPortletService(PortletService):

    def __init__(self, envPortlet):
        super(JobStatusPortletService, self).__init__(
            envPortlet, "env_health_dashboard/job_status_template.html")
        self.alexandria_services = AlexandriaServices(ALEXANDRIA_SERVER)

    def execute(self):
        self.env = self.envPortlet.config['env']
        self.job = self.envPortlet.config['job']
        self.failure_job_list = []
        self.exception = None
        self._set_view_or_job_link()
        self._set_failure_job_list()
        self.status_dict = self.get_status()

    def _set_failure_job_list(self):
        try:
            job_filter = JobsFilter(self.job['job_config_list'], self.alexandria_services)
            self.failure_job_list = job_filter.get_failure_jobs_list()
        except Exception as ex:
            self.exception = Exception("Not Reachable")

    def _set_view_or_job_link(self):
        job_repository = self.job['job_repository']
        path_appender = ""
        if "view_name" in self.job:
            path_appender = "/view/%s" % self.job['view_name']
        elif "job_name" in self.job:
            path_appender = "/job/%s" % self.job['job_name']
        path_server = server_locations.get_server(job_repository)
        self.job['link'] = path_server + path_appender

    def get_status(self):
        self.job_status = JobListStatus(self.failure_job_list, self.exception)
        self.job_status.determine_job_status()
        status_dict = {
            'status': self.job_status,
            'description': self.job['job_description'],
            'failure_job_list': self.failure_job_list,
            'link': self.job['link'],
        }
        return status_dict


class EnvStatusPortletService(JobStatusPortletService):

    def __init__(self, envPortlet):
        super(JobStatusPortletService, self).__init__(
            envPortlet, "env_health_dashboard/env_health_template.html")
        self.alexandria_services = AlexandriaServices(ALEXANDRIA_SERVER)

    def get_status(self):
        self.env_status = EnvironmentStatus(self.env, self.failure_job_list, self.exception)
        self.env_status.determine_env_status()
        self.set_env_health_failure_job_list()
        status_dict = {
            'status': self.env_status,
            'description': self.job['job_description'],
            'failure_job_list': self.failure_job_list,
            'env_status_failure_job_list': self.env_status_failure_job_list,
            'link': self.job['link'],
        }
        return status_dict

    def _get_test_result_failure_dict(self, test_result):
        test_result_dict = dict()
        test_name_split_list = test_result['test_name'].split("--")
        test_result_description = str(test_name_split_list[1]) + "-" + str(test_name_split_list[2])
        url = test_result['url']
        test_result_level_url = url[0:url.rfind("/") + 1]
        test_result_dict['test_result_description'] = test_result_description
        test_result_dict['test_result_level_url'] = test_result_level_url
        return test_result_dict

    def set_env_health_failure_job_list(self):
        self.env_status_failure_job_list = []
        for failure_job in self.failure_job_list:
            self._add_into_env_status_failure_job_list(failure_job)

    def _add_into_env_status_failure_job_list(self, failure_job):
        job_failure_tests = failure_job['failure_test_results']
        env_health_failure_test_list = []
        for test_result in job_failure_tests:
            env_health_failure_test_list.append(self._get_test_result_failure_dict(test_result))
        failure_job['env_status_failure_test_list'] = env_health_failure_test_list
        self.env_status_failure_job_list.append(failure_job)


class QueueStatusPortletService(PortletService):

    def __init__(self, envPortlet):
        super(QueueStatusPortletService, self).__init__(
            envPortlet, "env_health_dashboard/queue_status_template.html")
        self.alexandria_services = AlexandriaServices(ALEXANDRIA_SERVER)

    def execute(self):
        self.env = self.envPortlet.config['env']
        self.job_name = self.envPortlet.config['job_name']
        self.job_repository = self.envPortlet.config['job_repository']
        self.link = "%s/job/%s" % (server_locations.get_server(self.job_repository), self.job_name)
        self.queue_status = self._get_queue_status()
        self.queue_status.determine_queue_status()

    def _get_queue_status(self):
        job_status = ""
        exception = None
        try:
            job_status = self.alexandria_services.get_job_status(self.job_name, self.job_repository)
        except Exception as ex:
            self.exception = Exception("Not Reachable")
        return QueueStatus(job_status, exception)


class BrandPortletService(PortletService):

    def __init__(self, envPortlet):
        super(BrandPortletService, self).__init__(
            envPortlet, "env_health_dashboard/brand_status.html")
        self.alexandria_services = AlexandriaServices(ALEXANDRIA_SERVER)

    def execute(self):
        self.brand = self.envPortlet.config['brand']
        self.jobs = self.envPortlet.config['jobs']
        self.env_list = settings.ENV[self.brand]
        self.env_check_list = []
        self._add_each_env_check()

    def _add_each_env_check(self):
        for env in self.env_list:
            self._add_check_into_env_check_list(env)

    def _add_check_into_env_check_list(self, env):
        env_check_dict = {
            'env': env,
            'env_status': self._get_env_status_check(env),
            'job_status': self._get_job_status_check(env, 'job_status'),
            'web_sanity': self._get_job_status_check(env, 'web_sanity'),
            'test_job_queue': self._get_queue_status_check(env)
        }
        self.env_check_list.append(env_check_dict)

    def _get_env_status_config_list_from_env(self, env):
        return self.jobs[env]['env_status']

    def _get_env_status_check(self, env):
        failure_job_list = []
        exception = None
        try:
            env_config_list = self._get_env_status_config_list_from_env(env)
            job_filter = JobsFilter(env_config_list, self.alexandria_services)
            failure_job_list = job_filter.get_failure_jobs_list()
        except Exception as ex:
            exception = Exception("Not Implemented")
        env_status = EnvironmentStatus(env, failure_job_list, exception)
        env_status.determine_env_status()
        return env_status

    def _get_job_status_config_list_from_env(self, env, key):
        return self.jobs[env][key]

    def _get_job_status_check(self, env, key):
        failure_job_list = []
        exception = None
        try:
            env_config_list = self._get_job_status_config_list_from_env(env, key)
            job_filter = JobsFilter(env_config_list, self.alexandria_services)
            failure_job_list = job_filter.get_failure_jobs_list()
        except Exception as ex:
            exception = Exception("Not Implemented")
        job_status = JobListStatus(failure_job_list, exception)
        job_status.determine_job_status()
        return job_status

    def _get_queue_status_config_list_from_env(self, env):
        return self.jobs[env]['test_job_queue']

    def _get_queue_status_check(self, env):
        exception = None
        status = ''
        try:
            env_config = self._get_queue_status_config_list_from_env(env)
            status = self.alexandria_services.get_job_status(env_config['job_name'], env_config['job_repository'])
        except Exception as ex:
            exception = Exception("Not Implemented")
        queue_status = QueueStatus(status, exception)
        queue_status.determine_queue_status()
        return queue_status


class JobsFilter():

    def __init__(self, jobs_env_config_list, alexandria_services):
        self.alexandria_services = alexandria_services
        self.jobs_env_config_list = jobs_env_config_list
        self.failure_jobs = []

    def get_failure_jobs_list(self):
        for env_config in self.jobs_env_config_list:
            self._filter_one_job_into_failure_job_list_if_failure(env_config)
        return self.failure_jobs

    def _filter_one_job_into_failure_job_list_if_failure(self, env_config):
        status = self.alexandria_services.get_job_status(
            env_config['job_name'], env_config['job_repository'])
        if status != "SUCCESS":
            self._add_failure_job(env_config)

    def _add_failure_job(self, env_config):
        failure_test_results = \
            self.alexandria_services.get_last_job_test_result_failures(
                env_config['job_name'], env_config['job_repository'])
        env_config['failure_test_results'] = failure_test_results
        env_config['link'] = self._build_job_link(env_config['job_name'], env_config['job_repository'])
        self.failure_jobs.append(env_config)

    def _build_job_link(self, job_name, job_repository):
        path_server = server_locations.get_server(job_repository)
        path_job = "/job/%s" % job_name
        return path_server + path_job
