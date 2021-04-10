### Requirements:
- python 3.x

### How to execute:
```sh
python telnet_client.py <host> <port>
```
- Type "exit" (without quotes) and press Enter to stop the client.

#### Examples:

##### 1. Connect to a HTTP web server
```sh
python telnet_client.py google.com 80

GET / HTTP/1.1

# output will be displayed here
exit
```

##### 2. Connect to a Linux backend runnnig Telnet server
```sh
python telnet_client.py localhost 23

# <User> login: <your_username>
# Password: <your_password>


# ~$> <linux_command>
# output will be displayed here

exit
```

#### Note:
- When dealing with HTTP protocol, you may have to press Enter twice to let the server know that your request is complete.
- This client is implemented using a stripped down version of [telnetlib3](https://pypi.org/project/telnetlib3/) library.

Refer:
- [Telnetlib3 python docs](https://docs.python.org/3/library/telnetlib.html)
- [Telnetlib3 python source](https://github.com/python/cpython/blob/3.9/Lib/telnetlib.py)
- [Telnet protocol specification](https://tools.ietf.org/html/rfc854)