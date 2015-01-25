from pani import app

@app.template_filter('shorten_text')
def shorten_text(text):
    o = text 
    if len(text) > 50:
        o = '<span title="%s">%s</span>' % (text, text[:50])
    return o
