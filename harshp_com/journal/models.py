from django.db import models
from subdomains.utils import reverse
from django.utils import timezone
import markdown

from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_formatting
from utils.models import get_unique_slug

from sitebase.models import Post


class JournalTag(models.Model):
    """Tag specific to Journal.
    Repeated model (sitebase.Tag) to keep the journal tags separate from
    the other tags used elsewhere on the site."""

    name = models.CharField(max_length=128, db_index=True, unique=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    slug = models.SlugField(
        max_length=150, db_index=True, unique=True, blank=True)

    class Meta:

        ordering = ['name']
        verbose_name = 'Journal Tag'
        verbose_name_plural = 'Journal Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                JournalTag, self, 'name', name=self.name)
        return super(JournalTag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'journal:tags:get',
            args=[self.slug], subdomain='journal')


class JournalSection(models.Model):
    """Section of the Journal.
    Contains topic-specific entries."""

    name = models.CharField(max_length=128, db_index=True, unique=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    slug = models.SlugField(
        max_length=150, db_index=True, unique=True, blank=True)
    private = models.BooleanField(default=True, db_index=True)

    class Meta:

        ordering = ['name']
        verbose_name = 'Journal Section'
        verbose_name_plural = 'Journal Sections'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                JournalSection, self, 'name', name=self.name)
        return super(JournalSection, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'journal:sections:get',
            args=[self.slug], subdomain='journal')


class JournalEntry(Post):
    """Journal Entry.
    Can belong to a section."""

    private = models.BooleanField(default=True, db_index=True)
    journal_tags = models.ManyToManyField(JournalTag, related_name='entries')
    section = models.ForeignKey(
        JournalSection,
        related_name='entries', blank=True, null=True, db_index=True)
    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()

    class Meta:

        ordering = ['date_created']
        get_latest_by = 'date_published'
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'

    def __str__(self):
        return '#{} - {}'.format(self.section_id, self.date_published)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(JournalEntry, self, 'title')
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(JournalEntry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'journal:entries:get',
            args=[self.id], subdomain='journal')
