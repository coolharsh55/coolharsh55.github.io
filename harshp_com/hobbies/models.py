from django.db import models
from utils.speech_corrections import move_articles_to_end
from utils.models import get_unique_slug


class Movie(models.Model):
    '''A Movie, a Film'''
    title = models.CharField(max_length=256, db_index=True)
    seen = models.BooleanField(default=False, db_index=True)
    liked = models.BooleanField(default=True, db_index=True)

    class Meta(object):
        ordering = ['title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = move_articles_to_end(self.title)
        return super(Movie, self).save(*args, **kwargs)


class MovieList(models.Model):
    '''A list of movies'''
    title = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, db_index=True)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)
    movies = models.ManyToManyField(Movie, related_name='lists', blank=True)

    class Meta(object):
        ordering = ['title']
        verbose_name = 'Movie List'
        verbose_name_plural = 'Movie Lists'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                MovieList, self, 'title', title=self.title)
        return super(MovieList, self).save(*args, **kwargs)


class Book(models.Model):
    '''A book, a novel'''
    title = models.CharField(max_length=256, db_index=True)
    read = models.BooleanField(default=False, db_index=True)
    liked = models.BooleanField(default=False, db_index=True)
    fiction = models.BooleanField(default=True, db_index=True)

    class Meta(object):
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = move_articles_to_end(self.title)
        return super(Book, self).save(*args, **kwargs)


class BookList(models.Model):
    '''A list of books'''
    title = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)
    books = models.ManyToManyField(Book, related_name='lists', blank=True)

    class Meta(object):
        ordering = ['title']
        verbose_name = 'Book List'
        verbose_name_plural = 'Book Lists'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                BookList, self, 'title', title=self.title)
        return super(BookList, self).save(*args, **kwargs)


class BookAnnotation(models.Model):
    '''Annotation from a Book. Probably parsed from Kindle.'''
    content = models.TextField()
    book = models.ForeignKey(
            Book, on_delete=models.CASCADE,
            related_name='annotations')

    class Meta(object):
        ordering = ['pk']
        verbose_name = 'Book Annotation'
        verbose_name_plural = 'Book Annotations'

    def __str__(self):
        return '{} - {}'.format(self.content, self.book.title)
