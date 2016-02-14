from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone

from sitebase.models import Post

from sitebase.editors import EDITOR_TYPES

from utils.models import get_unique_slug


class BlogSeries(models.Model):
    """A series of blog posts on harshp_com"""

    title = models.CharField(max_length=128, db_index=True)
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)

    class Meta(object):

        ordering = ['title']
        verbose_name = 'Blog Series'
        verbose_name_plural = 'Blog Series'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                BlogSeries, self, 'title', title=self.title)
        super(BlogSeries, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:series', args=[self.slug])


class BlogPost(Post):
    """A blog post on harshp_com"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body = models.TextField()
    headerimage = models.URLField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(default=False)
    series = models.ForeignKey(
        BlogSeries,
        blank=True, null=True, default=None, db_index=True)

    class Meta(object):

        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                BlogPost, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        super(BlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.series:
            return reverse('blog:post', args=[self.series.slug, self.slug])
        return reverse('blog:post', args=[self.slug])
