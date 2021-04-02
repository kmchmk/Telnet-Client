### Requirements:
- python 3.x
- pip3

### Setup:
```sh
pip3 install telnetlib3
```

### Execute:
```sh
python telnet_client.py <host> <port>
```
- Type "exit" (without quotes) and press Enter to stop the client.

#### Note:
- When dealing with HTTP protocol, you may have to press Enter twice to let the server know that your request is complete.
- This client is implemented using [telnetlib3](https://pypi.org/project/telnetlib3/) library ([Docs here](https://docs.python.org/3/library/telnetlib.html)).