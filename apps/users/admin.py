from django.contrib import admin


from apps.users.models import User

class UserAdmin(admin.ModelAdmin):
    model = User

# Register your models here.
admin.site.register(User, UserAdmin)