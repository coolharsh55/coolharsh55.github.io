"""models for stories

    StoryPost
"""

from django.db import models
from ckeditor.fields import RichTextField

from django.utils import timezone
from django.utils.text import slugify


class StoryPost(models.Model):

    """Story post
    """
    # basic post
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250,)
    body = RichTextField()
    published = models.DateTimeField()

    # additional stuff
    modified = models.DateTimeField()
    tags = models.ManyToManyField('sitedata.Tag')
    slug = models.CharField(max_length=50, unique=True)
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
            self.created = timezone.now()
            dup = StoryPost.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title[:50])
        self.modified = timezone.now()

        return super(StoryPost, self).save(*args, **kwargs)
