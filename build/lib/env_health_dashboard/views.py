from django.http import HttpResponse
from django.template import RequestContext, loader
import version
import multiprocessing
from django.shortcuts import redirect
from django.conf import settings
from portlet_configuration_service import PorletConfigurationService

TIMEOUT_DURATION = 5

portlet_configuration_service = PorletConfigurationService()


def call_it(instance, name, args=(), kwargs=None):
    # indirect caller for instance methods and multiprocessing
    # as multiprocessing cannot call directly a method of a class
    if kwargs is None:
        kwargs = {}
    return getattr(instance, name)(*args, **kwargs)


def initialize_services(envPortlets):
    services = []
    workers = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=workers)
    # Start pool apply_async envPortlet.gatherAndReturnPortletData()
    # it calls asynchronously
    async_results = [
        pool.apply_async(call_it, args=(envPortlet, 'gatherAndReturnPortletData'))
        for envPortlet in envPortlets]
    # Prevents any more tasks from being submitted to the pool.
    pool.close()
    # Call get() method to retrieve the result of the function call.
    # The get() method blocks until the function is completed.
    try:
        for j in range(len(async_results)):
                try:
                    result = async_results[j]
                    service = result.get(timeout=TIMEOUT_DURATION)
                    services.append(service)
                except Exception as e:
                    service = envPortlets[j].returnPortletDataWithError(e)
                    services.append(service)
    except:
        pool.terminate()
    finally:
        # Wait for the worker processes to exit. Ensure all threads get cleaned up.
        pool.join()
    return services


def index(request, *callback_args, **callback_kwargs):
    return redirect('/brand')


def env_handler(request, *callback_args, **callback_kwargs):
    template = loader.get_template('env_health_dashboard/env.html')
    env = callback_kwargs['env'].lower()
    brand = callback_kwargs['brand']
    if brand not in settings.ENV:
        brand = settings.DEFAULT_BRAND

    if env != "self_test" and env not in settings.ENV[brand.lower()]:
        env = settings.DEFAULT_ENV

    skinnyColumnPortletAssignments = \
        portlet_configuration_service.get_skinny_column_portlet_assignment_from_env(env)
    wideColumnPortletAssignments = \
        portlet_configuration_service.get_wide_column_portlet_assignment_from_env(env)

    context = RequestContext(request, {
        'skinny_portlet_list': initialize_services(skinnyColumnPortletAssignments),
        'wide_portlet_list': initialize_services(wideColumnPortletAssignments),
        'env': env,
        'version': version.getVersion(),
        'brand': brand,
        'env_list': settings.ENV[brand.lower()]
    })

    return HttpResponse(template.render(context))


def brand_handler(request, *callback_args, **callback_kwargs):
    template = loader.get_template('env_health_dashboard/brand.html')
    brand = callback_kwargs['brand']

    brand_list = settings.ENV
    if brand not in brand_list:
        brand = settings.DEFAULT_BRAND

    portlet_list = portlet_configuration_service.get_brand_page_portlet_assignments(brand)

    context = RequestContext(request, {
        'brand': brand,
        'brand_list': brand_list,
        'portlet_list': initialize_services(portlet_list),
    })

    return HttpResponse(template.render(context))
