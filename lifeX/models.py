"""models for LifeX

    LifeXWeek
    LifeXIdea
    LifeXCategory
    LifeXPost
    LifeXBlog
"""

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from datetime import datetime, timedelta
from django.utils.text import slugify
from subdomains.utils import reverse


def lifex_start_date():
    """lifeX start date

    The date for when LifeX started. All weeks are calculated relative
    to this date

    Args:
        None

    Returns:
        DateTime: 2014-03-24 (25 Mar'14)

    Raises:
        None
    """
    return datetime(2014, 03, 24)


class LifeXWeek(models.Model):

    """Represents a LifeX Week
    A Week represents a date-week, starting from MONDAY to the
    following SUNDAY. Week numbers start from Week#1 representing
    2014-MAR-08.
    Each Week can have multiple Ideas associated with it, and each
    Idea can have multiple Posts associated with it.
    """
    number = models.AutoField(
        primary_key=True,
        verbose_name='Week#'
    )

    def __str__(self):
        """string representation of week

        Args:
            self(LifeXWeek)

        Returns:
            str: W123: 01-JUN-2015 to 07-JUN-2015
        """
        return ''.join((
            'Week',
            str(self.number),
            ': ',
            self._start_week(),
            ' to ',
            self._end_week()
        ))

    def _start_week(self):
        """Start of the current week

        calculate the starting of week based on its number

        Args:
            self(LifeXWeek)

        Returns:
            str: start date

        Raises:
            None
        """
        return LifeXWeek.str_week(
            lifex_start_date() + timedelta(weeks=self.number - 1)
        )

    def _end_week(self):
        """End of the current week

        calculate the ending of week based on its number

        Args:
            self(LifeXWeek)

        Returns:
            str: end date

        Raises:
            None
        """
        return LifeXWeek.str_week(
            lifex_start_date() + timedelta(weeks=self.number, days=-1)
        )

    @staticmethod
    def str_week(date):
        """string representation of current week

        format string as DD-MON-YYYY

        Args:
            self(LifeXWeek)

        Returns:
            str: date

        Raises:
            None
        """
        return date.strftime('%d-%b-%Y')

    class Meta:

        """verbose name for lifex weeks
        """
        verbose_name = 'LifeX Week'
        verbose_name_plural = 'LifeX Weeks'

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='lifeX:week',
            subdomain='lifex',
            kwargs={'week': self.number, })


class LifeXCategory(models.Model):

    """
    Represents a LifeX Idea Category
    A Category can have many different Ideas, and acts as away
    to categorize the various Ideas.
    """
    name = models.CharField(
        max_length=250,
        unique=True
    )
    slug = models.SlugField(
        max_length=250,
        unique=True
    )

    class Meta:

        """verbose names for lifex categories
        """
        verbose_name = 'LifeX Idea Category'
        verbose_name_plural = 'LifeX Idea Categories'

    def __str__(self):
        """string representation of category

        Args:
            self(LifeXCategory)

        Returns:
            str: category name

        Raises:
            None
        """
        return self.name

    def save(self, *args, **kwargs):
        """save category object to database

        Check for duplicate before saving

        Args:
            self(LifeXCategory)
            *args: arguments
            **kwargs: parameters

        Returns:
            LifeXCategory.super()

        Raises:
            None
        """
        if not self.pk:
            # check if slug is a duplicate
            dup = LifeXCategory.objects.filter(name=self.name)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.name[:249 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.name[:250])
        return super(LifeXCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='lifeX:category',
            subdomain='lifex',
            kwargs={'category': self.slug, })


class LifeXIdea(models.Model):

    """Represents a LifeX Idea
    An Idea is something that should be experimented on. It is just
    a string representing what the idea is all about, and a body for
    more details.
    Each Idea has a boolean counter for if it has been tried, and if
    it needs to be retried.
    """
    idea_id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        max_length=250,
    )
    body = RichTextField()
    tags = models.ManyToManyField('sitedata.Tag', blank=True,)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    experimented = models.BooleanField(
        default=False,
        verbose_name='tried',
    )
    retry = models.BooleanField(
        default=False,
        verbose_name='retry?',
    )
    category = models.ForeignKey(LifeXCategory)
    published = models.DateTimeField()
    modified = models.DateTimeField(blank=True,)

    def __str__(self):
        """string representation of idea

        If the idea is to be retried, append 'try again'
        Else if the idea has been experimented with, append 'done'
        Else append 'todo'

        Args:
            self(LifeXIdea)

        Returns:
            str: idea title prepended by status

        Raises:
            None
        """
        if self.retry:
            return '(try again) ' + self.title
        elif self.experimented:
            return '(tried) ' + self.title
        else:
            return '(todo) ' + self.title

    def save(self, *args, **kwargs):
        """save idea to database

        Set status based on retry and experimented
        Check for duplicates before saving

        Args:
            self(LifeXIdea)
            *args: arguments
            **kwargs: parameters

        Returns:
            LifeXIdea.super()

        Raises:
            None
        """
        if self.retry and not self.experimented:
            self.retry = False
        if not self.idea_id:
            # check if slug is a duplicate
            dup = LifeXIdea.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title)
        self.modified = timezone.now()
        super(LifeXIdea, self).save(*args, **kwargs)

    class Meta:

        """verbose names for ideas
        """
        verbose_name = 'LifeX Idea'
        verbose_name_plural = 'LifeX Ideas'
        ordering = ['title', ]

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='lifeX:idea',
            subdomain='lifex',
            kwargs={'category': self.category.slug, 'idea': self.slug, })


# TODO: reduce LifeX to empty class
# class LifeX(models.Model):
#     # basic post
#     post_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=250,)
#     body = RichTextField()
#     published = models.DateTimeField()

#     # additional stuff
#     modified = models.DateTimeField()
#     tags = models.ManyToManyField('sitedata.Tag')
#     headerimage = models.URLField(max_length=200,blank=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = 'Life Experiment'
#         verbose_name_plural = 'Life Experiments'

#     def save(self, *args, **kwargs):
#         ''' On save, update timestamps '''
#         if not self.post_id:
#             self.created = timezone.now()
#         self.modified = timezone.now()
#         return super(LifeX, self).save(*args, **kwargs)

class LifeXPost(models.Model):

    """
    Represents a LifeX Post
    A Post can be published multiple times per week or per idea
    Each Post is associated with a particular Week, and a particular
    Idea associated with that Week.
    """
    post_id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        max_length=250,
    )
    body = RichTextField()
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    published = models.DateField()
    modified = models.DateTimeField(blank=True,)
    tags = models.ManyToManyField('sitedata.Tag')
    week = models.ForeignKey(LifeXWeek)
    idea = models.ForeignKey(LifeXIdea)

    def __str__(self):
        """string representation of life x post

        W123: LifeX Django project

        Args:
            self(LifeXPost)

        Returns:
            str: W week number: post title

        Raises:
            None
        """
        return 'W' + str(self.week.number) + ': ' + self.title

    class Meta:

        """verbose name for lifex posts
        """
        verbose_name = 'LifeX Post'
        verbose_name_plural = 'LifeX Posts'

    def save(self, *args, **kwargs):
        """save lifex posts to database

        Check for duplicates before saving

        Args:
            self(LifeXPost)
            *args: arguments
            **kwargs: parameters

        Returns:
            LifeXPost.super()

        Raises:
            None
        """
        if not self.post_id:
            # check if slug is a duplicate
            dup = LifeXPost.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(
                    'W' + self.title)[:49 - len(dup)] + '-' + nos
            else:
                self.slug = slugify(
                    'W' + str(self.week.number) + '-' + self.title)[:50]
        self.modified = timezone.now()
        return super(LifeXPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='lifeX:post',
            subdomain='lifex',
            kwargs={'week': self.week.number, 'idea': self.idea.slug, })


class LifeXBlog(models.Model):

    """
    Represents a LifeX Blog Post
    This will contain news, reviews, articles and thoughts about
    Life Experiments. These are not related to any particular
    experiment or idea or week or category.
    """
    post_id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        max_length=250,
    )
    body = RichTextField()
    headerimage = models.URLField(max_length=200, blank=True)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    published = models.DateField()
    modified = models.DateTimeField(blank=True,)
    tags = models.ManyToManyField('sitedata.Tag')

    def __str__(self):
        """string representation of lifex blog

        Args:
            self(LifeXBlog)

        Returns:
            str: blog title

        Raises:
            None
        """
        return self.title

    class Meta:

        """verbose nameing for lifex blog
        """
        verbose_name = 'LifeX Blog'
        verbose_name_plural = 'LifeX Blog'

    def save(self, *args, **kwargs):
        """save lifex blog to database

        Check for duplicates before saving

        Args:
            self(LifeXBlog)
            *args: arguments
            **kwargs: parameters

        Returns:
            LifeXBlog.super()

        Raises:
            None
        """
        if not self.post_id:
            # check if slug is a duplicate
            dup = LifeXBlog.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title)[:50]
        self.modified = timezone.now()
        return super(LifeXBlog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='lifeX:blogpost',
            subdomain='lifex',
            kwargs={'blogpost': self.slug, })
