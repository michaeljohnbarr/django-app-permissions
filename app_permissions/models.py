# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals

# Django
from django import VERSION as DJANGO_VERSION
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.db import models
from django.db.models.query import QuerySet

# Local
from .settings import app_permissions_settings as settings


# ==============================================================================
# MANAGERS
# ==============================================================================
class AppPermissionManager(models.Manager):
    def get_queryset(self):
        # TODO: Remove once Django 1.4 no longer supported and uncomment below
        return QuerySet(self.model, using=self._db).filter(
            content_type__name=settings.APP_PERMISSIONS_CONTENT_TYPE_NAME,
        )
        # return super(AppPermissionManager, self).get_queryset().filter(
        #     content_type__name='app_permission',
        # )

    # TODO: Remove once Django 1.4 no longer supported
    if DJANGO_VERSION < (1, 6):
        get_query_set = get_queryset

    def for_app(self, app_name):
        return self.get_queryset().filter(content_type__app_label=app_name)

    def create_permission(self, name, codename, app_name):
        """Creates and saves a Permission with the given name, codename and
        custom content_type with the given app_name (ContentType.app_label).

        """
        content_type, created = ContentType.objects.get_or_create(
            name=settings.APP_PERMISSIONS_CONTENT_TYPE_NAME,
            app_label=app_name,
        )

        permission = self.model(
            name=name,
            codename=codename,
            content_type=content_type,
        )

        permission.save()

        return permission

    def create(self, name, codename, app_name):
        """Overrides the create() to add the required `app_name` argument."""
        return self.create_permission(name, codename, app_name)


# ==============================================================================
# MODELS
# ==============================================================================
class AppPermission(Permission):
    """An app-based permission, not attached to a model. The content_type name
    must be the same as settings.APP_PERMISSIONS_CONTENT_TYPE_NAME, which
    defaults to `app_permission`.

    Inspiration from:
        http://stackoverflow.com/questions/13932774/#13952198

    """
    objects = AppPermissionManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if hasattr(self, 'content_type'):
            if not self.content_type.name == settings.APP_PERMISSIONS_CONTENT_TYPE_NAME:
                raise FieldError(
                    'ContentType.name must be "{content_name}".'.format(
                        content_name=settings.APP_PERMISSIONS_CONTENT_TYPE_NAME
                    )
                )

        super(AppPermission, self).save(*args, **kwargs)
