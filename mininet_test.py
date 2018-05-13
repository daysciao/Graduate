from mininet.topo import Topo

class MyTopo( Topo ):

    def __init__( self ):

        # initilaize topology   
        Topo.__init__( self )

        # add hosts and switches
        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        switch1 = self.addSwitch( 's1' )
        switch2 = self.addSwitch( 's2' )
        switch3 = self.addSwitch( 's3' )
        switch4 = self.addSwitch( 's4' )

        # add links
        self.addLink(host1,switch1,1,1)
        self.addLink(switch1,switch2,2,1)
        self.addLink(switch2,switch3,2,1)
        self.addLink(switch3,switch4,2,1)
        self.addLink(switch4,host2,2,1)

topos = { 'mytopo': ( lambda: MyTopo() ) }