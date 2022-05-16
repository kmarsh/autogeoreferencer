# autogeoreferencer

An automated georeferencer based on Li and Briggs' 2006 paper "Automated
Georeferencing Based on Topological Point Pattern Matching" which relies on the
topology of point patterns (TPP) to capture the spatial information of a point
set.

## Steps

1. Extract intersection points from vector road network (and calculate TPPs)
2. Select intersection points from a raster image (and calculate TPPs)
3. Use matching algorithms to compare raster TPPs with vector TPPs
4. Verify CPPs and transformations
5. Transform and resample the raster image

## Progress

I'm in the very beginning stages of converting the paper's pseudocode and math from steps 3-4 using manually-collected points for input steps 1 and 2
into (hopefully) working Python.

Please help! Pull requests welcome.

## Disclaimer

I have no relation to the original authors or claim any copyright to their methods.

I just have a bunch of scanned maps I need to georeference and not much patience
to hand-select GCPs on my own.
