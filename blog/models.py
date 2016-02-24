"""Models for Blog
"""

from django.db import models
from django.utils import timezone
from redactor.fields import RedactorField
from subdomains.utils import reverse

from harshp.utils.duplicates import duplicate_slug


class BlogPost(models.Model):

    """BlogPost

    single blog post

    post id: primary key, autoincrements
    title(str): length=250
    body: ckeditor field
    published(date)
    modified(date)
    tags: sitedata.Tag
    slug(slugfield)
    headerimage(url): image at top of post
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
    headerimage = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """string representation of blog post

        Args:
            self(BlogPost)

        Returns:
            str: title of blog post

        Raises:
            None
        """
        return self.title

    class Meta:

        """verbose name for blog posts
        """
        verbose_name = 'Blog post'
        verbose_name_plural = 'Blog posts'

    def save(self, *args, **kwargs):
        """save blog post to database

        check for duplicates, and update modified timestamps

        Args:
            self(BlogPost)
            *args: arguments
            **kwargs: parameters

        Returns:
            BlogPost.super()

        Raises:
            None
        """
        if not self.post_id:
            self.published = timezone.now()
        self.slug = duplicate_slug(self, self.title, title=self.title)
        self.modified = timezone.now()

        return super(BlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='blog:post',
            subdomain='blog',
            kwargs={'blogpost': self.slug, })
