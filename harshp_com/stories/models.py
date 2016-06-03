from django.db import models
from subdomains.utils import reverse
from django.utils import timezone
import markdown

from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_formatting
from utils.models import get_unique_slug
from sitebase.models import Post


class StorySeries(models.Model):
    """A series of stories on harshp_com"""

    title = models.CharField(max_length=128, db_index=True)
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)

    class Meta(object):

        ordering = ['title']
        verbose_name = 'Story Series'
        verbose_name_plural = 'Story Series'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                StorySeries, self, 'title', title=self.title)
        return super(StorySeries, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('stories:series', args=[self.slug], subdomain='stories')


class Story(Post):
    """A story on harshp_com"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()
    headerimage = models.URLField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(default=False, db_index=True)
    series = models.ForeignKey(
        StorySeries,
        blank=True, null=True, default=None, db_index=True)

    class Meta(object):

        verbose_name = 'Story'
        verbose_name_plural = 'Stories'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Story, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(Story, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.series:
            return reverse(
                'stories:story',
                args=[self.series.slug, self.slug], subdomain='stories')
        return reverse('stories:story', args=[self.slug], subdomain='stories')

    def get_seo_meta(self):
        """get meta properties for this object"""
        meta = super(Story, self).get_seo_meta()
        if self.headerimage:
            meta['image'] = self.headerimage
        return meta
