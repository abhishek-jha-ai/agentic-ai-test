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


def test_navigation_script_is_deferred():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check nav.js is loaded with defer
    assert '<script defer src="nav.js"></script>' in content, "nav.js script should be loaded with defer for non-blocking navigation."


def test_navigation_menu_is_rendered_modularly():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # The <nav> element should be empty in the HTML markup (menu is rendered by JS)
    import re
    nav_match = re.search(r'<nav[^>]*id="main-nav"[^>]*>(.*?)</nav>', content, re.DOTALL)
    assert nav_match, "Main nav element with id='main-nav' missing."
    nav_inner = nav_match.group(1).strip()
    assert nav_inner == '', "Navigation menu should not be rendered inline in HTML; it should be injected by JS."


def test_navigation_script_avoids_inline_injection():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # The navigation script should not use innerHTML or document.write (to avoid injection points)
    nav_script_match = False
    for line in content.splitlines():
        if 'const navLinks' in line:
            nav_script_match = True
        if nav_script_match:
            assert 'innerHTML' not in line, "Navigation script should not use innerHTML (potential injection point)."
            assert 'document.write' not in line, "Navigation script should not use document.write (potential injection point)."
    # Also check that the script uses createElement for menu rendering
    assert 'createElement' in content, "Navigation script should use createElement for modular rendering."


def test_navigation_code_is_modular_and_not_inline():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # The navigation code should be wrapped in an IIFE (modular, not polluting global scope)
    assert '(function()' in content or '(function ()' in content, "Navigation code should be modular (IIFE pattern)."
    # The navigation code should only append to nav, not replace or overwrite
    assert 'appendChild' in content, "Navigation code should use appendChild for safe DOM updates."
