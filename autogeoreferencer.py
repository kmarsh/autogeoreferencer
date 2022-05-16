from scipy import spatial
from scipy.spatial import distance
import numpy as np
import math
import pickle
import hashlib
import os.path

CACHE_VECTOR_TPP = True

def length(v):
  return np.sqrt(np.dot(v, v))

def angle(v1, v2):
  return np.arccos(np.dot(v1, v2) / (length(v1) * length(v2)))

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)

    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)

    return(x, y)

def do_sort_by_polar_coordinates(coordinate_pair_1, coordinate_pair_2):
    # (r_i, theta_i) \prec (r_j, theta_j) if (r_i < r_j) or (r_i = r_j & theta_i < theta_j)
    r_1, theta_1 = cart2pol(*coordinate_pair_1)
    r_2, theta_2 = cart2pol(*coordinate_pair_2)

    if ((r_1 < r_2) or (r_1 == r_2 and theta_1 < theta_2)):
      return -1
    else:
      return 1

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def tpp(coordinateArray, anchorPointIndex, sort_by_polar_coordinates = True):
    new_coordinates = []

    tree = spatial.KDTree(coordinateArray)
    qpoint = coordinateArray[anchorPointIndex]
    nearestDistances, nearestIndices = tree.query(qpoint, 2)

    # print("nearest", nearestDistances)

    # The 0th returned is the query point, the second is the nearest neighbor
    closestIndex = 1

    # distance from anchor point to nearest point
    d_i = nearestDistances[closestIndex]

    # nearest point coordinates from anchor point
    nearestCoordinates = coordinateArray[nearestIndices[closestIndex]]

    # print("nearestCoordinates to ", qpoint, nearestCoordinates)

    for index, j in enumerate(coordinateArray):
        if (index != anchorPointIndex and j[0] != nearestCoordinates[0] and j[1] != nearestCoordinates[1]):
            try:
                # distance between anchor point and j
                d_ij = distance.euclidean(qpoint, j)
                r_ij = d_ij / d_i

                # Angle from vector vi vi' to vector vi vj
                theta_ij = angle(j, nearestCoordinates)

                x_prime_j = r_ij * math.cos(theta_ij)
                y_prime_j = r_ij * math.sin(theta_ij)

                new_coordinates.append([x_prime_j, y_prime_j])
            except:
                print("Error, skipping point", j)

    if sort_by_polar_coordinates:
        new_coordinates_sorted_by_polar = sorted(new_coordinates, key=cmp_to_key(do_sort_by_polar_coordinates))
        return np.array(new_coordinates_sorted_by_polar)
    else:
        return np.array(new_coordinates)

def find_candidate_cpps(raster_intersections, vector_intersections, delta_r_tolerance, delta_theta_tolerance):
    # Returns a CCM, a collection of CMs (candidate matching)

    ccm = []

    # select an anchor point r in R such that n(r) in R also is r's nearest neighbor in the image
    for r_index, _ in enumerate(raster_intersections):
        print(r_index, raster_intersections[r_index])

        # compute tpp(r) in R and sort based on polar coordinates
        tpp_r = tpp(raster_intersections, r_index, True)

        # for each point in v in V do
        #   compute tpp(v) and sort it based on the polar coordinates
        tpp_vi = {}

        cache_file = os.path.join("cache", hashlib.sha1(vector_intersections).hexdigest() + ".p")
        if CACHE_VECTOR_TPP and os.path.isfile(cache_file):
            tpp_vi = pickle.load(open(cache_file, "rb"))
        else:
            for index, i in enumerate(vector_intersections):
                tpp_vi[index] = tpp(vector_intersections, index, True)

            pickle.dump(tpp_vi, open(cache_file, "wb"))

        # for each v in V do
        #   if tpp(r) \subseteq tpp(v) then
        #     set acm to be the set of matching point pairs between tpp(r) and tpp(v)
        #     if (there are enough point pairs in acm) then
        #       add acm to ccm
        acm = []
        for index, i in enumerate(vector_intersections):
            r_i, theta_i = cart2pol(*tpp_r[0])
            r_j, theta_j = cart2pol(*tpp_vi[index][0])

            delta_r = r_i - r_j
            delta_theta = theta_i - theta_j

            if delta_r <= delta_r_tolerance and delta_theta <= delta_theta_tolerance:
                acm.append([raster_intersections[r_index], vector_intersections[index]])

        if (len(acm) > 6):
            ccm.append(acm)

    return ccm
