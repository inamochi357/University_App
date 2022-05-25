from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from user.models import MyUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'username',
                'password',
                'nickname',
                'grade',
                "department",
                'date_of_birth',
                'image',
                'url',
                'introduction',
                'date_joined',
            )
        }),
        (None, {
            'fields': (
                'is_active',
                'is_admin',
            )
        })
    )
    list_display = ('email', 'username', 'is_active')
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

    # --- adminでuser作成用に追加 ---
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password',),
        }),
    )
    # --- adminでuser作成用に追加 ---


admin.site.unregister(Group)
admin.site.register(MyUser, CustomUserAdmin)