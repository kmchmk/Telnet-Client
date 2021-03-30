import sys
import telnetlib

HOST = "6.tcp.ngrok.io"
PORT = "12076"

telnetObj = telnetlib.Telnet(HOST, PORT, 5)

def telnetInteract(until = "$ ", print_ = True):
    output = telnetObj.read_until(until.encode('ascii'), timeout=2)
    output = output.splitlines()
    output = list(map(bytes.decode, output))
    if (print_):
        print(*output[1:-1], sep = "\n")
    command = input(until)
    telnetObj.write(command.encode('ascii') + "\n".encode('ascii'))
    return command

telnetInteract("login: ")
telnetInteract("Password: ", print_= False)

while(True):
    command = telnetInteract("$ ")
    if(command in ["exit", "quit"]):
        break

telnetObj.close()