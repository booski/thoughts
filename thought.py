import random
import urllib
from os import chdir, path

'''
This function renders a template by replacing its tokens with provided values.

It accepts a template followed by the desired replacements as key-value mapped 
pairs. Each key is wrapped in leading and trailing '¤' characters and used to 
search the template for placeholders to be replaced by the corresponding value.
'''
def render_template(template, **replacements):
    result = template
    for key in sorted(replacements.keys(), 
                      key=len,
                      reverse=True):
        result = result.replace('¤'+key+'¤', replacements[key])
    return result

'''
Render a random thought from the list.

Returns the thought rendered as an html document based on a template.
'''
def random_thought():
    with open('./articles/Random thoughts') as f:
        return render_template('./support/page.html',
                               thought=random.choice([thought for thought
                                                      in f.readlines()
                                                      if thought.strip()]))

'''
WSGI entry point. Intended to be called by a WSGI-compliant web server.

Writes a formatted thought to the client.
'''
def application(environ, start_response):
    chdir(path.dirname(__file__))
    output = random_thought()
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [bytes(output, 'utf-8')]

'''
Standalone entry point.

Prints a formatted thought to stdout.
'''
if __name__ == '__main__':
    print(random_thought())
