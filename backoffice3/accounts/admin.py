from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'phone_number', 'status', 'level', 'permission_approve', 'permission_list', 'permission_edit', 'permission_delete' ]
    list_filter = ['status', 'level', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions', 'permission_approve', 'permission_list', 'permission_edit', 'permission_delete')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'date_rejected', 'reject_reason')}),
        ('User status', {'fields': ('status', 'level')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'password1', 'password2', 'is_superuser')}
        ),
    )
    search_fields = ['email', 'name', 'phone_number']
    ordering = ['-id']

admin.site.register(CustomUser, CustomUserAdmin)


