from django.contrib import admin

from sitebase.admin import PostAdmin

from .models import BrainbankIdea, BrainbankPost


@admin.register(BrainbankIdea)
class BrainbankIdeaAdmin(admin.ModelAdmin):
    """Admin for BrainBank Idea"""

    empty_value_display = 'None'
    fieldsets = [
        ('info', {
            'fields': ['title', 'short_description', 'repo', 'slug']
        }),
        ('body', {
            'fields': ['body_type', 'body']
        }),
        ('html', {
            'fields': ['body_text']
        }),
    ]
    list_display = ['title', 'repo', 'posts', 'deliverables']
    list_display_links = ['title', 'repo', 'deliverables']
    ordering = ['title']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')

    def posts(self, obj):
        return obj.posts.count()

    def deliverables(self, obj):
        return obj.posts.filter(deliverable=True).count()


@admin.register(BrainbankPost)
class BrainbankPostAdmin(PostAdmin):
    """Admin for BrainBank Post"""

    fieldsets = [
        ('info', {
            'fields': [
                'title', 'authors', 'idea', 'short_description', 'slug'],
        }),
        ('publish', {
            'fields': [
                'date_created', 'date_published',
                'is_published', 'highlight', 'deliverable'],
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
            'fields': ['headerimage', 'tags'],
        }),
    ]
    list_display = (
        'title', 'idea',
        'date_published', 'date_updated', 'highlight', 'is_published')
    list_display_editable = ('is_published', 'highlight')
    list_display_links = (
        'title', 'idea', 'date_published', 'date_updated')
    list_filter = [
        'is_published', 'authors', 'tags', 'idea',
        'highlight', 'deliverable']
    ordering = (
        'title', 'idea',
        'date_published', 'date_updated',
        'highlight', 'is_published', 'deliverable')
    search_fields = ['title', 'short_description', 'series__short_description']
