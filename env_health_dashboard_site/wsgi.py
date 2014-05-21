"""
WSGI config for env_health_dashboard_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import site
import os
import sys
sys.stdout = sys.stderr

appSiteFolder = os.path.dirname(__file__)
appSiteParentFolder = os.path.dirname(appSiteFolder)
virtualEnv = appSiteFolder + '/venv'

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(virtualEnv + '/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append(appSiteParentFolder)
sys.path.append(appSiteParentFolder + '/env_health_dashboard')

os.environ['DJANGO_SETTINGS_MODULE'] = 'env_health_dashboard_site.settings.local'

# Activate your virtual env
activate_env=os.path.expanduser(virtualEnv + "/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()




