# create scribble
from scribblebug.models import Scribble
from scribblebug import gemini
from datetime import datetime

def get_user_scribbles(spider):
    return list(Scribble.objects.filter(spider=spider))

#input = keywords
def create_scribble(spider, keywords): # pass in: user, kws as list

    # name of scribble
    now = datetime.now()
    format_string = "%y%m%d_%H%M%S"
    name = spider.username+now.strftime(format_string)

    code = gemini.make_content(gemini.make_initial_prompt(keywords))
    # slice out <html>...</html> and keep only that
    start_index = code.find("<html>")
    end_index = code.find("</html>") + len("</html>")
    if start_index != -1 and end_index != -1:
        code = code[start_index:end_index]
    else: code = "<html><body>Out of Juice :(</body></html>"

    create_scribble_indb(name, spider, code)


def create_scribble_indb(name, author, code, chat_hist=""):
    s = Scribble(name=name,
                 spider=author,
                 chat_history=chat_hist,
                 code=code)
    s.save()