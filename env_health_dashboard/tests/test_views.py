import django
from django.test.utils import setup_test_environment
from django.test.client import Client
from env_health_dashboard.models import PortletAssignment, Portlet
from env_health_dashboard import views
from datetime import datetime


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

    def test_multiprocess_with_timeout_error(self):
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

    def test_format_time(self):
        time_now = datetime(2015, 5, 13, 12, 30, 50)
        expect_time_string = "2015/05/13 12:30 (PDT)"
        rtn_time = views._format_time(time_now)
        self.assertEqual(str(rtn_time), expect_time_string)

    def test_get_next_refresh_time(self):
        time_now = datetime(2015, 5, 13, 12, 30, 50)
        time_expect = datetime(2015, 5, 13, 12, 31, 50)
        refresh = 60
        time_rtn = views._get_next_refresh_time(time_now, refresh)
        self.assertEqual(time_expect, time_rtn)

    def test_get_css_class(self):
        self.assertEqual('icon_medium', views._get_icon_css_class("true"))
        self.assertEqual('icon', views._get_icon_css_class(""))
