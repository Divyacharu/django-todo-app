# from django.contrib import admin
# from .models import Project,Todo

# # Register the Project model
# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_date')
#     search_fields = ('title',)
#     ordering = ('created_date',)


# @admin.register(Todo)
# class TodoAdmin(admin.ModelAdmin):
#     list_display = ('description', 'status', 'created_date', 'updated_date', 'project')
#     list_filter = ('status', 'project')
#     search_fields = ('description',)
#     ordering = ('created_date',)

from django.contrib import admin
from .models import Project, Todo

admin.site.register(Project)
admin.site.register(Todo)

