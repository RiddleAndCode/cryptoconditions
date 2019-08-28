import pkg_resources

def read_zencode(name):
    return pkg_resources.resource_string(__name__, name + ".lua").decode('utf-8')
