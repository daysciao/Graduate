# coding:utf-8

import time
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
from ryu.lib import hub

import numpy as np
from GAC0_1 import GA_routing, AC_routing, GAC_routing

class ProjectController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        super(ProjectController, self).__init__(*args, **kwargs)
        self.topology_api_app = self
        self.switch_es = []
        self.port_map = None
        self.toponet = None
        self.access = {}
        
        self.discover_thread = hub.spawn(self._discover)
    def _discover(self):
        i = 0
        while True:
            self.get_topology_data(None)
            hub.sleep(20)

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
        
    def get_switches(self):
        return self.switches
    
    def creat_port_table(self,links,node_num):
        self.toponet = (np.ones(node_num, dtype=np.int) - np.eye(node_num, dtype=np.int)) * 100
        self.port_map = np.zeros([node_num,node_num,2],dtype=int)
        for link in links:
            src = link.src
            dst = link.dst
            src_i = self.switch_es.index(src.dpid)
            dst_i = self.switch_es.index(dst.dpid)
            ports = np.array([src.port_no,dst.port_no])
            self.toponet[src_i][dst_i] = 1
            self.port_map[src_i][dst_i] = ports
                
    def creat_access_table(self,node_num):
        access_point = self.switch_es[::node_num/2]
        i = 0
        for point in access_point:
            i = i + 1
            self.access["10.0.0.%s"%i] = [point,1]
    
    events = [event.EventSwitchEnter,
              event.EventSwitchLeave, event.EventPortAdd,
              event.EventPortDelete, event.EventPortModify,
              event.EventLinkAdd, event.EventLinkDelete]

    @set_ev_cls(events)
    def get_topology_data(self, ev):
        print "\n-----------get_topology_data"
        switch_list = get_switch(self.topology_api_app, None)
        self.dps = [switch.dp for switch in switch_list]
        self.switch_es = [dp.id for dp in self.dps]
        node_num = len(self.switch_es)
        self.creat_access_table(node_num)
        links_list = get_link(self.topology_api_app, None)
        self.creat_port_table(links_list,node_num)
    
    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = datapath.ofproto_parser.OFPMatch(in_port=in_port, eth_dst=dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=1, instructions=inst)
        datapath.send_msg(mod)
        #print datapath.id,'added',mod

    def install_flow(self,path,in_port,dst,src):
        for i in range(len(path)-1):
            datapath = self.dps[path[i]]
            ports = self.port_map[path[i]][path[i+1]]
            out_port = ports[0]
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            self.add_flow(datapath, in_port, dst, actions)
            actions = [datapath.ofproto_parser.OFPActionOutput(in_port)]
            self.add_flow(datapath, out_port, src, actions)
            in_port = ports[1]
        datapath = self.dps[path[-1]]
        out_port = 1
        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
        self.add_flow(datapath, in_port, dst, actions)
        actions = [datapath.ofproto_parser.OFPActionOutput(in_port)]
        self.add_flow(datapath, out_port, src, actions)
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
    
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        arp_pkt = pkt.get_protocol(arp.arp)
        in_port = msg.match['in_port']
        
        if eth_pkt.ethertype == 2048:
            
            dst = eth_pkt.dst
            src = eth_pkt.src
            ip_dst = ip_pkt.dst
            ip_src = ip_pkt.src
            dpid = datapath.id
        
            src_i = self.switch_es.index(self.access[ip_src][0])
            dst_i = self.switch_es.index(self.access[ip_dst][0])
            
            s = time.clock()
            path = GA_routing(self.toponet,src_i,dst_i)
            e = time.clock()
            
            #print path,'----------------------',e-s
            
            self.install_flow(path,in_port,dst,src)

        
            if not (len(path)-1):
                out_port = self.access[ip_dst][1]
            else:
                out_port = self.port_map[path[0]][path[1]][0]
        
        
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

            out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions)
            #datapath.send_msg(out)
            #print 'packet_______________complete'