#From Preparation notebook 

from osgeo import gdal
import pycrs
gdal.UseExceptions()

def RasterLayerProperties(RasterLayer):
    """_summary_

    Args:
        RasterLayer (_type_): _description_
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

    
    
DTMLayer = gdal.Open( "data/dtm.map" )
RasterLayerProperties(DTMLayer)

BuildgLayer = gdal.Open( "data/buildg.map" )
RasterLayerProperties(BuildgLayer)

RoadsLayer = gdal.Open( "data/roads.map" )
RasterLayerProperties(RoadsLayer)

GWLevelLayer = gdal.Open( "data/gwlevel.map" )
RasterLayerProperties(GWLevelLayer)