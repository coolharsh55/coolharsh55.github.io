"""sitedata models

    Tag
"""

from django.db import models


class Tag(models.Model):

    """    Tag - meta for models
    """
    tagid = models.AutoField(primary_key=True)
    tagname = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150)

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

"""
# Future work
# User class
# Author relationship
# Comments class
# associate comments with each post
# page -> would be a template? auto-add related entries
# |-> create a specific tag and list that in the templates
"""
