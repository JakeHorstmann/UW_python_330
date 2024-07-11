import socket
import sys
import traceback
import os
import mimetypes
import subprocess


def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->

        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    # TODO: Implement response_ok
    response_line = b"HTTP/1.1 200 OK\r\n"
    mime_line = b"Content-Type: " + mimetype + b"\r\n"
    content = body
    response = response_line + mime_line + b"\r\n" + content
    return response


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # TODO: Implement response_method_not_allowed
    error = b"HTTP/1.1 405 Method Not Allowed\r\n"
    return error


def response_not_found():
    """Returns a 404 Not Found response"""

    # TODO: Implement response_not_found
    error = b"HTTP/1.1 404 Not Found\r\n"
    return error


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    # TODO: implement parse_request
    request_line = request.split("\r\n")[0]
    method = request_line.split(" ")[0]
    # do not handle if the request is not GET
    if method != "GET":
        raise NotImplementedError
    path = request_line.split(" ")[1]
    return path


def response_path(path):
    """
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """
    # set webroot as root directory
    root_dir = os.path.join(os.path.dirname(
        os.path.realpath(sys.argv[0])), "webroot")
    parsed_path = path.split("/")
    # TODO: Raise a NameError if the requested content is not present
    # under webroot.
    full_path = os.path.join(root_dir, *parsed_path)
    if not os.path.exists(full_path):
        raise NameError
    # TODO: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.
    content = b""
    mime_type = b""
    if os.path.isdir(full_path):
        files = get_dir_content(full_path)
        content = format_files_as_text(files)
        mime_type = b"text/plain"
    if os.path.isfile(full_path):
        content = get_file_content(full_path)
        mime_type = mimetypes.guess_type(full_path)[0].encode()
        # if python file, gather the output to the terminal
        if full_path[-3:] == ".py":
            output = get_python_file_output(full_path)
            filename = os.path.basename(full_path).encode()
            content += b"\nContent output from running " + filename + b':\n'
            content += output
    return content, mime_type


def get_python_file_output(path):
    """
    Runs a python file and returns the output it spit to console
    """
    relative_path = os.path.relpath(path)
    output = subprocess.run(["python", relative_path],
                            capture_output=True).stdout
    return output


def get_dir_content(path):
    """
    Returns files in a directory
    """
    # make sure path exists
    if not os.path.exists(path):
        raise NameError
    # make sure it is a directory
    if not os.path.isdir(path):
        return None
    files = os.listdir(path)
    return files


def format_files_as_text(files):
    """
    Takes a list of files and returns them as binary plain text
    """
    response = "\n".join(files)
    return response.encode()


def get_file_content(path):
    """
    Returns content in a file as binary text
    """
    # make sure path exists
    if not os.path.exists(path):
        raise NameError
    # make sure it is a file
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as f:
        content = f.read()
    return content


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(15)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            conn.settimeout(15)
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break

                print("Request received:\n{}\n\n".format(request))
                # TODO: Use parse_request to retrieve the path from the request.
                try:
                    path = parse_request(request)
                    # TODO: Use response_path to retrieve the content and the mimetype,
                    # based on the request path.
                    content, mime_type = response_path(path)
                    # TODO; If parse_request raised a NotImplementedError, then let
                    # response be a method_not_allowed response. If response_path raised
                    # a NameError, then let response be a not_found response. Else,
                    # use the content and mimetype from response_path to build a
                    # response_ok.
                    response = response_ok(
                        body=content,
                        mimetype=mime_type
                    )
                except NotImplementedError:
                    response = response_method_not_allowed()
                except NameError:
                    response = response_not_found()
                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)
