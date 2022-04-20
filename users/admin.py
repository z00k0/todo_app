from django.contrib import admin
from users.models import AppUser
from projects.models import Project, Task


class Slugifier(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('number', 'name')}


admin.site.register(AppUser)
admin.site.register(Project, Slugifier)
admin.site.register(Task, Slugifier)

# Register your models here.
