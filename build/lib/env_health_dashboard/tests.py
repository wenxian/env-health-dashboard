import django

from django.test.utils import setup_test_environment
from django.test.client import Client
from jenkins_services import JenkinsService
from server_locations import *
from models import PortletAssignment, Portlet
import handler_services
import views
from mock import MagicMock
from env_health_dashboard import alexandria_services
from django.core.urlresolvers import resolve
from datetime import datetime
from dateutil import tz
import portlet_services


class FunctionalTests(django.test.testcases.TestCase):

    def setUp(self):
        setup_test_environment()
        self.client = Client()

    def test_homepage_is_accessible(self):
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)

    def test_self_test_page(self):
        response = self.client.get('/env/sfly.self_test')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            text="Test Skinny Portlet",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Test Wide Portlet",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Delay Portlet Skinny",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Delay Portlet Wide",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="The content of this portlet",
                            count=2,
                            status_code=200)
        self.assertContains(response,
                            text="more content",
                            count=1,
                            status_code=200)

    def test_self_foxtrot_page_other_links_portlet(self):
        response = self.client.get('/env/sfly.foxtrot')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            text="Other Links",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Foxtrot Ignite Page",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Foxtrot Load Tests",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Recently Closed Env Tickets",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Foxtrot Deployment Pipeline",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Foxtrot App Pool Memory Usage",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Foxtrot WS Pool Memory Usage",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="Foxtrot API Pool Memory Usage",
                            count=1,
                            status_code=200)

    def test_self_foxtrot_page_jira_portlet(self):
        response = self.client.get('/env/sfly.foxtrot')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            text="Foxtrot Environment Tickets",
                            count=1,
                            status_code=200)

    def test_self_foxtrot_page_changelist_portlet(self):
        response = self.client.get('/env/sfly.foxtrot')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            text="Deployed Version",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="<b>Branch</b>",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="<b>Version</b>",
                            count=1,
                            status_code=200)
        self.assertContains(response,
                            text="<b>Change List</b>",
                            count=1,
                            status_code=200)

    def test_self_foxtrot_page_next_deployment_portlet(self):
        response = self.client.get('/env/sfly.foxtrot')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            text="Next scheduled deployment",
                            count=1,
                            status_code=200)

    def test_self_foxtrot_page_site_status_portlet(self):
        response = self.client.get('/env/sfly.foxtrot')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            text="Foxtrot Site Status",
                            count=1,
                            status_code=200)


class JenkinsServiceTests(django.test.testcases.TestCase):

    def setUp(self):
        self.jenkins = JenkinsService(SFLY_CHINA_JENKINS)

    def test_cron_schedule_grabbed_is_correct(self):
        conf_content = """
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <logRotator>
    <daysToKeep>7</daysToKeep>
    <numToKeep>-1</numToKeep>
    <artifactDaysToKeep>-1</artifactDaysToKeep>
    <artifactNumToKeep>-1</artifactNumToKeep>
  </logRotator>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>BRANCH</name>
          <description></description>
          <defaultValue>main</defaultValue>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <jdk>(Default)</jdk>
  <triggers class="vector">
    <hudson.triggers.TimerTrigger>
      <spec>0 20 * * 1-5</spec>
    </hudson.triggers.TimerTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>set -e

CLIST=`curl -s --globoff --url &quot;http://china.stage.shutterfly.com \
:2010/job/6--main_artifacts_upload/lastStableBuild/api/xml?xpath=/*/ \
action/parameter[name=%27CLIST%27]/value/text%28%29&quot;` || exit 1
VERSION=`curl -s --globoff --url &quot;http://china.stage.shutterfly.com \
:2010/job/6--main_artifacts_upload/lastStableBuild/api/xml?xpath=/*/ \
action/parameter%5Bname=%27VERSION%27%5D/value/text%28%29&quot;`|| exit 1

echo &quot;CLIST=$CLIST&quot;&gt; ${WORKSPACE}/CLIST
echo &quot;VERSION=$VERSION&quot;&gt;&gt; ${WORKSPACE}/CLIST
echo &quot;BRANCH=$BRANCH&quot; &gt;&gt; ${WORKSPACE}/CLIST</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.plugins.parameterizedtrigger.BuildTrigger>
      <configs>
        <hudson.plugins.parameterizedtrigger.BuildTriggerConfig>
          <configs>
            <hudson.plugins.parameterizedtrigger.FileBuildParameters>
              <propertiesFile>${WORKSPACE}/CLIST</propertiesFile>
            </hudson.plugins.parameterizedtrigger.FileBuildParameters>
          </configs>
          <projects>1--main_foxtrot_servers, </projects>
          <condition>SUCCESS</condition>
          <triggerWithNoParameters>false</triggerWithNoParameters>
        </hudson.plugins.parameterizedtrigger.BuildTriggerConfig>
      </configs>
    </hudson.plugins.parameterizedtrigger.BuildTrigger>
  </publishers>
  <buildWrappers/>
</project>
"""
        expect = "0 20 * * 1-5"
        generate = self.jenkins.grab_cron_time(conf_content)
        self.assertEqual(expect, generate)

    def test_next_cron_build_is_correct(self):
        schedule = "0 20 * * 1-5"
        generate_date = self.jenkins.get_next_time(schedule)
        expect_hour = 20
        expect_minute = 0
        expect_second = 0
        self.assertEqual(expect_hour, generate_date.hour)
        self.assertEqual(expect_minute, generate_date.minute)
        self.assertEqual(expect_second, generate_date.second)

    def test_changelist_parameters_os_correct(self):
        items_list = []
        parameters = list()
        parameters.append(self.generate_dict("REL", "main"))
        parameters.append(self.generate_dict("SITE", "foxtrot"))
        parameters.append(self.generate_dict("P4ROOT",
                          "/home/distro/jenkins-slave/workspace/1--main_foxtrot_servers"))
        parameters.append(self.generate_dict("BRANCH", "main"))
        parameters.append(self.generate_dict("VERSION",
                          "main-423168-20131218-181312"))
        parameters.append(self.generate_dict("CLIST", "423168"))
        tuple = 'parameters', parameters
        items_list.append(tuple)
        generate = self.jenkins.get_changelist_dict_from_items(items_list)
        expect_branch = "main"
        expect_version = "main-423168-20131218-181312"
        expect_clist = "423168"
        self.assertEqual(expect_branch, generate["branch"])
        self.assertEqual(expect_version, generate["version"])
        self.assertEqual(expect_clist, generate["cl"])

    def generate_dict(self, name, value):
        test_dict = dict()
        test_dict['name'] = name
        test_dict['value'] = value
        return test_dict

    def test_get_last_build_timestamp(self):
        self.jenkins.get_last_build_timestamp = MagicMock(return_value="timestamp")
        rtn_timestamp = self.jenkins.get_last_build_timestamp("test_job")
        self.assertEqual(rtn_timestamp, "timestamp")


class ViewTests(django.test.testcases.TestCase):

    def setUp(self):
        setup_test_environment()
        self.client = Client()

    def test_multiprocess(self):
        delayPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.DelayPortletService")
        envPortlet = [
            PortletAssignment(title="Delay Portlet One",
                              portlet=delayPortlet,
                              config=0),
            PortletAssignment(title="Delay Portlet Two",
                              portlet=delayPortlet,
                              config=1)
        ]
        services = views.initialize_services(envPortlet)
        self.assertEqual(services[0].title, "Delay Portlet One")
        self.assertEqual(services[1].title, "Delay Portlet Two")
        self.assertEqual(services[0].error, "")
        self.assertEqual(services[1].error, "")

    def test_multiprocess_with_timeout_erro(self):
        delayPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.DelayPortletService")
        envPortlet = [
            PortletAssignment(title="Delay Portlet One",
                              portlet=delayPortlet,
                              config=0),
            PortletAssignment(title="Delay Portlet With Error",
                              portlet=delayPortlet,
                              config=6)
        ]
        services = views.initialize_services(envPortlet)
        self.assertEqual(services[0].title, "Delay Portlet One")
        self.assertEqual(services[1].title, "Delay Portlet With Error")
        self.assertEqual(services[0].error, "")
        errorPosition = services[1].error.find("An exception has occurred:")
        self.assertNotEquals(-1, errorPosition)


class HandlerServiceTests(django.test.testcases.TestCase):

    def test_get_correct_env_status(self):
        foxtrot_config = dict()
        foxtrot_config['job_name'] = "job_name_test"
        foxtrot_config['job_repository'] = "job_repository_test"
        alexandria_services.get_site_status = MagicMock(return_value="SUCCESS")
        status_foxtrot = handler_services._get_status_from_env_config("foxtrot", foxtrot_config)
        self.assertEqual(status_foxtrot, "UP")

    def test_get_env_site_status_list_without_exception(self):
        env_list = ['env_test1', 'env_test2']
        handler_services._get_status_from_env_config = MagicMock(return_value="UP")
        env_status_list = handler_services._get_env_site_status_list(env_list)
        self.assertEqual(len(env_status_list), 2)
        for each_status in env_status_list:
            self.assertEqual(each_status['status']['description'], "All Ok")

    def test_get_env_site_status_list_with_exception(self):
        env_list = ['env_test1', 'env_test2']
        handler_services._get_status_from_env_config = MagicMock(side_effect=Exception('Exception!'))
        env_status_list = handler_services._get_env_site_status_list(env_list)
        self.assertEqual(len(env_status_list), 2)
        for each_status in env_status_list:
            self.assertEqual(each_status['status']['description'], 'Failed to get status')


class AlexandriaServicesTests(django.test.testcases.TestCase):

    def test_get_job_status(self):
        alexandria_services.get_url_content = MagicMock(return_value="SUCCESS")

        content = alexandria_services.get_site_status("job_name_test", "job_repository_test")

        alexandria_services.get_url_content.assert_called_with("http://test-results.internal.shutterfly.com/job/status?job_name=job_name_test&job_repository=job_repository_test")

        self.assertEqual(content, "SUCCESS")


class UrlHandlerTest(django.test.testcases.TestCase):

    def test_index_url_correct(self):
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'index')

    def test_env_url_correct(self):
        resolver = resolve('/env/sfly.foxtrot')
        self.assertEqual(resolver.view_name, 'env_handler')

        resolver = resolve('/env/tp.beta')
        self.assertEqual(resolver.view_name, 'env_handler')

    def test_env_url_incorrect(self):
        response = self.client.get('/env')
        self.assertEqual(404, response.status_code)

        response = self.client.get('/env/sfly.foxtrot/otherpending')
        self.assertEqual(404, response.status_code)

        response = self.client.get('/env/unknownbrand.foxtrot')
        self.assertEqual(404, response.status_code)

    def test_env_brand_correct(self):
        resolver = resolve('/brand/sfly')
        self.assertEqual(resolver.view_name, 'brand_handler')

        resolver = resolve('/brand/tp')
        self.assertEqual(resolver.view_name, 'brand_handler')

        resolver = resolve('/brand')
        self.assertEqual(resolver.view_name, 'brand_handler')

    def test_env_url_incorrect(self):
        response = self.client.get('/brand/unknown')
        self.assertEqual(404, response.status_code)


class PortletServiceTest(django.test.testcases.TestCase):

    def test_LastDeployTimePortletService(self):
        config = dict()
        config["server"] = "{SFLY_CHINA_JENKINS}"
        nextDeployTimePortlet = Portlet(serviceClass="env_health_dashboard.portlet_services.NextDeployTimePortletService")
        envPortlet = PortletAssignment(title="Next scheduled deployment", portlet=nextDeployTimePortlet, config=config)
        service = portlet_services.LastDeployTimePortletService(envPortlet)
        date_object_utc = datetime.strptime("2014-03-19 22:27:46", "%Y-%m-%d %H:%M:%S")
        utc_object = date_object_utc.replace(tzinfo=tz.tzutc())

        mocked_jenkins = MagicMock()
        portlet_services._get_jenkins = MagicMock(return_value=mocked_jenkins)
        mocked_jenkins.get_last_build_timestamp = MagicMock(return_value=utc_object)
        service.execute()

        portlet_services._get_jenkins.assert_called_with(SFLY_CHINA_JENKINS)
        mocked_jenkins.get_last_build_timestamp.assert_called_with(portlet_services.FOXTROT_CHANGELIST_JOB_NAME)
        self.assertEqual(service.textContent, "2014-03-19 15:27 (PDT)")














