"""admin for lifeX

    LifeXWeek: LifeXWeekAdmin
    LifeXIdea: LifeXIdeaAdmin
    LifeXCategory: LifeXCategoryAdmin
    LifeXPost: LifeXPostAdmin
    LifeXBlog: LifeXBlogAdmin
"""

from django.contrib import admin
from .models import LifeXWeek, LifeXIdea, LifeXCategory, LifeXPost, LifeXBlog


@admin.register(LifeXWeek)
class LifeXWeekAdmin(admin.ModelAdmin):

    """
    Admin for LifeX Week
    List: Week number, Start date, End date, No of posts
    Form: Nothing (week number is readonly)
    Search: Week number
    """
    list_display = (
        'number',
        'start_date',
        'end_date',
        'posts'
    )
    ordering = (
        '-number',
    )
    search_fields = (
        'number',
    )
    readonly_fields = (
        'number',
    )
    view_on_site = True

    def start_date(self, obj):
        """start date of week

        Args:
        self(LifeXWeekAdmin)
        obj(LifeXWeek)

        Returns:
            Date: starting date of the week

        Raises:
            None
        """
        return obj._start_week()

    def end_date(self, obj):
        """end date of week

        Args:
        self(LifeXWeekAdmin)
        obj(LifeXWeek)

        Returns:
            Date: ending date of the week

        Raises:
            None
        """
        return obj._end_week()

    def posts(self, obj):
        """no of posts

        Total posts associated with a week

        Args:
            self(LifeXWeekAdmin)
            obj(LifeXWeek)

        Returns:
            int: total posts associated with week

        Raises:
            None
        """
        return obj.lifexpost_set.count()


@admin.register(LifeXIdea)
class LifeXIdeaAdmin(admin.ModelAdmin):

    """Admin for LifeX Idea
    List: Id, Title, Experimented?, Retry?, Category
    Ordering: Id, Title, Experimented, Retry
    Filter: Category, Experimented?, Retry?
    Form: (ID is readonly) title, category, experimented, retry, body
    Search: ID, title
    """
    list_display = (
        'idea_id',
        'title',
        'experimented',
        'retry',
        'category',
    )
    ordering = (
        'idea_id',
        'title',
        'experimented',
        'retry',
    )
    search_fields = (
        'idea_id',
        'title',
    )
    list_filter = (
        'category',
        'experimented',
        'retry',
    )
    readonly_fields = (
        'idea_id',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'title',
                'category',
                'experimented',
                'retry',
            )
        }),
        ('Contents', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': (
                'body',
            )
        }),
    )


@admin.register(LifeXCategory)
class LifeXCategoryAdmin(admin.ModelAdmin):

    """
    Admin for LifeX Category
    List: Name, Count of Ideas
    Order: Name
    Search: Name
    Form: Name, Slug
    """
    list_display = (
        'name',
        'ideas'
    )
    ordering = (
        'name',
    )
    search_fields = (
        'name',
    )
    view_on_site = True

    def ideas(self, obj):
        """no of ideas

        count ideas associated with category

        Args:
            self(LifeXCategoryAdmin)
            obj(LifeXCategory)

        Returns:
            int: no of ideas

        Raises:
            None
        """
        return obj.lifexidea_set.count()


@admin.register(LifeXPost)
class LifeXPostAdmin(admin.ModelAdmin):

    """
    Admin for LifeX Posts
    List: ID, Title, Week, Idea, Date
    Order: Date, Week, ID
    Search: Title
    Date: date
    Filter: Tags, Week, Idea
    Form: ID(R), Title, Week(H), Idea(H), Date,
        Body, Tags(H)
    """
    list_display = (
        'post_id',
        'title',
        'week',
        'idea',
        'date',
    )
    ordering = (
        '-date',
        '-week',
        '-post_id',
    )
    search_fields = (
        'title',
    )
    date_hierarchy = 'date'
    list_filter = (
        'tags',
        'week',
        'idea',
    )
    filter_horizontal = (
        'tags',
    )
    readonly_fields = (
        'post_id',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'post_id',
                'title',
                'week',
                'idea',
                'date',
            )
        }),
        ('Contents', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': (
                'body',
            )
        }),
        ('Extras', {
            'classes': ('collapse',),
            'fields': (
                'tags',
            )
        }),
    )


@admin.register(LifeXBlog)
class LifeXBlogAdmin(admin.ModelAdmin):

    """
    Admin for LifeX Blog
    List: ID, Title, Date
    Order: Date, Title
    Search: Title
    Date: date
    Form: ID(R), Title, Date, Body, Tags(H)
    """
    list_display = (
        'post_id',
        'title',
        'date',
    )
    ordering = (
        '-date',
        'title',
    )
    search_fields = (
        'title',
    )
    date_hierarchy = 'date'
    filter_horizontal = (
        'tags',
    )
    readonly_fields = (
        'post_id',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'post_id',
                'title',
                'date',
                'headerimage',
            )
        }),
        ('Contents', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': (
                'body',
            )
        }),
        ('Extras', {
            'classes': ('collapse',),
            'fields': (
                'tags',
            )
        }),
    )
