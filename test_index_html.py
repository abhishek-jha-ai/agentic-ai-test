import os
from html.parser import HTMLParser

# Existing tests omitted for brevity...

def test_hello_section_modernized():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check Hello section exists with id and modern-card class
    assert '<section id="hello"' in content, 'Hello section with id="hello" missing.'
    assert 'class="modern-card"' in content, 'Hello section missing modern-card class.'
    # Check for accent line
    assert 'class="accent-line"' in content, 'Hello section missing accent line.'
    # Check for icon chip with hand wave icon
    assert 'fa-hand-wave' in content, 'Hello section missing hand wave icon chip.'
    # Check heading text
    assert '>Hello!' in content, 'Hello section heading text missing or incorrect.'
    # Check paragraph with welcome and explore text
    assert 'Welcome to my personal portfolio' in content or 'welcome' in content.lower(), 'Hello section welcome text missing.'
    assert 'Explore my work' in content or 'explore' in content.lower(), 'Hello section explore text missing.'
    # Check tabindex for accessibility
    assert 'tabindex="0"' in content, 'Hello section missing tabindex for keyboard focus.'


def test_about_section_modernized():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check About section exists with id and modern-card class
    assert '<section id="about"' in content, 'About section with id="about" missing.'
    assert 'class="modern-card"' in content, 'About section missing modern-card class.'
    # Check for accent line
    assert 'class="accent-line"' in content, 'About section missing accent line.'
    # Check for icon chip with user icon
    assert 'fa-user' in content, 'About section missing user icon chip.'
    # Check heading text
    assert '>About Me' in content, 'About section heading text missing or incorrect.'
    # Check paragraph with software engineer and portfolio text
    assert 'software engineer' in content.lower(), 'About section missing software engineer text.'
    assert 'portfolio' in content.lower(), 'About section missing portfolio text.'
    # Check tabindex for accessibility
    assert 'tabindex="0"' in content, 'About section missing tabindex for keyboard focus.'


def test_hello_about_responsive_and_accessible():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read().lower()
    # Check hello-about-wrapper container
    assert 'hello-about-wrapper' in content, 'Container for hello and about sections missing.'
    # Check fadeSlideIn animation presence
    assert '@keyframes fadeslidein' in content, 'Fade slide in animation missing for hello/about sections.'
    # Check modern-card hover/focus styles
    assert '.modern-card:hover' in content or '.modern-card:focus-within' in content, 'Modern card hover/focus styles missing.'
    # Check color contrast hints (dark text on light background)
    assert '#0f172a' in content, 'Expected dark text color missing in hello/about sections.'
    # Check presence of glass effect (backdrop-filter)
    assert 'backdrop-filter' in content or '-webkit-backdrop-filter' in content, 'Glass effect missing in hello/about sections.'
    # Check responsive media queries for hello-about-wrapper
    assert '@media (max-width: 600px)' in content, 'Responsive media query missing for hello/about sections.'
    # Check that the sections have aria-labels for accessibility
    assert 'aria-label="hello section"' in content, 'Hello section missing aria-label.'
    assert 'aria-label="about section"' in content, 'About section missing aria-label.'


def test_data_engineering_pipeline_project_card_present():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # Check the card title exists
    assert 'Data Engineering Pipeline' in html, 'Data Engineering Pipeline project card title missing.'
    # Check for ETL ingestion mention
    assert 'ETL ingestion' in html or 'ETL' in html, 'ETL ingestion not mentioned in Data Engineering Pipeline card.'
    # Check for warehouse modeling/star schema
    assert 'star schema' in html.lower(), 'Warehouse modeling (star schema) not mentioned.'
    # Check for orchestration/scheduling
    assert 'orchestration' in html.lower(), 'Orchestration not mentioned.'
    assert 'scheduling' in html.lower(), 'Scheduling not mentioned.'
    # Check for observability/alerts/freshness/row-count
    assert 'observability' in html.lower(), 'Observability not mentioned.'
    assert 'freshness' in html.lower(), 'Data freshness not mentioned.'
    assert 'row-count' in html.lower() or 'row count' in html.lower(), 'Row-count checks not mentioned.'
    # Check for tech stack tags
    for tag in ['Python', 'Airflow', 'dbt', 'Postgres', 'Great Expectations', 'APIs']:
        assert tag in html, f'Tech stack tag {tag} missing from Data Engineering Pipeline card.'
    # Check card is in projects-grid
    assert 'projects-grid' in html, 'Projects grid missing.'
    # Check card uses project-card class
    assert 'project-card' in html, 'Project card class missing for Data Engineering Pipeline.'


def test_data_engineering_pipeline_card_visual_consistency():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # Check that the Data Engineering Pipeline card uses the same classes as other cards
    # Find all project-card articles
    from html.parser import HTMLParser
    class ProjectCardParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.cards = []
            self.current = None
            self.in_article = False
        def handle_starttag(self, tag, attrs):
            if tag == 'article':
                for k, v in attrs:
                    if k == 'class' and 'project-card' in v:
                        self.in_article = True
                        self.current = ''
            if self.in_article:
                self.current += self.get_starttag_text() or ''
        def handle_endtag(self, tag):
            if tag == 'article' and self.in_article:
                self.cards.append(self.current)
                self.in_article = False
                self.current = None
            elif self.in_article:
                self.current += f'</{tag}>'
        def handle_data(self, data):
            if self.in_article:
                self.current += data
    parser = ProjectCardParser()
    parser.feed(html)
    # There should be at least 4 cards (including Data Engineering Pipeline)
    assert len(parser.cards) >= 4, 'Expected at least 4 project cards.'
    # Find the Data Engineering Pipeline card
    found = False
    for card in parser.cards:
        if 'Data Engineering Pipeline' in card:
            found = True
            # Check for project-image, project-content, project-title, project-description, project-tags, project-actions
            assert 'project-image' in card, 'project-image class missing in Data Engineering Pipeline card.'
            assert 'project-content' in card, 'project-content class missing in Data Engineering Pipeline card.'
            assert 'project-title' in card, 'project-title class missing in Data Engineering Pipeline card.'
            assert 'project-description' in card, 'project-description class missing in Data Engineering Pipeline card.'
            assert 'project-tags' in card, 'project-tags class missing in Data Engineering Pipeline card.'
            assert 'project-actions' in card, 'project-actions class missing in Data Engineering Pipeline card.'
    assert found, 'Data Engineering Pipeline card not found among project cards.'


def test_data_engineering_pipeline_card_responsive():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read().lower()
    # Check for responsive grid media queries
    assert '@media (max-width: 600px)' in html, 'Responsive media query missing for projects grid.'
    # Check that the card does not use fixed pixel widths that would break on mobile
    assert 'width: 100%' in html or 'grid-template-columns: 1fr' in html, 'Projects grid may not be responsive.'
    # Check that the card is readable (has project-title and project-description)
    assert 'project-title' in html, 'Project title missing in responsive check.'
    assert 'project-description' in html, 'Project description missing in responsive check.'
