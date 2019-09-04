import pkg_resources

def read_zencode(name):
    """
    Reads a lua file in `cryptoconditions.zencode` as a string. This is
    particulary useful for evaluating Zencode scenarios using `zenroom_minimal`
    in the context of cryptoconditions.
    """
    return pkg_resources.resource_string(__name__, name + ".lua").decode('utf-8')
