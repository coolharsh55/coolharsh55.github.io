#!/usr/bin/env bash

dates=$(grep -oP '[^#]\s+hpcom:date_book_read "\K([0-9\-]+)' content/hobbies/books.ttl) ;

for i in {1995..2021} ; do
    echo "$i :: $(echo $dates | grep -o $i | wc -w)" ;
done