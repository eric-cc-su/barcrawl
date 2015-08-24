# =============================================================================
# tsp_solver.py - Solves TSP Problem
# Based off of https://github.com/dmishin/tsp-solver
# Modified and documented to learn to implement solution for TSP
# =============================================================================
from itertools import islice
import numpy
from array import array as pyarray

# Python 2 uses xrange function; Python 3 replaces it w/ range
if "xrange" not in globals():
    xrange = range
else:
    pass

# -----------------------------------------------------------------------------
# Takes the number of cities and an array of an array of distances from each
# city to each other city.
# Returns an array of pairs of nodes representing cities sorted by ascending
# distances. Ex:
#   [   (0,1),      # City 0 to city 1
#       (1,2),      # City 1 to city 2 ...
#       (0,3),
#       (2,3),
#       (1,3)   ]
# -----------------------------------------------------------------------------
def pairs_by_dist(num_of_cities, distances):
    # Initialize array of pairs of cities w/ distance.
    # Ex: [ (0.0,0,0), (0.0,0,0) (0.0,0,0)] # 1st field (distance) removed later
    pairs = numpy.zeros((num_of_cities * (num_of_cities-1) // 2,), # // is floor division
                        dtype='f4, i2, i2') # float, int, int (distance, city1, city2)

    # Populate pairs
    index = 0
    for i in xrange(num_of_cities):
        row_size = num_of_cities - i - 1
        dist_i = distances[i]
        pairs[index:(index + row_size)] = \
            [(dist_i[j], i, j) for j in xrange(i+1, num_of_cities)]
        index += row_size

    # Sort by ascending distances (1st field)
    pairs.sort(order=["f0"])
    # Return array of pairs of nodes (just 2nd and 3rd fields)
    return pairs[["f1", "f2"]]

# -----------------------------------------------------------------------------
# Tries to optimize the solution - A LITTLE HAZY HERE
# -----------------------------------------------------------------------------
def optimize_solution(distances, connections):
    print('Optimizing solution...')
    num_of_cities = len(connections)
    path = create_path(connections)
    # ---------------
    # distance between ith and jth points of path
    # ---------------
    def ds(i,j):
        return distances[path[i]][path[j]]
    d_total = 0.0
    optimizations = 0

    for a in xrange(num_of_cities - 1):
        b = a + 1
        for c in xrange(b + 2, num_of_cities - 1):
            d = c + 1
            delta_d = ds(a,b)+ds(c,d) -( ds(a,c)+ds(b,d))
            if delta_d > 0:
                d_total += delta_d
                optimizations += 1
                connections[path[a]].remove(path[b])
                connections[path[a]].append(path[c])
                connections[path[b]].remove(path[a])
                connections[path[b]].append(path[d])

                connections[path[c]].remove(path[d])
                connections[path[c]].append(path[a])
                connections[path[d]].remove(path[c])
                connections[path[d]].append(path[b])
                path[:] = create_path(connections)

    return optimizations, d_total

# -----------------------------------------------------------------------------
# Takes array of connections
# Connection is:
#   -Start / end city (special case where array only 1 element)
#   -Pairs of indices of cities (each pair represents the route between the
#    corresponding cities)
# Ex:
#   [   [1,2],        # city 0 connects to 1 and 2
#       [0],          # city 1 connects to 0
#       [0]  ]        # city 2 connects to 0
# Returns array of cities (represented by their numbers) in order of route
# Ex: [1,0,2,1]
# -----------------------------------------------------------------------------
def create_path(connections):
    # Get connections w/ only one element (so know is start / end) and set the
    # index of that connection to start / end
    start, end = [index
                  for index, conn in enumerate(connections)
                  if len(conn) == 1]

    # Initialize path at starting city
    path = [start]
    prev_city = None
    cur_city = start

    # Iterate through connections to create route
    while True:
        next_cities = [city
                       for city in connections[cur_city]
                       if city != prev_city ]
        # If no more cities
        if not next_cities:
            break
        # Get city and append to route
        next_city = next_cities[0]
        path.append(next_city)
        # Update cities
        prev_city, cur_city = cur_city, next_city

    # Append start to cycle back
    #path.append(start)

    return path

# -----------------------------------------------------------------------------
# Takes an array of an array of distances from each city to each other city. Ex:
#   [   [0,4,5],        # 1st city
#       [4,0,6],        # 2nd city
#       [5,6,0]     ]   # 3rd city
# Takes the # of times to recalculate route to optimize. (See optimize_solution)
# Returns list of cities in order of approximated shortest route
# -----------------------------------------------------------------------------
def solve_tsp(distances, opt_steps):
    #print('Distances: ')
    #print(distances)

    # Get number of cities
    num_cities = len(distances)
    if num_cities == 0: return []
    if num_cities == 1: return [0]

    # Check if square matrix
    for row in distances:
        if len(row) != num_cities: raise ValueError( "Matrix is not square.")

    # State of the TSP solver algorithm
    node_valency = pyarray('i', [2]) * num_cities # Initially, each node has 2 sticky ends

    # For each node, stores 1 or 2 connected nodes
    connections = [[] for i in xrange(num_cities)]

    # ---------------
    # Join segments - A LITTLE HAZY HERE
    # ---------------
    def join_segments(sorted_pairs):
        # Segments of nodes. Initially, each segment contains only 1 node.
        segments = [[i] for i in xrange(num_cities)]

        # ---------------
        # Filter pairs - A LITTLE HAZY HERE
        # ---------------
        def filtered_pairs():
            for ij in sorted_pairs:
                i, j = ij
                # If no more free ends, skip
                if not node_valency[i] or \
                        not node_valency[j] or\
                        (segments[i] is segments[j]):
                    continue
                yield ij

        for i, j in islice(filtered_pairs(), num_cities-1):
            node_valency[i] -= 1
            node_valency[j] -= 1
            connections[i].append(j)
            connections[j].append(i)
            # Merge segment J into segment I.
            seg_i = segments[i]
            seg_j = segments[j]
            if len(seg_j) > len(seg_i):
                seg_i, seg_j = seg_j, seg_i
                i, j = j, i
            for node_index in seg_j:
                segments[node_index] = seg_i
            seg_i.extend(seg_j)

    join_segments(pairs_by_dist(num_cities, distances))

    # Try to optimize route w/ # of steps specified
    # More steps --> more optimal route but more time consuming
    for steps in range(opt_steps):
        remaining_steps, dtotal = optimize_solution(distances, connections)
        if remaining_steps == 0:
            break

    # Get cities to traverse in order
    route = create_path(connections)

    #print('Route: ')
    #print (route)

    return route
