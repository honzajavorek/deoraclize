import re

import requests
from lxml import html
from flask import Flask, redirect, jsonify, request, abort


app = Flask(__name__)


@app.route('/')
def index():
    return redirect('http://docs.deoraclize.apiary.io')


@app.route('/search')
def api():
    if frozenset(request.args.keys()) != frozenset(['q']):
        abort(404)

    q = request.args.get('q')
    if not q:
        abort(422)

    results = list(lookup(q))
    return jsonify({'count': len(results), 'results': results})


def lookup(term):
    res = requests.get('https://www.oracle.com/products/acquired-a-z.html')
    dom = html.fromstring(res.content)
    dom.make_links_absolute(res.url)
    links = dom.cssselect('.cn12 li a')

    for link in links:
        if term.lower() in (link.text_content() or '').lower():
            url = link.get('href')
            if url:
                url = re.sub(r'^.+oracle\.com/', 'https://www.oracle.com/', url)

            yield {
                'title': link.text_content().strip(),
                'description': 'Acquired company product.',
                'url': url,
            }

    res = requests.get('https://www.oracle.com/products/oracle-a-z.html')
    dom = html.fromstring(res.content)
    dom.make_links_absolute(res.url)
    links = dom.cssselect('.cn12 li a')

    for link in links:
        if term.lower() in (link.text_content() or '').lower():
            url = link.get('href')
            if url:
                url = re.sub(r'^.+oracle\.com/', 'https://www.oracle.com/', url)

            yield {
                'title': link.text_content().strip(),
                'description': 'Product. {}.'.format(link.getparent().text_content().strip()),
                'url': url,
            }

    base_url = 'https://docs.oracle.com/cloud/latest/stcomputecs/STCSG/GUID-6CB9D494-4F3C-4B78-BD03-127983FEC357.htm'
    res = requests.get(base_url)
    dom = html.fromstring(res.content)
    dom.make_links_absolute(res.url)
    rows = dom.cssselect('tr')

    for row in rows:
        try:
            cells = row.cssselect('td')
            term_cell = cells[0]
            def_cell = cells[1]
        except LookupError as e:
            continue

        if term.lower() in (term_cell.text_content() or '').lower():
            url = '{}#{}'.format(base_url, term_cell.get('id'))

            yield {
                'title': term_cell.text_content().strip(),
                'description': 'Oracle Compute Cloud Service Term. {}.'.format(def_cell.text_content().strip()),
                'url': url,
            }

    base_url = 'https://github.com/honzajavorek/deoraclize/wiki/Deoraclize'
    res = requests.get(base_url)
    dom = html.fromstring(res.content)
    dom.make_links_absolute(res.url)
    headings = dom.cssselect('.wiki-body h2')

    for heading in headings:
        if term.lower() in (heading.text_content() or '').lower():
            try:
                url = '{}{}'.format(base_url, heading.cssselect('a[href^="#"]')[0].get('href'))
            except LookupError:
                url = base_url

            desc_parts = []
            element = heading
            while True:
                element = element.getnext()
                if element is None or element.tag == 'h2':
                    break
                desc_parts.append(element.text_content().strip())
            if desc_parts:
                description = '\n\n'.join(desc_parts)
            else:
                description = 'Community-contributed term.'

            yield {
                'title': heading.text_content().strip(),
                'description': description,
                'url': url,
            }

    base_url = 'https://en.wikipedia.org/wiki/List_of_acquisitions_by_Oracle'
    res = requests.get(base_url)
    dom = html.fromstring(res.content)
    dom.make_links_absolute(res.url)
    rows = dom.cssselect('.wikitable tr')

    for row in rows:
        try:
            cells = row.cssselect('td')
            date_cell = cells[0]
            term_cell = cells[1]
            def_cell = cells[2]
        except LookupError as e:
            continue

        if term.lower() in (term_cell.text_content() or '').lower():
            try:
                url = term_cell.cssselect('a')[0].get('href')
                if url and 'action=edit' in url:
                    url = base_url
                else:
                    url = 'https://en.wikipedia.org' + url
            except LookupError:
                url = base_url

            try:
                date = date_cell.cssselect('span')[-1].text_content().strip()
            except LookupError:
                date = date_cell.text_content().strip()

            yield {
                'title': term_cell.text_content().strip(),
                'description': 'Oracle acquisition ({}). {}.'.format(
                    date,
                    def_cell.text_content().strip().rstrip('.')
                ),
                'url': url,
            }


if __name__ == '__main__':
    app.run(debug=True)
