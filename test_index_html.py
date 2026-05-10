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

# --- Projects Section Tests ---
class ProjectsSectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_projects_section = False
        self.projects_section_found = False
        self.project_cards = []
        self.current_project = None
        self.current_tag = None
        self.card_img = None
        self.card_tags = []
        self.card_btns = []
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            for k, v in attrs:
                if k == 'id' and v.lower() == 'projects':
                    self.in_projects_section = True
                    self.projects_section_found = True
        if self.in_projects_section and tag == 'article':
            for k, v in attrs:
                if k == 'class' and 'project-card' in v:
                    self.current_project = {
                        'title': '',
                        'description': '',
                        'img': None,
                        'tags': [],
                        'btns': []
                    }
        if self.current_project is not None:
            if tag == 'img':
                for k, v in attrs:
                    if k == 'class' and 'project-image' in v:
                        self.current_project['img'] = dict(attrs)
            elif tag == 'h3':
                self.current_tag = 'title'
            elif tag == 'p':
                self.current_tag = 'description'
            elif tag == 'span':
                for k, v in attrs:
                    if k == 'class' and 'project-tag' in v:
                        self.current_tag = 'tag'
            elif tag == 'a':
                for k, v in attrs:
                    if k == 'class' and 'project-btn' in v:
                        self.current_tag = 'btn'
                        self.card_btn_href = dict(attrs).get('href', None)
                        self.card_btn_class = dict(attrs).get('class', '')
                        self.card_btn_text = ''
    def handle_endtag(self, tag):
        if tag == 'section' and self.in_projects_section:
            self.in_projects_section = False
        if tag == 'article' and self.current_project is not None:
            self.project_cards.append(self.current_project)
            self.current_project = None
            self.current_tag = None
        if self.current_tag == 'tag' and tag == 'span':
            self.current_tag = None
        if self.current_tag == 'btn' and tag == 'a':
            self.current_project['btns'].append({
                'href': self.card_btn_href,
                'class': self.card_btn_class,
                'text': self.card_btn_text.strip()
            })
            self.current_tag = None
        if self.current_tag in ('title', 'description') and tag in ('h3', 'p'):
            self.current_tag = None
    def handle_data(self, data):
        if self.current_project is not None:
            if self.current_tag == 'title':
                self.current_project['title'] += data.strip()
            elif self.current_tag == 'description':
                self.current_project['description'] += data.strip()
            elif self.current_tag == 'tag':
                self.current_project['tags'].append(data.strip())
            elif self.current_tag == 'btn':
                self.card_btn_text += data

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
        # Check for image
        assert project['img'] is not None, 'Each project card should have a project image.'
        assert 'src' in project['img'] and project['img']['src'], 'Project image should have a src attribute.'
        assert 'alt' in project['img'] and project['img']['alt'], 'Project image should have an alt attribute.'
        # Check for tags
        assert len(project['tags']) >= 2, 'Each project card should have at least 2 tech stack tags.'
        # Check for buttons
        btn_texts = [b['text'].lower() for b in project['btns']]
        assert any('live demo' in t for t in btn_texts), 'Each project card should have a Live Demo button.'
        assert any('github' in t for t in btn_texts), 'Each project card should have a GitHub button.'
        # Check for button hrefs
        for btn in project['btns']:
            assert btn['href'] is not None, 'Project action button should have an href.'
            assert btn['href'].startswith('#') or btn['href'].startswith('http') or btn['href'] == '#', 'Project button href should be a valid URL or anchor.'


def test_projects_section_intro_and_heading():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read().lower()
    # Section intro text
    assert 'explore a selection of my recent work' in content or 'projects' in content, 'Projects section should have an intro text.'
    # Section heading
    assert '<h2' in content and 'projects' in content, 'Projects section should have a heading.'


def test_projects_section_responsive_grid():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for CSS grid layout
    assert '.projects-grid' in content, 'Projects section should use a grid layout.'
    assert 'grid-template-columns' in content, 'Projects grid should define grid-template-columns.'
    # Responsive breakpoints
    assert '@media (max-width: 900px)' in content, 'Projects grid should be responsive for tablets.'
    assert '@media (max-width: 600px)' in content, 'Projects grid should be responsive for mobile.'


def test_projects_card_modern_styles():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read().lower()
    # Glassmorphism, rounded corners, shadows, gradient accents
    assert 'backdrop-filter' in content or '-webkit-backdrop-filter' in content, 'Project cards should use glassmorphism (backdrop-filter).'
    assert 'border-radius: 22px' in content or 'border-radius: 20px' in content, 'Project cards should have large rounded corners.'
    assert 'box-shadow' in content, 'Project cards should have soft shadows.'
    # Gradient accent for tags/buttons
    assert 'linear-gradient' in content, 'Project cards should use gradient accents.'


def test_projects_card_hover_effects():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read().lower()
    # Card hover lift
    assert '.project-card:hover' in content or '.project-card:focus-within' in content, 'Project cards should have a hover/focus lift effect.'
    assert 'transform:' in content, 'Project card hover should use transform for lift/scale.'
    # Glow/gradient border on hover
    assert 'box-shadow' in content and 'project-card:hover' in content, 'Project card hover should have a glow or shadow.'
    # Image zoom effect
    assert '.project-card:hover .project-image' in content or '.project-card:focus-within .project-image' in content, 'Project image should zoom on card hover.'


def test_projects_card_buttons_and_animations():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read().lower()
    # Button styles
    assert '.project-btn' in content, 'Project cards should have modern CTA buttons.'
    assert 'border-radius: 14px' in content or 'border-radius: 12px' in content, 'Project buttons should have rounded corners.'
    # Button hover/animation
    assert '.project-btn:hover' in content or '.project-btn:focus' in content, 'Project buttons should have hover/focus effect.'
    assert 'transform:' in content, 'Project button hover should use transform for animation.'
    # Arrow icon animation
    assert '.arrow' in content, 'Project button should have an arrow icon.'
    assert '.project-btn:hover .arrow' in content or '.project-btn:focus .arrow' in content, 'Arrow icon should animate on button hover.'
