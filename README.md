django-app-permissions
======================
App-based permissions for Django based off of URL patterns. Django's [Permission and Authorization](https://docs.djangoproject.com/en/dev/topics/auth/default/#permissions-and-authorization) tightly couples the models with the permissions via [the contenttypes framework](https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/). The problem is that an app can contain views that have nothing to do with the models.

With django-app-permissions, you can now prevent the view from being displayed to the User if the User doesn't have permissions for the app, and either raise an [exception](https://docs.djangoproject.com/en/dev/ref/exceptions/) or return a custom [HttpResponse](https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-subclasses).

**Supported Django Versions:** 1.4+

**Note:** This app is currently in an **alpha** development state. Please [submit an issue](https://github.com/michaeljohnbarr/django-app-permissions/issues) if you have suggestions or run into problems.

### Creating app-based permissions
For each application that you want to protect with application permissions, create an AppPermission:

    from app_permissions.models import AppPermission
    
    # Create an AppPermission for the app "myapp"
    AppPermission.objects.create(
        name='Can View MyApp', 
        codename='can_view_myapp', 
        app_name='myapp'
    )

### Preparing your URLs
In order for django-app-permissions to work, each application should have their URLs included as follows:

    urlpatterns = patterns('',
        url(r'^myapp/', include('myapp.urls', app_name='myapp')),
    )
    
The key here is the `app_name` argument in the includes. Without it, the `app_permissions.middleware.AppPermissionsMiddleware` will not work. For more information, see Django's documentation on [Reversing namespaced URLs](https://docs.djangoproject.com/en/dev/topics/http/urls/#reversing-namespaced-urls).

### Configuration
1. Add `app_permissions` to `settings.INSTALLED_APPS`.
2. Create permissions (will look into automating this in future versions)
3. Add `app_permissions.middleware.AppPermissionsMiddleware` to your `settings.MIDDLEWARE_CLASSES`.
4. Configure the `APP_PERMISSIONS` (see below) - make sure to add your protected apps to `APP_PERMISSIONS['PROTECTED_APPS']`


### APP_PERMISSIONS defaults
    APP_PERMISSIONS = {
        'APP_PERMISSIONS_CONTENT_TYPE_NAME': 'app_permission',
        'APP_PERMISSIONS_MIDDLEWARE_ACTION': 'django.core.exceptions.PermissionDenied',
        'APP_PERMISSIONS_MIDDLEWARE_MESSAGE': ugettext_lazy(
            'You do not have sufficient privileges to view this application.'
        ),
        'PROTECTED_APPS': (),
    }
