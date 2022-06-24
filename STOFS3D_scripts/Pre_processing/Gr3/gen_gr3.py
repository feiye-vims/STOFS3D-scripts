from pyschism.mesh.hgrid import Hgrid
from pyschism.mesh.gridgr3 import Albedo, Diffmax, Diffmin, Watertype, Windrot

if __name__ == '__main__':
    hgrid = Hgrid.open('./hgrid.gr3', crs='epsg:4326')

    albedo = Albedo.constant(hgrid, 0.15)
    albedo.write('albedo.gr3', overwrite=True)

    diffmax = Diffmax.constant(hgrid, 1.0)
    diffmax.write('diffmax.gr3', overwrite=True)

    diffmin = Diffmax.constant(hgrid, 1e-6)
    diffmin.write('diffmin.gr3', overwrite=True)

    watertype = Watertype.constant(hgrid, 1.0) 
    watertype.write('watertype.gr3', overwrite=True)

    windrot=Windrot.constant(hgrid, 0.0)
    windrot.write('windrot_geo2proj.gr3', overwrite=True)
