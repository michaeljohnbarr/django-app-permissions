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
        url(r'^myapp/', include('myapp.urls', namespace='myapp', app_name='myapp')),
    )
    
The key here is the `namespace` and `app_name` arguments in the includes. Without these, the `app_permissions.middleware.AppPermissionsMiddleware` will not work. For more information, see Django's documentation on [Reversing namespaced URLs](https://docs.djangoproject.com/en/dev/topics/http/urls/#reversing-namespaced-urls). How it works is that the middleware will check both the `namespace` and `current_app` for any `APP_PERMISSIONS['PROTECTED_APPS']`. 

As an example, if we had a nested URL structure:

    # Root URL patterns   ./api/
    urlpatterns = patterns('',
        url(r'^api/', includes('api.urls', namespace='api', app_name='api')),
    )
    
    # api.urls patterns   ./api/myapp/
    urlpatterns('',
        url(r'^myapp/', includes('myapp.api.urls', namespace='myapp', app_name='myapp')),
    )

...and we had this setup in our settings:

    APP_PERMISSIONS = {
        'PROTECTED_APPS': ('myapp', )
    }
    
Any URL with "myapp" in the `namespace` or `current_app` would be protected. Note that the middleware utilizes [django.contrib.auth.models.User.has_module_perms](https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_module_perms), which means that if the user has individual permissions to Create/Update/Delete any model in the application, they will be granted access without you having to create any custom permissions using `app_permissions.models.AppPermissions`.

### Configuration
1. Add `app_permissions` to `settings.INSTALLED_APPS`.
2. Create permissions (will look into automating this in future versions)
3. Add `app_permissions.middleware.AppPermissionsMiddleware` to your `settings.MIDDLEWARE_CLASSES`.
4. Configure the `APP_PERMISSIONS` ([see below](#app_permissions-defaults)) - make sure to add your protected apps to `APP_PERMISSIONS['PROTECTED_APPS']`


### APP_PERMISSIONS defaults
    APP_PERMISSIONS = {
        'APP_PERMISSIONS_CONTENT_TYPE_NAME': 'app_permission',
        'APP_PERMISSIONS_MIDDLEWARE_ACTION': 'django.core.exceptions.PermissionDenied',
        'APP_PERMISSIONS_MIDDLEWARE_MESSAGE': ugettext_lazy(
            'You do not have sufficient privileges to view this application.'
        ),
        'PROTECTED_APPS': (),
    }
