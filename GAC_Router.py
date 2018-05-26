# coding:utf-8

from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp
from ryu.lib.packet import ether_types
from ryu.lib import mac
from ryu.topology.api import get_switch, get_link
from ryu.app.wsgi import ControllerBase
from ryu.topology import event, switches

import numpy as np
from GAC0_1 import GA_routing, AC_routing, GAC_routing



class ProjectController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]


    def __init__(self, *args, **kwargs):
        super(ProjectController, self).__init__(*args, **kwargs)
        self.topology_api_app = self
        self.ARP_table = {'10.0.0.1':'00:00:00:00:00:01',
                          '10.0.0.2':'00:00:00:00:00:02',
                          '10.0.0.3':'00:00:00:00:00:03'}
        self.switch_es = []
        self.port_map = None
        self.toponet = None
        self.access = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        print "\n-----------switch_features_handler is called"
        msg = ev.msg
        print 'OFPSwitchFeatures received: datapath_id=0x%016x n_buffers=%d n_tables=%d auxiliary_id=%d capabilities=0x%08x' % (
            msg.datapath_id, msg.n_buffers, msg.n_tables, msg.auxiliary_id, msg.capabilities)
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0, priority=0, instructions=inst)
        datapath.send_msg(mod)
        print "switch_features_handler is over"
    
    def creat_switch_table(self,):
    
    def creat_port_table(self,links,node_num):
        self.toponet = (np.ones(node_num, dtype=np.int16) - np.eye(node_num, dtype=np.int16)) * 100
        self.port_map = np.zeros([node_num,node_num,2],dtype=int16)
        for link in links:
            src = link.src
            dst = link.dst
            if src.dpid in self.switch_es and dst.dpid in self.switch_es:
                src_i = self.switch_es.index(src.dpid)
                dst_i = self.switch_es.index(dst.dpid)
                ports = np.array([src.port_no,dst.port_no])
                self.toponet[src_i][dst_i] = 1
                self.port_map[src_i][dst_i] = ports
            elif src.dpid in self.switch_es:
                self.access[dst] = [src.dpid,dst.port_no]
                
    
    events = [event.EventSwitchEnter,
              event.EventSwitchLeave, event.EventPortAdd,
              event.EventPortDelete, event.EventPortModify,
              event.EventLinkAdd, event.EventLinkDelete]

    @set_ev_cls(events)
    def get_topology_data(self, ev):
        print "\n-----------get_topology_data"
        switch_list = get_switch(self.topology_api_app, None)
        self.switch_es = [switch.dp.id for switch in switch_list]
        print self.switch_es
        print switches
        node_num = len(self.switches_es)
        links_list = get_link(self.topology_api_app, None)
        self.creat_port_table()
        print self.toponet,self.port_map,self.access        

    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = datapath.ofproto_parser.OFPMatch(in_port=in_port, eth_dst=dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4,ipv4)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:            # ignore lldp packet
            return

        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # print "nodes"
        # print self.net.nodes()
        # print "edges"
        # print self.net.edges()
        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        if src not in self.net:
            self.net.add_node(src)
            self.net.add_edge(dpid, src, port=in_port, weight=0)
            self.net.add_edge(src, dpid, weight=0)
        if dst in self.net:
            path = nx.shortest_path(self.net, src, dst, weight="weight")
            # print path
            # print G[path[0]][path[1]]
            # print G[path[-2]][path[-1]]
            print "dpid=", dpid
            print "length=", nx.shortest_path_length(self.net, src, dst, weight="weight")

            next = path[path.index(dpid) + 1]
            out_port = self.net[dpid][next]['port']
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, in_port, dst, actions)
        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions)
        datapath.send_msg(out)
