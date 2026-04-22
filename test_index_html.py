import os
from html.parser import HTMLParser

def test_index_html_exists():
    assert os.path.exists('index.html'), 'index.html does not exist.'

def test_index_html_has_html_structure():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<html' in content.lower(), 'index.html missing <html> tag.'
    assert '<head' in content.lower(), 'index.html missing <head> tag.'
    assert '<body' in content.lower(), 'index.html missing <body> tag.'

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

def test_index_html_has_title():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = TitleParser()
    parser.feed(content)
    assert parser.title is not None and parser.title != '', 'index.html missing <title> or it is empty.'

# --- Navigation Bar Tests ---
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

# --- Navigation Color Tests ---
def test_index_html_navbar_background_pink():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check nav background is pink
    assert 'nav {' in content
    # Accepts background: pink; or background: pink;
    found = False
    for line in content.splitlines():
        if line.strip().startswith('nav {'):
            found = True
        if found and 'background:' in line:
            if 'pink' in line:
                return
            # Accept background: #ffc0cb (hex for pink)
            if '#ffc0cb' in line.lower():
                return
        if found and '}' in line:
            break
    assert False, 'Navigation bar background should be pink.'

def test_index_html_navbar_text_white():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check nav link color is white
    found = False
    for line in content.splitlines():
        if 'nav ul li a' in line:
            found = True
        if found and 'color:' in line:
            if 'white' in line or '#fff' in line.lower():
                return
        if found and '}' in line:
            break
    assert False, 'Navigation bar link text should be white.'

# --- Premium Navigation Tests ---
def test_index_html_navbar_has_box_shadow():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for box-shadow in nav style
    assert 'nav {' in content
    assert 'box-shadow' in content, 'Navigation bar should have a box-shadow for premium look.'

def test_index_html_navbar_links_have_hover_effect():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for hover/active/focus effect on nav links
    assert 'nav ul li a:hover' in content or 'nav ul li a:focus' in content, 'Navigation links should have hover/focus effect.'
    assert 'transform: scale(1.1)' in content or 'background: rgba(255, 255, 255, 0.3)' in content, 'Navigation links should have premium hover/focus styling.'

def test_index_html_navbar_is_sticky():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for sticky positioning
    assert 'position: sticky' in content or 'position: -webkit-sticky' in content, 'Navigation bar should be sticky.'
    assert 'top: 0' in content, 'Sticky navigation bar should have top: 0.'

def test_index_html_navbar_links_have_blur_effect():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for backdrop-filter blur on nav links
    assert 'backdrop-filter: blur(6px)' in content or '-webkit-backdrop-filter: blur(6px)' in content, 'Navigation links should have a blur effect for premium look.'

# --- Hero Section (Header) Tests ---
class HeaderImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_header = False
        self.hero_img_found = False
        self.hero_img_src = None
        self.hero_img_alt = None
        self.hero_img_class = None
    def handle_starttag(self, tag, attrs):
        if tag == 'header':
            self.in_header = True
        if self.in_header and tag == 'img':
            for k, v in attrs:
                if k == 'class' and 'hero-image' in v:
                    self.hero_img_found = True
                    for k2, v2 in attrs:
                        if k2 == 'src':
                            self.hero_img_src = v2
                        if k2 == 'alt':
                            self.hero_img_alt = v2
                        if k2 == 'class':
                            self.hero_img_class = v2
    def handle_endtag(self, tag):
        if tag == 'header':
            self.in_header = False

def test_index_html_header_has_hero_image():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    parser = HeaderImageParser()
    parser.feed(content)
    assert parser.hero_img_found, 'Hero section should have a premium image with class="hero-image".'
    assert parser.hero_img_src is not None and parser.hero_img_src.strip() != '', 'Hero image should have a src attribute.'
    assert parser.hero_img_alt is not None and parser.hero_img_alt.strip() != '', 'Hero image should have an alt attribute.'
    assert 'hero-image' in parser.hero_img_class, 'Hero image should have class="hero-image".'

def test_index_html_header_hero_image_style():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for .hero-image CSS
    assert '.hero-image' in content, 'Hero image CSS class missing.'
    assert 'box-shadow' in content, 'Hero image should have box-shadow for premium look.'
    assert 'border-radius' in content, 'Hero image should have border-radius for polish.'
    assert 'opacity: 0.9' in content or 'opacity:0.9' in content, 'Hero image should have opacity for polish.'

def test_index_html_has_header_section():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<header' in content.lower(), 'index.html missing <header> section.'
    assert 'welcome to my portfolio' in content.lower(), 'Header should contain welcome message.'

def test_index_html_header_has_h1_and_p():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<h1>' in content.lower(), 'Header missing <h1> tag.'
    assert '<p>' in content.lower(), 'Header missing <p> tag.'

# --- About Section Tests ---
def test_index_html_has_about_section():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<section id="about"' in content.lower(), 'index.html missing about section with id="about".'
    assert 'software engineer' in content.lower(), 'About section should mention software engineer.'
    assert 'portfolio' in content.lower(), 'About section should mention portfolio.'

# --- Contact Section Tests ---
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
