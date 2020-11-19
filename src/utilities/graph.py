import numpy as np
import math

def dist_euclid(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def neighbors(p, q, points):
	d = dist_euclid(p, q)
	for r in points:
		if np.array_equal(r, p) or np.array_equal(r, q):
			continue
		if dist_euclid(p, r) < d and dist_euclid(q, r) < d:
			return False
	return True

def rel_neighborhood(pointset):
    edges = []
    for i in range(len(pointset)):
        p = pointset[i]
        for j in range(len(pointset[i+1:])):
            q = pointset[i+1+j]
            if neighbors(p, q, pointset):
                edges.append((p,q))
    return edges


if __name__ == "__main__":
    pointset = np.random.rand(20,2)
    print(rel_neighborhood(pointset))
