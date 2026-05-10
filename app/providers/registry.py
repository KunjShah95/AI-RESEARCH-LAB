"""Provider registry"""

_providers = {}


def list_providers():
    return list(_providers.keys())


def get_provider(name):
    return _providers.get(name)


def register_provider(name, provider):
    _providers[name] = provider
