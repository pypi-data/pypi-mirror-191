# gerent
Gerent is a simple and lightweight web-framework for MicroPython.  

# pypi link:
https://pypi.org/project/gerent/

# TODO:
- beautify pyproject.toml  
- ✅ add post and put methods  
- ✅ add custom http_headers option  
- create docs (how does it work, pictures)  
- add favicon.ico support  
- ✅ create API root, with all url's  
- add examples  
- beutify micropython code?  
- add unitest tests  
- beautify web root site, add unified style  
- query params  
- optimize create_root_site  


# Currently supported devices:  
- Raspberry Pi Pico W  
- ESP8266  

# Example:
```python
import gerent, socket

@gerent.route("/hello/world")
def hello_world(request):
  return(200, {}, "Hello from gerent framework!")

# create socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

# run gerent client
while True:
  gerent.listen(s)
```
# Docs:
How does it work?  
While defining routes, for example:  
```python
@gerent.route("/hello/world", ['POST'])
def hello_world(request):
  return(200, {}, "Hello from gerent framework!")
```
Gerent backend creates an entry in url linker register:  
```python
{'route': '/hello/world', 'methods': ['POST'], 'function': <function hello_world at 0x2000c1c0>}
```
Url linker contains basic informations about route, avaliable methods and linked function for defined url.  
While Gerent client is running:  
```python
while True:
  gerent.listen(socket)
```
it's listening for incoming traffic, analyzing requests and properly responding to client's requests.  
