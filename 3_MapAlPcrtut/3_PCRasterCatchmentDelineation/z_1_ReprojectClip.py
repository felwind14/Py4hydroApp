from osgeo import gdal


def reprojectAndClip(inputraster,outputraster,projection,shapefile,resolution):
    options = gdal.WarpOptions(cutlineDSName=shapefile,
                           cropToCutline=True,
                           format='GTIFF',
                           dstSRS=projection,
                           xRes=resolution,
                           yRes=resolution)
    outimage=gdal.Warp(srcDSOrSrcDSTab=inputraster,
                           destNameOrDestDS=outputraster,
                           options=options)
    
def main():

    Mosaic = 'data/fmosaic.vrt'
    DEMSubset = 'data/fDEMsubset.tif'
    EPSG = 'EPSG:32632'
    Polygon = 'data/boundingbox.shp'    
    spatialResolution = 30
    

    reprojectAndClip(Mosaic,DEMSubset,EPSG,Polygon,spatialResolution)

if __name__== "__main__":
    main()