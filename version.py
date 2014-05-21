import os

def getVersion():
    version_prop_file = open(os.path.join(os.path.dirname(__file__), 'version.properties'))
    version_props = dict(line.strip().split('=') for line in version_prop_file)
    return version_props['version']
