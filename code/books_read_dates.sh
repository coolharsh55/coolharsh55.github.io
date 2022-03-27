#!/usr/bin/env bash

dates=$(grep -oP '[^#]\s+hpcom:date_book_read "\K([0-9\-]+)' content/hobbies/books.ttl) ;
year_max=$(date +%Y)
for i in $(seq 1995 $year_max) ; do
    echo "$i :: $(echo $dates | grep -o $i | wc -w)" ;
done
