'''
This code is a stripped down version of telnetlib3
Source: https://github.com/python/cpython/blob/3.9/Lib/telnetlib.py

Credit goes to original authors
'''

import sys, socket, selectors

# Telnet protocol characters
IAC  = bytes([255]) # "Interpret As Command"
DONT = bytes([254])
DO   = bytes([253])
WONT = bytes([252])
WILL = bytes([251])
SB =  bytes([250])  # Subnegotiation Begin
SE  = bytes([240])  # Subnegotiation End
theNULL = bytes([0])

# poll/select have the advantage of not requiring any extra file descriptor,
# contrarily to epoll/kqueue (also, they require a single syscall).
if hasattr(selectors, 'PollSelector'):
    _TelnetSelector = selectors.PollSelector
else:
    _TelnetSelector = selectors.SelectSelector


class Telnet:

    def __init__(self, host, port, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.rawq = b''
        self.irawq = 0
        self.cookedq = b''
        self.eof = 0
        self.iacseq = b'' # Buffer for IAC sequence.
        self.sb = 0 # flag for SB and SE sequence.
        self.sbdataq = b''

    def open(self):
        self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def close(self):
        sock = self.sock
        self.sock = None
        self.eof = True
        self.iacseq = b''
        self.sb = 0
        if sock:
            sock.close()

    def fileno(self): # Return the file descriptor of socket
        return self.sock.fileno()

    def write(self, buffer): # Send contents via socket
        if IAC in buffer:
            buffer = buffer.replace(IAC, IAC+IAC) # Double IAC characters.
        self.sock.sendall(buffer)

    def read_content(self): # AKA read_eager
        self.process_rawq()
        while not self.cookedq and not self.eof and self.sock_avail():
            self.fill_rawq()
            self.process_rawq()
        buf = self.cookedq
        self.cookedq = b''
        if not buf and self.eof and not self.rawq:
            raise EOFError('telnet connection closed')
        return buf

    def process_rawq(self): # Transfer from raw queue to cooked queue.
        buf = [b'', b'']
        try:
            while self.rawq:
                c = self.rawq_getchar()
                if not self.iacseq:
                    if c == theNULL:
                        continue
                    if c == b"\021":
                        continue
                    if c != IAC:
                        buf[self.sb] = buf[self.sb] + c
                        continue
                    else:
                        self.iacseq += c
                elif len(self.iacseq) == 1:
                    # 'IAC: IAC CMD [OPTION only for WILL/WONT/DO/DONT]'
                    if c in (DO, DONT, WILL, WONT):
                        self.iacseq += c
                        continue

                    self.iacseq = b''
                    if c == IAC:
                        buf[self.sb] = buf[self.sb] + c
                    else:
                        if c == SB: # SB ... SE start.
                            self.sb = 1
                            self.sbdataq = b''
                        elif c == SE:
                            self.sb = 0
                            self.sbdataq = self.sbdataq + buf[1]
                            buf[1] = b''
                elif len(self.iacseq) == 2:
                    cmd = self.iacseq[1:2]
                    self.iacseq = b''
                    opt = c
                    if cmd in (DO, DONT):
                        self.sock.sendall(IAC + WONT + opt)
                    elif cmd in (WILL, WONT):
                        self.sock.sendall(IAC + DONT + opt)
        except EOFError: # raised by self.rawq_getchar()
            self.iacseq = b'' # Reset on EOF
            self.sb = 0
            pass
        self.cookedq = self.cookedq + buf[0]
        self.sbdataq = self.sbdataq + buf[1]

    def rawq_getchar(self): # Get next char from raw queue.
        if not self.rawq:
            self.fill_rawq()
            if self.eof:
                raise EOFError
        c = self.rawq[self.irawq:self.irawq+1]
        self.irawq = self.irawq + 1
        if self.irawq >= len(self.rawq):
            self.rawq = b''
            self.irawq = 0
        return c

    def fill_rawq(self): # Fill raw queue from exactly one recv() system call.
        if self.irawq >= len(self.rawq):
            self.rawq = b''
            self.irawq = 0
        # The buffer size should be fairly small so as to avoid quadratic
        # behavior in process_rawq() above
        buf = self.sock.recv(50)
        self.eof = (not buf)
        self.rawq = self.rawq + buf

    def sock_avail(self): # Test whether data is available on the socket.
        with _TelnetSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            return bool(selector.select(0))
