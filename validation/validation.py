from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import validationTopos as vt

def perfTestArgs(algo, link, payload_size, window_size, corrupt_prob, file):
    if (algo == 'GBN'):
        h1script = 'gbn_server.py'
        h2script = 'gbn_client.py'
    elif (algo == 'SR'):
        h1script = 'sr_server.py'
        h2script = 'sr_client.py'
    else:
        raise Exception('Invalid algo parameter set')

    # Construct commands
    h1cmd = f'python3 {h1script} {payload_size} {window_size} {corrupt_prob} {file}'
    h2cmd = f'python3 {h2script} {payload_size} {window_size} {corrupt_prob} {file}'

    "Create network"
    net = Mininet(topo=link, link=TCLink)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    c0, h1, h2 = net.get('c0', 'h1', 'h2')
    print('c0.IP, h1.IP, h2.IP = ', c0.IP, h1.IP(), h2.IP())
    h1.cmd(h1cmd)
    h2.cmd(h2cmd)
    print("IP address of h1 is ", h1.IP())
    print("IP address of h2 is ", h2.IP())

    CLI(net)
    net.stop()

def GBN_basic():
    payload_size = 100
    link = vt.linkOneGigNoDelayNoLoss
    window_size = 10
    corrupt_prob = 10
    file = '500K.txt'
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)

def SR_basic():
    payload_size = 100
    link = vt.linkOneGigNoDelayNoLoss
    window_size = 10
    corrupt_prob = 10
    file = '500K.txt'
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)

def GBN_window():
    payload_size = 100
    link = vt.linkOneGig5Delay10Loss
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    window_size = 20
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    window_size = 40
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)

def SR_window():
    payload_size = 100
    link = vt.linkOneGig5Delay10Loss
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    window_size = 20
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    window_size = 40
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)

def GBN_payload():
    link = vt.linkOneGig5Delay10Loss
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    payload_size = 25
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    payload_size = 50
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    payload_size = 100
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)

def SR_payload():
    link = vt.linkOneGig5Delay10Loss
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    payload_size = 25
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    payload_size = 50
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    payload_size = 100
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)

def GBN_delay():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    link = vt.linkOneGig0Delay10Loss
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig5Delay10Loss
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig10Delay10Loss
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)

def SR_delay():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    link = vt.linkOneGig0Delay10Loss
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig5Delay10Loss
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig10Delay10Loss
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)

def GBN_loss():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    link = vt.linkOneGig5Delay5Loss
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig5Delay10Loss
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig5Delay20Loss
    perfTestArgs('GBN', link, payload_size, window_size, corrupt_prob, file)

def SR_loss():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    link = vt.linkOneGig5Delay5Loss
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig5Delay10Loss
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)
    link = vt.linkOneGig5Delay20Loss
    perfTestArgs('SR', link, payload_size, window_size, corrupt_prob, file)

if __name__ == '__main__':

    # tell mininet to print useful info
    setLogLevel('info')

    # run tests
    GBN_basic()
    SR_basic()
    GBN_window()
    SR_window()
    GBN_payload()
    SR_payload()
    GBN_delay()
    SR_delay()
    GBN_loss()
    SR_loss()