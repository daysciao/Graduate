from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController,CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections


class MyTopo(Topo):

    def __init__(self):

        # initilaize topology   
        Topo.__init__(self)
        
        edges = [(0, 2), (0, 3), (1, 2), (2, 3), (2, 4), (2, 5), 
                 (2, 6), (3, 4), (3, 5), (3, 7), (4, 7), (5, 6)]
        s = []
        node_num = 8
        
        hostConfig = {'cpu':1}
        linkConfig = {'bw':10, 'delay':'1ms'}
        
        # add hosts
        h1 = self.addHost('h1',**hostConfig)
        h2 = self.addHost('h2',**hostConfig)
        
        # add switchs
        for i in range(node_num):
            sw = self.addSwitch( 's{}'.format( i+1 ) )
            s.append(sw)
            
        # add links
        
        self.addLink(h1,s[0])
        self.addLink(h2,s[4])
        
        for v,w in edges:
            self.addLink(s[v],s[w],**linkConfig)
        

topos = { 'mytopo': ( lambda: MyTopo() ) }
