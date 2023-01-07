#!/usr/bin/env bash
echo "=========================="
echo "Summary of Reading History"
echo "=========================="
dates=$(grep -oP '[^#]\s+hpcom:date_book_read "\K([0-9\-]+)' content/hobbies/books.ttl) ;
year_max=$(date +%Y)
for i in $(seq 1995 $year_max) ; do
    books_read=$(echo $dates | grep -o $i | wc -w)
    echo "$i :: $books_read" ;
done
weeks="$(date +%V)"
books_per_week=$(echo "num=$books_read/$((10#$weeks));print(f'{num:.2f}')" | python3)
books_per_month=$(echo "num=$books_read/$((10#$weeks))*4;print(f'{num:.2f}')" | python3)
projected_books_read_year=$(echo "num=$books_per_week*54; print(f'{num:.2f}')" | python3)
echo " --- "
echo "books read per week this year: $books_per_week"
echo "books read per month this year: $books_per_month"
echo "projected books read this year: $projected_books_read_year"
echo " --- "
printf "%-20s\n" "books in TCD:  $(grep -oP 'list:TCD' content/hobbies/books.ttl | wc -l | xargs)"
printf "%-20s\n" "books in Cork: $(grep -oP 'list:cork' content/hobbies/books.ttl | wc -l | xargs)"
echo "=========================="