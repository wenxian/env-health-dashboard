from abc import ABCMeta
from urllib import quote

from jira.client import JIRA
from dateutil import parser
from dateutil import tz
from django.conf import settings

from server_locations import *
from jenkins_services import JenkinsService
from environment_status import EnvironmentStatus
from job_list_status import JobListStatus
from alexandria_services import AlexandriaServices
from ackbar_service import AckbarService
from version_service import VersionService
from collections import OrderedDict


TIMEZONE = tz.tzlocal()


def _convert_timestamp_from_utc(utc_time):
    convert = utc_time.astimezone(TIMEZONE)
    return convert


def _format_time(time):
    TIME_FORMAT = "%Y-%m-%d %H:%M (%Z)"
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
            ticket['key'] = str(issue.key)
            ticket['link'] = server + "/browse/" + issue.key
            ticket['date_object'] = _format_time(parser.parse(issue.fields.created))
            ticket['summary'] = str(issue.fields.summary)
            tickets.append(ticket)
        return tickets


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
        nextbuild_local = _format_time(nextbuild_local)
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
        lastbuild_local = _format_time(lastbuild_local)
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
        self._set_failure_job_list()
        self.status_dict = self.get_status()

    def _set_failure_job_list(self):
        try:
            job_filter = JobsFilter(self.job['job_config_list'], self.alexandria_services)
            self.failure_job_list = job_filter.get_failure_jobs_list()
        except Exception as ex:
            self.exception = Exception("Not Reachable")

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

    def get_status(self):
        self.env_status = EnvironmentStatus(self.env, self.failure_job_list, self.exception)
        self.env_status.determine_env_status()
        status_dict = {
            'status': self.env_status,
            'description': self.job['job_description'],
            'failure_job_list': self.failure_job_list,
            'link': self.job['link'],
        }
        return status_dict


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
            'job_status': self._get_job_status_check(env)
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

    def _get_job_status_config_list_from_env(self, env):
        return self.jobs[env]['job_status']

    def _get_job_status_check(self, env):
        failure_job_list = []
        exception = None
        try:
            env_config_list = self._get_job_status_config_list_from_env(env)
            job_filter = JobsFilter(env_config_list, self.alexandria_services)
            failure_job_list = job_filter.get_failure_jobs_list()
        except Exception as ex:
            exception = Exception("Not Implemented")
        job_status = JobListStatus(failure_job_list, exception)
        job_status.determine_job_status()
        return job_status


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
        self.failure_jobs.append(env_config)