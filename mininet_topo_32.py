from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController,CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections


class MyTopo(Topo):

    def __init__(self):

        # initilaize topology   
        Topo.__init__(self)
        
        edges = [(0, 25), (0, 2), (1, 11), (1, 16), (1, 2), (1, 3), (1, 15), (2, 3), (2, 4), (2, 5), 
                 (2, 6), (2, 8), (2, 10), (2, 11), (2, 12), (2, 21), (2, 24), (3, 4), (3, 5), (3, 18), 
                 (3, 24), (3, 27), (3, 29), (3, 31), (4, 6), (4, 7), (4, 8), (4, 14), (4, 25), (5, 9), 
                 (5, 30), (6, 31), (6, 7), (7, 22), (7, 13), (7, 23), (8, 9), (8, 10), (8, 13), (8, 14), 
                 (8, 17), (8, 18), (8, 22), (8, 26), (8, 28), (8, 29), (9, 17), (10, 12), (10, 21), (10, 15), 
                 (12, 26), (12, 19), (12, 20), (14, 16), (14, 19), (16, 20), (17, 28), (17, 30), (17, 23), (18, 27)]
        s = []
        node_num = 32
        
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
        self.addLink(h2,s[16])

        
        for v,w in edges:
            self.addLink(s[v],s[w])
        

topos = { 'mytopo': ( lambda: MyTopo() ) }
