from django.contrib import admin

from sitebase.admin import PostAdmin

from .models import JournalTag, JournalEntry, JournalSection


@admin.register(JournalTag)
class JournalTagAdmin(admin.ModelAdmin):

    list_display = ['name', 'description', 'entries']
    ordering = ['name']
    search_fields = ['name', 'description']

    def entries(self, obj):
        return obj.entries.count()


@admin.register(JournalEntry)
class JournalEntryAdmin(PostAdmin):

    filter_horizontal = ['journal_tags']
    list_display = [
        'title', 'section', 'date_published', 'date_updated',
        'is_published', 'private']
    list_display_editable = ['is_published', 'private']
    list_filter = ['is_published', 'private', 'section']
    list_display_links = [
        'title', 'section', 'date_published', 'date_updated',
        'is_published', 'private']
    ordering = ['-date_published', 'title']
    search_fields = ['title', 'short_description']

    fieldsets = [
        ('info', {
            'fields': [
                'title', 'section', 'short_description', 'slug'],
        }),
        ('publish', {
            'fields': [
                'date_created', 'date_published',
                'is_published', 'private'],
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
            'fields': ['journal_tags'],
        }),
    ]


@admin.register(JournalSection)
class JournalSectionAdmin(admin.ModelAdmin):

    list_display = ['name', 'private', 'entries']
    list_filter = ['private']
    list_display_links = ['name', 'private', 'entries']

    def entries(self, obj):
        return obj.entries.count()
