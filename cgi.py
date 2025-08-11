# cgi.py - Minimal replacement for removed Python 3.13 cgi module
# Only includes the parts commonly used by libraries like httpx/googletrans.

def parse_header(line):
    """Stub for cgi.parse_header. Returns (line, params) tuple."""
    return line, {}

# If any library tries to import cgi.FieldStorage, define a dummy one
class FieldStorage:
    def __init__(self, *args, **kwargs):
        self.list = []
