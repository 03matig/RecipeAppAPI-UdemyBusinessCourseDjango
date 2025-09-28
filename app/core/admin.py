"""
Django admin customization.
"""

from django.contrib import admin

# We import the user admin base class and making some changes to it.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext_lazy as _

# Now, we'll import all our custom models we want to register on our Django Admin.
from core import models


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users. """
    ordering = ['id'] # We're going to order them by ID
    list_display = ['email', 'name']

    # Now, we're going to specify the fields that only exist on our models.
    fieldsets= (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),  # Permission functionality assigned fields
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (
            (_('Important dates'), {  # Important dates functionality assigned fields
                'fields': (
                    ('last_login', )
                )
            })
        ),

    )
    readonly_fields = ['last_login']



"""
If you now were just to type
admin.site.register(models.User), then it would register the user model, but it wouldn't assign
the actual custom user model we defined on line 14, so we're going to do the following:
"""
admin.site.register(models.User, UserAdmin)