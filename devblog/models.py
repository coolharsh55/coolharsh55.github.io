from django.db import models
from django.utils import timezone
from django.utils.text import slugify

import pytz
from redactor.fields import RedactorField
from subdomains.utils import reverse

# from sitedata.models import CSSLink
from sitedata.models import JSLink

# TODO: can posts be duplicates if series are different?
# post 'title' in one series can be different than
# post 'title' in another series
# str should return title
# display should contain series if present
# like 'title (series)'
# or (series) title
#
# TODO: first write tests for all classes and views and urls
# TODO: then write views, complete views
# TODO: then write templates


class DevBlogPost(models.Model):

    """dev blog post

    has normal attributes as a blog post, plus some special fields for
    linking dev related stuff

    flags:
        draft: denotes that this post is a draft, and must not be published
        future: denotes the future date of publishing for the post

    the combination of draft (D) and future (F) flags:
    _________________________________________________________________
    |=D=|=F=|===================comment=============================|
    -----------------------------------------------------------------
    | T | F | just a regular draft                                  |
    | T | T | a draft with a future date set, future date is ignored|
    | F | F | published post, date must be in past                  |
    | F | T | finished post, published in future                    |
    ----------------------------------------------------------------|
    """

    # basic post
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250,)
    body = RedactorField()
    published = models.DateTimeField()
    series = models.ForeignKey(
        'devblog.DevBlogSeries', blank=True, null=True)

    # additional stuff
    modified = models.DateTimeField(blank=True,)
    tags = models.ManyToManyField('sitedata.Tag')
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    headerimage = models.URLField(max_length=200, blank=True, null=True)

    # customcss
    css = models.ManyToManyField('sitedata.CSSLink', blank=True,)
    # customjs
    js = models.ManyToManyField('sitedata.JSLink', blank=True,)

    # draft
    draft = models.BooleanField(default=False)

    # future publishing
    future = models.DateTimeField(blank=True, null=True)

    class Meta(object):
        verbose_name = 'dev blog post'
        verbose_name_plural = 'dev blog posts'

    def __str__(self):
        """return post name

        Args:
            self: instance of DevBlogPost

        Returns:
            str: title

        Raises:
            None
        """
        return self.title

    def get_absolute_url(self):
        """url for dev blog post

        Args:
            self: instance of DevBlogPost

        Returns:
            url: reverse for name 'blogpost'

        Raises:
            None
        """
        series_slug = 'blog' if self.series is None else self.series.slug
        return reverse(
            viewname='devblog:blog_post',
            subdomain='dev',
            kwargs={'series': series_slug, 'blog_post': self.slug, })

    def save(self, *args, **kwargs):
        """save post

        Args:
            self: instance of DevBlogPost
            args: positional arguments
            kwargs: keyword arguments

        Returns:
            calls super.save()

        Raises:
            ValueError:
                incorrect condition where draft is not set,
                but date is in future
        """
        if self.future:
            if timezone.is_naive(self.future):
                self.future = self.future.replace(tzinfo=pytz.UTC)
            if self.future <= timezone.now():
                # the 'future' date isn't set in the future!
                raise ValueError('The future date is not in the future!')

        # use prettify if post contains code
        if '/code' in self.body:
            js = JSLink.objects.get(name='code-prettify')
            if js not in self.js.all():
                self.js.add(js)

        if not self.pk:
            # check for duplicates
            duplicates = DevBlogPost.objects.filter(title=self.title)
            if len(duplicates) > 0:
                # duplicates exist
                self.slug = slugify(
                    self.title[-len(str(duplicates)):] + str(duplicates))
            else:
                self.slug = slugify(self.title)
        self.modified = timezone.now()

        # check for duplicates
        # duplicate post within same series is not allowed
        post = DevBlogPost.objects.filter(
            series=self.series,
            title=self.title,
        )
        if len(post) == 1 and self.pk is not None:
            # self is not a duplicate of itself
            pass
        elif len(post) > 0:
            raise AssertionError('Duplicates are not allowed in series')

        super(DevBlogPost, self).save(*args, **kwargs)


class DevBlogSeries(models.Model):

    """dev blog series - a collection of dev blog posts

    all grouped together under a common topic,
    subject, or just a stack of posts
    """

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = RedactorField()

    class Meta(object):
        verbose_name = 'dev blog series'
        verbose_name_plural = 'dev blog series'

    def __str__(self):
        """return series name

        Args:
            self: instance of DevBlogSeries

        Returns:
            str: name

        Raises:
            None
        """
        return self.name

    def save(self, *args, **kwargs):
        """save series

        check if at least one post is present

        Args:
            self: instance of DevBlogSeries
            args: positional arguments
            kwargs: keyword arguments

        Returns:
            calls super.save()

        Raises:
            ValueError:
                series has no posts
        """
        if not self.pk:
            self.slug = slugify(self.name)

        super(DevBlogSeries, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """url for dev blog series
        """
        return reverse(
            viewname='devblog:blog_series',
            subdomain='dev',
            kwargs={'series': self.slug, })
