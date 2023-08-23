import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse

from .models import Author, Post


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'birth_date', 'location')
    list_filter = ('is_staff', 'date_joined', 'last_login', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'birth_date', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    actions = ['make_inactive', 'make_active']

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Make selected authors inactive"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Make selected authors active"


admin.site.register(Author, CustomUserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_published', 'published_date')
    list_filter = ('is_published', 'published_date', 'owner')
    search_fields = ('title', 'short_description', 'full_description')
    actions = ['make_published', 'make_unpublished', 'export_selected_posts']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    def export_selected_posts(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="posts.csv"'
        writer = csv.writer(response)
        writer.writerow(['Published Date', 'Owner', 'Title', 'short_description', 'full_description'])
        for post in queryset:
            writer.writerow([post.published_date, post.owner.username, post.title, post.short_description,
                             post.full_description])
        return response


admin.site.register(Post, PostAdmin)
