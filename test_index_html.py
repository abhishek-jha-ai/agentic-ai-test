import os
from html.parser import HTMLParser

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()

def test_index_html_exists():
    assert os.path.exists('index.html'), 'index.html does not exist.'

def test_index_html_has_html_structure():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<html' in content.lower(), 'index.html missing <html> tag.'
    assert '<head' in content.lower(), 'index.html missing <head> tag.'
    assert '<body' in content.lower(), 'index.html missing <body> tag.'

def test_index_html_has_title():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = TitleParser()
    parser.feed(content)
    assert parser.title is not None and parser.title != '', 'index.html missing <title> or it is empty.'


# --- Navigation Bar Tests ---
from html.parser import HTMLParser

class NavBarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nav_found = False
        self.nav_links = []
        self.in_nav = False
        self.current_link = None
    def handle_starttag(self, tag, attrs):
        if tag == 'nav':
            self.nav_found = True
            self.in_nav = True
        if self.in_nav and tag == 'a':
            href = None
            for k, v in attrs:
                if k == 'href':
                    href = v
            self.current_link = {'href': href, 'text': ''}
    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_nav = False
        if self.in_nav and tag == 'a' and self.current_link:
            self.nav_links.append(self.current_link)
            self.current_link = None
    def handle_data(self, data):
        if self.in_nav and self.current_link is not None:
            self.current_link['text'] += data.strip()

def test_index_html_has_navbar():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = NavBarParser()
    parser.feed(content)
    assert parser.nav_found, 'index.html missing <nav> navigation bar.'

def test_index_html_navbar_has_links():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = NavBarParser()
    parser.feed(content)
    assert parser.nav_found, 'index.html missing <nav> navigation bar.'
    # At least two links expected for navigation
    assert len(parser.nav_links) >= 2, 'Navigation bar should have at least two links.'
    for link in parser.nav_links:
        assert link['href'] is not None and link['href'].startswith('#'), 'Navigation links should use anchor hrefs.'
        assert link['text'], 'Navigation link text should not be empty.'
