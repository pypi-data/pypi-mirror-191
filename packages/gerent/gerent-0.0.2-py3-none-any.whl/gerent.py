import json


BUFFER_SIZE = 512
url_linker = []


def __get_route(request):
    decoded_request = request.decode()
    response_array = decoded_request.split("\n")
    if response_array == ['']:
        return ''
    route = response_array[0].split(' ')[1]

    return route


def __get_method(request):
    decoded_request = request.decode()
    response_array = decoded_request.split("\n")
    method = response_array[0].split(' ')[0]

    return method


def __extract_payload(request):
    request_lines = request.split(b'\r\n')
    payload_start_index = request_lines.index(b'') + 1
    payload = b'\r\n'.join(request_lines[payload_start_index:])

    return json.loads(payload.decode('utf-8'))


def __validate_method(method, route):
    for entry in url_linker:
        if entry["route"] == route:
            if method in entry["methods"]:
                return True
    return False


def __send_respone(client, code, headers, response):
    main_header = f'HTTP/1.0 {code} OK\r\nContent-type: text/html\r\n'
    http_headers = __create_combined_headers(main_header, headers)

    client.send(http_headers)

    client.send(response)
    client.close()


def __create_combined_headers(main_header, headers):
    combined_headers = main_header
    bytes_headers = bytes(combined_headers, 'utf-8')

    for header in headers:
        bytes_headers += header+"\r\n"
    bytes_headers += "\r\n\r\n"
    return bytes_headers


def __create_url_linker(url, methods, function):
    # Check if path exists:
    found = False
    for entry in url_linker:
        if entry["route"] == url:
            found = True
            break
    # If path not exists- create new entry in url_linker
    if not found:
        url_linker.append({
            "route": url,
            "methods": methods,
            "function": function,
        })


def __get_route_function(route):
    function = None

    for entry in url_linker:
        if entry["route"] == route:
            function = entry["function"]

    return function


def __create_root_site():
    html_root = "<html><body><h1>Server root:\n</h1>"
    html_root += "<h2>possible routes:\n</h2>"
    for entry in url_linker:
        html_root += "<h3>\t- " + entry["route"] + "</h3>" + "\n"
    html_root += "</body></html>"

    return html_root


def listen(socket):
    html_root_view = __create_root_site()
    client, addrress = socket.accept()
    request = client.recv(BUFFER_SIZE)

    route = __get_route(request)
    function = __get_route_function(route)
    method = __get_method(request)

    print(f'New connection from: {addrress}')
    print("\n", request, "\n")

    if method == 'POST' or method == 'PUT':
        payload = __extract_payload(request)
        print(payload)

    if function != None:
        # Check if method is defined
        if __validate_method(method, route) == False:
            __send_respone(client, 405, [], "405 Method not allowed")
        # If method is defined, send normal response
        else:
            code, headers, response = function(request)
            __send_respone(client, code, headers, response)
    # if "/"- root url is not defined in url_linker send default response:
    elif route == "/":
        __send_respone(client, 200, [], html_root_view)
    else:
        with open("404.html", "r") as html_404:
            __send_respone(client, 404, [], html_404.read())


def route(url, methods=['GET']):
    return lambda function: __create_url_linker(url, methods, function)
