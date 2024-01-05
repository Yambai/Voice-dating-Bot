import json
from html.parser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = ""

    def handle_data(self, data):
        self.text += data

def remove_html_tags(text):
    parser = MyHTMLParser()
    parser.feed(text)
    return parser.text
def remove_tags(text):
    for tag in ['<', '>', '/','\n', ' ']:
        text = text.replace(tag, '')
    return text



async def get_date(message):
    data = json.loads(f"{message}")["date"]
    text = json.dumps(data, indent=6, ensure_ascii=False)
    return text

