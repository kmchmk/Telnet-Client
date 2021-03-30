import sys
import telnetlib

HOST = "6.tcp.ngrok.io"
PORT = "12076"

telnetObj = telnetlib.Telnet(HOST, PORT, 5)

def telnetInteract(until = "$ ", print_first_line = True):
    output = telnetObj.read_until(until.encode('ascii'), timeout=5)
    output = output.splitlines()
    output = list(map(bytes.decode, output))
    if not print_first_line:
        output = output[1:]
    output = "\n".join(output)
    command = input(output)
    telnetObj.write(command.encode('ascii') + "\n".encode('ascii'))
    return command

telnetInteract("login: ")
telnetInteract("Password: ")

while(True):
    command = telnetInteract("$ ", print_first_line = False)
    if(command in ["exit", "quit"]):
        break

telnetObj.close()