from mininet.topo import Topo

linkOneGigNoDelayNoLoss = dict(bw=1000, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)

# Not pretty but hard to implement another way
linkOneGig0Delay10Loss = dict(bw=1000, delay='0ms', loss=10, max_queue_size=1000, use_htb=True)
linkOneGig5Delay5Loss = dict(bw=1000, delay='5ms', loss=5, max_queue_size=1000, use_htb=True)
linkOneGig5Delay10Loss = dict(bw=1000, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
linkOneGig5Delay20Loss = dict(bw=1000, delay='5ms', loss=20, max_queue_size=1000, use_htb=True)
linkOneGig10Delay10Loss = dict(bw=1000, delay='10ms', loss=10, max_queue_size=1000, use_htb=True)


class TopoNoDelayNoLoss(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1')
        self.addLink(host1, switch1, **linkOneGigNoDelayNoLoss)
        host2 = self.addHost('h2')
        self.addLink(host2, switch1, **linkOneGigNoDelayNoLoss)


class Topo0Delay10Loss(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1')
        self.addLink(host1, switch1, **linkOneGig0Delay10Loss)
        host2 = self.addHost('h2')
        self.addLink(host2, switch1, **linkOneGig0Delay10Loss)


class Topo5Delay5Loss(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1')
        self.addLink(host1, switch1, **linkOneGig5Delay5Loss)
        host2 = self.addHost('h2')
        self.addLink(host2, switch1, **linkOneGig5Delay5Loss)


class Topo5Delay10Loss(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1')
        self.addLink(host1, switch1, **linkOneGig5Delay10Loss)
        host2 = self.addHost('h2')
        self.addLink(host2, switch1, **linkOneGig5Delay10Loss)


class Topo5Delay20Loss(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1')
        self.addLink(host1, switch1, **linkOneGig5Delay20Loss)
        host2 = self.addHost('h2')
        self.addLink(host2, switch1, **linkOneGig5Delay20Loss)


class Topo10Delay10Loss(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1')
        self.addLink(host1, switch1, **linkOneGig10Delay10Loss)
        host2 = self.addHost('h2')
        self.addLink(host2, switch1, **linkOneGig10Delay10Loss)
