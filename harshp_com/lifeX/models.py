from django.db import models

from django.utils import timezone
import markdown
from django.core.urlresolvers import reverse
from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_all
from utils.models import get_unique_slug
from utils.lifeX import week_dates
from sitebase import ratings

from sitebase.models import Post, Tag


class LifeXWeek(models.Model):
    """LifeX Week"""

    number = models.AutoField(
        primary_key=True, verbose_name='week#', db_index=True)
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)

    def __str__(self):
        return 'W{week}: {start} - {end}'.format(
            week=self.number, start=self.date_start, end=self.date_end)

    def save(self, *args, **kwargs):
        next_number = LifeXWeek.objects.all().count() + 1
        self.date_start, self.date_end = week_dates(next_number)
        return super(LifeXWeek, self).save(*args, **kwargs)

    class Meta:
        ordering = ['number']
        get_latest_by = 'number'
        verbose_name = "LifeX Week"
        verbose_name_plural = "LifeX Weeks"

    def get_absolute_url(self):
        return reverse(
            'lifeX:experiments:week', args=[self.number])


class LifeXCategory(models.Model):
    """LifeX Idea Category"""

    name = models.CharField(max_length=150)
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "LifeX Idea Category"
        verbose_name_plural = "LifeX Idea Categories"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                LifeXCategory, self, 'name', name=self.name)
        return super(LifeXCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'lifeX:ideas:category', args=[self.slug])


class LifeXIdea(models.Model):
    """LifeX Idea"""

    title = models.CharField(max_length=128)
    category = models.ForeignKey(
        LifeXCategory, related_name='ideas', db_index=True)
    short_description = models.CharField(max_length=150)
    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    description = models.TextField(blank=True, null=True)
    body_text = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True)
    tried = models.BooleanField(default=False, db_index=True)
    retry = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        strrep = '{idea} ({category})'.format(
            idea=self.title, category=self.category.name)
        if self.tried:
            if self.retry:
                suffix = '(retry)'
            else:
                suffix = ''
        else:
            suffix = '(todo)'
        return '{} {}'.format(strrep, suffix)

    class Meta:
        verbose_name = "LifeX Idea"
        verbose_name_plural = "LifeX Ideas"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                LifeXIdea, self, 'title', title=self.title)
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.description, extensions=ext_all, output_format='html5')
        else:
            self.body_text = self.description
        return super(LifeXIdea, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'lifeX:ideas:idea',
            args=[self.category.slug, self.slug])


class LifeXExperiment(Post):
    """LifeX Experiment
    Occurs on a specific Week with a Idea"""

    week = models.ForeignKey(
        LifeXWeek, related_name='experiments', db_index=True)
    idea = models.ForeignKey(
        LifeXIdea, related_name='experiments', db_index=True)
    rating = models.IntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    premise = models.TextField()
    premise_body = models.TextField(blank=True)
    outcome = models.TextField(blank=True, null=True)
    outcome_body = models.TextField(blank=True, null=True)

    def __str__(self):
        return '(W#{week}) {title}'.format(
            week=self.week.number, title=self.title)

    class Meta:
        verbose_name = 'LifeX Experiment'
        verbose_name_plural = 'LifeX Experiments'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                LifeXExperiment, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.premise_body = markdown.markdown(
                self.premise, extensions=ext_all, output_format='html5')
            self.outcome_body = markdown.markdown(self.outcome, extensions=[
                'markdown.extensions.abbr',
                # 'markdown.extensions.codehilite',
                'markdown.extensions.smarty',
            ], output_format='html5')
        else:
            self.premise_body = self.premise
            self.outcome_body = self.outcome
        return super(LifeXExperiment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'lifeX:experiments:experiment',
            args=[self.week.number, self.slug])


class LifeXGoal(models.Model):
    """LifeX Goal - what I want to do  in life"""

    title = models.CharField(max_length=128)
    parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=150, unique=True, blank=True, db_index=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'LifeX Goal'
        verbose_name_plural = 'LifeX Goals'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                LifeXGoal, self, 'title', title=self.title)
        return super(LifeXGoal, self).save(*args, **kwargs)


class LifeXBlog(Post):
    """A blog post for lifeX on harshp_com"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()

    class Meta(object):

        verbose_name = 'LifeX Blog Post'
        verbose_name_plural = 'LifeX Blog Posts'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                LifeXBlog, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_all, output_format='html5')
        else:
            self.body_text = self.body
        return super(LifeXBlog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('lifeX:blog:post', args=[self.slug])
