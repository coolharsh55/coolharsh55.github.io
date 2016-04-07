from django.db import models
from subdomains.utils import reverse
from django.utils import timezone
import markdown

from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_all
from utils.models import get_unique_slug
from sitebase.models import Post


class BrainbankIdea(models.Model):
    """represents an idea"""

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=256, db_index=True)
    short_description = models.CharField(max_length=150)
    body_type = models.CharField(
        max_length=8,
        choices=EDITOR_TYPES, default='markdown', db_index=True)
    body = models.TextField()
    body_text = models.TextField(blank=True)
    repo = models.URLField(
        max_length=512, blank=True, null=True, db_index=True)

    class Meta:
        ordering = ['title', 'slug']
        verbose_name = 'BrainBank idea'
        verbose_name_plural = 'BrainBank Ideas'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(BrainbankIdea, self, 'title')
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_all, output_format='html5')
        else:
            self.body_text = self.body
        return super(BrainbankIdea, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'brainbank:idea', args=[self.slug], subdomain='brainbank')


class BrainbankPost(Post):
    """represents a post about an idea"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()
    headerimage = models.URLField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(default=False, db_index=True)
    deliverable = models.BooleanField(default=False, db_index=True)
    idea = models.ForeignKey(
        BrainbankIdea, related_name='posts', db_index=True)

    class Meta(object):

        verbose_name = 'BrainBank Idea Post'
        verbose_name_plural = 'BrainBank Idea Posts'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(BrainbankPost, self, 'title')
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_all, output_format='html5')
        else:
            self.body_text = self.body
        super(BrainbankPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'brainbank:post',
            args=[self.idea.slug, self.slug], subdomain='brainbank')

    def get_seo_meta(self):
        """get meta properties for this object"""
        return super(BrainbankPost, self).get_seo_meta()
