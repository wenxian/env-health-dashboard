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
        self.brandPortlet = Portlet(
            serviceClass="env_health_dashboard.portlet_services.BrandPortletService")

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
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ]
            },
            'int': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Int',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ]
            },
            'beta': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Beta',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ]
            },
            'foxtrot': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Foxtrot',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': "1--main_foxtrot_servers",
                        'link': "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                                "1--main_foxtrot_servers/",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "2--main_deploy_foxtrot",
                        'link': "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                                "2--main_deploy_foxtrot/",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "foxtrot-CP",
                        'link': "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                                "foxtrot-CP",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "foxtrot-SP",
                        'link': "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                                "foxtrot-SP",
                        "job_repository": "china",
                    },
                    {
                        'job_name': "3--foxtrot_selenium_test",
                        'link': "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                                "3--foxtrot_selenium_test/",
                        "job_repository": "china",
                    },
                ]
            },
            'stage': {
                'env_status': [
                    {
                        'job_name': 'Env_Health_Check-Stage',
                        'job_repository': "tre-jenkins",
                    },
                ],
                'job_status': [
                    {
                        'job_name': '',
                        'job_repository': "",
                    },
                ]
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
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Next scheduled deployment",
                                  portlet=self.nextDeployTimePortlet,
                                  config=config_deploy),
                ]

    def _get_foxtrot_skinny_portlet_assignments(self, env):
        config_deploy = dict()
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_deploy["jobname"] = "0--main_foxtrot_changelist"
        config_other_link = open(settings.TEMPLATE_DIR +
                                 "/env_health_dashboard/foxtrot_other_link.html").read()
        config_changelist = dict()
        config_changelist["env"] = env
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Next scheduled deployment",
                                  portlet=self.nextDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Other Links",
                                  portlet=self.textPortlet,
                                  config=config_other_link)]

    def _get_stage_skinny_portlet_assignments(self, env):
        config_deploy = dict()
        config_deploy["jobname"] = "0--main_stage_changelist"
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_other_link = open(settings.TEMPLATE_DIR +
                                 "/env_health_dashboard/stage_other_link.html").read()
        config_changelist = dict()
        config_changelist["env"] = env
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Next scheduled deployment",
                                  portlet=self.nextDeployTimePortlet,
                                  config=config_deploy),
                PortletAssignment(title="Other Links",
                                  portlet=self.textPortlet,
                                  config=config_other_link)
                ]

    def _get_dev_skinny_portlet_assignments(self, env):
        config_deploy = dict()
        config_deploy["jobname"] = "2--main_deploy_int1"
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        config_changelist = dict()
        config_changelist["env"] = env
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                ]

    def _get_int_skinny_portlet_assignments(self, env):
        config_changelist = dict()
        config_changelist["env"] = env
        config_deploy = dict()
        config_deploy["jobname"] = "4--main_deploy_int2"
        config_deploy["server"] = "{SFLY_CHINA_JENKINS}"
        return [PortletAssignment(title=env + " Deployed Version",
                                  portlet=self.changelistPortlet,
                                  config=config_changelist),
                PortletAssignment(title="Last scheduled deployment",
                                  portlet=self.lastDeployTimePortlet,
                                  config=config_deploy),
                ]

    def _get_beta_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Beta AND ' \
            'status in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_non_env = dict()
        config_jira_non_env["server"] = "{SFLY_JIRA}"
        config_jira_non_env["query"] = \
            'project != "Environments - preproduction" AND issuetype = Bug AND ' \
            '"Environment Found" = Beta AND status in (Open, "In Progress", Reopened) AND ' \
            'priority in (Critical, "Non-Production Blocker", "Production Blocker") ORDER BY ' \
            'created DESC'
        config_jira_recently_closed = dict()
        config_jira_recently_closed["server"] = "{SFLY_JIRA}"
        config_jira_recently_closed["query"] = \
            'project = ENV AND status = Closed AND resolved >= -7d AND "Environment Found" = ' \
            'Beta AND priority in (Critical, "Non-Production Blocker", "Production Blocker") ' \
            'ORDER BY resolved DESC'
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Environment Health Check",
            'link':
                "http://tre-jenkins.internal.shutterfly.com:8080/view/Env Health Check/job/"
                "Env_Health_Check-Beta/",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Beta',
                    'job_repository': "tre-jenkins",
                },

            ],
        }
        config_site_status['job'] = env_health_check_job
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Open Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open Non-Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_non_env),
            PortletAssignment(title=env + " Recently Closed Environments Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_recently_closed),
        ]

    def _get_foxtrot_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Foxtrot AND ' \
            'status in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_non_env = dict()
        config_jira_non_env["server"] = "{SFLY_JIRA}"
        config_jira_non_env["query"] = \
            'project != "Environments - preproduction" AND issuetype = Bug AND ' \
            '"Environment Found" = Foxtrot AND status in (Open, "In Progress", Reopened) ' \
            'AND priority in (Critical, "Non-Production Blocker", "Production Blocker") ORDER ' \
            'BY created DESC'
        config_jira_recently_closed = dict()
        config_jira_recently_closed["server"] = "{SFLY_JIRA}"
        config_jira_recently_closed["query"] = \
            'project = ENV AND status = Closed AND resolved >= -7d AND "Environment Found" = ' \
            'Foxtrot AND priority in (Critical, "Non-Production Blocker", "Production Blocker") ' \
            'ORDER BY resolved DESC'
        config_env_status = dict()
        config_env_status['env'] = env
        env_health_check_job = {
            'job_description': "Environment Health Check",
            'link':
                "http://tre-jenkins.internal.shutterfly.com:8080/view/Env Health Check/job/"
                "Env_Health_Check-Foxtrot/",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Foxtrot',
                    'job_repository': "tre-jenkins",
                },

            ],
        }
        config_env_status['job'] = env_health_check_job

        config_deployment_status = dict()
        config_deployment_status['env'] = env
        deployment_job = {
            "job_description": "Deployment Job Check",
            'link': "http://china.stage.shutterfly.com:2010/view/main-foxtrot/",
            'job_config_list': [
                {
                    'job_name': "1--main_foxtrot_servers",
                    'link':
                        "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                        "1--main_foxtrot_servers/",
                    "job_repository": "china",
                },
                {
                    'job_name': "2--main_deploy_foxtrot",
                    'link':
                        "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                        "2--main_deploy_foxtrot/",
                    "job_repository": "china",
                },
                {
                    'job_name': "foxtrot-CP",
                    'link':
                        "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/foxtrot-CP",
                    "job_repository": "china",
                    },
                {
                    'job_name': "foxtrot-SP",
                    'link':
                        "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/foxtrot-SP",
                    "job_repository": "china",
                },
                {
                    'job_name': "3--foxtrot_selenium_test",
                    'link':
                        "http://china.stage.shutterfly.com:2010/view/main-foxtrot/job/"
                        "3--foxtrot_selenium_test/",
                    "job_repository": "china",
                },

            ],
        }
        config_deployment_status['job'] = deployment_job

        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_env_status),
            PortletAssignment(title=env + " Deployment Status",
                              portlet=self.jobStatusPortlet,
                              config=config_deployment_status),
            PortletAssignment(title=env + " Open Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open Non-Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_non_env),
            PortletAssignment(title=env + " Recently Closed Environments Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_recently_closed),
        ]

    def _get_stage_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Staging AND ' \
            'status in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_non_env = dict()
        config_jira_non_env["server"] = "{SFLY_JIRA}"
        config_jira_non_env["query"] = \
            'project != "Environments - preproduction" AND issuetype = Bug AND ' \
            '"Environment Found" = Staging AND status in (Open, "In Progress", Reopened) AND ' \
            'priority in (Critical, "Non-Production Blocker", "Production Blocker") ' \
            'ORDER BY created DESC'
        config_jira_recently_closed = dict()
        config_jira_recently_closed["server"] = "{SFLY_JIRA}"
        config_jira_recently_closed["query"] = \
            'project = ENV AND status = Closed AND resolved >= -7d AND "Environment Found" = ' \
            'Staging AND priority in (Critical, "Non-Production Blocker", "Production Blocker") ' \
            'ORDER BY resolved DESC'
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Environment Health Check",
            'link':
                "http://tre-jenkins.internal.shutterfly.com:8080/view/Env Health Check/job/"
                "Env_Health_Check-Stage/",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Stage',
                    'job_repository': "tre-jenkins",
                },

            ],
        }
        config_site_status['job'] = env_health_check_job
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Open Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open Non-Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_non_env),
            PortletAssignment(title=env + " Recently Closed Environments Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_recently_closed),
        ]

    def _get_dev_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = Dev AND status ' \
            'in (Open, "In Progress", Reopened) AND priority in (Critical, ' \
            '"Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_non_env = dict()
        config_jira_non_env["server"] = "{SFLY_JIRA}"
        config_jira_non_env["query"] = \
            'project != "Environments - preproduction" AND issuetype = Bug AND ' \
            '"Environment Found" = Dev AND status in (Open, "In Progress", Reopened) AND ' \
            'priority in (Critical, "Non-Production Blocker", "Production Blocker") ' \
            'ORDER BY created DESC'
        config_jira_recently_closed = dict()
        config_jira_recently_closed["server"] = "{SFLY_JIRA}"
        config_jira_recently_closed["query"] = \
            'project = ENV AND status = Closed AND resolved >= -7d AND "Environment Found" = Dev ' \
            'AND priority in (Critical, "Non-Production Blocker", "Production Blocker") ' \
            'ORDER BY resolved DESC'
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Environment Health Check",
            'link':
                "http://tre-jenkins.internal.shutterfly.com:8080/view/Env Health Check/"
                "job/Env_Health_Check-Dev/",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Dev',
                    'job_repository': "tre-jenkins",
                },
            ],
        }
        config_site_status['job'] = env_health_check_job
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Open Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open Non-Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_non_env),
            PortletAssignment(title=env + " Recently Closed Environments Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_recently_closed),
        ]

    def _get_int_wide_portlet_assignments(self, env):
        config_jira_env = dict()
        config_jira_env["server"] = "{SFLY_JIRA}"
        config_jira_env["query"] = \
            'project = "Environments - preproduction" AND "Environment Found" = "Int" ' \
            'AND status in (Open, "In Progress", Reopened) AND priority in (Critical,' \
            ' "Non-Production Blocker", "Production Blocker") ORDER BY created DESC'
        config_jira_non_env = dict()
        config_jira_non_env["server"] = "{SFLY_JIRA}"
        config_jira_non_env["query"] = \
            'project != "Environments - preproduction" AND issuetype = Bug AND ' \
            '"Environment Found" = "Int" AND status in (Open, "In Progress", Reopened) AND ' \
            'priority in (Critical, "Non-Production Blocker", "Production Blocker") ' \
            'ORDER BY created DESC'
        config_jira_recently_closed = dict()
        config_jira_recently_closed["server"] = "{SFLY_JIRA}"
        config_jira_recently_closed["query"] = \
            'project = ENV AND status = Closed AND resolved >= -7d AND ' \
            '"Environment Found" = "Int" AND priority in ' \
            '(Critical, "Non-Production Blocker", "Production Blocker") ORDER BY resolved DESC'
        config_site_status = dict()
        config_site_status['env'] = env
        env_health_check_job = {
            'job_description': "Environment Health Check",
            'link':
                "http://tre-jenkins.internal.shutterfly.com:8080/view/Env Health Check/job/"
                "Env_Health_Check-Int/",
            'job_config_list': [
                {
                    'job_name': 'Env_Health_Check-Int',
                    'job_repository': "tre-jenkins",
                },

            ],
        }
        config_site_status['job'] = env_health_check_job
        return [
            PortletAssignment(title=env + " Environment Status",
                              portlet=self.envStatusPortlet,
                              config=config_site_status),
            PortletAssignment(title=env + " Open Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_env),
            PortletAssignment(title=env + " Open Non-Environment Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_non_env),
            PortletAssignment(title=env + " Recently Closed Environments Tickets",
                              portlet=self.jiraPortlet,
                              config=config_jira_recently_closed),
        ]
