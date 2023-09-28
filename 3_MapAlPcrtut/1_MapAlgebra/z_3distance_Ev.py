# Import the library
from pcraster import *

def WithinDistance(raster,maxdistance):
    ResultWithinDistance = spreadmaxzone(raster, 0, 1, maxdistance)
    return ResultWithinDistance
    
def BeyondDistance(raster,mindistance):
    ResultBeyondDistance = ~ spreadmaxzone(raster, 0, 1, mindistance)
    return ResultBeyondDistance

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
Houses150m = WithinDistance(Houses,DistanceCondition1)

IsRoad = Roads != 0
Roads150m = WithinDistance(IsRoad,DistanceCondition1)

# Condition 2: No Industry, Mine, or Landfill within X Meters from Wells
Industry = lookupboolean("industry.tbl", Buildings)
IndustryMin300m = BeyondDistance(Industry,DistanceCondition2)

# Condition 3: Wells Less than X Meters Deep
WellDepth = DTM - GWLevel
NotDeep = WellDepth < DepthCondition3

# Combine conditions
AccessibleWells = Houses150m & Roads150m & IndustryMin300m & NotDeep

# Write result to disk and visualise
report(AccessibleWells,"faccessiblewells.map")
plot(AccessibleWells,labels={0:"Not accessible",1:"Accessible"},title="Wells",filename=None)