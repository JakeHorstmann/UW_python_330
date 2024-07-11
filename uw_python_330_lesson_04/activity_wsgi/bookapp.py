import re
import traceback
from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    main_html = book_html(book)
    footer = '<a href="/">Back to the list</a>'
    return main_html + "\n" + footer


def book_html(book):
    page = """
    <h2>{title}</h2>
    <table>
        <tr><th>Author</th><td>{author}</td><tr>
        <tr><th>Publisher</th><td>{publisher}</td><tr>
        <tr><th>ISBN</th><td>{isbn}</td><tr>
    </table>
    """
    return page.format(**book)


def books():
    response = "<h1>a list of books</h1>"
    for title in DB.titles():
        id = title["id"]
        book = DB.title_info(id)
        response += "\n" + "<h1>{}</h1>".format(id) + book_html(book)
    return response


def resolve_path(path):
    funcs = {
        "": books,
        "book": book
    }

    path = path.strip("/").split("/")
    func_name = path[0]
    args = path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
