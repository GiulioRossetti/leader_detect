import sys, time
import networkx as nx

start = time.time()

G = nx.Graph()

f = open("network", "r")
for line in f:
   fields = line.strip().split()
   G.add_edge(int(fields[0]), int(fields[1]))
f.close()

sys.stderr.write("Data load! Runtime: %s\n" % (time.time() - start))

avg_clusterings = nx.clustering(G)

sys.stderr.write("Clusering calculated! Runtime: %s\n" % (time.time() - start))

neigh_degree = nx.average_neighbor_degree(G)

sys.stderr.write("AVG Neighbor degree calculated! Runtime: %s\n" % (time.time() - start))

bet_centr = nx.betweenness_centrality(G, k = 10000)

sys.stderr.write("Betweenness centrality calculated! Runtime: %s\n" % (time.time() - start))

clo_centr = nx.closeness_centrality(G)

sys.stderr.write("Closeness centrality calculated! Runtime: %s\n" % (time.time() - start))

f = open("node_stats_approx", 'w')
for i in G:
   f.write("%d::%s::%s::%s::%s\n" % (i, avg_clusterings[i], neigh_degree[i], bet_centr[i], clo_centr[i]))
f.close()

sys.stderr.write("Done! Runtime: %s\n" % (time.time() - start))
