#!/usr/bin/env python3

"""Generator for HTML

This is the main file that takes in the data written inside ttl files
and renders it into static HTML files that can be served via a server.

The gist of the approach is thus:
* RDF data is based on IRIs which act as unique identifiers for each node 
* A RenderedItem is a class that represents nodes to be rendered in HTML
* The generator loads all RDF data, then looks for instances of RenderedItem
* A 'view' is a way to render a node
* Views can be defined at any arbitrary level e.g. node, class, generic
* The generator will find an appropriate view to render the node
* The generator then executes the view
* If the view contains a SPARQL query, the generator will execute it
* Results of the query are passed to the view as data

The file is to be executed as a script `python generator.py`
It does not have a mains method.
"""

import datetime
import os
# RDFlib is used to interact with RDF data
from rdflib import Graph
from rdflib import Namespace
from rdflib.namespace import NamespaceManager
from rdflib.namespace import XSD
from rdflib import RDF, RDFS
from rdflib.term import Literal, URIRef
# RDF-SPARQL is a plugin for RDFlib for executing SPARQL queries
from rdflib.plugins.sparql import prepareQuery
# RDF-ORM is a custom library for conveniently using RDF in Python
from rdform import DataGraph, RDFS_Resource
# Jinja2 is used as the templating engine for rendering HTML
from jinja2 import FileSystemLoader
from jinja2 import Environment

# logging configuration for debugging to console
import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

# Namespaces used in the RDF files
# RDF-ORM can also auto-detect them
SCHEMA = Namespace('https://schema.org/')
HPCOM = Namespace('https://harshp.com/code/vocab#')
HPVIEWS = Namespace('https://harshp.com/code/views#')

# load data from files into graph
graph = Graph()
graph.load('vocab.ttl', format='turtle')
graph.load('views.ttl', format='turtle')
graph.load('content/site.ttl', format='turtle')
graph.load('content/tags.ttl', format='turtle')
graph.load('../me.ttl', format='turtle')
# blog, hobbies, dev
graph.load('content/blog/blog.ttl', format='turtle')
graph.load('content/poems/poems.ttl', format='turtle')
graph.load('content/stories/stories.ttl', format='turtle')
graph.load('content/dev/dev.ttl', format='turtle')
graph.load('content/research/blog/research_blog.ttl', format='turtle')
graph.load('content/hobbies/books.ttl', format='turtle')
# research
graph.load('content/research/research.ttl', format='turtle')
graph.load('content/research/publications/publications.ttl', format='turtle')
graph.load('content/research/publications/authors.ttl', format='turtle')
graph.load('content/research/publications/venues.ttl', format='turtle')
graph.load('content/research/supervision/supervision.ttl', format='turtle')
graph.load('content/research/projects/risky/risky.ttl', format='turtle')
graph.load('content/research/projects/paecg/paecg.ttl', format='turtle')

# create data graph through ORM
data = DataGraph()
data.load(graph)
# This create a namespace mapping for the namespaces defined in graph
# E.g. 'rdfs' will be k="rdfs" v="Namespace(RDFS IRI)"
data.graph.ns = { k:v for k,v in data.graph.namespaces() }

# rendered items are those that should be created into files
# they are defined as hpcom:RenderedItem
rendered_items = data.get_instances_of('hpcom_RenderedItem')

# ########################
# hyper-lazy testing shell
# this provides a lazy way to load data and check some output

# check for duplicate dates
# set_published = dict()
# for item in data.get_instances_of('schema_Book'):
#     if not hasattr(item, 'hpcom_book_read'):
#         continue
#     date_published = str(item.hpcom_book_read)
#     if date_published not in set_published:
#         set_published[date_published] = item.schema_name
#         continue
#     print(item, item.rdf_type)
#     print(f'same as: {set_published[date_published]}')
# import sys
# sys.exit()
# ########################

# Views define how the RDF data gets rendered into formats
views = data.get_instances_of('hpcom_View')
DEBUG(f'registered views: {views}')
# RDFS Resource View is a generic view targeting rdfs:Resource
# If all other views fail or are not found, it gets selected
view_rdfs_resource = data.get_entity('hpview_RDFSResourceView')
DEBUG(f'default view: {view_rdfs_resource}')
RenderedItem = data.get_entity('hpcom_RenderedItem')

# Tests that can be used within Jinja2 code
JINJA2_TESTS = {
    'RDFS_Resource': lambda x: type(x) is RDFS_Resource,
    'BNode': lambda x: x.startswith('u'),
}

# Path where rendered data is exported or to be stored
LOCAL_PATH = '../'


def _get_localised_path(iri):
    if not iri.startswith('https://harshp.com/'):
        raise Exception(f'Path {iri} is not local to harshp.com')
    return iri.replace('https://harshp.com/', LOCAL_PATH, 1)


def _get_view(item):
    """determine view to render this item with"""

    def _find_view(item):
        # DEBUG(item.iri)
        for view in views:
            if hasattr(view, 'hpcom_view_target'):
                target = view.hpcom_view_target
                # DEBUG(f'checking view {view} with target {target}')
                # DEBUG(f'{target.iri}')
                if target.iri == item.iri:
                    return view
    # a view can be defined in (order of checking)
    # content object associated with it
    # view declared as targeting this object
    # view declared as targeting the classes of this object
    # view declared as targeting the parent classes of this object
    # view declared as targeting rdfs:Resource (generic fallback)

    # checking content for associated view
    if hasattr(item, 'hpcom_content'):
        content = item.hpcom_content
        # DEBUG(f'item has content {content}')
        if hasattr(content, 'hpcom_renderWith'):
            # DEBUG('item declared its own renderer')
            return content.hpcom_renderWith

    # object either has content with no view attached
    # or object does not have content
    # regardless, check if there is a view associated with iri
    for view in views:
        if hasattr(view, 'hpcom_view_target') and view.hpcom_view_target is item:
            return view

    # check view associated with classes of this object
    for parent in item.rdf_type:
        if parent is RenderedItem:
            continue
        # DEBUG(f'find view for parent: {parent} {type(parent)}')
        view = _find_view(parent)
        if view is not None:
            return view

    # check views associated with parents of parents
    ancestors = [p.rdf_type for p in item.rdf_type if hasattr(p, 'rdf_type')]
    while ancestors:
        ancestor = ancestors.pop()
        if type(ancestor) is list:
            temp = ancestor.pop()
            for a in ancestor:
                ancestors.insert(0, a)
            ancestor = temp
        view = _find_view(ancestor)
        if view is not None:
            return view

    # all avenues exhausted
    # return view for rdfs:resource
    return view_rdfs_resource


def prefix_this(item):
    # DEBUG(f'item: {item} type: {type(item)}')
    if type(item) is RDFS_Resource:
        item = item.iri
    elif type(item) is URIRef:
        item = str(item)
    if type(item) is str and item.startswith('http'):
        iri = URIRef(item).n3(data.graph.namespace_manager)
    else:
        iri = item
    if iri.count('_') > 0:
        iri = iri.split('_', 1)[1]
    # DEBUG(f'prefixed {item} to: {iri}')
    return iri


def _execute_sparql(query, bindings=None):
    """execute given sparql query and return results
    supplement query with given bindings"""
    DEBUG(f'executing query: {query}')
    results = data.graph.query(query, initBindings=bindings)
    for row in results:
        DEBUG(row)
        # DEBUG(data.resolve_entities_to_objects(row))
    DEBUG(f'query returned {len(results)} rows')
    return [data.resolve_entities_to_objects(row) for row in results]


def _view_filecopy(path, *args):
    """simple writer --> will write contents to path
    ensures folder structure exists before writing"""
    with open(path, 'w') as fd:
        DEBUG(f'writing file {path}')
        fd.writelines(contents)
    return


JINAJ2_TEMPLATE_VARS = {
    'RDF_DESC_PROP': ('rdf_type', 'schema_name', 'schema_url'),
    'prefix_this': prefix_this,
}


def html_view(item):
    if hasattr(item, 'schema_url'):
        s = f'<a href="{item.schema_url}">{str(item)}</a>'
    elif type(item) is RDFS_Resource:
        s = f'<a href="{item.iri}">{str(item)}</a>'
    elif type(item) is str and item.startswith('http'):
        s = f'<a href="{item}">{str(item)}</a>'
    else:
        s = item
        if s == "true":
            s = "✅"
        elif s == "false":
            s = "❌"
    # DEBUG(f'html for item {item} type{type(item)} is {s}')
    return s

def publication_type(publication):
    type_iris = [URIRef(t.iri) for t in publication.rdf_type]
    # for cat in publication.rdf_type:
    #     DEBUG(f'{cat} {type(cat)} {type(HPCOM.FullPaper)}')
    if HPCOM.Thesis in type_iris:
        s = f'Thesis'
    elif HPCOM.FullPaper in type_iris:
        if hasattr(publication, 'schema_publisher'):
            if type(publication.schema_publisher.rdf_type) is list:
                for parent in publication.schema_publisher.rdf_type:
                    if str(parent) == str(SCHEMA.Periodical):
                        s = 'Journal'
                        break
            elif str(publication.schema_publisher.rdf_type) == str(SCHEMA.Periodical):
                s = 'Journal'
            else:
                s = str(publication.schema_publication.hpcom_event_type)
        else:
            s = str(publication.schema_publication.hpcom_event_type)
    elif HPCOM.ShortPaper in type_iris:
        s = 'Short Paper'
    elif HPCOM.Abstract in type_iris:
        s = 'Abstract'
    elif HPCOM.ExtendedAbstract in type_iris:
        s = 'Ext. Abstract'
    elif HPCOM.BookChapter in type_iris:
        s = 'Book Chapter'
    elif HPCOM.Report in type_iris:
        s = 'Report'
    else:
        s = 'Publication'
    # if hasattr(publication, 'hpcom_peer_reviewed') \
    #     and publication.hpcom_peer_reviewed == "true":
    #     s = f'{s}, peer-reviewed'
    return s


JINJA2_FILTERS = {
    'html_view': html_view,
    'publication_type': publication_type,
    'year': lambda x: x,
}


def _view_jinja2(path, metadata=None):
    """jinja2 renderer --> renders contents using Jinja2
    requires metadata['template'] to render with"""
    assert('template' in metadata)
    template_dir, template_file = os.path.split(
        _get_localised_path(metadata['template']))
    template_loader = FileSystemLoader(searchpath=template_dir)
    template_env = Environment(
        loader=template_loader, 
        autoescape=True, trim_blocks=True, lstrip_blocks=True)
    template_env.tests.update(JINJA2_TESTS)
    template_env.filters.update(JINJA2_FILTERS)
    template = template_env.get_template(template_file)
    if not path.endswith('html'):
        path = f'{path}.html'
    # DEBUG(metadata.keys())
    # if 'item' in metadata:
    #     DEBUG(metadata['item'])
    DEBUG(f'writing {metadata["item"].iri} to {path}')
    with open(path, 'w+') as fd:
        fd.write(template.render(
            **metadata, RenderedItem=RenderedItem, **JINAJ2_TEMPLATE_VARS))


def _view_empty(*args, **kwargs):
    """dummy view, does nothing"""
    pass


VIEW_DICT = {
    'https://harshp.com/code/vocab#FileCopy': _view_filecopy,
    'https://harshp.com/code/vocab#Jinja2': _view_jinja2,
    'https://harshp.com/code/vocab#EmptyRenderer': _view_empty,
}


def _resolve_view_and_write(view, path, metadata=None):
    """gets view associated with renderer and passes on data to it
    metadata can contain anything required for the view to render
    """
    # DEBUG(f'{view.hpcom_view_renderer}')
    renderer = view.hpcom_view_renderer
    if renderer.iri not in VIEW_DICT:
        raise Exception(f'Renderer {renderer} is not registered with any handler')

    view = VIEW_DICT[renderer.iri]
    view(path, metadata)


def _today():
    literal = Literal(datetime.datetime.now(), datatype=XSD.dateTime)
    return literal

def _year_start():
    literal = Literal(
        datetime.date.today().replace(day=1,month=1), datatype=XSD.date)

SPARQL_ACTIONS = {
    'date-today': _today,
    'date_year_start': _year_start,
}


def render_item(item):
    """generate html file for item using its view"""
    assert(item.view)
    DEBUG(f'rendering {item} with view {item.view}')

    # at this point, the object can be rendered
    view = item.view
    metadata = { 'item': item }  # metadata of item for rendering

    # 1) get template attached with file if it exists
    # 2) if (1) does not exist, get template attached with view
    template = None
    if hasattr(item, 'hpcom_content') \
            and hasattr(item.hpcom_content, 'hpcom_view_template'):
        template = item.hpcom_content.hpcom_view_template
    elif hasattr(view, 'hpcom_view_template'):
        template = view.hpcom_view_template
    else:
        template = 'https://harshp.com/code/templates/template_base.jinja2'
    metadata['template'] = template

    # 3) get content file for item if it exists
    contents = None
    if hasattr(item, 'hpcom_content') \
            and hasattr(item.hpcom_content, 'hpcom_contentFile'):
        content_file = item.hpcom_content.hpcom_contentFile
        content_file_format = item.hpcom_content.hpcom_contentFileFormat
        path = _get_localised_path(content_file)
        with open(path, 'r') as fd:
            contents = fd.read()
    metadata['contents'] = contents

    if not contents and not template:
        # no contents, no template --> this item cannot be rendered
        raise Exception(f'{iri} has no content nor template, cannot render')

    # 4) get SPARQL query for renderer if exists
    sparql_source = None
    if hasattr(item, 'hpcom_sparql'):
        sparql_source = item.hpcom_sparql
    elif hasattr(view, 'hpcom_sparql'):
        sparql_source = view.hpcom_sparql

    if sparql_source:
        # DEBUG(f'sparql source: {sparql_source}')
        if type(sparql_source) is not list:
            sparql_source = [sparql_source]
        for node in sparql_source:
            label = str(node.rdfs_label)
            bindings= { 'iri': URIRef(item.iri) }
            if hasattr(node, 'hpcom_queryParam'):
                param = node.hpcom_queryParam
                param_label = str(param.hpcom_queryParamLabel)
                param_action = SPARQL_ACTIONS[str(param.hpcom_queryParamValue)]
                param_value = param_action()
                # DEBUG(f'query parameters with label {param_label} and value {param_value}')
                bindings[param_label] = param_value

            metadata[f'{label}_sparql'] = node.hpcom_queryString
            metadata [label] = _execute_sparql(
                    node.hpcom_queryString, bindings=bindings)

    # call function handling views
    # just contents, no template --> directly generate the file
    path = _get_localised_path(item.iri)
    if path.endswith('/'):
        path = f'{path}index.html'
    if path.startswith('../code/vocab#'):
        path = path.replace('../code/vocab#', '../resources/')
    _resolve_view_and_write(view, path, metadata)


logging.info('Retrieving Views and Renderers')
for item in rendered_items:
    DEBUG(f'handling item: {item}')

    view = _get_view(item)
    DEBUG(f'render with: {view}')
    assert(view)
    item.view = view
    render_item(item)

# store missing tags
sparql_missing_tags = """
    SELECT DISTINCT ?tag WHERE {
        ?article hpcom:tag ?tag .
        FILTER NOT EXISTS { ?tag schema:name ?name } .
    } ORDER BY ?tag
    """
results = data.graph.query(sparql_missing_tags)
if len(results) > 0:
    with open('tags_missing.ttl', 'w+') as fd:
        for tag in results:
            iri = tag[0]
            prefixed = prefix_this(iri)
            name = prefixed.split(':')[1]
            print(f"""{prefixed} a hpcom:RenderedItem, hpcom:Tag ;
                schema:name "{name}"@en ;
                schema:url "{iri}"^^xsd:anyURI .
                """, file=fd)
    logging.warning(f'found {len(results)} missing tags, check tags_missing.ttl')