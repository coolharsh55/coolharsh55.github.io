"""models for Poem

    Poem
"""
from django.db import models
from redactor.fields import RedactorField
from django.utils import timezone
from django.utils.text import slugify
from subdomains.utils import reverse


class Poem(models.Model):

    """Poem

    id: primary key, autoincrement
    title(str): length=250
    body: ckeditor field
    published(datetime)
    modified(datetime)
    tags: sitedata.Tag
    slug(slugfield)
    headerimage(url): image at top of poem
    """

    # basic post
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250,)
    body = RedactorField()
    published = models.DateTimeField()

    # additional stuff
    modified = models.DateTimeField(blank=True,)
    tags = models.ManyToManyField('sitedata.Tag')
    slug = models.CharField(max_length=50, unique=True)
    headerimage = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """string representation of poem

        Args:
            self(Poem)

        Returns:
            str: poem title

        Raises:
            None
        """
        return self.title

    class Meta:

        """verbose name for poems
        """
        verbose_name = 'Poem'
        verbose_name_plural = 'Poems'

    def save(self, *args, **kwargs):
        """save poems to database

        check for duplicates, and update modified timestamps

        Args:
            self(Poem)
            *args: arguments
            **kwargs: parameters

        Returns:
            Poem.super()

        Raises:
            None
        """
        dup = None
        if not self.post_id:
            self.created = timezone.now()
            dup = Poem.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title[:50])

        self.modified = timezone.now()

        return super(Poem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='poems:post',
            subdomain='poems',
            kwargs={'poem': self.slug, })
