import numpy as np
import time

from autogeoreferencer import find_candidate_cpps

# Test set of major road intersection points in Champaign County, Ohio
vector = np.loadtxt("data/39021-intersections-3857.psv", delimiter="|")
raster = np.loadtxt("data/OH-Champaign-72-01.csv", delimiter=",", usecols=(0, 1))

# TODO: Create a ground truth mapping of raster point to vector point

start_time = time.time()

ccm = find_candidate_cpps(raster, vector, -50, 0.2)
print(f"found {len(ccm)} candidate matching pairs")

for i, c in enumerate(ccm):
    print(f"{i}: {len(c)}")

# TODO: Evaluate if any CMs contain the correct mapping

print("--- %s seconds ---" % (time.time() - start_time))
