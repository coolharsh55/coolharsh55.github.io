#!/usr/bin/env bash

dates=$(grep -oP '[^#]\s+hpcom:date_book_read "\K([0-9\-]+)' content/hobbies/books.ttl) ;
year_max=$(date +%Y)
for i in $(seq 1995 $year_max) ; do
    books_read=$(echo $dates | grep -o $i | wc -w)
    echo "$i :: $books_read" ;
done
current_month=$(date +%m)
books_per_month=$((books_read/current_month))
projected_books_read_year=$((books_per_month*12))
echo "books read per month this year: $books_per_month"
echo "projected books read this year: $projected_books_read_year"

