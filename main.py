import numpy as np
import time

from autogeoreferencer import find_candidate_cpps

# Test set of major road intersection points in Champaign County, Ohio
vector = np.loadtxt("data/39021-intersections-3857.psv", delimiter="|")
raster = np.loadtxt("data/OH-Champaign-72-01.csv", delimiter=",")

start_time = time.time()

ccm = find_candidate_cpps(raster, vector, -100, 0.5)
print(ccm)

print("--- %s seconds ---" % (time.time() - start_time))
