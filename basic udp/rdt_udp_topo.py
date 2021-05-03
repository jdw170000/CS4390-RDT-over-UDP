# Used for rdt over UDP project
# to inject losses and delay
import sys
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

linkOneGigNoDelayNoLoss = dict(bw=1000, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)


class SimpleTopo(Topo):
    "Two hosts connected through a switch"

    def build(self):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1')
        self.addLink(host1, switch1, **linkOneGigNoDelayNoLoss)
        # self.addLink(host1, switch1, **linkOneGigDelayLoss)

        host2 = self.addHost('h2')
        self.addLink(host2, switch1, **linkOneGigNoDelayNoLoss)
        # self.addLink(host2, switch1, **linkOneGigDelayLoss)


def perfTest():
    "Create network"
    topo = SimpleTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    c0, h1, h2 = net.get('c0', 'h1', 'h2')
    print('c0.IP, h1.IP, h2.IP = ', c0.IP, h1.IP(), h2.IP())

    # debug stuff
    # print(topo)
    # print(vars(topo))
    # print(f'net: {net}')
    # print(vars(net))

    h1.cmd('python3 basic-udp-server.py out.out > r.out &')
    h2.cmd('python3 basic-udp-client.py med.txt 100 5 30 > s.out &')
    # h1.cmd('python3 ../validation/cmd_launcher.py -m server -a GBN -ip 10.0.0.1 -p 5006 -ws 10 > s.out')
    # h2.cmd("python3 ../validation/cmd_launcher.py -m client -a GBN -ip 10.0.0.1 -p 5006 -ws 10 -cp 0 -ps 10 -f 'testFile.txt'> r.out &")
    print("IP address of h1 is ", h1.IP())
    print("IP address of h2 is ", h2.IP())

    # CLI(net)  #####
    net.stop()


if __name__ == '__main__':
    # tell mininet to print useful info
    setLogLevel('info')
    perfTest()
