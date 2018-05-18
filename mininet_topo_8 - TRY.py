from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController,CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections


class MyTopo(Topo):

    def __init__(self):

        # initilaize topology   
        Topo.__init__(self)
        
        edges = [(0, 3), (0, 4), (0, 7), (1, 3), (1, 4),
                 (1, 5), (1, 6), (2, 3), (2, 5), (3, 4), 
                 (3, 5), (3, 6), (3, 7), (5, 6), (5, 7)]
        s = []
        node_num = 8
        
        hostConfig = {'cpu':1}
        linkConfig = {'bw':10,'delay':'10ms','loss':0,'max_queue_size':None}
        
        # add hosts
        h1 = self.addHost('h1',**hostConfig)
        h2 = self.addHost('h2',**hostConfig)
        h3 = self.addHost('h3',**hostConfig)
        
        
        # add switchs
        for i in range(node_num):
            sw = self.addSwitch( 's{}'.format( i ) )
            s.append(sw)
            
        # add links
        
        self.addLink(h1,s[2],**linkConfig)
        self.addLink(h2,s[4],**linkConfig)
        self.addLink(h3,s[7],**linkConfig)
        
        for v,w in edges:
            self.addLink(s[v],s[w],**linkConfig)
        

topos = { 'mytopo': ( lambda: MyTopo() ) }
