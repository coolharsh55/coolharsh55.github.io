"""sitedata models

    Tag
"""

from django.db import models
from django.utils.text import slugify
from subdomains.utils import reverse


class Tag(models.Model):

    """    Tag - meta for models
    """
    tagid = models.AutoField(primary_key=True)
    tagname = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        """string representation for tags

        Args:
            self(Tag)

        Returns:
            str: tag name

        Raises:
            None
        """
        return self.tagname

    class Meta:

        """attributes for tag
        """
        ordering = ('tagname',)

    def save(self, *args, **kwargs):
        """save tags to database

        check for duplicates, and update modified timestamps

        Args:
            self(Tag)
            *args: arguments
            **kwargs: parameters

        Returns:
            return from Tag.super()

        Raises:
            None
        """
        self.slug = slugify(self.tagname)

        return super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='sitedata:tagname',
            subdomain='www',
            kwargs={'tagname': self.slug, })

"""
# Future work
# User class
# Author relationship
# Comments class
# associate comments with each post
# page -> would be a template? auto-add related entries
# |-> create a specific tag and list that in the templates
"""
