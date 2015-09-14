from django.db import models
from django.utils import timezone
from django.utils.text import slugify

import pytz
from redactor.fields import RedactorField
from subdomains.utils import reverse

# from sitedata.models import CSSLink
from sitedata.models import JSLink


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
        return reverse(
            viewname='devblog:blog_post',
            subdomain='dev',
            kwargs={'blog_post': self.slug, })

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
        super(DevBlogPost, self).save(*args, **kwargs)


class DevBlogSeries(models.Model):

    """dev blog series - a collection of dev blog posts

    all grouped together under a common topic,
    subject, or just a stack of posts
    """

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    posts = models.ManyToManyField('devblog.DevBlogPost')

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
        # check if series has at least one post
        if self.posts.count() == 0:
            raise ValueError("A series must have at least one post.")

        if not self.pk:
            self.slug = slugify(self.name)

        super(DevBlogSeries, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """url for dev blog series
        """
        return reverse(
            viewname='dev:blog_series',
            subdomain='dev',
            kwargs={'series': self.slug, })
