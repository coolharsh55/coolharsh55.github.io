"""modesl for brainbank

    BrainBankIdea
    BrainBankPost
    BrainBankDemo
"""

from django.db import models
from ckeditor.fields import RichTextField
from sitedata.models import Tag
from django.utils.text import slugify


class BrainBankIdea(models.Model):

    """BrainBank Idea
    ID auto primary key
    Idea Title, Body, Slug, Published
    Slug created on save
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    title = models.CharField(
        max_length=250,
    )
    body = RichTextField()
    slug = models.SlugField(
        max_length=50,
    )
    repo = models.URLField(max_length=500, null=True, blank=True)
    published = models.DateField()

    def __str__(self):
        """string representation of an idea

        Args:
            self(BrainBankIdea)

        Returns:
            str: title of idea

        Raises:
            None
        """
        return self.title

    class Meta:

        """verbose name for ideas
        """
        verbose_name = 'BrainBank Idea'
        verbose_name_plural = 'BrainBank Ideas'

    def save(self, *args, **kwargs):
        """save brainbank idea to database

        check for duplicate, and update modified timestamp

        Args:
            self(BrainBankIdea)
            *args: arguments
            **kwargs: parameters

        Returns:
            BrainBankIdea.super()

        Raises:
            None
        """
        if not self.id:
            # check if slug is a duplicate
            dup = BrainBankIdea.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title[:50])
        return super(BrainBankIdea, self).save(*args, **kwargs)


class BrainBankPost(models.Model):

    """
    BrainBank Idea Post
    ID auto primary key
    Post title, body, published, tags, slug
    Linked to BrainBank Idea
    Slug created on save
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    title = models.CharField(
        max_length=250,
    )
    body = RichTextField()
    published = models.DateField()
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    idea = models.ForeignKey(BrainBankIdea)

    def __str__(self):
        """string representation of post

        Represent Idea Post by the Idea title suffixed by Post title

        Args:
            self(BrainBankPost)

        Returns:
            str: post title (idea title)
        """
        return self.title + ' (' + self.idea.title + ')'

    class Meta:

        """verbose name for posts
        """
        verbose_name = 'BrainBank Idea Post'
        verbose_name_plural = 'BrainBank Idea Posts'

    def save(self, *args, **kwargs):
        """save brainbank post to database

        check if duplicate, and update modified timestamp
        """
        if not self.id:
            # check if slug is a duplicate
            dup = BrainBankPost.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title)[:50]
        return super(BrainBankPost, self).save(*args, **kwargs)


class BrainBankDemo(models.Model):

    """BrainBank Idea Demo
    ID auto primary key
    Idea Demo title, body, slug, custom css and js
    Linked to BrainBank Idea
    Slug created on save
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    title = models.CharField(
        max_length=250,
    )
    js = RichTextField(
        verbose_name='javascript'
    )
    css = RichTextField(
        verbose_name='CSS'
    )
    body = RichTextField(
        verbose_name='content'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    idea = models.ForeignKey(BrainBankIdea)

    def __str__(self):
        """string representation fo BrainBankDemo

        Demo title suffixed by idea title

        Args:
            self(BrainBankDemo)

        Returns:
            str: demo title (idea title)
        """
        return self.title + ' (Demo for ' + self.idea.title + ')'

    class Meta:

        """verbose names for brainbank demo
        """
        verbose_name = 'BrainBank Idea Demo'
        verbose_name_plural = 'BrainBank Ideas Demos'

    def save(self, *args, **kwargs):
        """save brainbank demo to database

        check for duplicates, and update modified timestamps

        Args:
            self(BrainBankDemo)
            *args: arguments
            **kwargs: parameters

        Returns:
            BrainBankDemo.super()

        Raises:
            None
        """
        if not self.id:
            # check if slug is a duplicate
            dup = BrainBankDemo.objects.filter(title=self.title)
            if len(dup) > 0:
                # objects with the same slug exist -> duplicate!
                nos = str(len(dup))
                # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.idea.title + '-' + self.title)[:50]
        return super(BrainBankDemo, self).save(*args, **kwargs)
