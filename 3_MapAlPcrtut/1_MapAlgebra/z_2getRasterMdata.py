#From Preparation notebook 

from osgeo import gdal
import pycrs
import os

gdal.UseExceptions()

def RasterLayerProperties(RasterLayer):
    """_summary_

    Args:
        RasterLayer (_type_): Entry layer to know the properties
    """    

    print("Raster file: {}".format(RasterLayer.GetDescription()))
    print("Driver: {}/{}".format(RasterLayer.GetDriver().ShortName,
                            RasterLayer.GetDriver().LongName))
    print("Size is {} x {} x {}".format(RasterLayer.RasterXSize,
                                    RasterLayer.RasterYSize,
                                    RasterLayer.RasterCount))
    
    RasterLayerProjection = RasterLayer.GetProjection()
    crs = pycrs.parse.from_ogc_wkt(RasterLayerProjection)
    print("Projection:",crs.name)
    print("Map units:",crs.unit.unitname.ogc_wkt)

    geotransform = RasterLayer.GetGeoTransform()
    if geotransform:
        print("Origin = ({}, {})".format(geotransform[0], geotransform[3])) 
        print("Pixel Size = ({} {}, {} {})".format(geotransform[1],crs.unit.unitname.ogc_wkt, \
                                                   geotransform[5],crs.unit.unitname.ogc_wkt))  
    RasterLayerBand = RasterLayer.GetRasterBand(1)
    print("Minimum: {}".format(RasterLayerBand.GetMinimum()))
    print("Maximum: {}".format(RasterLayerBand.GetMaximum()))
    
    print()
    RasterLayer = None

def main(): 

    #Get the path directory containing the Map files produced by the user in this case starting with f
    dir_path = "data"

    #Get the list of Map files in the directory
    map_files = os.listdir(dir_path)

   # Iterate over the Map files and convert them to PCRaster maps
    for map_file in map_files:
        if map_file.startswith('f') and map_file.endswith(".map"):
            map_path = os.path.join(dir_path, map_file)  # Construct the full path
            mapLayer = gdal.Open(map_path)
            if mapLayer is not None:
                RasterLayerProperties(mapLayer)
            else:
                print(f"Failed to open {map_file}")
            


if __name__ == "__main__":
    main()    

#The following lines were replaced by main function to do indefinite number of layers    
    
# DTMLayer = gdal.Open( "data/dtm.map" )
# RasterLayerProperties(DTMLayer)

# BuildgLayer = gdal.Open( "data/buildg.map" )
# RasterLayerProperties(BuildgLayer)

# RoadsLayer = gdal.Open( "data/roads.map" )
# RasterLayerProperties(RoadsLayer)

# GWLevelLayer = gdal.Open( "data/gwlevel.map" )
# RasterLayerProperties(GWLevelLayer)