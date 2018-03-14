#!/usr/bin/env python3

# Imports books from CSV file
# TITLE,SEEN,LIKED
# delimiter = '^'

import os
from hobbies.models import Book, BookList, BookAnnotation
from utils.speech_corrections import move_articles_to_end


class Record(object):

    def __init__(self, title, read='N', liked='N', fiction='Y'):
        self.title = move_articles_to_end(title)
        self.read = True if read == 'Y' else False
        self.liked = True if liked == 'Y' else False
        self.fiction = True if fiction == 'Y' else False

    def __str__(self):
        return self.title

    def add_book(self):
        try:
            book = Book.objects.filter(title=self.title)[0]
        except IndexError:
            book = Book(title=self.title)
            print('book does not exist', book)
        book.read, book.liked, book.fiction =\
            self.read, self.liked, self.fiction
        print(book.title)
        book.save()
        return book


def add(filepath):
    assert os.path.isfile(filepath)

    import csv
    with open(filepath, 'r') as f:
        data = csv.reader(f, delimiter=';')
        records = [Record(*item) for item in data]
        for record in records:
            record.add_book()


def add_now_reading(filepath):
    try:
        reading_list = BookList.objects.get(title='Now Reading')
    except BookList.DoesNotExist:
        reading_list = BookList(title='Now Reading')
    reading_list.books.clear()

    assert os.path.isfile(filepath)

    with open(filepath, 'r') as f:
        data = f.readlines()
        records = [Record(line.strip()) for line in data]
        for record in records:
            book = record.add_book()
            reading_list.books.add(book)
        reading_list.save()


def parse_kindle_annotations(filepath):
    assert os.path.isfile(filepath)

    # first, decode the kindle parser using chardet,
    # and then load it using klip
    with open(filepath, 'rb') as fd:
        data = fd.readlines()
    import chardet
    encoding = chardet.detect(data[0])['encoding']
    data = [line.decode(encoding) for line in data]
    with open('/tmp/clippings.txt', 'w') as fd:
        for line in data:
            fd.write(line)
    import klip
    data = klip.load_from_file('/tmp/clippings.txt', 'Kindle4')
    for item in data:
        title = move_articles_to_end(item['title'])
        content = item['content']
        try:
            book = Book.objects.get(title=title)
        except Book.DoesNotExist:
            book = Book(title=title, read=True)
            book.save()
        try:
            BookAnnotation.objects.get(content=content, book__title=title)
        except BookAnnotation.DoesNotExist:
            annotation = BookAnnotation(content=content, book=book)
            annotation.save()
