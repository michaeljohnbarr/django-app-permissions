# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals

# Django
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve

# Local
from .settings import app_permissions_settings as settings


# ==============================================================================
# MIDDLEWARE CLASSES
# ==============================================================================
class AppPermissionsMiddleware(object):
    """This is a very simple middleware that parses a request and decides what
    translation object to install in the current thread context depending on the
    user's account. This allows pages to be dynamically translated to the
    language the user desires (if the language is available, of course). This
    will fall back to the settings.DEFAULT_LANGUAGE if the language requested
    is not available.

    """
    def check_user_perms(self, request):
        if request.current_app in settings.APP_PERMISSIONS:
            if not any([
                request.user.has_module_perms(request.current_app),
            ]):
                raise PermissionDenied(settings.APP_PERMISSIONS_MIDDLEWARE_MESSAGE)

    def process_response(self, request, response):
        request.current_app = resolve(request.path).app_name

        self.check_user_perms(request)

        return response
