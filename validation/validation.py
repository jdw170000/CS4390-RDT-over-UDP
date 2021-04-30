import os, sys
sys.path.insert(0, os.path.abspath(".."))

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import validationTopos as vt


def perfTestArgs(algo, topo, payload_size, window_size, corrupt_prob, file, testname):
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
    h1.cmd(f'python3 cmd_launcher.py -m server -a {algo} -ip {h2.IP()} -p 5006 -ws {window_size} > {testname}server.out')
    h2.cmd(f'python3 cmd_launcher.py -m client -a {algo} -ip {h1.IP()} -p 5006 -ws {window_size} -ps {payload_size} -cp {corrupt_prob} -f {file} > {testname}client.out')
    net.stop()


def GBN_basic():
    payload_size = 100
    topo = vt.TopoNoDelayNoLoss
    window_size = 10
    corrupt_prob = 10
    file = 'testFile.txt'
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNBasic')


def SR_basic():
    payload_size = 100
    topo = vt.TopoNoDelayNoLoss
    window_size = 10
    corrupt_prob = 10
    file = '500K.txt'
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRBasic')


def GBN_window():
    payload_size = 100
    topo = vt.Topo5Delay10Loss
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNWindow1')
    window_size = 20
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNWindow2')
    window_size = 40
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNWindow3')


def SR_window():
    payload_size = 100
    topo = vt.Topo5Delay10Loss
    corrupt_prob = 0
    file = '500K.txt'

    window_size = 10
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRWindow1')
    window_size = 20
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRWindow2')
    window_size = 40
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRWindow3')


def GBN_payload():
    topo = vt.Topo5Delay10Loss
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    payload_size = 25
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNPayload1')
    payload_size = 50
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNPayload2')
    payload_size = 100
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNPayload3')


def SR_payload():
    topo = vt.Topo5Delay10Loss
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    payload_size = 25
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRPayload1')
    payload_size = 50
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRPayload2')
    payload_size = 100
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRPayload3')


def GBN_delay():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo0Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNDelay1')
    topo = vt.Topo5Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNDelay2')
    topo = vt.Topo10Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNDelay3')


def SR_delay():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo0Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRDelay1')
    topo = vt.Topo5Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRDelay2')
    topo = vt.Topo10Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRDelay3')


def GBN_loss():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo5Delay5Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNLoss1')
    topo = vt.Topo5Delay10Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNLoss2')
    topo = vt.Topo5Delay20Loss
    perfTestArgs('GBN', topo, payload_size, window_size, corrupt_prob, file, 'GBNLoss3')


def SR_loss():
    payload_size = 100
    window_size = 0
    corrupt_prob = 10
    file = '500K.txt'

    topo = vt.Topo5Delay5Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRLoss1')
    topo = vt.Topo5Delay10Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRLoss2')
    topo = vt.Topo5Delay20Loss
    perfTestArgs('SR', topo, payload_size, window_size, corrupt_prob, file, 'SRLoss3')


if __name__ == '__main__':
    # tell mininet to print useful info
    setLogLevel('info')

    # run tests
    print('GBN_basic')
    GBN_basic()
    print('SR_basic')
    SR_basic()
    print('GBN_window')
    GBN_window()
    print('SR_window')
    SR_window()
    print('GBN_payload')
    GBN_payload()
    print('SR_payload')
    SR_payload()
    print('GBN_delay')
    GBN_delay()
    print('SR_delay')
    SR_delay()
    print('GBN_loss')
    GBN_loss()
    print('SR_loss')
    SR_loss()
