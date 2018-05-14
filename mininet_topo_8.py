from mininet.topo import Topo

class MyTopo(Topo):

    def __init__(self):

        # initilaize topology   
        Topo.__init__(self)
        
        node_num = 8
        hostConfig = {'cpu':cpu}
        linkConfig = {'bw':10,'delay':'10ms',loss:0,'max_queue_size':max_queue_size}
        
        edges = [(0, 3), (0, 5), (0, 7), (1, 3), (1, 4), 
                 (2, 3), (2, 4), (2, 5), (3, 4), (3, 6), 
                 (3, 7), (4, 5), (4, 6), (4, 7), (5, 6)]

        # add hosts
        h1 = self.addHost('h1',**hostConfig)
        h2 = self.addHost('h2',**hostConfig)
        
        # add switchs
        for node in range(node_num):
            self.addSwitch(node)
            
        # add links
        self.addLink(h1,2,**linkConfig)
        self.addLink(h2,7,**linkConfig)
        
        for v,w in edges:
            self.addLink(v,w,**linkConfig)

topos = { 'mytopo': ( lambda: MyTopo() ) }
