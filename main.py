import numpy as np
import time

from autogeoreferencer import find_candidate_cpps

# Test set of major road intersection points in Champaign County, Ohio
coords = np.loadtxt("data/39021-intersections.psv", delimiter ="|", usecols=(3, 4), unpack=True)
uniqueCoords = np.array(list(set(tuple(p) for p in coords.transpose())))

# Test set of a few intersections hand picked from a raster map
src = np.array((
                (792.51,  496.17 ),
                (4963.53, 1010.73),
                (1024.57, 2882.35),
                (1062.05, 1958.79),
                (3434.94, 2139.96),
                (1088.57, 1039.68),
                (4620.34, 2538.56),
        ))

start_time = time.time()

ccm = find_candidate_cpps(src, uniqueCoords, -100, 0.5)
print(ccm)

print("--- %s seconds ---" % (time.time() - start_time))
