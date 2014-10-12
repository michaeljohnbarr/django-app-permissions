# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals

# Django
from django.core.urlresolvers import resolve

# Local
from .settings import app_permissions_settings as settings


# ==============================================================================
# MIDDLEWARE CLASSES
# ==============================================================================
class AppPermissionsMiddleware(object):
    """Middleware which checks to see if a User has permissions to the current
    app. If not, it will process the response/exception set up in the
    APP_PERMISSIONS_MIDDLEWARE_ACTION using the
    APP_PERMISSIONS_MIDDLEWARE_MESSAGE.

    """
    def check_user_perms(self, request):
        if request.current_app in settings.PROTECTED_APPS:
            if not any([
                request.user.has_module_perms(request.current_app),
            ]):
                if issubclass(
                    settings.APP_PERMISSIONS_MIDDLEWARE_ACTION,
                    BaseException
                ):
                    raise settings.APP_PERMISSIONS_MIDDLEWARE_ACTION(
                        settings.APP_PERMISSIONS_MIDDLEWARE_MESSAGE
                    )
                else:
                    return False

        return True

    def process_response(self, request, response):
        # Set the current_app in the context
        request.current_app = resolve(request.path).app_name

        # See if the user has any permissions for the current app
        has_permissions = self.check_user_perms(request)

        if not has_permissions:
            return settings.APP_PERMISSIONS_MIDDLEWARE_ACTION(
                settings.APP_PERMISSIONS_MIDDLEWARE_MESSAGE
            )

        return response
