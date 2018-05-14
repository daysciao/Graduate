from mininet.topo import Topo

class MyTopo(Topo):

    def __init__(self,cpu=1,max_queue_size=None,**params):

        # initilaize topology   
        Topo.__init__(self,**params)
        
        node_num = 8
        hostConfig = {'cpu':cpu}
        linkConfig = {'bw':10,'delay':'10ms','loss':0,'max_queue_size':max_queue_size}
        
        # add hosts
        h1 = self.addHost('h1',**hostConfig)
        h2 = self.addHost('h2',**hostConfig)
        
        # add switchs
        s0 = self.addSwitch('s0')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
            
        # add links
        self.addLink(h1,s2,**linkConfig)
        self.addLink(h2,s7,**linkConfig)        
        self.addLink(s0, s3,**linkConfig)
        self.addLink(s0, s5,**linkConfig)
        self.addLink(s0, s7,**linkConfig)
        self.addLink(s1, s3,**linkConfig)
        self.addLink(s1, s4,**linkConfig)
        self.addLink(s2, s3,**linkConfig)
        self.addLink(s2, s4,**linkConfig)
        self.addLink(s2, s5,**linkConfig)
        self.addLink(s3, s4,**linkConfig)
        self.addLink(s3, s6,**linkConfig)
        self.addLink(s3, s7,**linkConfig)
        self.addLink(s4, s5,**linkConfig)
        self.addLink(s4, s6,**linkConfig)
        self.addLink(s4, s7,**linkConfig)
        self.addLink(s5, s6,**linkConfig)

topos = { 'mytopo': ( lambda: MyTopo() ) }
