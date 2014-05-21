from models import PortletAssignment, Portlet
from django.conf import settings


class PorletConfigurationService():

    def __init__(self):
        self.delayPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.DelayPortletService")
        self.jiraPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.JiraPortletService")
        self.nextDeployTimePortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.NextDeployTimePortletService")
        self.lastDeployTimePortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.LastDeployTimePortletService")
        self.changelistPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.ChangelistPortletService")
        self.textPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.TextPortletService")
        self.envStatusPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.EnvStatusPortletService")
        self.jobStatusPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.JobStatusPortletService")
        self.queueStatusPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.QueueStatusPortletService")
        self.brandPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.BrandPortletService")
        self.quickLinkPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.QuickLinkPortletService")

    def get_skinny_column_portlet_assignment_from_env(self, env):
        skinnyColumnPortletAssignments = []

        if env == 'self_test':
            skinnyColumnPortletAssignments = self._get_self_test_skinny_portlet_assignments(env)
        elif env == 'beta':
            skinnyColumnPortletAssignments = self._get_beta_skinny_portlet_assignments(env)
        elif env == 'foxtrot':
            skinnyColumnPortletAssignments = self._get_foxtrot_skinny_portlet_assignments(env)
        elif env == 'stage':
            skinnyColumnPortletAssignments = self._get_stage_skinny_portlet_assignments(env)
        elif env == 'dev':
            skinnyColumnPortletAssignments = self._get_dev_skinny_portlet_assignments(env)
        elif env == 'int':
            skinnyColumnPortletAssignments = self._get_int_skinny_portlet_assignments(env)

        return skinnyColumnPortletAssignments

    def get_wide_column_portlet_assignment_from_env(self, env):
        wideColumnPortletAssignments = []

        if env == 'self_test':
            wideColumnPortletAssignments = self._get_self_test_wide_portlet_assignments(env)
        elif env == 'beta':
            wideColumnPortletAssignments = self._get_beta_wide_portlet_assignments(env)
        elif env == 'foxtrot':
            wideColumnPortletAssignments = self._get_foxtrot_wide_portlet_assignments(env)
        elif env == 'stage':
            wideColumnPortletAssignments = self._get_stage_wide_portlet_assignments(env)
        elif env == 'dev':
            wideColumnPortletAssignments = self._get_dev_wide_portlet_assignments(env)
        elif env == 'int':
            wideColumnPortletAssignments = self._get_int_wide_portlet_assignments(env)

        return wideColumnPortletAssignments

    def get_brand_page_portlet_assignments(self, brand):
        config = dict()
        config['brand'] = brand
        config['jobs'] = {
            'dev': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Dev',
                        'job_repository': "tre-jenkins",
                    },
                    {
                        'job_name': 'Env_Availability_Check-Dev',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ],
                'web_sanity': [
                    {
                        'job_name': 'Web_Functional_Tests-Dev',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'test_job_queue': {
                    'job_name': '',
                    'job_repository': '',
                },
            },
            'int': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Int',
                        'job_repository': "tre-jenkins",
                    },
                    {
                        'job_name': 'Env_Availability_Check-Int',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ],
                'web_sanity': [
                    {
                        'job_name': 'Web_Functional_Tests-Int2',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'test_job_queue': {
                    'job_name': '',
                    'job_repository': '',
                },
            },
            'beta': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Beta',
                        'job_repository': "tre-jenkins",
                    },
                    {
                        'job_name': 'Env_Availability_Check-Beta',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ],
                'web_sanity': [
                    {
                        'job_name': 'Web_Functional_Tests-Beta',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'test_job_queue': {
                    'job_name': 'TRE_TestQueueGatekeeper_Beta',
                    'job_repository': 'tre-jenkins',
                },
            },
            'foxtrot': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Foxtrot',
                        'job_repository': "tre-jenkins",
                    },
                    {
                        'job_name': 'Env_Availability_Check-Foxtrot',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': "1--main_foxtrot_servers",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "2--main_deploy_foxtrot",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "foxtrot-CP",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "foxtrot-SP",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "3--foxtrot_selenium_test",
                        "job_repository": "china",
                    },
                ],
                'web_sanity': [
                    {
                        'job_name': '3--foxtrot_selenium_test',
                        'job_repository': "china",
                    },
                    {
                        'job_name': 'Web_Functional_Tests-Foxtrot',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'test_job_queue': {
                    'job_name': 'TRE_TestQueueGatekeeper_Foxtrot',
                    'job_repository': "tre-jenkins",
                },
            },
            'stage': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Stage',
                        'job_repository': "tre-jenkins",
                    },
                    {
                        'job_name': 'Env_Availability_Check-Stage',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ],
                'web_sanity': [
                    {
                        'job_name': 'Web_Functional_Tests-Stage',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'test_job_queue': {
                    'job_name': 'TRE_TestQueueGatekeeper_Stage',
                    'job_repository': 'tre-jenkins',
                },
            },
        }

        return [PortletAssignment(portlet=self.brandPortlet,
                                  config=config),
                ]

    def _get_self_test_skinny_portlet_assignments(self, env):
        return [
            PortletAssignment(title="Test Skinny Portlet",
                              portlet=self.textPortlet,
                              config="The content of this portlet"),
            PortletAssignment(title="Delay Portlet Skinny",
                              portlet=self.delayPortlet,
                              config="1"),
        ]

    def _get_self_test_wide_portlet_assignments(self, env):
        return [
            PortletAssignment(title="Test Wide Portlet",
                              portlet=self.textPortlet,
                              config="The content of this portlet<br/> \
                              <b>more content</b><ol><li>one<li>two</ol>"),
            PortletAssignment(title="Delay Portlet Wide",
                              portlet=self.delayPortlet,
                              config="2"),
        ]

    def _get_beta_skinny_portlet_assignments(self, env):
        config_deploy = dict()
        config_deploy["jobname"] = "0--main_beta_changelist"
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_changelist = dict()
        config_changelist["env"] = env
        config_quicklink = dict()
        config_quicklink["link_list"] = [
            {
                "name": "Open Critical Jira Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20!=%20%22Environments%20-%20"
                        "preproduction%22%20AND%20issuetype%20=%20"
                        "Bug%20AND%20%22Environment%20Found%22%20=%20"
                        "Beta%20AND%20status%20in%20(Open,%20%22In%20"
                        "Progress%22,%20Reopened)%20AND%20priority%20"
                        "in%20(Critical,%20%22Non-Production%20Blocker"
                        "%22,%20%22Production%20Blocker%22)%20ORDER%20"
                        "BY%20created%20DESC",
            },
            {
                "name": "Recently Closed Critical ENV Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20ENV%20AND%20status%20"
                        "=%20Closed%20AND%20resolved%20>=%20-7d%20"
                        "AND%20%22Environment%20Found%22%20=%20Beta"
                        "%20AND%20priority%20in%20(Critical,%20%22"
                        "Non-Production%20Blocker%22,%20%22Production"
                        "%20Blocker%22)%20ORDER%20BY%20resolved%20DESC"
            },
            {
                "name": "Recently Closed NCP Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20%22Nonprod%20Change"
                        "%20Process%22%20AND%20status%20=%20Closed"
                        "%20AND%20%22Environments%20Affected%22%20=%20"
                        "beta%20AND%20resolutiondate%20>%20%22-7d%22"
            },
            {
                "name": "Web Page",
                "link": "http://www.beta.shutterfly.com/",
            },
            {
                "name": "Deployment Pipeline",
                "link": "http://build.stage.shutterfly.com:2010/view/main-beta",
            },
            {
                "name": "Wildcat Status",
                "link": "http://wildcat.stage.shutterfly.com/status/",
            },
            {
                "name": "Server List",
                "link": "http://serverlist.internal.shutterfly.com/serverlist.txt",
            },

        ]

        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Next scheduled deployment",
                                  portlet=self.nextDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Quick Links",
                                  portlet=self.quickLinkPortlet,
                                  config=config_quicklink),
                ]

    def _get_foxtrot_skinny_portlet_assignments(self, env):
        config_deploy = dict()
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_deploy["jobname"] = "0--main_foxtrot_changelist"
        config_changelist = dict()
        config_changelist["env"] = env
        config_quicklink = dict()
        config_quicklink["link_list"] = [
            {
                "name": "Ignite Page",
                "link": "https://ignite.shutterfly.com/groups/foxtrot-nonproduction-environment",
            },
            {
                "name": "Load Tests",
                "link": "http://tre-jenkins.internal.shutterfly.com:8080/view/Load%20Tests%20-%20foxtrot/",
            },
            {
                "name": "App Pool Memory Usage",
                "link": "http://tre-stats.internal.shutterfly.com/dashboard/#foxtrot - garbage collection - app",
            },
            {
                "name": "WS Pool Memory Usage",
                "link": "http://tre-stats.internal.shutterfly.com/dashboard/#foxtrot - garbage collection - ws",
            },
            {
                "name": "API Pool Memory Usage",
                "link": "http://tre-stats.internal.shutterfly.com/dashboard/#foxtrot - garbage collection - api",
            },
            {
                "name": "Open Critical Jira Tickets",
                "link": "https://bugs.tinyprints.com/issues/?jql="
                        "project%20!=%20%22Environments%20-%20preproduction"
                        "%22%20AND%20issuetype%20=%20Bug%20AND%20%22Environment%20"
                        "Found%22%20=%20Foxtrot%20AND%20status%20in%20(Open,%20%22"
                        "In%20Progress%22,%20Reopened)%20AND%20priority%20in%20"
                        "(Critical,%20%22Non-Production%20Blocker%22,%20%22"
                        "Production%20Blocker%22)%20ORDER%20BY%20created%20DESC",
            },
            {
                "name": "Recently Closed Critical ENV Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20ENV%20AND%20status%20"
                        "=%20Closed%20AND%20resolved%20>=%20-7d%20"
                        "AND%20%22Environment%20Found%22%20=%20Foxtrot"
                        "%20AND%20priority%20in%20(Critical,%20%22"
                        "Non-Production%20Blocker%22,%20%22Production"
                        "%20Blocker%22)%20ORDER%20BY%20resolved%20DESC"
            },
            {
                "name": "Recently Closed NCP Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20%22Nonprod%20Change"
                        "%20Process%22%20AND%20status%20=%20Closed"
                        "%20AND%20%22Environments%20Affected%22%20=%20"
                        "foxtrot%20AND%20resolutiondate%20>%20%22-7d%22"
            },
            {
                "name": "Web Page",
                "link": "http://www.foxtrot.shutterfly.com/",
            },
            {
                "name": "Deployment Pipeline",
                "link": "http://build.stage.shutterfly.com:2010/view/main-foxtrot",
            },
            {
                "name": "Wildcat Status",
                "link": "http://wildcat.stage.shutterfly.com/status/",
            },
            {
                "name": "Server List",
                "link": "http://serverlist.internal.shutterfly.com/serverlist.txt",
            },
        ]
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Next scheduled deployment",
                                  portlet=self.nextDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Quick Links",
                                  portlet=self.quickLinkPortlet,
                                  config=config_quicklink)]

    def _get_stage_skinny_portlet_assignments(self, env):
        config_deploy = dict()
        config_deploy["jobname"] = "0--main_stage_changelist"
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_changelist = dict()
        config_changelist["env"] = env
        config_quicklink = dict()
        config_quicklink["link_list"] = [
            {
                "name": "Patch Listing",
                "link": "http://wildcat.stage.shutterfly.com/patch",
            },
            {
                "name": "Software Deployments",
                "link": "http://china.stage.shutterfly.com:2010/view/Sfly%20Stage/job/PatchSfly-stage/",
            },
            {
                "name": "Open Critical Jira Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20!=%20%22Environments%20-%20"
                        "preproduction%22%20AND%20issuetype%20=%20"
                        "Bug%20AND%20%22Environment%20Found%22%20=%20"
                        "Staging%20AND%20status%20in%20(Open,%20%22"
                        "In%20Progress%22,%20Reopened)%20AND%20priority"
                        "%20in%20(Critical,%20%22Non-Production%20"
                        "Blocker%22,%20%22Production%20Blocker%22)"
                        "%20ORDER%20BY%20created%20DESC",
            },
            {
                "name": "Recently Closed Critical ENV Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20ENV%20AND%20status%20"
                        "=%20Closed%20AND%20resolved%20>=%20-7d%20"
                        "AND%20%22Environment%20Found%22%20=%20Staging"
                        "%20AND%20priority%20in%20(Critical,%20%22"
                        "Non-Production%20Blocker%22,%20%22Production"
                        "%20Blocker%22)%20ORDER%20BY%20resolved%20DESC"
            },
            {
                "name": "Recently Closed NCP Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20%22Nonprod%20Change"
                        "%20Process%22%20AND%20status%20=%20Closed"
                        "%20AND%20%22Environments%20Affected%22%20=%20"
                        "staging%20AND%20resolutiondate%20>%20%22-7d%22"
            },
            {
                "name": "Web Page",
                "link": "http://www.stage.shutterfly.com/",
            },
            {
                "name": "Wildcat Status",
                "link": "http://wildcat.stage.shutterfly.com/status/",
            },
            {
                "name": "Server List",
                "link": "http://serverlist.internal.shutterfly.com/serverlist.txt",
            },

        ]
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Next scheduled deployment",
                                  portlet=self.nextDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Quick Links",
                                  portlet=self.quickLinkPortlet,
                                  config=config_quicklink)
                ]

    def _get_dev_skinny_portlet_assignments(self, env):
        config_deploy = dict()
        config_deploy["jobname"] = "2--main_deploy_int1"
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_changelist = dict()
        config_changelist["env"] = env
        config_quicklink = dict()
        config_quicklink["link_list"] = [
            {
                "name": "Open Critical Jira Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20!=%20%22Environments%20"
                        "-%20preproduction%22%20AND%20issuetype"
                        "%20=%20Bug%20AND%20%22Environment%20"
                        "Found%22%20=%20Dev%20AND%20status%20"
                        "in%20(Open,%20%22In%20Progress%22,%20"
                        "Reopened)%20AND%20priority%20in%20(Critical,"
                        "%20%22Non-Production%20Blocker%22,"
                        "%20%22Production%20Blocker%22)%20"
                        "ORDER%20BY%20created%20DESC",
            },
            {
                "name": "Recently Closed Critical ENV Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20ENV%20AND%20status%20"
                        "=%20Closed%20AND%20resolved%20>=%20-7d%20"
                        "AND%20%22Environment%20Found%22%20=%20Dev"
                        "%20AND%20priority%20in%20(Critical,%20%22"
                        "Non-Production%20Blocker%22,%20%22Production"
                        "%20Blocker%22)%20ORDER%20BY%20resolved%20DESC"
            },
            {
                "name": "Recently Closed NCP Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20%22Nonprod%20Change"
                        "%20Process%22%20AND%20status%20=%20Closed"
                        "%20AND%20%22Environments%20Affected%22%20=%20"
                        "dev%20AND%20resolutiondate%20>%20%22-7d%22"
            },
            {
                "name": "Web Page",
                "link": "http://www.dev.shutterfly.com/",
            },
            {
                "name": "Deployment Pipeline",
                "link": "http://build.stage.shutterfly.com:2010/view/main-dev",
            },
            {
                "name": "Wildcat Status",
                "link": "http://wildcat.stage.shutterfly.com/status/",
            },
            {
                "name": "Server List",
                "link": "http://serverlist.internal.shutterfly.com/serverlist.txt",
            },
        ]
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Quick Links",
                                  portlet=self.quickLinkPortlet,
                                  config=config_quicklink)
                ]

    def _get_int_skinny_portlet_assignments(self, env):
        config_changelist = dict()
        config_changelist["env"] = env
        config_deploy = dict()
        config_deploy["jobname"] = "4--main_deploy_int2"
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_quicklink = dict()
        config_quicklink["link_list"] = [
            {
                "name": "Open Critical Jira Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                                            "jql=project%20!=%20%22Environments%20"
                                            "-%20preproduction%22%20AND%20issuetype"
                                            "%20=%20Bug%20AND%20%22Environment%20Found"
                                            "%22%20=%20%22Int%22%20AND%20status%20in%20"
                                            "(Open,%20%22In%20Progress%22,%20Reopened)"
                                            "%20AND%20priority%20in%20(Critical,%20%22"
                                            "Non-Production%20Blocker%22,%20%22Production"
                                            "%20Blocker%22)%20ORDER%20BY%20created%20DESC",
            },
            {
                "name": "Recently Closed Critical ENV Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20ENV%20AND%20status%20"
                        "=%20Closed%20AND%20resolved%20>=%20-7d%20"
                        "AND%20%22Environment%20Found%22%20=%20%22Int%22"
                        "%20AND%20priority%20in%20(Critical,%20%22"
                        "Non-Production%20Blocker%22,%20%22Production"
                        "%20Blocker%22)%20ORDER%20BY%20resolved%20DESC"
            },
            {
                "name": "Recently Closed NCP Tickets",
                "link": "https://bugs.tinyprints.com/issues/?"
                        "jql=project%20=%20%22Nonprod%20Change"
                        "%20Process%22%20AND%20status%20=%20Closed"
                        "%20AND%20%22Environments%20Affected%22%20=%20"
                        "%22Int%22%20AND%20resolutiondate%20>%20%22-7d%22"
            },
            {
                "name": "Web Page",
                "link": "http://www.int.shutterfly.com/",
            },
            {
                "name": "Deployment Pipeline",
                "link": "http://build.stage.shutterfly.com:2010/view/GREEN-MAIN/"
            },
            {
                "name": "Wildcat Status",
                "link": "http://wildcat.stage.shutterfly.com/status/"
            },
            {
                "name": "Server List",
                "link": "http://serverlist.internal.shutterfly.com/serverlist.txt",
            },
        ]
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Quick Links",
                                  portlet=self.quickLinkPortlet,
                                  config=config_quicklink)
                ]

    def _get_beta_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Beta AND ' \
            'status in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_env["columns"] = ["priority", "summary", "reporter", "assignee", "creation time", "last update time"]
        config_jira_ncp = dict()
        config_jira_ncp["server"] = "{SFLY_JIRA}"
        config_jira_ncp["query"] = \
            'project = "Nonprod Change Process" AND status != Closed AND "Environments Affected" = beta ORDER BY status DESC'
        config_jira_ncp["columns"] = ["summary", "reporter", "assignee", "creation time", "last update time"]
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Host/Pool Status",
            'job_name': 'Env_Health_Check-Beta',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Beta',
                    'job_repository': "tre-jenkins",
                },
                {
                    'job_name': 'Env_Availability_Check-Beta',
                    'job_repository': "tre-jenkins",
                },

            ],
        }
        config_site_status['job'] = env_health_check_job
        config_web_sanity = dict()
        config_web_sanity['env'] = env
        config_web_sanity_job = {
            'job_description': "Web Sanity Status",
            'job_name': "Web_Functional_Tests-Beta",
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Web_Functional_Tests-Beta',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_web_sanity['job'] = config_web_sanity_job
        config_queue_status = dict()
        config_queue_status['env'] = env
        config_queue_status['job_name'] = 'TRE_TestQueueGatekeeper_Beta'
        config_queue_status['job_repository'] = 'tre-jenkins'
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Web Sanity Status",
                              portlet=self.jobStatusPortlet,
                              config=config_web_sanity),
            PortletAssignment(title=env + " Test Job Queue Status",
                              portlet=self.queueStatusPortlet,
                              config=config_queue_status),
            PortletAssignment(title=env + " Open Critical ENV Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open NCP Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_ncp),
        ]

    def _get_foxtrot_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Foxtrot AND ' \
            'status in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_env["columns"] = ["priority", "summary", "reporter", "assignee", "creation time", "last update time"]
        config_jira_ncp = dict()
        config_jira_ncp["server"] = "{SFLY_JIRA}"
        config_jira_ncp["query"] = \
            'project = "Nonprod Change Process" AND status != Closed AND "Environments Affected" = foxtrot ORDER BY status DESC'
        config_jira_ncp["columns"] = ["summary", "reporter", "assignee", "creation time", "last update time"]
        config_env_status = dict()
        config_env_status['env'] = env
        env_health_check_job = {
            'job_description': "Host/Pool Status",
            'job_name': 'Env_Health_Check-Foxtrot',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Foxtrot',
                    'job_repository': "tre-jenkins",
                },
                {
                    'job_name': 'Env_Availability_Check-Foxtrot',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_env_status['job'] = env_health_check_job

        config_deployment_status = dict()
        config_deployment_status['env'] = env
        deployment_job = {
            "job_description": "Deployment Status",
            'view_name': "main-foxtrot",
            "job_repository": "china",
            'job_config_list': [
                {
                    'job_name': "1--main_foxtrot_servers",
                    "job_repository": "china",
                },
                {
                    'job_name': "2--main_deploy_foxtrot",
                    "job_repository": "china",
                },
                {
                    'job_name': "foxtrot-CP",
                    "job_repository": "china",
                },
                {
                    'job_name': "foxtrot-SP",
                    "job_repository": "china",
                },
                {
                    'job_name': "3--foxtrot_selenium_test",
                    "job_repository": "china",
                },

            ],
        }
        config_deployment_status['job'] = deployment_job
        config_web_sanity = dict()
        config_web_sanity['env'] = env
        config_web_sanity_job = {
            'job_description': "Web Sanity Status",
            'job_name': 'Web_Functional_Tests-Foxtrot',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Web_Functional_Tests-Foxtrot',
                    'job_repository': "tre-jenkins",
                },
                {
                    'job_name': '3--foxtrot_selenium_test',
                    'job_repository': "china",
                },
            ],
        }
        config_web_sanity['job'] = config_web_sanity_job

        config_queue_status = dict()
        config_queue_status['env'] = env
        config_queue_status['job_name'] = 'TRE_TestQueueGatekeeper_Foxtrot'
        config_queue_status['job_repository'] = 'tre-jenkins'

        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_env_status),
            PortletAssignment(title=env + " Deployment Status",
                              portlet=self.jobStatusPortlet,
                              config=config_deployment_status),
            PortletAssignment(title=env + " Web Sanity Status",
                              portlet=self.jobStatusPortlet,
                              config=config_web_sanity),
            PortletAssignment(title=env + " Test Job Queue Status",
                              portlet=self.queueStatusPortlet,
                              config=config_queue_status),
            PortletAssignment(title=env + " Open Critical ENV Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open NCP Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_ncp),
        ]

    def _get_stage_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Staging AND ' \
            'status in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_env["columns"] = ["priority", "summary", "reporter", "assignee", "creation time", "last update time"]
        config_jira_ncp = dict()
        config_jira_ncp["server"] = "{SFLY_JIRA}"
        config_jira_ncp["query"] = \
            'project = "Nonprod Change Process" AND status != Closed AND "Environments Affected" = staging ORDER BY status DESC'
        config_jira_ncp["columns"] = ["summary", "reporter", "assignee", "creation time", "last update time"]
        config_jira_open_patch = dict()
        config_jira_open_patch["server"] = "{SFLY_JIRA}"
        config_jira_open_patch["query"] = \
            'project = "Nonprod Change Process" AND status = Closed AND "Environments Affected" = staging AND resolutiondate > "-7d"'
        config_jira_open_patch["columns"] = ["issue type", "priority", "summary", "reporter", "assignee", "creation time", "last update time"]
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Host/Pool Status",
            'job_name': 'Env_Health_Check-Stage',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Stage',
                    'job_repository': "tre-jenkins",
                },
                {
                    'job_name': 'Env_Availability_Check-Stage',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_site_status['job'] = env_health_check_job
        config_web_sanity = dict()
        config_web_sanity['env'] = env
        config_web_sanity_job = {
            'job_description': "Web Sanity Status",
            'job_name': 'Web_Functional_Tests-Stage',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Web_Functional_Tests-Stage',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_web_sanity['job'] = config_web_sanity_job
        config_queue_status = dict()
        config_queue_status['env'] = env
        config_queue_status['job_name'] = 'TRE_TestQueueGatekeeper_Stage'
        config_queue_status['job_repository'] = 'tre-jenkins'
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Web Sanity Status",
                              portlet=self.jobStatusPortlet,
                              config=config_web_sanity),
            PortletAssignment(title=env + " Test Job Queue Status",
                              portlet=self.queueStatusPortlet,
                              config=config_queue_status),
            PortletAssignment(title=env + " Open Critical ENV Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open PATCH Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_open_patch),
            PortletAssignment(title=env + " Open NCP Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_ncp),
        ]

    def _get_dev_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Dev AND status ' \
            'in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_env["columns"] = ["priority", "summary", "reporter", "assignee", "creation time", "last update time"]
        config_jira_ncp = dict()
        config_jira_ncp["server"] = "{SFLY_JIRA}"
        config_jira_ncp["query"] = \
            'project = "Nonprod Change Process" AND status != Closed AND "Environments Affected" = dev ORDER BY status DESC'
        config_jira_ncp["columns"] = ["summary", "reporter", "assignee", "creation time", "last update time"]
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Host/Pool Status",
            'job_name': 'Env_Health_Check-Dev',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Dev',
                    'job_repository': "tre-jenkins",
                },
                {
                    'job_name': 'Env_Availability_Check-Dev',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_site_status['job'] = env_health_check_job
        config_web_sanity = dict()
        config_web_sanity['env'] = env
        config_web_sanity_job = {
            'job_description': "Web Sanity Status",
            'job_name': 'Web_Functional_Tests-Dev',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Web_Functional_Tests-Dev',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_web_sanity['job'] = config_web_sanity_job
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Web Sanity Status",
                              portlet=self.jobStatusPortlet,
                              config=config_web_sanity),
            PortletAssignment(title=env + " Open Critical ENV Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open NCP Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_ncp),
        ]

    def _get_int_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = "Int" ' \
            'AND status in (Open, "In Progress", Reopened) AND priority in (Critical,' \
            ' "Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_env["columns"] = ["priority", "summary", "reporter", "assignee", "creation time", "last update time"]
        config_jira_ncp = dict()
        config_jira_ncp["server"] = "{SFLY_JIRA}"
        config_jira_ncp["query"] = \
            'project = "Nonprod Change Process" AND status != Closed AND "Environments Affected" = "int" ORDER BY status DESC'
        config_jira_ncp["columns"] = ["summary", "reporter", "assignee", "creation time", "last update time"]
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Host/Pool Status",
            'job_name': 'Env_Health_Check-Int',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Int',
                    'job_repository': "tre-jenkins",
                },
                {
                    'job_name': 'Env_Availability_Check-Int',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_site_status['job'] = env_health_check_job
        config_web_sanity = dict()
        config_web_sanity['env'] = env
        config_web_sanity_job = {
            'job_description': "Web Sanity Status",
            'job_name': 'Web_Functional_Tests-Int2',
            'job_repository': "tre-jenkins",
            'job_config_list': [
                {
                    'job_name': 'Web_Functional_Tests-Int2',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_web_sanity['job'] = config_web_sanity_job
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Web Sanity Status",
                              portlet=self.jobStatusPortlet,
                              config=config_web_sanity),
            PortletAssignment(title=env + " Open Critical ENV Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open NCP Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_ncp),
        ]
