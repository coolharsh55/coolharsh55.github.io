"""models for stories

    StoryPost
"""

from django.db import models
from redactor.fields import RedactorField
from subdomains.utils import reverse
from django.utils import timezone

from harshp.utils.duplicates import duplicate_slug


class StoryPost(models.Model):

    """Story post
    """
    # basic post
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250,)
    body = RedactorField()
    published = models.DateTimeField()

    # additional stuff
    modified = models.DateTimeField(blank=True,)
    tags = models.ManyToManyField('sitedata.Tag')
    slug = models.CharField(max_length=250, blank=True, unique=True)
    headerimage = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """string representation of story
        """
        return self.title

    class Meta:

        """verbose name for stories
        """
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'

    def save(self, *args, **kwargs):
        """save story post to database

        check for duplicates
        """
        if not self.post_id:
            self.published = timezone.now()
        self.slug = duplicate_slug(self, self.title, title=self.title)
        self.modified = timezone.now()

        return super(StoryPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='stories:post',
            subdomain='stories',
            kwargs={'story': self.slug, })
