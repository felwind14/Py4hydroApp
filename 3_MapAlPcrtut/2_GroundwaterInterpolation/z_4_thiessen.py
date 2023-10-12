from pcraster import *

def boreh2map():
    #to be improved to read any borehole data
    os.chdir("./Data")
    command = "col2map -S -x 2 -y 3 -v 1 boreholesdxy.csv fboreholedepth.map --clone clone.map" #clones is a mask 
    print("Borehole data read")
    os.system(command)
    bore_map=readmap("fboreholedepth.map")
    return bore_map
  

def thiessen(BoreholeDepth):
    """Function that obtains the thiessen polygons from a borehole data map and assigns
    and assigns the corresponding depth

    Args:
        BoreholeDepth (Raster): Raster generated from csv points with function boreh2map

    Returns:
        _type_: Raster
    """    
    Boreholes = defined(BoreholeDepth)
    BoreholeID = nominal(uniqueid(Boreholes))
    ThiessenID = spreadzone(BoreholeID,0,1)
    BoreholeDepthThiessen = areamaximum(BoreholeDepth,ThiessenID)
    return BoreholeDepthThiessen

def visualiser(raster1, raster2):
    #to be improved to read and plot multiple rasters
    aguila(raster1, raster2)
    

def main():
    #we dont use ./data/"sss.map" because there is boreh2map function locates us in data folder already
    borehole=boreh2map()
    Depth =readmap("fboreholedepth.map")
    DepthThiessen = thiessen(Depth)
    report(DepthThiessen, "fdepththiessen.map")

    visualiser(DepthThiessen, borehole)

if __name__ == "__main__":
    main() 
