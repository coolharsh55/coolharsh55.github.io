#!/usr/bin/env python3

import json
from jinja2 import Environment, FileSystemLoader
import os

ENV = Environment(
    loader=FileSystemLoader('templates')
    )

INDEX = []


def _load(filename):
    with open(filename, 'r') as fd:
        data = json.load(fd)
    return data


def _load_tags():
    with open('Tag-2019-05-28.json', 'r') as fd:
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
        with open(f'./docs/{name}/{blog["slug"]}.html', 'w') as fd:
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
    with open(f'./docs/{name}/index.html', 'w') as fd:
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


def _generate_docs():
    for root, directory, files in os.walk('content'):
        if not files:
            continue
        directory = root.split('/')[-1]
        # replace content path with docs path
        # create directory if it does not exist
        directorypath = 'docs' + root.replace('content', '', 1)
        if not os.path.exists(directorypath):
            os.makedirs(directorypath)
        index = []
        # render templates
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
                f'{directory}/{filename}',
                data['description'],
                directory,
                ))
            docspath = 'docs' + path.replace('content', '', 1)
            if extension == ".html":
                template = ENV.get_template(f'template_{directory}')
                with open(docspath, 'w') as fd:
                    fd.write(template.render(data))
            # TODO: more format generators
            # e.g. markdown (md), text (txt)
        index.sort(key=lambda x: x[1], reverse=True)
        template = ENV.get_template(f'index_{directory}')
        with open(f'./{directorypath}/index.html', 'w') as fd:
            fd.write(template.render(blogs=index))
    INDEX.sort(key=lambda x: x[1], reverse=True)
    template = ENV.get_template('template_homepage')
    with open('./docs/index.html', 'w') as fd:
        fd.write(template.render(latest=INDEX[0], posts=INDEX[:10]))
    # template = ENV.get_template('template_all')
    # with open('./docs/all.html', 'w') as fd:
    #     fd.write(template.render(posts=INDEX[:10]))


if __name__ == '__main__':
    # _generate('BlogPost-2019-05-27.json', 'blog')
    # _generate('Poem-2019-05-27.json', 'poems')
    # _generate('Story-2019-05-27.json', 'stories')
    # _generate('DevPost-2019-05-27.json', 'dev')
    # _generate('ResearchBlogPost-2019-05-27.json', 'research')
    # _export_content('BlogPost-2019-05-27.json', 'blog')
    # _export_content('Poem-2019-05-27.json', 'poems')
    # _export_content('Story-2019-05-27.json', 'stories')
    # _export_content('DevPost-2019-05-27.json', 'dev')
    _generate_docs()
