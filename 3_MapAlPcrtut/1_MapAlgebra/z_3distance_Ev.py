# Import the library
from pcraster import *

def withinDistance(raster,maxdistance):
    ResultWithinDistance = spreadmaxzone(raster, 0, 1, maxdistance)
    return ResultWithinDistance
    
def beyondDistance(raster,mindistance):
    ResultBeyondDistance = ~ spreadmaxzone(raster, 0, 1, mindistance)
    return ResultBeyondDistance

def intersect(*args):   
    if not args:
        return None
    # Initialize the result raster with the first raster in rasters
    inters = args[0]
    # Iterate through the remaining rasters and perform the intersection
    for raster in args[1:]:
        inters = inters & raster
    return inters

def visual(raster):
    # Write result to disk and visualise
    report(raster,"faccessiblewells.map")
    plot(raster,labels={0:"Not accessible",1:"Accessible"},title="Wells",filename=None)

def main():
    # Change to data folder if needed
    os.chdir("./data")
    # Read all input maps
    Buildings = readmap("fbuildg.map")
    Roads = readmap("froads.map")
    GWLevel = readmap("fgwlevel.map")
    DTM = readmap("fdtm.map")

    # Set thresholds for conditions
    DistanceCondition1 = 150
    DistanceCondition2 = 300
    DepthCondition3 = 40

    # Condition 1: Wells within X Meters of Houses or Roads
    Houses = Buildings == 1
    Houses150m = withinDistance(Houses,DistanceCondition1)

    IsRoad = Roads != 0
    Roads150m = withinDistance(IsRoad,DistanceCondition1)

    # Condition 2: No Industry, Mine, or Landfill within X Meters from Wells
    Industry = lookupboolean("industry.tbl", Buildings)
    IndustryMin300m = beyondDistance(Industry,DistanceCondition2)

    # Condition 3: Wells Less than X Meters Deep
    WellDepth = DTM - GWLevel
    NotDeep = WellDepth < DepthCondition3

    # Combine conditions
    AccessibleWells = intersect(Houses150m, Roads150m, IndustryMin300m, NotDeep)
    #Visualization
    visual(AccessibleWells)



if __name__ == "__main__":
    main()    






