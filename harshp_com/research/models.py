from django.db import models

from django.utils import timezone
import markdown
from django.core.urlresolvers import reverse
from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_formatting
from utils.models import get_unique_slug
from sitebase.models import Post


class ResearchBlogSeries(models.Model):
    """A series of blog posts on harshp_com"""

    title = models.CharField(max_length=128, db_index=True)
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)

    class Meta(object):

        ordering = ['title']
        verbose_name = 'Research Blog Series'
        verbose_name_plural = 'Research Blog Series'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                ResearchBlogSeries, self, 'title', title=self.title)
        return super(ResearchBlogSeries, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
        	'research:blog:series', args=[self.slug])


class ResearchBlogPost(Post):
    """A blog post on harshp_com"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()
    headerimage = models.URLField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(default=False, db_index=True)
    series = models.ForeignKey(ResearchBlogSeries, db_index=True)

    class Meta(object):

        verbose_name = 'Research Blog Post'
        verbose_name_plural = 'Research Blog Posts'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                ResearchBlogPost, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(ResearchBlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'research:blog:post',
            args=[self.series.slug, self.slug])

    def get_seo_meta(self):
        """get meta properties for this object"""
        meta = super(ResearchBlogPost, self).get_seo_meta()
        if self.headerimage:
            meta['image'] = self.headerimage
        return meta
