#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

"""Extract RDF metadata from content and remove markup"""

# There's a content folder called `CONTENT_DIR`
# There are folders and files in there
# Each file *may* have some metadata at the top of the file
# Or it may not - in which case it was meant to be copied as is
# The metadata in file is one per line, with final line containing ===
# keywords: title, published, modified, tags, description, headerimage
# 
# The purpose of this script is to walk each file
# Open it, read the metadata and contents
# Convert the metadata to RDF using schema.org and add to a collected graph
# Write the contents back to the file without metadata
# Finally, write the RDF graph to a `METADATA.ttl` file.


import os
from rdflib import Graph, Namespace, Literal, BNode
from rdflib import URIRef
from rdflib import RDF, RDFS
from rdflib.namespace import NamespaceManager, XSD

from generate import _read_content as parse_file_metadata

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

SCHEMA = Namespace('https://schema.org/')
HPCOM = Namespace('https://harshp.com/code/vocab#')

CONTENT_DIR = 'content'


# for root, dirs, files in os.walk(CONTENT_DIR, topdown=False):
#     DEBUG(f'root: {root}')
#     # DEBUG(f'dirs: {dirs}')
#     # DEBUG(f'files: {files}')
#     for file in files:
#         DEBUG(f'file: {file}')
#         # check if file is 'metadata'
#         if file == 'metadata':
#             # save data for directory
#             continue
#         # otherwise file is potentially content
#         filepath = os.path.join(root, file)
#         with open(filepath, 'r') as fd:
#             filedata = fd.read()
#         if filedata.startswith('title:'):
#             # extract metadata and read content
#             filedata = parse_file_metadata(filepath)
#             # DEBUG('file has metadata')
#         else:
#             # copy content as is
#             # DEBUG('file has no metadata')
#             pass

g = Graph()
tagset = set()

for root, dirs, files in os.walk('content/dev'):
    for file in files:
        # DEBUG(f'file: {file}')
        filepath = os.path.join(root, file)
        # check if file is 'metadata'
        if file == 'metadata':
            # save data for directory
            with open(filepath, 'r') as fd:
                name = fd.readline().split(':')[1].strip()
                iri = URIRef(root.replace('content', 'https://harshp.com'))
                g.add((iri, RDF.type, HPCOM.DevProject))
                g.add((iri, RDF.type, HPCOM.RenderedItem))
                g.add((iri, RDFS.subClassOf, URIRef('https://harshp.com/dev')))
                g.add((iri, SCHEMA.name, Literal(name, lang="en")))
                g.add((iri, SCHEMA.url, Literal(iri, datatype=XSD.anyURI)))
            continue
        # otherwise file is potentially content
        iri = URIRef(os.path.splitext(filepath)[0].replace('content', 'https://harshp.com'))
        with open(filepath, 'r') as fd:
            filedata = fd.read()
        assert(filedata.startswith('title:'))
        # extract metadata and read content
        filedata = parse_file_metadata(filepath)
        with open(filepath, 'w') as fd:
            fd.write(filedata['content'])
        title = filedata['title']
        published = filedata['published']
        modified = filedata['modified']
        tags = filedata['tags']
        # if len(tags) < 2:
        #     logging.error(file)
        # continue
        assert(len(tags) > 1)
        tagset.update(tags)
        description = filedata['description']
        headerimage = filedata['headerimage']
        if headerimage is not None and headerimage.startswith('//'):
            headerimage = f'https:{headerimage}'
        DEBUG(f'tags: {tags}')
        DEBUG(f'image: {headerimage}')

        g.add((iri, RDF.type, URIRef('https://harshp.com/dev')))
        g.add((iri, RDF.type, HPCOM.DevProjectPost))
        g.add((iri, RDF.type, HPCOM.RenderedItem))
        g.add((iri, SCHEMA.name, Literal(title, lang="en")))
        g.add((iri, SCHEMA.datePublished, Literal(published, datatype=XSD.dateTime)))
        if modified != published:
            g.add((iri, SCHEMA.dateModified, Literal(modified, datatype=XSD.dateTime)))
        for tag in tags:
            g.add((iri, HPCOM.tag , URIRef(f'https://harshp.com/tag/{tag}')))
        g.add((iri, SCHEMA.description, Literal(description, lang="en")))
        if headerimage:
            g.add((iri, SCHEMA.image, Literal(headerimage)))
        content = BNode()
        g.add((iri, HPCOM.content, content))
        g.add((content, RDF.type, HPCOM.Content))
        g.add((content, HPCOM.contentFile, Literal(f'https://harshp.com/code/{filepath}')))
        g.add((content, HPCOM.contentFileFormat, HPCOM.formatHTML))
        g.add((iri, SCHEMA.url, Literal(iri, datatype=XSD.anyURI)))
        g.add((iri, SCHEMA.author, URIRef('https://harshp.com/me')))
        g.add((iri, SCHEMA.isPartOf, URIRef(root.replace('content', 'https://harshp.com'))))
g.bind("schema", SCHEMA)
g.bind("hpcom", HPCOM)
g.serialize('dev.ttl', format='turtle')

g = Graph()
g.load('tags.ttl', format='turtle')
for tag in tagset:
    iri = URIRef(f'https://harshp.com/tag/{tag}')
    g.add((iri, RDF.type, HPCOM.Tag))
    g.add((iri, RDF.type, HPCOM.RenderedItem))
    g.add((iri, SCHEMA.name, Literal(tag)))
    g.add((iri, SCHEMA.url, Literal(iri, datatype=XSD.anyURI)))
g.bind("schema", SCHEMA)
g.bind("hpcom", HPCOM)
g.serialize('tags.ttl', format='turtle')
