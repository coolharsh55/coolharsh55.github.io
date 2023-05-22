#!/usr/bin/env python3

from rdflib import Graph

graph = Graph()
graph.parse('data_combined.ttl', format='turtle')
results = graph.query('''
    PREFIX hpcom: <https://harshp.com/code/vocab#>
    PREFIX schema: <https://schema.org/>

    SELECT ?book ?title WHERE {
        ?book hpcom:book_status hpcom:book-read .
        FILTER NOT EXISTS {?book hpcom:book_read_medium ?medium} .
        ?book schema:name ?title .
    }
    ''')

for row in results:
    print(*row)