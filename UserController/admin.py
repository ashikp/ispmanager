from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role
from django.utils.translation import gettext_lazy as _ 


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

    # Fields to allow the admin to edit in the form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Role info'), {'fields': ('role',)}),  # Adding the role field here
    )

    # Fields shown when creating a new user in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),  # Adding role field here
        }),
    )

    # Specify that the role field is available when searching
    search_fields = ('username', 'email', 'role__name')
    ordering = ('username',)

    # Allow admin to filter users based on their role
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    def save_model(self, request, obj, form, change):
        # Assign the role with id=2 (Customer) if no role is provided
        if obj.role is None:
            try:
                obj.role = Role.objects.get(id=3)  # Assuming role with id=2 is "Customer"
            except Role.DoesNotExist:
                raise ValueError("Role with id=3 does not exist. Please create the 'Customer' role.")
        
        # Call the original save_model method
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)