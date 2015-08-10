"""admin configuration for brainbank

    BrainBankIdea: BrainBankIdeaAdmin
    BrainBankPost: BrainBankPostAdmin
    BrainBankDemo: BrainBankDemoAdmin
"""

from django.contrib import admin
from brainbank.models import BrainBankIdea
from brainbank.models import BrainBankPost
from brainbank.models import BrainBankDemo


@admin.register(BrainBankIdea)
class BrainBankIdeaAdmin(admin.ModelAdmin):

    """Admin for BrainBank Ideas
    List: ID, Title, Published, No of posts, No of demos
    Form: ID, Title, Published, Body
    Search: Title
    """
    list_display = (
        'id',
        'title',
        'published',
        'posts',
        'demos',
        'repo',
    )
    ordering = (
        '-published',
    )
    search_fields = (
        'title',
        'repo',
    )
    date_hierarchy = 'published'
    readonly_fields = (
        'id',
    )
    prepopulated_fields = {
        "slug": (
            "title",
        )
    }
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'id',
                'title',
                'slug',
                'published',
                'repo',
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

    def posts(self, obj):
        """posts count

        count of posts associated with idea

        Args:
            self(BrainBankIdeaAdmin)
            obj(BrainBankIdea)

        Returns:
            int: no of posts associated with idea

        Raises:
            None
        """
        return obj.brainbankpost_set.count()

    def demos(self, obj):
        """demos count

        count of demos associated with idea

        Args:
            self(BrainBankIdeaAdmin)
            obj(BrainBankIdea)

        Returns:
            int: no of demos associated with idea

        Raises:
            None
        """
        return obj.brainbankdemo_set.count()


@admin.register(BrainBankPost)
class BrainBankPostAdmin(admin.ModelAdmin):

    """
    Admin for BrainBank Posts
    List: ID, Title, Published, Idea
    Form: ID, Title, Published, Idea, Body, Tags
    Search: Title, Idea
    Filter: Idea, Tags
    """
    list_display = (
        'id',
        'title',
        'published',
        'idea',
    )
    ordering = (
        '-published',
        'title',
        'idea',
    )
    search_fields = (
        'title',
        'idea',
    )
    date_hierarchy = 'published'
    list_filter = (
        'idea__title',
        'tags',
    )
    filter_horizontal = (
        'tags',
    )
    readonly_fields = (
        'id',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'id',
                'title',
                'published',
                'slug',
                'idea',
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


@admin.register(BrainBankDemo)
class BrainBankDemoAdmin(admin.ModelAdmin):

    """
    Admin for BrainBank Demos
    List: ID, Title, Idea
    Form: ID, Title, Idea, Body, CSS, JS
    Search: Title, Idea
    Filter: Idea
    """
    list_display = (
        'id',
        'title',
        'idea',
    )
    ordering = (
        'idea',
        'title',
    )
    search_fields = (
        'title',
        'idea',
    )
    list_filter = (
        'idea',
    )
    readonly_fields = (
        'id',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'id',
                'title',
                'slug',
                'idea',
            )
        }),
        ('Content', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': (
                'body',
            )
        }),
        ('css', {
            'classes': ('full-width',),
            'fields': (
                'css',
            )
        }),
        ('js', {
            'classes': ('full-width',),
            'fields': (
                'js',
            )
        }),
    )
