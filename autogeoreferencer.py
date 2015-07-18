from scipy import spatial
from scipy.spatial import distance
import numpy as np
import math

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
    nearest = tree.query(qpoint, 2)

    # HACK but if we get the same point back consider the next point as the closest
    closestIndex = 1

    d_i = nearest[0][closestIndex] # distance from anchor point to nearest point
    nearestCoordinates = coordinateArray[nearest[1][closestIndex]] # nearest point coordinates from anchor point

    for index, j in enumerate(coordinateArray):
        if (index != anchorPointIndex and j[0] != nearestCoordinates[0] and j[1] != nearestCoordinates[1]):
            try:
                d_ij = distance.euclidean(qpoint, j) # distance between anchor point and j
                r_ij = d_ij / d_i

                theta_ij = angle(j, nearestCoordinates) # Angle from vector vi vi' to vector vi vj

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
    r_index = 0

    # compute tpp(r) in R and sort based on polar coordinates
    tpp_r = tpp(raster_intersections, r_index, True)

    print(tpp_r)

    # for each point in v in V do
    #   compute tpp(v) and sort it based on the polar coordinates
    # TODO Precompute, store, and load here
    tpp_vi = {}
    for index, i in enumerate(vector_intersections):
        tpp_vi[index] = tpp(vector_intersections, index, True)

    # for each v in V do
    #   if tpp(r) \subseteq tpp(v) then
    #     set acm to be the set of matching point pairs between tpp(r) and tpp(v)
    #     if (there are enough point pairs in acm) then
    #       add acm to ccm
    for index, i in enumerate(vector_intersections):
        r_i, theta_i = cart2pol(*tpp_r[0])

        r_j, theta_j = cart2pol(*tpp_vi[index][0])

        delta_r = r_i - r_j
        delta_theta = theta_i - theta_j

        acm = []
        if delta_r <= delta_r_tolerance and delta_theta <= delta_theta_tolerance:
            print([raster_intersections[r_index], vector_intersections[index]], delta_r, delta_theta)
#             acm.append([raster_intersections[r_index], vector_intersections[index]])
#             if (len(acm) > 3): # TODO verify?
#                 ccm.append(acm)

    return ccm
