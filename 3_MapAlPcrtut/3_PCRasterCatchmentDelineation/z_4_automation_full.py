import os, glob
from pcraster import *
from osgeo import gdal, gdalconst

def mosaic(inputpattern,outputmosaic):
    InputFiles = glob.glob(inputpattern)
    mosaic = gdal.BuildVRT(outputmosaic,InputFiles)
    mosaic.FlushCache()
    
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

def ConvertToPCRaster(src_filename,dst_filename,ot,VS):
    #Open existing dataset
    src_ds = gdal.Open( src_filename )
    
    #GDAL Translate
    dst_ds = gdal.Translate(dst_filename, src_ds, format='PCRaster', outputType=ot, metadataOptions=VS)
    
    #Properly close the datasets to flush to disk
    dst_ds = None
    src_ds = None
    
def CalculateFlowDirection(DEMFile):
    DEM = readmap(DEMFile)
    FlowDirectionMap = lddcreate(DEM,1e31,1e31,1e31,1e31)
    return FlowDirectionMap

def StreamDelineation(FlowDirectionMap,Threshold):
    StrahlerOrders = streamorder(FlowDirectionMap)
    Stream = ifthen(StrahlerOrders >= Threshold, boolean(1))
    return Stream
    
def col2map(x,y,clone):
    with open('location.txt', 'w') as f:
        f.write(str(x) + ' ' + str(y) + ' 1')
    cmd = 'col2map -N location.txt location.map --clone {0}'.format(clone)
    os.system(cmd)
    Map = readmap('location.map')
    return Map
    
def main():

    # Define inputs and settings
    # Note that outputs of previous runs need to be removed to avoid errors
    os.chdir('./Data/')

    #Data for mosaic
    TileExtension = '*.tif'
    MosaicOutput = 'mosaic.vrt'
    #Data for reproject and clip
    BoundaryPolygon = 'boundingbox.shp'
    OutputProjection = 'EPSG:32632'
    OutputSpatialResolution = 30.0
    DEMSubsetOutput = 'fDEMsubset.tif' #input to transform tif to map
    #Data tiff to pcraster
    PCRasterDEMOutput = 'fdem.map' #also used in lddr
    #Data for ldd
    #FlowDirectionOutput = 'fflowdir.map'
    StrahlerOrderThreshold = 8
    OutletX = 288880.648
    OutletY = 5675880.258
    clone = PCRasterDEMOutput


    # Apply stream and catchment delineation workflow
    print('Creating mosaic...')
    mosaic(TileExtension,MosaicOutput)
    print('Done!')

    print('Reprojecting and clipping...')
    reprojectAndClip(MosaicOutput,DEMSubsetOutput,OutputProjection,BoundaryPolygon,OutputSpatialResolution)
    print('Done')

    print('Converting to PCRaster format...')
    ConvertToPCRaster(DEMSubsetOutput,PCRasterDEMOutput,gdalconst.GDT_Float32,"VS_SCALAR")
    print('Done!')

    print('Calculating flow direction...')
    setclone(clone)
    FlowDirection = CalculateFlowDirection(PCRasterDEMOutput)
    print('Done!')

    print('Delineating channels...')
    River = StreamDelineation(FlowDirection,StrahlerOrderThreshold)
    print('Done')

    print('Delineating the catchment...')
    Outlet = col2map(OutletX,OutletY,clone)
    CatchmentArea = catchment(FlowDirection,Outlet)
    print('Done')

    #Visualise what you need
    aguila(CatchmentArea)
    aguila(FlowDirection)
    aguila(River)

    #Report what you need
    report(CatchmentArea,'fcatchment.map')
    report(FlowDirection,'fflowdir.map')
    report(River,'fchannels.map')