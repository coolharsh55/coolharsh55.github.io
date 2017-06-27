from django.db import models


class Movie(models.Model):
    '''A Movie, a Film'''
    title = models.CharField(max_length=256, db_index=True)
    seen = models.BooleanField(default=False)
    liked = models.BooleanField(default=True)

    class Meta(object):
        ordering = ['title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # change the case of title to Title case
        self.title = self.title.title()
        # remove redundant words at start
        unwanted = ['The ', 'A ', 'An ']
        for word in unwanted:
            if self.title.startswith(word):
                self.title = self.title[len(word):] + ', ' + word
                print(self.title)
                break
        return super().save(*args, **kwargs)


class MovieList(models.Model):
    '''A list of movies'''
    title = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, db_index=True)
    movies = models.ManyToManyField(Movie, related_name='lists')
    
    class Meta(object):
        ordering = ['title']
        verbose_name = 'Movie List'
        verbose_name_plural = 'Movie Lists'

    def __str__(self):
        return self.title

