import django
from django.test.utils import setup_test_environment
from django.core.urlresolvers import resolve


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
