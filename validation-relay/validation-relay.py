import os, sys
sys.path.insert(0, os.path.abspath(".."))
import subprocess

def perfTestArgs(algo, delay, loss, payload_size, window_size, corrupt_prob, file, testname):

    # open log files
    server_out = open(f'{testname}-server.out', 'wb')
    server_err = open(f'{testname}-server.err', 'wb')
    client_out = open(f'{testname}-client.out', 'wb')
    client_err = open(f'{testname}-client.err', 'wb')

    # Spawn relay server
    relay_process = subprocess.Popen(['python3', 'relay.py', '-d', f'{delay}', '-l', f'{loss}'], stdout = subprocess.DEVNULL)
    print('Started relay process')

    # Spawn RDT server
    server_process = subprocess.Popen(['python3', 'cmd_launcher.py', '-m', 'server', '-a', f'{algo}', '-ip', '127.0.0.1', '-p', '5006', '-ws', f'{window_size}'], stdout = server_out, stderr = server_err)
    print('Started server process')

    # Spawn RDT client
    client_process = subprocess.Popen(['python3', 'cmd_launcher.py', '-m', 'client', '-a', f'{algo}', '-ip', '127.0.0.1', '-p', '5007', '-ws', f'{window_size}', '-ps', f'{payload_size}', '-cp', f'{corrupt_prob}', '-f', f'\'{file}\''], stdout = client_out, stderr = client_err)
    print('Started client process')

    # wait for server to terminate
    server_process.wait()
    print('Server process complete')

    #wait for client process to terminate
    client_process.wait()
    print('Client process complete')

    # terminate relay server
    relay_process.terminate()
    print('Closed relay process')

    # close log files
    server_out.close()
    server_err.close()
    client_out.close()
    client_err.close()

def GBN_basic():
    payload_size = 100
    delay = 0
    loss = 0
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNBasic')


def SR_basic():
    payload_size = 100
    delay = 0
    loss = 0
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRBasic')


def GBN_window():
    payload_size = 100
    delay = 0.005
    loss = 10
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNWindow1')
    window_size = 20
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNWindow2')
    window_size = 40
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNWindow3')


def SR_window():
    payload_size = 100
    delay = 0.005
    loss = 10
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRWindow1')
    window_size = 20
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRWindow2')
    window_size = 40
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRWindow3')


def GBN_payload():
    delay = 0.005
    loss = 10
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'

    '''payload_size = 25
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNPayload1')
    payload_size = 50
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNPayload2')'''
    payload_size = 100
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNPayload3')


def SR_payload():
    delay = 0.005
    loss = 10
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'

    payload_size = 25
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRPayload1')
    payload_size = 50
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRPayload2')
    payload_size = 100
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRPayload3')


def GBN_delay():
    payload_size = 100
    delay = 0
    loss = 10
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'

    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNDelay1')
    delay = 0.005
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNDelay2')
    delay = 0.010
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNDelay3')


def SR_delay():
    payload_size = 100
    delay = 0
    loss = 10
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'

    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRDelay1')
    delay = 0.005
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRDelay2')
    delay = 0.010
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRDelay3')


def GBN_loss():
    payload_size = 100
    delay = 0.005
    loss = 5
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'

    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNLoss1')
    loss = 10
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNLoss2')
    loss = 20
    perfTestArgs('GBN', delay, loss, payload_size, window_size, corrupt_prob, file, 'GBNLoss3')


def SR_loss():
    payload_size = 100
    delay = 0.005
    loss = 5
    window_size = 10
    corrupt_prob = 0.1
    file = '500K.txt'

    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRLoss1')
    loss = 10
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRLoss2')
    loss = 20
    perfTestArgs('SR', delay, loss, payload_size, window_size, corrupt_prob, file, 'SRLoss3')


if __name__ == '__main__':
    # run tests
    '''print('GBN_basic')
    GBN_basic()
    print('SR_basic')
    SR_basic()
    print('GBN_window')
    GBN_window()
    print('SR_window')
    SR_window()'''
    print('GBN_payload')
    GBN_payload()
    '''print('SR_payload')
    SR_payload()
    print('GBN_delay')
    GBN_delay()
    print('SR_delay')
    SR_delay()
    print('GBN_loss')
    GBN_loss()
    print('SR_loss')
    SR_loss()'''
