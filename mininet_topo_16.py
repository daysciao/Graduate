from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController,CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections


class MyTopo(Topo):

    def __init__(self):

        # initilaize topology   
        Topo.__init__(self)
        
        edges = [[(0, 2), (0, 4), (0, 7), (1, 2), (1, 3), (1, 7), (1, 10), 
                  (1, 11), (1, 13), (2, 3), (2, 5), (2, 6), (2, 10), (2, 12), 
                  (2, 13), (3, 8), (3, 4), (4, 5), (4, 15), (5, 6), (5, 8), 
                  (5, 9), (5, 12), (5, 14), (6, 14), (7, 11), (7, 9), (11, 15)]
        s = []
        node_num = 16
        
        hostConfig = {'cpu':1}
        
        # add hosts
        h1 = self.addHost('h1',**hostConfig)
        h2 = self.addHost('h2',**hostConfig)
        
        # add switchs
        for i in range(node_num):
            sw = self.addSwitch( 's{}'.format( i+1 ) )
            s.append(sw)
            
        # add links
        
        self.addLink(h1,s[0])
        self.addLink(h2,s[8])

        
        for v,w in edges:
            self.addLink(s[v],s[w])
        

topos = { 'mytopo': ( lambda: MyTopo() ) }
