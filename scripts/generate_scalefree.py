"""Generate and output scale-free graph as a degree-distribution CSV file

"""

import numpy as np
import networkx as nx
from collections import Counter
import csv
import sys





def kronecker_generator(scale, edgefactor):
  """Kronecker graph generator
  Ported from octave code in https://graph500.org/?page_id=12#alg:generator
  """
  N = 2**scale  # Number of vertices
  M = N * edgefactor  # Number of edges
  A, B, C = (0.57, 0.19, 0.19)  # Initiator probabilities
  ijw = np.ones((3, M))  # Index arrays

  ab = A + B
  c_norm = C/(1 - (A + B))
  a_norm = A/(A + B)

  for ib in range(scale):
    ii_bit = (np.random.rand(1, M) > ab).astype(int)
    ac = c_norm * ii_bit + a_norm * (1 - ii_bit)
    jj_bit = (np.random.rand(1, M) > ac).astype(int)
    ijw[:2,:] = ijw[:2,:] + 2**ib * np.vstack((ii_bit, jj_bit))

  ijw[2,:] = np.random.rand(1, M)
  ijw[:2,:] = ijw[:2,:] - 1
  q = range(M)
  np.random.shuffle(q)
  ijw = ijw[:,q]
  edges = ijw[:2,:].astype(int).T
  g = nx.DiGraph()
  g.add_edges_from(edges)
  return g


def kronecker_generator_general(N, M):
  # TODO: Accept general number of nodes
  A, B, C = (0.57, 0.19, 0.19)  # Initiator probabilities
  ijw = np.ones((3, M))  # Index arrays
  ab = A + B
  c_norm = C/(1 - (A + B))
  a_norm = A/(A + B)
  tmp = N
  while tmp > 0:
    tmp /= 2
    ii_bit = (np.random.rand(1, M) > ab).astype(int)
    ac = c_norm * ii_bit + a_norm * (1 - ii_bit)
    jj_bit = (np.random.rand(1, M) > ac).astype(int)
    ijw[:2,:] = ijw[:2,:] + tmp * np.vstack((ii_bit, jj_bit))
  ijw[2,:] = np.random.rand(1, M)
  ijw[:2,:] = ijw[:2,:] - 1
  q = range(M)
  np.random.shuffle(q)
  ijw = ijw[:,q]
  edges = ijw[:2,:].astype(int).T
  g = nx.DiGraph()
  g.add_edges_from(edges)
  return g


def powerlaw_cluster_generator(N, edgefactor):
  edges = nx.barabasi_albert_graph(N, edgefactor, seed=0).edges()  # Undirected edges
  # Swap the direction of half edges to diffuse degree
  #di_edges = [(edges[i][0], edges[i][1]) if i % 2==0 else (edges[i][1], edges[i][0]) for i in range(len(edges))]
  edges = nx.barabasi_albert_graph(N, edgefactor, seed=0).edges()  # Undirected edges
  di_edges = [(u,v) if i%2==0 else (v,u) for i,(u,v) in enumerate(edges)]
  g = nx.DiGraph()
  g.add_edges_from(di_edges)  # Create a directed graph
  return g



if __name__ == "__main__":
  argv = sys.argv
  if len(argv) < 4:
    print("Usage: python %s [NumVertices] [EdgeFactor] [DegCSV]" % argv[0])
    exit(1)

  n = int(argv[1])
  factor = int(argv[2])
  g = powerlaw_cluster_generator(n, factor)

  print("Number of vertices: %d" % g.number_of_nodes())  # Number of vertices (accounts)
  print("Number of edges: %d" % g.number_of_edges())  # Number of edges (transactions)

  in_deg = Counter([v for v in g.in_degree().values()])
  out_deg = Counter([v for v in g.out_degree().values()])

  counts = sorted(set(in_deg.keys()).union(set(out_deg.keys())))

  with open(argv[3], "w") as wf:
    writer = csv.writer(wf)
    writer.writerow(["Count","In-degree","Out-degree"])
    for k in counts:
      writer.writerow([k, in_deg[k], out_deg[k]])

