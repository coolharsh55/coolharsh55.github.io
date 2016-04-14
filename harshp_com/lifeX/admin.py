from django.contrib import admin

from sitebase.admin import PostAdmin

from .models import LifeXWeek, LifeXExperiment
from .models import LifeXCategory, LifeXIdea
from .models import LifeXGoal
from .models import LifeXBlog


@admin.register(LifeXWeek)
class LifeXWeekAdmin(admin.ModelAdmin):

    date_hierarchy = 'date_start'
    list_display = ('number', 'date_start', 'date_end', 'no_experiments')
    list_display_links = ('number', 'date_start', 'date_end')
    ordering = ('-number',)

    def no_experiments(self, obj):
        return obj.experiments.count()


@admin.register(LifeXExperiment)
class LifeXExperimenAdmin(admin.ModelAdmin):

    list_display = ('week', 'title', 'idea', 'rating')
    list_display_links = ('week', 'title', 'idea', 'rating')
    list_filter = ('week__number', 'idea__category')
    fieldsets = [
        ('info', {
            'fields': [
                'title', 'week', 'idea', 'authors',
                'short_description', 'slug'],
        }),
        ('publish', {
            'fields': ['date_created', 'date_published', 'is_published'],
        }),
        ('content', {
            'fields': ['body_type', 'premise', 'outcome'],
        }),
        ('html', {
            'fields': ['premise_body', 'outcome_body'],
        }),
        ('meta', {
            'fields': ['rating', 'tags'],
        })
    ]
    ordering = ('-week__number', 'title')
    search_fields = ('title', 'short_description', 'idea__title',)


@admin.register(LifeXCategory)
class LifeXCategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'ideas_count')
    list_display_links = ('name', 'ideas_count')
    ordering = ('name',)
    search_fields = ('name',)

    def ideas_count(self, obj):
        return obj.ideas.count()


@admin.register(LifeXIdea)
class LifeXIdeaAdmin(admin.ModelAdmin):

    list_display = ('title', 'category', 'experiments', 'tried', 'retry')
    list_display_links = ('title', 'category', 'experiments', 'tried', 'retry')
    list_filter = ('category',)
    fieldsets = [
        ('info', {
            'fields': [
                'title', 'category', 'short_description',
                'tried', 'retry', 'slug'],
        }),
        ('content', {
            'fields': ['body_type', 'description'],
        }),
        ('html', {
            'fields': ['body_text'],
        }),
        ('meta', {
            'fields': ['tags', ]
        })
    ]
    ordering = ('title', 'category', 'tried', 'retry')
    search_fields = ('title',)

    def experiments(self, obj):
        return obj.experiments.count()


@admin.register(LifeXGoal)
class LifeXGoalAdmin(admin.ModelAdmin):
    """admin for LifeX Goals"""

    list_display = ('title', 'parent', 'children')
    list_display_links = ('title', 'parent', 'children')
    list_filter = ('parent',)
    ordering = ('title',)
    search_fields = ('title', 'short_description')

    def children(self, obj):
        return obj.lifexgoal_set.all().count()


@admin.register(LifeXBlog)
class LifeXBlogAdmin(PostAdmin):
    """admin for Blog Post"""

    fieldsets = [
        ('info', {
            'fields': [
                'title', 'authors', 'short_description', 'slug'],
        }),
        ('publish', {
            'fields': [
                'date_created', 'date_published',
                'is_published', ],
        }),
        ('content', {
            'classes': ('wide',),
            'fields': ['body_type', 'body'],
        }),
        ('html', {
            'classes': ('wide',),
            'fields': ['body_text'],
        }),
        ('meta', {
            'fields': ['tags'],
        }),
    ]
    list_display = (
        'title', 'date_published', 'date_updated', 'is_published')
    list_display_editable = ('is_published',)
    list_display_links = (
        'title', 'date_published', 'date_updated')
    list_filter = ['is_published', 'authors', 'tags']
    ordering = (
        'title', 'date_published', 'date_updated', 'is_published')
    search_fields = ['title', 'short_description']
