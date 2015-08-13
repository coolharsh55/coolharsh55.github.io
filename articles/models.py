"""ARTICLE MODELS

    Article
"""

from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.utils.text import slugify
from subdomains.utils import reverse


class Article(models.Model):

    """Article

        post id: primary key, autoincrement
        title: length=250
        body: ckeditor
        published(date)
        modified(date)
        tags: sitedata.Tag
        slug: slugfield
        headerimage: image displayed at top of post
    """
    # basic post
    post_id = models.AutoField(
        primary_key=True,
        verbose_name='Post #',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Article Title'
    )
    body = RichTextField()
    published = models.DateTimeField(
        verbose_name='Published',
    )

    # additional stuff
    modified = models.DateTimeField(
        blank=True,
        verbose_name='Last Modified',
    )
    tags = models.ManyToManyField(
        'sitedata.Tag',
        verbose_name='Tags',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    headerimage = models.URLField(
        max_length=200,
        blank=True,
        verbose_name='Header Image',
    )

    def __str__(self):
        """Article string representation

        return title as string representation

        Args:
            self: Article object

        Returns:
            (str): title of article

        Raises:
            None
        """
        return self.title

    class Meta:

        """verbose names for articles
        """
        verbose_name = 'Article post'
        verbose_name_plural = 'Article posts'

    def save(self, *args, **kwargs):
        """save articles to database

        check for duplicates, and update modified timestamps

        Args:
            self: article object
            *args: arguments
            **kwargs: parameters

        Returns:
            calls Article.super()

        Raises:
            None
        """
        if not self.post_id:
            self.created = timezone.now()
            dup = Article.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title[:50])
        self.modified = timezone.now()

        return super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='articles:post',
            subdomain='articles',
            kwargs={'article': self.slug, })
