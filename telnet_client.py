import telnetlib, sys, time
from threading import Thread

def receive_data(telnetObj): # For a separate thread
    while(True):
        try:
            output = telnetObj.read_eager() # Read readily available data
            if(output):
                try:
                    decodedoutput = output.decode('ascii')
                    sys.stdout.write(decodedoutput)
                except: # Some web contents contain non ascii values. In that case let's print without decoding
                    sys.stdout.write(str(output))
            else:
                sys.stdout.flush()
        except: # If some error occured while receiving, this thread should exit without crashing
            print("Connection closed!")
            break

if(len(sys.argv) != 3):
    print ("Invalit argument count.\n * Usage: python {} <host> <port>".format(__file__))
    sys.exit(1)

host = sys.argv[1]
port = sys.argv[2]
try:
    telnetObj = telnetlib.Telnet(host, port, timeout=5) # Initiate
    print("Successfully connected to {}:{}".format(host, port))
except: # If incorrect host and port were given or any network issue occured
    print("Error occured while trying to connect {}:{}".format(host, port))
    sys.exit(1)

thread = Thread(target=receive_data, args=(telnetObj, )) # Create a new thread to listen
thread.start()

while(True):
    try:
        command = input() # Take inputs from user
        telnetObj.write(command.encode('ascii') + "\n".encode('ascii')) # Send user input to the server
        if(command in ["exit", "quit"] or thread._is_stopped):
            # If user wanted to exit or if the listening thread is not running the client should stop
            break
    except:
        # print(sys.exc_info()[0])
        print("Error occured!")
        break


telnetObj.close() # Close the telnet socket. This will also make the listening thread exit
thread.join() # Wait for the listening thread to finish
print("Finished!")