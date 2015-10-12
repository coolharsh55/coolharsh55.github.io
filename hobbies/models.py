"""Hobbies Models

    Book
    Movie
    TV Show
    Game
    Photography -> in development, commented out

"""

from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from subdomains.utils import reverse

from harshp.utils.duplicates import duplicate_slug


class Book(models.Model):

    """    Book - something I've read/reading
    A Book has a title (no Author as of now)
    It has dates for when I've started reading, and finished reading
    A read boolean field represents if I've finished reading the book
    """
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200, unique=True)
    published = models.DateTimeField()
    modified = models.DateTimeField(blank=True,)
    date_start = models.DateField(verbose_name='Started')
    date_end = models.DateField(
        verbose_name='Completed', blank=True, null=True)
    finished = models.BooleanField(
        verbose_name='Finished?', default=False)
    headerimage = models.URLField(max_length=500, blank=True, null=True)
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
            '-date_start',
            '-date_end',
            'title',
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
        if not self._id:
            self.published = timezone.now()
        self.slug = duplicate_slug(self, self.title, title=self.title)
        if self.date_end:
            if self.date_start > self.date_end:
                self.date_end = self.date_start
        self.modified = timezone.now()
        return super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'books', 'hobbytitle': self.slug, })


class Movie(models.Model):

    """    Movie - A Movie I've seen
    A Movie has a name (no cast or director as of now)
    A date_seen field depicts the date I've seen the movie
    """
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200, unique=True)
    date_seen = models.DateField(verbose_name='Seen on')
    published = models.DateTimeField()
    modified = models.DateTimeField(blank=True,)
    finished = models.BooleanField(verbose_name='Finished?', default=False,)
    headerimage = models.URLField(max_length=500, blank=True, null=True)
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
            '-date_seen',
            'title',
            'finished',
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
        if not self._id:
            self.published = timezone.now()
        self.slug = duplicate_slug(self, self.title, title=self.title)
        self.modified = timezone.now()
        return super(Movie, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'movies', 'hobbytitle': self.slug, })


class TVShow(models.Model):

    """    TV Show - A series I'm watching/watched
    A TV Show has a name (no cast, or other info as of now)
    Date fields for when I started and finished watching
    A watched boolean field represents if I've completed the series
    A Latest Season/Episode notation, if available
    Season, where a default of 0 means ALL seasons
    """
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,)
    season = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200, unique=True)
    date_start = models.DateField(verbose_name='Started',)
    date_end = models.DateField(
        verbose_name='Finished', blank=True, null=True)
    published = models.DateTimeField()
    modified = models.DateTimeField(blank=True,)
    finished = models.BooleanField(default=False, verbose_name='Finished?',)
    headerimage = models.URLField(max_length=500, blank=True, null=True)
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
        string = self.title
        if self.season > 0:
            string += ' - ' + 'Season %d' % self.season
        return string

    class Meta:

        """attributes and verbose names for tv shows
        """
        ordering = (
            '-date_start',
            '-date_end',
            'title',
            'finished',
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
        if not self._id:
            self.published = timezone.now()
        self.slug = duplicate_slug(self, self.title, title=self.title)
        if self.date_end:
            if self.date_start > self.date_end:
                self.date_end = self.date_start
        self.modified = timezone.now()
        return super(TVShow, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'tvshows', 'hobbytitle': self.slug, })


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
    date_end = models.DateField(
        verbose_name='Finished', blank=True, null=True)
    continuing = models.BooleanField(default=False, verbose_name='Continuing?')
    published = models.DateTimeField()
    modified = models.DateTimeField(blank=True,)
    finished = models.BooleanField(default=False, verbose_name='Finished?')
    headerimage = models.URLField(max_length=500, blank=True, null=True)
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
            '-date_start',
            '-date_end',
            'title',
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
        if not self._id:
            self.slug = slugify(self.title)
            self.published = timezone.now()
        if self.date_end:
            if self.date_start > self.date_end:
                self.date_end = self.date_start
        self.modified = timezone.now()
        return super(Game, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='hobbies:type_item',
            subdomain='hobbies',
            kwargs={'hobbytype': 'games', 'hobbytitle': self.slug, })

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
