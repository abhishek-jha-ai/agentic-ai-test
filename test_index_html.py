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


# --- Hero Section (Premium) Tests ---
from html.parser import HTMLParser

class HeaderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_header = False
        self.header_found = False
        self.header_id = None
        self.h1 = None
        self.p = None
        self.btn_text = None
        self.btn_href = None
        self.in_h1 = False
        self.in_p = False
        self.in_btn = False
        self.btn_class = None
    def handle_starttag(self, tag, attrs):
        if tag == 'header':
            self.in_header = True
            self.header_found = True
            for k, v in attrs:
                if k == 'id':
                    self.header_id = v
        if self.in_header and tag == 'h1':
            self.in_h1 = True
        if self.in_header and tag == 'p':
            self.in_p = True
        if self.in_header and tag == 'a':
            for k, v in attrs:
                if k == 'class' and 'btn' in v:
                    self.in_btn = True
                    self.btn_class = v
                if k == 'href':
                    self.btn_href = v
    def handle_endtag(self, tag):
        if tag == 'header':
            self.in_header = False
        if tag == 'h1':
            self.in_h1 = False
        if tag == 'p':
            self.in_p = False
        if tag == 'a':
            self.in_btn = False
    def handle_data(self, data):
        if self.in_header and self.in_h1:
            self.h1 = (self.h1 or '') + data.strip()
        if self.in_header and self.in_p:
            self.p = (self.p or '') + data.strip()
        if self.in_header and self.in_btn:
            self.btn_text = (self.btn_text or '') + data.strip()

def test_index_html_has_premium_hero_section():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for <header> with id="home"
    parser = HeaderParser()
    parser.feed(content)
    assert parser.header_found, 'index.html missing <header> section.'
    assert parser.header_id == 'home', 'Hero section <header> should have id="home".'
    # Check for premium wording in h1
    assert parser.h1 is not None and 'premium' in parser.h1.lower(), 'Hero section <h1> should mention "premium".'
    # Check for a call-to-action button
    assert parser.btn_text is not None and parser.btn_text.strip() != '', 'Hero section should have a call-to-action button.'
    assert parser.btn_href is not None and parser.btn_href.startswith('#'), 'Hero section button should link to a section.'
    # Check for background image and overlay in style
    assert "background:" in content and "url('https://images.unsplash.com/photo-1506744038136-46273834b3fb" in content, 'Hero section should have a premium background image.'
    assert 'header::before' in content and 'background: rgba(0, 0, 0, 0.6)' in content, 'Hero section should have a dark overlay for premium effect.'
    # Check for premium subtitle
    assert parser.p is not None and ("exclusive" in parser.p.lower() or "experience" in parser.p.lower()), 'Hero section <p> should have premium/exclusive wording.'


# --- Contact Section Tests ---
from html.parser import HTMLParser

class ContactSectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_contact_section = False
        self.contact_section_found = False
        self.links = []
        self.emails = []
        self.current_link = None
        self.current_tag = None
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            for k, v in attrs:
                if k == 'id' and v.lower() == 'contact':
                    self.in_contact_section = True
                    self.contact_section_found = True
        if self.in_contact_section and tag == 'a':
            href = None
            for k, v in attrs:
                if k == 'href':
                    href = v
            self.current_link = {'href': href, 'text': ''}
            self.current_tag = 'a'
        if self.in_contact_section and tag == 'span':
            self.current_tag = 'span'
    def handle_endtag(self, tag):
        if tag == 'section' and self.in_contact_section:
            self.in_contact_section = False
        if self.in_contact_section and tag == 'a' and self.current_link:
            self.links.append(self.current_link)
            self.current_link = None
            self.current_tag = None
        if self.in_contact_section and tag == 'span':
            self.current_tag = None
    def handle_data(self, data):
        if self.in_contact_section and self.current_tag == 'a' and self.current_link is not None:
            self.current_link['text'] += data.strip()
        if self.in_contact_section and self.current_tag == 'span':
            text = data.strip()
            if '@' in text:
                self.emails.append(text)

def test_index_html_has_contact_section():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = ContactSectionParser()
    parser.feed(content)
    assert parser.contact_section_found, 'index.html missing contact section with id="contact".'

def test_index_html_contact_section_has_email_and_links():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = ContactSectionParser()
    parser.feed(content)
    # At least one email placeholder (could be a span or mailto link)
    has_email = len(parser.emails) > 0 or any(l['href'] and l['href'].startswith('mailto:') for l in parser.links)
    assert has_email, 'Contact section should have an email placeholder.'
    # At least one GitHub or LinkedIn link placeholder
    has_github = any(l['href'] and 'github' in l['href'].lower() for l in parser.links)
    has_linkedin = any(l['href'] and 'linkedin' in l['href'].lower() for l in parser.links)
    assert has_github or has_linkedin, 'Contact section should have a GitHub or LinkedIn link placeholder.'


# --- Projects Section Tests ---
from html.parser import HTMLParser

class ProjectsSectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_projects_section = False
        self.projects_section_found = False
        self.project_cards = []
        self.current_project = None
        self.current_tag = None
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            for k, v in attrs:
                if k == 'id' and v.lower() == 'projects':
                    self.in_projects_section = True
                    self.projects_section_found = True
        if self.in_projects_section and tag == 'article':
            for k, v in attrs:
                if k == 'class' and 'project-card' in v:
                    self.current_project = {'title': '', 'description': '', 'link': None}
        if self.current_project is not None:
            if tag == 'h3':
                self.current_tag = 'title'
            elif tag == 'p':
                self.current_tag = 'description'
            elif tag == 'a':
                href = None
                for k, v in attrs:
                    if k == 'href':
                        href = v
                self.current_project['link'] = href
                self.current_tag = 'link'
    def handle_endtag(self, tag):
        if tag == 'section' and self.in_projects_section:
            self.in_projects_section = False
        if tag == 'article' and self.current_project is not None:
            self.project_cards.append(self.current_project)
            self.current_project = None
            self.current_tag = None
        if self.current_tag in ('title', 'description', 'link') and tag in ('h3', 'p', 'a'):
            self.current_tag = None
    def handle_data(self, data):
        if self.current_project is not None and self.current_tag in ('title', 'description'):
            self.current_project[self.current_tag] += data.strip()

def test_index_html_has_projects_section():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = ProjectsSectionParser()
    parser.feed(content)
    assert parser.projects_section_found, 'index.html missing projects section with id="projects".'
    # At least 3 project cards
    assert len(parser.project_cards) >= 3, 'Projects section should have at least 3 project cards.'
    for project in parser.project_cards:
        assert project['title'], 'Each project card should have a title.'
        assert project['description'], 'Each project card should have a description.'
        assert project['link'] is not None, 'Each project card should have a link.'
        assert project['link'].startswith('#') or project['link'].startswith('http'), 'Project link should be a valid URL or anchor.'
