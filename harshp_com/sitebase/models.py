from django.db import models


from utils.meta_generator import create_meta
from django.core.urlresolvers import reverse
from utils.models import get_unique_slug


class Tag(models.Model):
    """Tag for descriptive Posts.
    Allows meta-tagging for better linking and descriptions.

    Has the following attributes:
     - name
     - description

    Has the following methods:
     -
    """

    name = models.CharField(max_length=128, db_index=True, unique=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    slug = models.SlugField(
        max_length=150, db_index=True, unique=True, blank=True)

    class Meta:

        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(Tag, self, 'name', name=self.name)
        return super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sitebase:tags:get', args=[self.slug])


class Author(models.Model):
    """Author class for Posts.
    Represents the person authoring the Post.

    Has the following attributes:
     - name
     - email
     - short_bio
     - long_bio
     - profile_pic
     - web_link

    Has the following methods:
     -
    """

    name = models.CharField(max_length=128, db_index=True)
    email = models.EmailField(max_length=256, unique=True)
    short_bio = models.CharField(max_length=256)
    long_bio = models.CharField(max_length=1024, blank=True, unique=True)
    profile_pic = models.URLField(max_length=256, blank=True, null=True)
    slug = models.SlugField(
        max_length=150, db_index=True, unique=True, blank=True)

    class Meta:

        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(Author, self, 'name', name=self.name)
        return super(Author, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'sitebase:authors:get', args=[self.slug])


class Post(models.Model):
    """Post base ABSTRACT model.
    Represents a basic post on harshp_com.

    Has the following attributes:
     - title
     - date created
     - date published
     - date updated
     - is_published
     - author
     - short_description
     - tags (sitebase:Tag)

    Has the following methods:
     -
    """

    title = models.CharField(max_length=128, db_index=True)
    authors = models.ManyToManyField(Author)

    date_created = models.DateTimeField()
    date_published = models.DateTimeField(blank=True, null=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=False, db_index=True, verbose_name='published')

    short_description = models.CharField(max_length=150)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)

    class Meta(object):

        abstract = True
        ordering = ['title']
        get_latest_by = 'date_updated'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def get_seo_meta(self):
        """get meta properties for this object"""
        meta = create_meta(
            title=self.title,
            description=self.short_description,
            keywords=[tag.name for tag in self.tags.all()],
            url=self.get_absolute_url(),
        )
        return meta


class Feedback(models.Model):
    '''Represents a feedback on a page
    A Feedback should have:
        - text of the feedback
        - timestamp for when it was given
        - an anonymous field for specifying name / contact details
        - a URL field for the page
        - a category field based on the page
        - a title field for the page
    '''
    url = models.URLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True, blank=True, db_index=True)
    text = models.TextField()
    feedback = models.TextField(blank=True)
    user = models.TextField()
    category = models.CharField(
            max_length=150, db_index=True, blank=True, null=True)
    title = models.CharField(
            max_length=250, db_index=True, blank=True, null=True)

    class Meta(object):
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ['-pk']

    def __str__(self):
        return '({date}) {url}'.format(date=self.timestamp, url=self.url)

    def save(self, *args, **kwargs):
        if not self.user or len(self.user.strip()) == 0:
            self.user = 'Anonymous'
        return super(Feedback, self).save(*args, **kwargs)
