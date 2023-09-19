# """
# Created on Mon 14 August 
# The same as the jupyter notebook
#Automation of preparation of maps
  

# @author: Felipe.Fonseca
# """

from osgeo import gdal, gdalconst
import os
gdal.UseExceptions() #not in the course but used to from Gdal4.0


def convert_to_pcraster(src_filename, dst_filename, ot, VS):
    """Converts a raster dataset to a PCRaster map.

        Args:
            src_dataset (gdal.Dataset): The source raster dataset.
            dst_dataset (str): The path to the destination PCRaster map.
            ot (gdalconst.GDT_*): The band type of the source raster dataset.
            VS (str): The value scale of the destination PCRaster map.

        Returns:
            None.
   """

    # Open existing dataset
    src_ds = gdal.Open(src_filename)

    # GDAL Translate
    dst_ds = gdal.Translate(dst_filename, src_ds, format= 'PCRaster',\
                             outputType=ot, metadataOptions=VS)
   
    # Properly close the datasets to flush to disk
    dst_ds = None 
    src_ds = None 

def main(): 

    #Get the path directory containing the TIF files
    dir_path = "data"

    #Get the list of TIF files in the directory
    tif_files = os.listdir(dir_path)

    #Iterate over the TIF files and convert them to PCRaster maps

    for tif_file in tif_files:
        if tif_file.endswith(".tif"):
            src_dataset = os.path.join(dir_path, tif_file)
            dst_dataset = f"f{tif_file[:-4]}.map"
        #    convert_to_pcraster(src_dataset,dst_dataset, gdal.GDT_Float32, 'VS_SCALAR')

        #line replaced to store files in the origin folder
            convert_to_pcraster(src_dataset,os.path.join(os.path.dirname(src_dataset), dst_dataset),\
                                 gdal.GDT_Float32, 'VS_SCALAR')


if __name__ == "__main__":
    main()



# """
# Created on Sun Mar 28 21:23:36 2021
# The same as the jupyter notebook
#Here the original one but abvove the complete documented one
# @author: Felipe.Fonseca
# """


# from osgeo import gdal, gdalconst

# def ConvertToPCRaster(src_filename, dst_filename,ot,VS):
#     #Open existing dataset
#     src_ds = gdal.Open(src_filename)
    
#     #GDAL Translate 
#     dst_ds = gdal.Translate(src_filename,src_ds,format='PCRaster', \
#                             outputType=ot, metadataOptions=VS)
    
#     #Properly close the datasets to flush to disk
#     dst_ds = None 
#     src_ds = None 

# ConvertToPCRaster("data/buildg.tif","data/buildg.map",gdalconst.GDT_Int32, 'VS_NOMINAL')
# ConvertToPCRaster("data/roads.tif","data/roads.map",gdalconst.GDT_Int32, 'VS_NOMINAL')  
# ConvertToPCRaster("data/gwlevel.tif","data/gwlevel.map",gdalconst.GDT_Float32, 'VS_SCALAR')   
# ConvertToPCRaster("data/dtm.tif","data/dtm.map",gdalconst.GDT_Float32, 'VS_SCALAR')