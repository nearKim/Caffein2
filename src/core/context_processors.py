from django.utils.functional import SimpleLazyObject

from core.models import OperationScheme


def latest_os(request):
    # https://mlvin.xyz/django-templates-context-processors.html
    def lazy_latest_os():
        return OperationScheme.latest()

    return {'os': SimpleLazyObject(lazy_latest_os), 'request': request}
