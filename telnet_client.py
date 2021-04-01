import telnetlib, sys, _thread

HOST = "6.tcp.ngrok.io"
PORT = "17013"

# HOST = 'google.com'
# PORT = 80

telnetObj = telnetlib.Telnet(HOST, PORT)

# def telnetInteract(until = "$ ", print_first_line = True):
#     output = telnetObj.read_until(until.encode('ascii'), timeout=5)
#     output = output.splitlines()
#     output = list(map(bytes.decode, output))
#     if not print_first_line:
#         output = output[1:]
#     output = "\n".join(output)
#     command = input(output)
#     telnetObj.write(command.encode('ascii') + "\n".encode('ascii'))
#     return command

# telnetInteract("login: ")
# telnetInteract("Password: ")

def receive_data(telnetObj):
    while(True):
        output = telnetObj.read_eager().decode('ascii')
        if(output):
            print(output)
            # sys.stdout.write(output)
            if('exit' in output):
                break

_thread.start_new_thread(receive_data, (telnetObj,))

while(True):
    command = input()
    telnetObj.write(command.encode('ascii') + "\n".encode('ascii'))
    if(command in ["exit", "quit"]):
        break

telnetObj.close()