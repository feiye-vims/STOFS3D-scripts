import glob
import shutil
import os
import subprocess
import copy

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.validation import make_valid
#import fiona
from geopandas import GeoDataFrame

from pyschism.mesh.hgrid import Hgrid

def contour_to_gdf(hgrid, maxelev):
    h = -hgrid.values
    elev = Hgrid.open(maxelev, crs='EPSG:4326')
    mzeta = -elev.values
    D = copy.deepcopy(mzeta)

    #Mask dry nodes
    NP = len(mzeta)
    idxs = np.where(h < 0)
    D[idxs] = np.maximum(0, mzeta[idxs]+h[idxs])

    idry = np.zeros(NP)
    idxs = np.where(mzeta+h <= 1e-6)
    idry[idxs] = 1

    MinVal = np.min(D)
    MaxVal = np.max(D)
    NumLevels = 21

    if True:
        MinVal = max(MinVal, 0.5)
        MaxVal = min(MaxVal, 3.0)
        NumLevels = 12
    print(f'MinVal is {MinVal}')
    print(f'MaxVal is {MaxVal}')

    step = 0.2  # m 
    levels = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9]
    print(f'levels is {levels}')
    fig = plt.figure()
    ax = fig.add_subplot()
    tri = elev.triangulation
    mask = np.any(np.where(idry[tri.triangles], True, False), axis=1)
    tri.set_mask(mask)

    my_cmap = plt.cm.jet
    contour = ax.tricontourf(tri, D, vmin=MinVal, vmax=MaxVal,levels=levels, cmap=my_cmap, extend='max')

    #Transform a `matplotlib.contour.QuadContourSet` to a GeoDataFrame
    polygons, colors = [], []
    for i, polygon in enumerate(contour.collections):
        mpoly = []
        for path in polygon.get_paths():
            try:
                path.should_simplify = False
                poly = path.to_polygons()
                # Each polygon should contain an exterior ring + maybe hole(s):
                exterior, holes = [], []
                if len(poly) > 0 and len(poly[0]) > 3:
                    # The first of the list is the exterior ring :
                    exterior = poly[0]
                    # Other(s) are hole(s):
                    if len(poly) > 1:
                        holes = [h for h in poly[1:] if len(h) > 3]
                mpoly.append(make_valid(Polygon(exterior, holes)))
            except:
                print('Warning: Geometry error when making polygon #{}'.format(i))

        if len(mpoly) > 1:
            mpoly = MultiPolygon(mpoly)
            polygons.append(mpoly)
            colors.append(polygon.get_facecolor().tolist()[0])
        elif len(mpoly) == 1:
            polygons.append(mpoly[0])
            colors.append(polygon.get_facecolor().tolist()[0])
    plt.close('all')
    #return GeoDataFrame(geometry=polygons, data={'RGBA': colors}, crs={'init': 'epsg:4326'})
    return GeoDataFrame(geometry=polygons, crs={'init': 'epsg:4326'})

if __name__ == "__main__":
#   path = f'/home1/06923/hyu05/work/oper_3D/fcst'
#   fcst = glob.glob(f'{path}/2021*')
#   fcst.sort()
#   fname = f'{fcst[-1]}/maxelev.gr3.gz'
#   work_dir = './'
#   shutil.copy(fname, work_dir)
#   cmd='gunzip -f maxelev.gr3.gz'
#   subprocess.check_call(cmd, shell=True)

    fgrd = Hgrid.open('./hgrid.gr3', crs='epsg:4326')
    felev = 'maxelev.gr3'

    gdf = contour_to_gdf(fgrd, felev)


    #Get color in Hex
    colors_elev = []
    my_cmap = plt.cm.jet

    for i in range(len(gdf)):
        color = my_cmap(i/len(gdf))
        colors_elev.append(mpl.colors.to_hex(color))

    gdf['RGBA'] = colors_elev
    gdf.to_file('./disturbance.json', driver="GeoJSON")

