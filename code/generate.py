#!/usr/bin/env python3

import json
from jinja2 import Environment, FileSystemLoader
import logging
import os

ENV = Environment(
    loader=FileSystemLoader('templates'))
INDEX = []
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def _load(filename):
    with open(filename, 'r') as fd:
        data = json.load(fd)
    return data


def _load_tags():
    with open('legacy_data/Tag-2019-05-28.json', 'r') as fd:
        data = json.load(fd)
    tags = {}
    for tag in data:
        tags[str(tag['id'])] = tag['name']
    return tags


def _generate(datadump, name):
    data = _load(datadump)
    tags = _load_tags()
    template = ENV.get_template(f'template_{name}')
    index = []
    for blog in data:
        blog['tags'] = [tags[tag] for tag in blog['tags'].split(',')]
        with open(f'../{name}/{blog["slug"]}.html', 'w') as fd:
            fd.write(template.render(
                title=blog['title'],
                description=blog['short_description'],
                published=blog['date_published'],
                modified=blog['date_updated'],
                tags=blog['tags'],
                content=blog['body_text'],
                headerimage=blog['headerimage']
            ))
        index.append((
            blog['title'],
            blog['date_published'],
            blog['date_updated'],
            blog['slug'],
            blog['short_description'],
        ))
    index.sort(key=lambda x: x[1], reverse=True)
    template = ENV.get_template(f'index_{name}')
    with open(f'../{name}/index.html', 'w') as fd:
        fd.write(template.render(blogs=index))


def _export_content(datadump, name):
    data = _load(datadump)
    tags = _load_tags()
    template = ENV.get_template(f'template_content')
    for blog in data:
        blog['tags'] = [tags[tag] for tag in blog['tags'].split(',')]
        with open(f'./content/{name}/{blog["slug"]}.html', 'w') as fd:
            fd.write(template.render(
                title=blog['title'],
                description=blog['short_description'],
                published=blog['date_published'],
                modified=blog['date_updated'],
                tags=blog['tags'],
                content=blog['body_text'],
                headerimage=blog['headerimage']
            ))


def _read_content(path):
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
    logging.debug(f'generating docs for {name}')
    for root, _, files in os.walk('content/' + contentpath):
        if not files:
            logging.debug(f'skipped: found no files in {root}')
            continue

        directorypath = root.replace('content', '..', 1)
        logging.debug(f'directorypath is {directorypath}')
        if not os.path.exists(directorypath):
            logging.debug(f'created directory {directorypath}')
            os.makedirs(directorypath)
        index = []
        for f in files:
            filename, extension = os.path.splitext(f)
            path = os.path.join(root, f)
            data = _read_content(path)
            index.append((
                data['title'],
                data['published'],
                data['modified'],
                filename,
                data['description'],
            ))
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
            if extension == ".html":
                template = ENV.get_template(template_content)
                with open(docspath, 'w') as fd:
                    fd.write(template.render(data))
            logging.debug(f'generated file {docspath}')
            # TODO: more format generators
            # e.g. markdown (md), text (txt)
        index.sort(key=lambda x: x[1], reverse=True)
        template = ENV.get_template(template_index)
        with open(f'{directorypath}/index.html', 'w') as fd:
            fd.write(template.render(blogs=index))
        logging.info(f'generated {name} index')


def generate_sectioned_docs(
        name, contentpath, template_content, template_index):

    def _generate_sectioned_docs(path):
        if os.path.isfile(path + '/metadata'):
            with open(path + '/metadata', 'r') as fd:
                section = fd.read().split(':')[-1].strip()
        else:
            section = 'general'
        logging.debug(f'generating section-docs for {path}')
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
                logging.debug(f'reading {path}')
                index.append((
                    data['title'],
                    data['published'],
                    data['modified'],
                    filename,
                    data['description'],
                    section,
                ))
                INDEX.append((
                    data['title'],
                    data['published'],
                    data['modified'],
                    f'{path}/{filename}',
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
                fd.write(template.render(blogs=index))
        break

    dev_index.sort(key=lambda x: x[1][1][1], reverse=True)
    with open('../' + contentpath + '/index.html', 'w') as fd:
        template = ENV.get_template(template_index)
        fd.write(template.render(sections=dev_index))


def generate_index():
    INDEX.sort(key=lambda x: x[1], reverse=True)
    template = ENV.get_template('template_homepage')
    with open('../index.html', 'w') as fd:
        fd.write(template.render(latest=INDEX[0], posts=INDEX[:10]))
    logging.info('generated homepage index')
    template = ENV.get_template('index_all')
    with open('../all.html', 'w') as fd:
        fd.write(template.render(posts=INDEX))


if __name__ == '__main__':
    # extract data from dump
    # _generate('BlogPost-2019-05-27.json', 'blog')
    # _generate('Poem-2019-05-27.json', 'poems')
    # _generate('Story-2019-05-27.json', 'stories')
    # _generate('DevPost-2019-05-27.json', 'dev')
    # _generate('ResearchBlogPost-2019-05-27.json', 'research')

    # generate content files
    # _export_content('BlogPost-2019-05-27.json', 'blog')
    # _export_content('Poem-2019-05-27.json', 'poems')
    # _export_content('Story-2019-05-27.json', 'stories')
    # _export_content('DevPost-2019-05-27.json', 'dev')
    # _export_content(
    #     'legacy_data/ResearchBlogPost-2019-05-27.json', 'research/blog')

    # generate statis documents for serving
    generate_docs('Blog', 'blog', 'template_blog', 'index_blog')
    generate_docs('Poems', 'poems', 'template_poems', 'index_poems')
    generate_docs('Stories', 'stories', 'template_stories', 'index_stories')
    generate_sectioned_docs('dev', 'dev', 'template_dev', 'index_dev')
    generate_docs(
        'Research Blog', 'research/blog',
        'template_research_blog', 'index_research_blog')
    generate_index()
