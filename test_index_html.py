import os
import re

def test_index_html_exists():
    assert os.path.exists('index.html'), 'index.html does not exist.'

def test_index_html_structure():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for doctype
    assert re.search(r'<!DOCTYPE html>', content, re.IGNORECASE), 'Missing <!DOCTYPE html> declaration.'
    # Check for html, head, and body tags
    assert '<html' in content.lower(), 'Missing <html> tag.'
    assert '<head' in content.lower(), 'Missing <head> tag.'
    assert '<body' in content.lower(), 'Missing <body> tag.'
