import django
from django.test.utils import setup_test_environment
from env_health_dashboard.jenkins_services import JenkinsService
from env_health_dashboard.server_locations import *
from mock import MagicMock


class JenkinsServiceTests(django.test.testcases.TestCase):

    def setUp(self):
        self.jenkins = JenkinsService(SFLY_CHINA_JENKINS)

    def test_cron_schedule_grabbed_is_correct(self):
        conf_content = """<?xml version='1.0' encoding='UTF-8'?>
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
        expect_cron_content_list = ["0 20 * * 1-5"]
        generate_cron_content_list = self.jenkins.grab_cron_time(conf_content)
        self.assertEqual(expect_cron_content_list, generate_cron_content_list)

    def test_next_cron_build_is_correct(self):
        schedule_list = ["00 4 * * 1-5"]
        generate_date = self.jenkins.get_next_time(schedule_list)
        expect_hour = 4
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
                                             "/home/distro/jenkins-slave/workspace/"
                                             "1--main_foxtrot_servers"))
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
