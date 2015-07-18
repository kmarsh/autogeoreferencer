# autogeoreferencer

An automated georeferencer based on Li and Brigg's 2006 paper "Automated
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

I'm in the very beginning stages of converting the papers pseudocode and math
into (hopefully) working Python.

Please help!

## Disclaimer

I have no relation to the original authors or claim any copyright to their methods.
I just have a bunch of scanned maps I need to georeference and not much patience
to hand-select GCPs on my own.
