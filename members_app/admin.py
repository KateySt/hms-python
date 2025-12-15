from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from members_app.models import Member


@admin.register(Member)
class MemberAdmin(BaseUserAdmin):
    list_display = ('phone', 'email', 'full_name', 'is_staff', 'is_superuser', 'is_active', 'is_deleted')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_deleted')
    search_fields = ('phone', 'email', 'first_name', 'last_name')
    ordering = ('phone', 'email', 'first_name', 'last_name')

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'last_login', 'date_joined'),
            'classes': ('wide',)
        }),
        ('Permissions',
         {'fields': ('is_staff', 'is_superuser', 'is_active', 'is_deleted', 'groups', 'user_permissions'),
          'classes': ('collapse',)}),
        ('Member settings', {
            'fields': ('color', 'gender', 'language', 'image', 'courses'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2'),
        }),
    )

    def full_name(self, obj):
        return obj.full_name()

    full_name.short_description = 'Full name'
