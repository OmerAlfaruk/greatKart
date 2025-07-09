from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
        "is_active",
        "is_admin",
    )
    list_display_links = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    search_fields = ("email", "username")
    readonly_fields = ("date_joined", "last_login")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
