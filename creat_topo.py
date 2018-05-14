# -*- coding: UTF-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

node = 8

net = nx.barabasi_albert_graph(node,3)

nx.draw(net)
plt.show()
