# import django
# from django.test.utils import setup_test_environment
# from django.test.client import Client
#
#
# class FunctionalTests(django.test.testcases.TestCase):
#
#     def setUp(self):
#         setup_test_environment()
#         self.client = Client()
#
#     def test_homepage_is_accessible(self):
#         response = self.client.get('/')
#         self.assertEqual(302, response.status_code)
#
#     def test_self_test_page(self):
#         response = self.client.get('/env/sfly.self_test')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Test Skinny Portlet",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Test Wide Portlet",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Delay Portlet Skinny",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Delay Portlet Wide",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="The content of this portlet",
#                             count=2,
#                             status_code=200)
#         self.assertContains(response,
#                             text="more content",
#                             count=1,
#                             status_code=200)
#
#     def test_foxtrot_page_other_links_portlet(self):
#         response = self.client.get('/env/sfly.foxtrot')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Quick Links",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Ignite Page",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Load Tests",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Deployment Pipeline",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Server List",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Wildcat Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Open Critical Jira Tickets",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="App Pool Memory Usage",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="WS Pool Memory Usage",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="API Pool Memory Usage",
#                             count=1,
#                             status_code=200)
#
#     def test_stage_page_other_links_portlet(self):
#         response = self.client.get('/env/sfly.stage')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Quick Links",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Patch Listing",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Server List",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Wildcat Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Open Critical Jira Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_beta_page_other_links_portlet(self):
#         response = self.client.get('/env/sfly.beta')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Quick Links",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Deployment Pipeline",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Server List",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Wildcat Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Open Critical Jira Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_int_page_other_links_portlet(self):
#         response = self.client.get('/env/sfly.int')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Quick Links",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Deployment Pipeline",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Server List",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Wildcat Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Open Critical Jira Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_dev_page_other_links_portlet(self):
#         response = self.client.get('/env/sfly.dev')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Quick Links",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Deployment Pipeline",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Server List",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Wildcat Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Open Critical Jira Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_beta_page_jira_portlet(self):
#         response = self.client.get('/env/sfly.beta')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Beta Open Critical ENV Tickets",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Beta Open NCP Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_foxtrot_page_jira_portlet(self):
#         response = self.client.get('/env/sfly.foxtrot')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Foxtrot Open Critical ENV Tickets",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Foxtrot Open NCP Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_stage_page_jira_portlet(self):
#         response = self.client.get('/env/sfly.stage')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Stage Open Critical ENV Tickets",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Stage Open PATCH Tickets",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Stage Open NCP Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_dev_page_jira_portlet(self):
#         response = self.client.get('/env/sfly.dev')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Dev Open Critical ENV Tickets",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Dev Open NCP Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_int_page_jira_portlet(self):
#         response = self.client.get('/env/sfly.int')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Int Open Critical ENV Tickets",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Int Open NCP Tickets",
#                             count=1,
#                             status_code=200)
#
#     def test_beta_page_changelist_portlet(self):
#         response = self.client.get('/env/sfly.beta')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Beta Deployed Version",
#                             count=1,
#                             status_code=200)
#
#     def test_foxtrot_page_changelist_portlet(self):
#         response = self.client.get('/env/sfly.foxtrot')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Foxtrot Deployed Version",
#                             count=1,
#                             status_code=200)
#
#     def test_dev_page_changelist_portlet(self):
#         response = self.client.get('/env/sfly.dev')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Dev Deployed Version",
#                             count=1,
#                             status_code=200)
#
#     def test_int_page_changelist_portlet(self):
#         response = self.client.get('/env/sfly.int')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Int Deployed Version",
#                             count=1,
#                             status_code=200)
#
#     def test_beta_page_deployment_portlet(self):
#         response = self.client.get('/env/sfly.beta')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Next scheduled deployment",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Last scheduled deployment",
#                             count=1,
#                             status_code=200)
#
#     def test_foxtrot_page_deployment_portlet(self):
#         response = self.client.get('/env/sfly.foxtrot')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Next scheduled deployment",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Last scheduled deployment",
#                             count=1,
#                             status_code=200)
#
#     def test_stage_page_deployment_portlet(self):
#         response = self.client.get('/env/sfly.stage')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Last scheduled deployment",
#                             count=1,
#                             status_code=200)
#
#     def test_dev_page_deployment_portlet(self):
#         response = self.client.get('/env/sfly.dev')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Last scheduled deployment",
#                             count=1,
#                             status_code=200)
#
#     def test_int_page_deployment_portlet(self):
#         response = self.client.get('/env/sfly.int')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Last scheduled deployment",
#                             count=1,
#                             status_code=200)
#
#     def test_beta_page_site_status_portlet(self):
#         response = self.client.get('/env/sfly.beta')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Beta Environment Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Beta Web Sanity Status",
#                             count=1,
#                             status_code=200)
#
#     def test_foxtrot_page_site_status_portlet(self):
#         response = self.client.get('/env/sfly.foxtrot')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Foxtrot Environment Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Foxtrot Deployment Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Foxtrot Web Sanity Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Foxtrot Test Job Queue Status",
#                             count=1,
#                             status_code=200)
#
#     def test_stage_page_site_status_portlet(self):
#         response = self.client.get('/env/sfly.stage')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Stage Environment Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Stage Web Sanity Status",
#                             count=1,
#                             status_code=200)
#
#     def test_dev_page_site_status_portlet(self):
#         response = self.client.get('/env/sfly.dev')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Dev Environment Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Dev Web Sanity Status",
#                             count=1,
#                             status_code=200)
#
#     def test_int_page_site_status_portlet(self):
#         response = self.client.get('/env/sfly.int')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Int Environment Status",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Int Web Sanity Status",
#                             count=1,
#                             status_code=200)
#
#     def test_brand_page_footer(self):
#         response = self.client.get('/brand/sfly')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Page Loaded:",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Next Refresh:",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Contact reliabilityeng@shutterfly.com",
#                             count=1,
#                             status_code=200)
#
#     def test_env_page_footer(self):
#         response = self.client.get('/env/sfly.foxtrot')
#         self.assertEqual(200, response.status_code)
#         self.assertContains(response,
#                             text="Page Loaded:",
#                             count=1,
#                             status_code=200)
#         self.assertContains(response,
#                             text="Contact reliabilityeng@shutterfly.com",
#                             count=1,
#                             status_code=200)
#
