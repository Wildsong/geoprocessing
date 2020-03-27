# __main__.py
#
# This file contains code that will run
# when this package is called as a module ("python -m geoprocessing")
import sys, os
import re
from osgeo import gdal

from surface import Surface
from contour import Contour

datadir = '/data' # this is a docker volume

hh = []
be = []
intensity = []
shapefiles = []

def collect_filenames() :

    re_bareearth_hillshade = re.compile(r'(.*)/(be\d+.*h)$')
    re_bareearth = re.compile(r'(.*)/(be\d+.*)')
    re_highesthit_hillshade = re.compile(r'(.*)/(hh\d+.*h)$')
    re_highesthit = re.compile(r'(.*)/(hh\d+.*)')

    # I need to shave off the "/data" since that is just a volume name
    os.chdir(datadir)

    for (d, dirnames, filenames) in os.walk('.'):

        mo = re.search(re_bareearth_hillshade,d)
        if (mo):
            #print("Ignoring this hillshade", mo.group(2))
            continue
        mo = re.search(re_bareearth,d)
        if (mo):
            be.append((mo.group(1), mo.group(2)))
            continue

        mo = re.search(re_highesthit_hillshade,d)
        if (mo):
            #print("Ignoring this hillshade", mo.group(2))
            continue
        mo = re.search(re_highesthit,d)
        if (mo):
            hh.append((mo.group(1), mo.group(2)))
            continue

        if d.find('Intensity') >= 0 :
            for tif in filenames:
                (n,x) = os.path.splitext(tif)
                if x.upper() == '.TIF':
                    intensity.append((d, tif))
            continue

        if d.find('Shapefiles') >= 0 :
            for shp in filenames:
                (n,x) = os.path.splitext(shp)
                if x.upper() == '.SHP':
                    shapefiles.append((d, shp))
            continue
    return

print("gdal version is", gdal.__version__)

print("Searching for files...")
collect_filenames()
print("I found %d shapefiles, %d intensity files, %d bareearth files, and %d highest hit files."
    % (len(shapefiles), len(intensity), len(be), len(hh)))

# Maybe I can collect all the shapefiles into one database?
# All the intensity files can be in a VRT
print("Processing Bare Earth")
be_folder = os.path.join(datadir, "be")
if not os.path.exists(be_folder):
    os.mkdir(be_folder)
s = Surface(overwrite=False)
betiff = s.grid_to_tiff(be, be_folder)
s = None

print("Building mosaic")
vrt = gdal.BuildVRT(os.path.join(datadir,"be.vrt"), betiff)

print("Processing Highest Hits")
hh_folder = os.path.join(datadir, "hh")
if not os.path.exists(hh_folder):
    os.mkdir(hh_folder)
s = Surface(overwrite=False)
hhtiff = s.grid_to_tiff(hh, hh_folder)
s = None

print("Building mosaic")
vrt = gdal.BuildVRT(os.path.join(datadir,"hh.vrt"), hhtiff)

c = Contour()
c.build()

pass
