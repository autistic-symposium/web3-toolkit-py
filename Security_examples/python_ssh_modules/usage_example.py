import paramiko
import sys
import getopt


def main():
    if not len(sys.argv[1:]):
        usage()
    IP = '0.0.0.0'
    USER = ''
    PASSWORD = ''
    KEY = ''
    COMMAND = ''
    PORT = 0
    try:
        opts = getopt.getopt(sys.argv[2:],"p:u:a:i:c:", \
            ['PORT', 'USER', 'PASSWORD', 'KEY', 'COMMAND'])[0]
    except getopt.GetoptError as err:
        print str(err)
        usage()
    IP = sys.argv[1]
    print(f'[*] Initializing connection to {IP}')
    # Handle the options and arguments. 
    # TODO: add KeyError error handler.
    for t in opts:
        if t[0] in ('-a'):
            PASSWORD = t[1]
        elif t[0] in ('-i'):
            KEY = t[1]
        elif t[0] in ('-c'):
            COMMAND = t[1]
        elif t[0] in ('-p'):
            PORT = int(t[1])
        elif t[0] in ('-u'):
            USER = t[1]
        else:
            print('This option does not exist!')
            usage()


if USER:
        print(f'[*] User set to {USER}')
    if PORT:
        print(f'[*] The port to be used is PORT}')
    if PASSWORD:
        print(f'[*] Password length {len(PASSWORD)} was submitted.')
    if KEY:
        print(f'[*] The key at {KEY} will be used.')
    if COMMAND:
        print(f'[*] Executing the command {COMMAND} in the host...')
    else:
        print('You need to specify the command to the host.')
        usage()
    # Start the client.
    ssh_client(IP, PORT, USER, PASSWORD, KEY, COMMAND)
    

if __name__ == '__main__':
    main()