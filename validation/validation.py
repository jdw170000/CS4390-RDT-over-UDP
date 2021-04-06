from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import validationTopos as vt

def perfTestArgs(algo, topo, payload_size, window_size, corrupt_prob, file):
    topoInstance = topo()

    "Create network"
    net = Mininet(topo=topoInstance, link=TCLink)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    c0, h1, h2 = net.get('c0', 'h1', 'h2')
    print('c0.IP, h1.IP, h2.IP = ', c0.IP, h1.IP(), h2.IP())
    h1.cmd(f'python3 -m server -a {algo} -ip {h2.IP()} -p 5006 -ws {window_size}')
    h2.cmd(f'python3 -m client -a {algo} -ip {h1.IP()} -p 5006 -ws {window_size} -ps {payload_size} -cp {corrupt_prob} -f {file}')
    print("IP address of h1 is ", h1.IP())
    print("IP address of h2 is ", h2.IP())

    # CLI(net)
    net.stop()

def GBN_basic():
    payload_size = 100
    topo = vt.TopoNoDelayNoLoss
    window_size = 10
    corrupt_prob = 10
    file = '500K.txt'
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)

def SR_basic():
    payload_size = 100
    topo = vt.TopoNoDelayNoLoss
    window_size = 10
    corrupt_prob = 10
    file = '500K.txt'
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)

def GBN_window():
    payload_size = 100
    topo = vt.Topo5Delay10Loss
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    window_size = 20
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    window_size = 40
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)

def SR_window():
    payload_size = 100
    topo = vt.Topo5Delay10Loss
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    window_size = 20
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    window_size = 40
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)

def GBN_payload():
    topo = vt.Topo5Delay10Loss
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    payload_size = 25
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    payload_size = 50
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    payload_size = 100
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)

def SR_payload():
    topo = vt.Topo5Delay10Loss
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    payload_size = 25
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    payload_size = 50
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    payload_size = 100
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)

def GBN_delay():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo0Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo5Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo10Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)

def SR_delay():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo0Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo5Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo10Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)

def GBN_loss():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo5Delay5Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo5Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo5Delay20Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file)

def SR_loss():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo5Delay5Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo5Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)
    topo = vt.Topo5Delay20Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file)

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