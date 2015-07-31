"""sitedata models

    Tag
    Book
    Movie
    TVShow
    Game
"""

from django.db import models
from django.utils.text import slugify


class Tag(models.Model):

    """    Tag - meta for models
    """
    tagid = models.AutoField(primary_key=True)
    tagname = models.CharField(max_length=150,)

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


class Book(models.Model):

    """    Book - something I've read/reading
    A Book has a title (no Author as of now)
    It has dates for when I've started reading, and finished reading
    A read boolean field represents if I've finished reading the book
    """
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    read = models.BooleanField(default=False, verbose_name='read?')
    date_start = models.DateField(verbose_name='Started')
    date_end = models.DateField(verbose_name='Finished', blank=True)
    tags = models.ManyToManyField('sitedata.Tag',)

    def __str__(self):
        """string representation for books

        Args:
            self(Tag)

        Returns:
            str: book title

        Raises:
            None
        """
        return self.title

    class Meta:

        """attributes for books
        """
        ordering = (
            'title',
            'date_start',
            'date_end',
        )

    def save(self, *args, **kwargs):
        """save book to database

        create slugfield

        Args:
            self(Book)
            *args: arguments
            **kwargs: parameters

        Returns:
            Book.super()

        Raises:
            None
        """
        self.slug = slugify(self.title)
        return super(Book, self).save(*args, **kwargs)


class Movie(models.Model):

    """    Movie - A Movie I've seen
    A Movie has a name (no cast or director as of now)
    A date_seen field depicts the date I've seen the movie
    """
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    date_seen = models.DateField(verbose_name='Seen on')
    tags = models.ManyToManyField('sitedata.Tag')

    def __str__(self):
        """string representation for movies

        Args:
            self(Tag)

        Returns:
            str: movie title

        Raises:
            None
        """
        return self.title

    class Meta:

        """attributes for movies
        """
        ordering = (
            'title',
            'date_seen',
        )

    def save(self, *args, **kwargs):
        """save movie to database

        Args:
            self(Movie)
            *args: arguments
            **kwargs: parameters

        Returns:
            Movie.super()

        Raises:
            None
        """
        self.slug = slugify(self.title)
        return super(Movie, self).save(*args, **kwargs)


class TVShow(models.Model):

    """    TV Show - A series I'm watching/watched
    A TV Show has a name (no cast, or other info as of now)
    Date fields for when I started and finished watching
    A watched boolean field represents if I've completed the series
    A Latest Season/Episode notation, if available
    """
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    date_start = models.DateField(verbose_name='Started',)
    date_end = models.DateField(verbose_name='Finished',)
    watched = models.BooleanField(default=False, verbose_name='Finished?',)
    tags = models.ManyToManyField('sitedata.Tag',)

    def __str__(self):
        """string representation for tv shows

        Args:
            self(Tag)

        Returns:
            str: tv show title

        Raises:
            None
        """
        return self.title

    class Meta:

        """attributes and verbose names for tv shows
        """
        ordering = (
            'title',
            'date_start',
            'date_end',
            'watched',
        )
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'

    def save(self, *args, **kwargs):
        """save tv show to database

        Args:
            self(TVShow)
            *args: arguments
            **kwargs: parameters

        Returns:
            TVShow.super()

        Raises:
            None
        """
        self.slug = slugify(self.title)
        return super(TVShow, self).save(*args, **kwargs)


class Game(models.Model):

    """    Game I've played/playing
    A Game has a name (no creator, or other info as of now)
    Date fields for when I started and finished playing
    A finished boolean field
    """
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    date_start = models.DateField(verbose_name='Started')
    date_end = models.DateField(verbose_name='Finished')
    finished = models.BooleanField(default=False, verbose_name='Finished?')
    tags = models.ManyToManyField('sitedata.Tag')

    def __str__(self):
        """string representation for games

        Args:
            self(Tag)

        Returns:
            str: game title

        Raises:
            None
        """
        return self.title

    class Meta:

        """attributes and verbose name for games
        """
        ordering = (
            'title',
            'date_start',
            'date_end',
            'finished',
        )
        verbose_name = 'Video Game'
        verbose_name_plural = 'Video Games'

    def save(self, *args, **kwargs):
        """save game to database

        Args:
            self(Game)
            *args: arguments
            **kwargs: parameters

        Returns:
            Game.super()

        Raises:
            None
        """
        self.slug = slugify(self.title)
        return super(Game, self).save(*args, **kwargs)

# class PhotoshootCategory(models.Model):
#     '''
#     A Photoshoot or Photo Expedition Type/Category
#     Each Category has a name and a short explanation
#     Types:
#         Festival - A festive gathering and its associated photos,
#             St.Patrick's Day, Diwali, etc.
#         Macro - close or small objects magnified
#         Field Trip - Going out into nature
#             Beach, Landscapes, Trees, Flowers, etc.
#         Street - People and culture on the streets
#         Experiment - Trying out new and cool things
#         Photoshoot - Taking a model(s) and focusing on it
#         Trip - Going out with a group of people, photos of journey
#     '''
#     _id = models.Autofield(primary_key=True)
#     name = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(max_length=100, unique=True)

#     def __str__(self):
#         ''' return Photoshoot Category name '''
#         return self.name

#     class Meta:
#         verbose_name = 'Photoshoot Category'
#         verbose_name_plural = 'Photoshoot Categories'

#     def save(self, *args, **kwargs):
#         ''' save slug '''
#         self.slug = slugify(self.name)
#         return super(PhotoshootCategory, self).super(*args, **kwargs)

# class Photoshoot(models.Model):
#     '''
#     A Photoshoot or Photo Expedition
#     The title that acts as the album name
#     Date and Location (text)
#     Photoshoot Category
#     URL to the photos (Flickr or Google Photos)
#     '''
#     _id = models.Autofield(primary_key=True)
#     title = models.CharField(max_length=200, unique=True)
#     slug = models.CharField(max_length=200, unique=True)
#     category = models.ForeignKey('sitedata.PhotoshootCategory')
#     date = models.DateField()
#     location = models.CharField(max_length=200,)
#     url = models.URLField()

#     def __str__(self):
#         ''' return photoshoot title and date '''
#         return ' '.join(self.title,'on',self.date)

#     def save(self, *args, **kwargs):
#         ''' save slug '''
#         self.slug = slugify(self.title)
#         return super(Photoshoot, self).save(*args, **kwargs)
