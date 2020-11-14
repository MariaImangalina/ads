from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    list_display = ['username', 'email', 'expiration_date', 'paid']
    

    def expiration_date(self, obj):
        return obj.profile.expiration_date

    def paid(self, obj):
        return obj.profile.paid

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

