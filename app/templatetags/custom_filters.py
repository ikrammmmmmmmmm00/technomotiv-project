from django import template  # Import the Django template module
import re

# Register the custom filter
register = template.Library()

@register.filter
def extract_file_id(drive_url):
    # Match Google Drive File IDs in URLs
    match = re.search(r'd/([^/]+)', drive_url)
    return match.group(1) if match else ''
