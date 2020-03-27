import sys, os
import re
from osgeo import gdal
from osgeo import osr
gdal.UseExceptions() # Enable exceptions

# gdal_translate grid_folder -of GTiff grid.tif

class Surface(object):

    epsg = '/usr/share/proj/epsg'
    forceProj4 = False

    def __init__(self, overwrite=False):
        self.overwrite = overwrite
        pass

    def getEpsg(self,src):

        prj = src.GetProjection()
        srs = osr.SpatialReference(wkt = prj)

        cstype = ''
        if srs.IsLocal() == 1:
            return srs.ExportToWkt()

        if srs.IsGeographic() == 1:
            cstype = 'GEOCS'
        else:
            cstype = 'PROJCS'
        an = srs.GetAuthorityName(cstype)
        ac = srs.GetAuthorityCode(cstype)
        if an is not None and ac is not None:  # return the EPSG code
            return '%s:%s' % (an,ac)

        # try brute force approach by grokking proj epsg definition file
        code = None
        p_out = srs.ExportToProj4()
        if p_out:
            if Surface.forceProj4 is True:
                return p_out
            f = open(Surface.epsg)
            for line in f:
                if line.find(p_out) != -1:
                    m = re.search('<(\\d+)>', line)
                    if m:
                        code = m.group(1)
                        break
            if code:  # match
                return 'EPSG:%s' % code

        return "????"

    def grid_to_tiff(self, rasters, output_folder):

        tiffs = []
        
        first_epsg = None
        # TIFFTAG_GDAL_NODATA ??
        gdal.SetConfigOption("NUM_THREADS","ALL_CPUS")
        gdal.SetConfigOption("COMPRESS","LZW")

        for (folder,fname) in rasters:

            src = os.path.join(folder, fname)

            try:
                gobj = gdal.Open(src)
                print("Raster size =", gobj.RasterXSize, gobj.RasterYSize)
            except Exception as e:
                print("***ERROR: %s %s", (e, src))
                continue

            dst = os.path.join(output_folder, fname + ".tif")
            if os.path.exists(dst):
                if self.overwrite:
                    print("Overwriting", dst)
                    os.unlink(dst)
                else:
                    tiffs.append(dst)
                    # print("Already got one", dst)
                    continue
            
            #print("gdal_translate %s -of %s" % (src, dst))
                
            epsg = self.getEpsg(gobj)
            if first_epsg:
                if epsg != first_epsg:
                    raise Exception("Projection is different on " + src + " " + epsg)
            else:
                first_epsg = epsg
                print("Projection =", epsg)

            status = gdal.Translate(dst, src)
            #print(status)
            tiffs = dst

            gobj = None 
        return tiffs

if __name__ == '__main__':
    print("unit test goes here")
    s = Surface()
    s.build()

