import telnetlib, sys, time, re
from threading import Thread

def receive_data(telnetObj):
    while(True):
        try:
            output = telnetObj.read_eager()
            if(output):
                try:
                    decodedoutput = output.decode('ascii')
                    sys.stdout.write(decodedoutput)
                except:
                    sys.stdout.write(str(output))
            else:
                sys.stdout.flush()
        except:
            print("Connection closed!")
            break

if(len(sys.argv) != 3):
    raise Exception("Invalit argument count:\n Usage:\n{} <host> <port>".format(__file__)) 

host = sys.argv[1]
port = sys.argv[2]
try:
    telnetObj = telnetlib.Telnet(host, port, timeout=5)
    print("Successfully connected to {}:{}".format(host, port))
except:
    print("Error occured while trying to connect {}:{}".format(host, port))
    sys.exit()

thread = Thread(target=receive_data, args=(telnetObj, ))
thread.start()

while(True):
    try:
        command = input()
        telnetObj.write(command.encode('ascii') + "\n".encode('ascii'))
        if(command in ["exit", "quit"] or thread._is_stopped):
            break
    except:
        # print(sys.exc_info()[0])
        print("Error occured!")
        break


telnetObj.close()
thread.join()
print("Finished!")