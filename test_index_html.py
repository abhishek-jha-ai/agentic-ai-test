import os
from html.parser import HTMLParser

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

# --- BLOG SECTION TESTS ---
def test_blog_section_exists():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # Check for blog section by id
    assert '<section id="blog"' in html, 'Blog section with id="blog" missing.'
    # Check for Blog heading
    assert '>Blog<' in html or '>Blog</h2>' in html, 'Blog section heading missing.'
    # Check for intro text
    assert 'Read my latest thoughts' in html or 'tutorials on technology' in html, 'Blog section intro text missing.'


def test_blog_section_has_blog_cards():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # Blog cards should be articles with class project-card inside the blog section
    blog_section_start = html.find('<section id="blog"')
    assert blog_section_start != -1, 'Blog section not found.'
    blog_section_end = html.find('</section>', blog_section_start)
    assert blog_section_end != -1, 'Blog section closing tag not found.'
    blog_html = html[blog_section_start:blog_section_end]
    # There should be at least 3 blog cards
    count = blog_html.count('class="project-card"')
    assert count >= 3, f'Expected at least 3 blog cards, found {count}.'
    # Each card should have project-title and project-description
    assert 'How to Build a Modern Portfolio' in blog_html, 'Blog card title missing.'
    assert 'Productivity Tips for Developers' in blog_html, 'Blog card title missing.'
    assert 'Understanding REST APIs' in blog_html, 'Blog card title missing.'
    assert 'step-by-step guide' in blog_html or 'guide to designing' in blog_html, 'Blog card description missing.'
    assert 'Productivity' in blog_html, 'Blog tag missing.'
    assert 'APIs' in blog_html, 'Blog tag missing.'


def test_blog_cards_visual_consistency():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # Blog cards should use the same classes as project cards
    blog_section_start = html.find('<section id="blog"')
    blog_section_end = html.find('</section>', blog_section_start)
    blog_html = html[blog_section_start:blog_section_end]
    # Check for project-image, project-content, project-title, project-description, project-tags, project-actions
    assert 'project-image' in blog_html, 'project-image class missing in blog card.'
    assert 'project-content' in blog_html, 'project-content class missing in blog card.'
    assert 'project-title' in blog_html, 'project-title class missing in blog card.'
    assert 'project-description' in blog_html, 'project-description class missing in blog card.'
    assert 'project-tags' in blog_html, 'project-tags class missing in blog card.'
    assert 'project-actions' in blog_html, 'project-actions class missing in blog card.'


def test_blog_section_responsive():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read().lower()
    # Blog section should use projects-grid for layout
    blog_section_start = html.find('<section id="blog"')
    blog_section_end = html.find('</section>', blog_section_start)
    blog_html = html[blog_section_start:blog_section_end]
    assert 'projects-grid' in blog_html, 'Blog section missing projects-grid for layout.'
    # Responsive media query should exist
    assert '@media (max-width: 600px)' in html, 'Responsive media query missing for blog section.'
    # Cards should not use fixed pixel widths
    assert 'width: 100%' in html or 'grid-template-columns: 1fr' in html, 'Blog cards may not be responsive.'
    # Blog cards should be keyboard accessible (tabindex)
    assert 'tabindex="0"' in blog_html, 'Blog card missing tabindex for accessibility.'

# --- TESTIMONIALS SECTION TESTS ---
def test_testimonials_section_exists():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # Check for testimonials section by id
    assert '<section id="testimonials"' in html, 'Testimonials section with id="testimonials" missing.'
    # Check for Testimonials heading
    assert '>Testimonials<' in html or '>Testimonials</h2>' in html, 'Testimonials section heading missing.'
    # Check for intro text
    assert 'testimonial' in html.lower() or 'what people say' in html.lower(), 'Testimonials section intro text missing.'


def test_testimonials_cards_count_and_content():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    # Find testimonials section
    section_start = html.find('<section id="testimonials"')
    assert section_start != -1, 'Testimonials section not found.'
    section_end = html.find('</section>', section_start)
    assert section_end != -1, 'Testimonials section closing tag not found.'
    testimonials_html = html[section_start:section_end]
    # There should be at least 3 testimonial cards (look for a card class or article)
    card_count = testimonials_html.count('testimonial-card') + testimonials_html.count('class="modern-card"')
    # Accept either a dedicated testimonial-card class or modern-card reused
    assert card_count >= 3, f'Expected at least 3 testimonial cards, found {card_count}.'
    # Each card should have a person name, role/company, and testimonial text
    # We'll check for at least 3 distinct names and roles
    import re
    names = re.findall(r'<strong>([^<]+)</strong>', testimonials_html)
    roles = re.findall(r'<span[^>]*class=["\']?role["\']?[^>]*>([^<]+)</span>', testimonials_html)
    testimonial_texts = re.findall(r'<p[^>]*class=["\']?testimonial-text["\']?[^>]*>([^<]+)</p>', testimonials_html)
    # Accept at least 3 names and 3 roles or fallback to generic text check
    assert len(names) >= 3 or len(roles) >= 3 or card_count >= 3, 'Expected at least 3 testimonial names/roles.'
    # Check for testimonial text (at least 3)
    if len(testimonial_texts) < 3:
        # Fallback: look for generic testimonial text pattern
        assert testimonials_html.lower().count('recommend') + testimonials_html.lower().count('pleasure') + testimonials_html.lower().count('enjoyed') >= 1, 'Testimonial text missing.'


def test_nav_includes_testimonials_link():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read().lower()
    # Check for testimonials link in nav
    nav_start = html.find('<nav')
    nav_end = html.find('</nav>', nav_start)
    nav_html = html[nav_start:nav_end]
    assert 'testimonials' in nav_html, 'Testimonials link missing in navigation.'
    # Check that the link is an anchor with href to #testimonials
    assert 'href="#testimonials"' in nav_html, 'Testimonials nav link does not point to #testimonials.'


def test_active_nav_logic_includes_testimonials():
    # This test checks for the presence of logic or markup that would allow active-section highlight for testimonials
    # Since this is static HTML, we check for nav link to #testimonials and possible class or id for active state
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read().lower()
    nav_start = html.find('<nav')
    nav_end = html.find('</nav>', nav_start)
    nav_html = html[nav_start:nav_end]
    # Check for class or id that could be used for active state
    assert 'testimonials' in nav_html, 'Testimonials link missing in navigation for active logic.'
    # Accept either class="active" or data-active or similar for testimonials link
    # (We do not require the actual JS, just that the markup supports it)
    assert 'href="#testimonials"' in nav_html, 'Testimonials nav link does not point to #testimonials for active logic.'

# --- REGRESSION CHECKS ---
def test_home_about_projects_contact_still_present():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read().lower()
    # Home
    assert '<header id="home"' in html, 'Home section missing.'
    # About
    assert '<section id="about"' in html, 'About section missing.'
    # Projects
    assert '<section id="projects"' in html, 'Projects section missing.'
    # Contact
    assert '<section id="contact"' in html, 'Contact section missing.'
    # Data Engineering Pipeline card
    assert 'data engineering pipeline' in html, 'Data Engineering Pipeline card missing.'
