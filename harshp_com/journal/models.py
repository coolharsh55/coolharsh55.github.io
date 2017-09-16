from django.db import models
from django.utils import timezone
import markdown
from django.core.urlresolvers import reverse
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
            args=[self.slug])


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
            args=[self.slug])


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
            args=[self.id])


# class Chain(models.Model):
#     '''represents a chain in don't break the chain'''

#     title = models.CharField(max_length=256)
#     message = models.CharField(max_length=256)
#     public = models.BooleanField(default=False)
#     started_on = models.DateField()
#     total = models.PositiveSmallIntegerField(default=0)
#     current_length = models.PositiveSmallIntegerField(default=0)
#     max_length = models.PositiveSmallIntegerField(default=0)

#     class Meta(object):
#         ordering = ['title']
#         verbose_name = 'Chain'
#         verbose_name_plural = 'Chains'

#     def __str__(self):
#         return self.title
    
#     def save(self, *args, **kwargs):
#         # if the current chain length is greater than the maximum length,
#         # update the maximum length
#         if self.current_length > self.max_length:
#             self.max_length = self.current_length
#         return super(Chain, self).save(*args, **kwargs)

    
# class ChainRecord(models.Model):
#     '''represents a record in don't break the chain'''

#     date = models.DateField(db_index=True)
#     action = models.BooleanField(db_index=True, default=False)
#     chain = models.ForeignKey(Chain, related_name='records', db_index=True)

#     class Meta(object):
#         ordering = ['-date']
#         verbose_name = 'Chain Record'
#         verbose_name_plural = 'Chain Records'
#         unique_together = ('date', 'chain')

#     def __str__(self):
#         return '{action}-{date}-{chain}'.format(
#                 action=self.action,
#                 date=self.date,
#                 chain=self.chain.title)

#     def save(self, *args, **kwargs):
#         # if the action is true, then increment the chain records
#         if self.pk:
#             # if this is not a new object, get its previous iteration
#             previous_iteration = ChainRecord.objects.get(
#                     date=self.date, chain=self.chain)
#             # check whether there are any differences in the action
#             if self.action != previous_iteration.action:
#                 # if the current action is true, then the previous was false
#                 if self.action:
#                     # increment the chain length
#                     self.chain.current_length += 1
#                 # otherwise the current action is false, previous true
#                 else:
#                     # decrement the chain length
#                     self.chain.current_length -= 1
#         else:
#             # this is a new object, therefore, only increment the chain
#             # length when the current action is true
#             if self.action:
#                 self.chain.current_length += 1
#             # increment the chain total length
#             self.chain.total += 1
#         # finally, save the chain
#         self.chain.save()
#         return super(ChainRecord, self).save(*args, **kwargs)
