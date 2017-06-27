#!/usr/bin/env python3

# Imports movies from CSV file
# TITLE,SEEN,LIKED
# delimiter = '^'


class Record(object):

    def __init__(self, title, seen='X', liked='N'):
        self.title = title
        self.seen = True if seen == 'Y' else False
        self.liked = True if seen == 'Y' else False

    def __str__(self):
        return self.title


def run(filepath):
    import os
    assert os.path.isfile(filepath)

    import csv
    with open(filepath, 'r') as f:
        data = csv.reader(f, delimiter='^')
        movies = [Record(*item) for item in data]

    from hobbies.models import Movie
    for record in movies:
        movie = Movie()
        movie.title, movie.seen, movie.liked =\
            record.title, record.seen, record.liked
        movie.save()
