from django.db import models
from subdomains.utils import reverse
from django.utils import timezone
import markdown

from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_formatting
from utils.models import get_unique_slug
from sitebase.models import Post


class DevSection(models.Model):
    """Dev section"""


    # section types
    DEFAULT = 'default'
    RESOURCES = 'res'
    GUIDES_TUTORIALS = 'guide'
    DISCUSSION = 'discuss'
    MYSTACK = 'mystack'
    PROJECT = 'project'
    SECTION_TYPES = (
        (DEFAULT, 'default'),
        (RESOURCES, 'resources'),
        (GUIDES_TUTORIALS, 'guides & tutorials'),
        (DISCUSSION, 'discussions'),
        (MYSTACK, 'my stack'),
        (PROJECT, 'projects'))

    title = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)
    section_type = models.CharField(
        max_length=8, choices=SECTION_TYPES, default=DEFAULT, 
        db_index=True)

    class Meta(object):
        ordering = ['title']
        verbose_name = 'dev section'
        verbose_name_plural = 'dev sections'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                DevSection, self, 'title', title=self.title)
        return super(DevSection, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dev:section', args=[self.slug], subdomain='dev')


class DevPost(Post):
    """A dev post"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()
    headerimage = models.URLField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(default=False, db_index=True)
    section = models.ForeignKey(DevSection, db_index=True)

    class Meta(object):

        verbose_name = 'dev post'
        verbose_name_plural = 'dev posts'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                DevPost, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(DevPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'dev:post',
            args=[self.section.slug, self.slug], subdomain='dev')

    def get_seo_meta(self):
        """get meta properties for this object"""
        meta = super(DevPost, self).get_seo_meta()
        if self.headerimage:
            meta['image'] = self.headerimage
        return meta
