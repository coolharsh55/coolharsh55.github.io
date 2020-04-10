#!/usr/bin/env python3

'''Generate static documents for serving.
Content is stored in ./code/content folder.
Explicitly state the folder to be considered as content.
The script will then generate the corresponding html in the root.
'''

from jinja2 import Environment, FileSystemLoader
import logging
import os

# tell jinja2 where to find templates
ENV = Environment(
    loader=FileSystemLoader('templates'))
# global variables
INDEX = []  # index of ALL documents
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def _read_content(path):
    '''Read and interpret data from a content file.
    Returns data as dictionary.
    The fileformat is:
    title: Title
    published: 20XX-XX-XX
    modified: 20XX-XX-XX
    tags: X,Y,Z
    description: lorem ipsum
    headerimage: https://example.com
    ===
    content'''
    with open(path, 'r') as fd:
        title = fd.readline().split(':')[-1].strip()
        published = fd.readline().split(': ')[-1].strip()
        modified = fd.readline().split(': ')[-1].strip()
        tags = [
            tag.strip()
            for tag in fd.readline().split(':')[-1].split(',')]
        description = fd.readline().split(':')[-1].strip()
        headerimage = fd.readline().split(':')[-1].strip()
        separator = fd.readline().strip()
        assert separator == '==='
        content = fd.read()
    return {
        'title': title,
        'published': published,
        'modified': modified,
        'tags': tags,
        'description': description,
        'headerimage': headerimage,
        'content': content
    }


def generate_docs(
        name: str, contentpath: str,
        template_content: str, template_index: str):
    '''Generate content document.
    name: name of the section e.g. blog, poems
    contentpath: path of the content folder
    template_content: template for content
    template_index: template for content index
    '''
    logging.debug(f'generating docs for {name}')
    for root, _, files in os.walk('content/' + contentpath):
        if not files:
            logging.debug(f'skipped: found no files in {root}')
            continue
        # replace path from content to root as files are served from root
        directorypath = root.replace('content', '..', 1)
        logging.debug(f'directorypath is {directorypath}')
        # generate directories in serving folder if necessary
        if not os.path.exists(directorypath):
            logging.debug(f'created directory {directorypath}')
            os.makedirs(directorypath)
        # iterate files, read content, add them to index
        index = []
        files = sorted(files, key=lambda x: x.lower())
        for f in files:
            filename, extension = os.path.splitext(f)
            path = os.path.join(root, f)
            data = _read_content(path)
            # this is the local content index
            index.append((
                data['title'],
                data['published'],
                data['modified'],
                filename,
                data['description'],
            ))
            # this is the global index (site-level)
            INDEX.append((
                data['title'],
                data['published'],
                data['modified'],
                f'{contentpath}/{filename}',
                data['description'],
                name,
                contentpath,
            ))
            docspath = '..' + path.replace('content', '', 1)
            # render file according to file format
            if extension == ".html":
                template = ENV.get_template(template_content)
                with open(docspath, 'w') as fd:
                    fd.write(template.render(data))
            logging.debug(f'generated file {docspath}')
            # TODO: more format generators
            # e.g. markdown (md), text (txt)
        # sort by date published
        index.sort(key=lambda x: x[1], reverse=True)
        # render document
        template = ENV.get_template(template_index)
        with open(f'{directorypath}/index.html', 'w') as fd:
            fd.write(template.render(blogs=index, section=contentpath))
        logging.info(f'generated {name} index')


def generate_sectioned_docs(
        name, contentpath, template_content, template_index):
    '''Generate documents for a particular section.
    Can be a folder within another folder e.g. research/blog.'''
    def _generate_sectioned_docs(path):
        '''Generate documents for specified section.'''
        # The metadata file indicates info for that section, e.g. name
        if os.path.isfile(path + '/metadata'):
            with open(path + '/metadata', 'r') as fd:
                section = fd.read().split(':')[-1].strip()
        else:
            section = 'general'
        logging.debug(f'generating section-docs for {path}')
        # generate docs - same as generate_docs
        # TODO: Refactor document generation between sections
        # create another function to actually generate the documents
        # and call it from these two functions for generating docs
        index = []
        for root, _, files in os.walk(path):
            directorypath = root.replace('content', '..', 1)
            if not os.path.exists(directorypath):
                logging.debug(f'created directory {directorypath}')
                os.makedirs(directorypath)
            for f in files:
                filename, extension = os.path.splitext(f)
                if filename == 'metadata':
                    continue
                path = os.path.join(root, f)
                logging.debug(f'reading {path}')
                data = _read_content(path)
                index.append((
                    data['title'],
                    data['published'],
                    data['modified'],
                    filename,
                    data['description'],
                    section,
                    path
                ))
                INDEX.append((
                    data['title'],
                    data['published'],
                    data['modified'],
                    f'{directorypath.replace("../","")}/{filename}',
                    data['description'],
                    name,
                    contentpath,
                ))
                docspath = '..' + path.replace('content', '', 1)
                if extension == ".html":
                    template = ENV.get_template(template_content)
                    with open(docspath, 'w') as fd:
                        fd.write(template.render(data))
                logging.debug(f'generated file {docspath}')
                # TODO: more format generators
                # e.g. markdown (md), text (txt)
            break

        index.sort(key=lambda x: x[1], reverse=True)
        return index, section
    # generate the index
    # This is different from the usual index as sectioned indexes have
    # their posts grouped by the section
    logging.debug(f'generating docs for {name}')
    dev_index = []
    for root, directories, files in os.walk('content/' + contentpath):
        if not files and not directories:
            logging.debug(f'skipped: found no files in {root}')
            continue

        general_index, _ = _generate_sectioned_docs(root)
        dev_index.append(('General', general_index, '.'))
        for directory in directories:
            directorypath = os.path.join(root, directory)
            index, section = _generate_sectioned_docs(directorypath)
            dev_index.append((section, index, directory))
            directorypath = os.path.join(directorypath, 'index.html')
            directorypath = directorypath.replace('content', '..')
            with open(directorypath, 'w') as fd:
                template = ENV.get_template(template_index)
                fd.write(template.render(blogs=index,title=section))
        break
    # Sort the sections by date_published of their posts
    # So the section with the latest post is at the top
    dev_index.sort(key=lambda x: x[1][0][2], reverse=True)
    with open('../' + contentpath + '/index.html', 'w') as fd:
        template = ENV.get_template(template_index)
        fd.write(template.render(
            sections=dev_index, root=contentpath, title=name))


def generate_unindexed_docs(name: str, contentpath: str, template: str = None):
    '''Generate docs with no index.
    The content may supply the index itself or it can have no index.
    '''
    for file in os.listdir('content/' + contentpath):
        path = os.path.join('content/' + contentpath, file)
        if os.path.isdir(path):
            continue
        logging.debug(f'working on unindexed file {path}')
        filename, extension = os.path.splitext(file)
        with open(path, 'r') as fd:
            data = fd.read()
        docspath = '..' + path.replace('content', '', 1)
        # read metadata
        data = _read_content(path)
        # render file according to file format
        if extension == ".html":
            with open(docspath, 'w') as fd:
                if template:
                    template = ENV.get_template(template)
                    fd.write(template.render(data))
                else:
                    fd.write(data['content'])
        logging.debug(f'generated file {docspath}')
        # TODO: more format generators
        # e.g. markdown (md), text (txt)


def generate_index():
    # Generate index page i.e. homepage
    INDEX.sort(key=lambda x: x[1], reverse=True)
    template = ENV.get_template('template_homepage')
    with open('../index.html', 'w') as fd:
        fd.write(template.render(posts=INDEX))
    logging.info('generated homepage index')
    # By default, the index page only contains a few recent posts
    # The index_all contains an index of all posts
    template = ENV.get_template('index_all')
    with open('../all.html', 'w') as fd:
        fd.write(template.render(posts=INDEX))


if __name__ == '__main__':
    generate_docs('Blog', 'blog', 'template_blog', 'index_blog')
    generate_docs('Poems', 'poems', 'template_poems', 'index_poems')
    generate_docs('Stories', 'stories', 'template_stories', 'index_stories')
    generate_sectioned_docs('dev', 'dev', 'template_dev', 'index_dev')
    generate_unindexed_docs('Research', 'research', 'template_research')
    generate_docs(
        'Research Blog', 'research/blog',
        'template_research_blog', 'index_research_blog')
    generate_index()
