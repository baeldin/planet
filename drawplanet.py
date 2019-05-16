import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import os
import argparse
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def normalize_height_field(zz,normalized_maximum=7990.):
    normalize_origin = np.max(np.absolute(zz))
    #normalization_factor = normalized_maximum/normalize_origin
    normalization_factor = 0.002
    zz = zz*normalization_factor
    zz = np.where((zz >= 0) & (zz < 0.01), 0.01, zz)
    zz = np.where((zz <  0) & (zz > -0.01), -0.01, zz)
    return zz


def make_global(seed):
    print("generating global height field")
    planet_string="./planet \
    -s %f \
    -o temp_%s_global.asc \
    -w 4000 \
    -h 2000 \
    -H \
    -n \
    -p q" % (seed, str(seed).zfill(3))
    os.system(planet_string)
    data = np.loadtxt('temp_'+str(seed).zfill(3)+'_global.asc')
    lat = np.linspace(90., -90., 2000)
    lon = np.linspace(-180., 180., 4000)
    xx, yy = np.meshgrid(lon,lat)
    return xx, yy, normalize_height_field(data)


def make_zoom(seed, lon0, lat0, zoom):
    print("Generating zoomed height field")
    planet_string="./planet \
    -s %f \
    -o %s_temp_zoom.asc \
    -l %f \
    -L %f \
    -m %f \
    -w 500 \
    -h 500 \
    -H \
    -n \
    -p s" % (seed, str(seed).zfill(3), lon0, lat0, zoom)
    os.system(planet_string)
    data = np.loadtxt(str(seed).zfill(3)+'temp_zoom.asc')
    # lat boundaries
    lon_min = lon0-180./zoom
    lon_max = lon0+180./zoom
    lat_min = lat0-180./zoom
    lat_max = lat0+180./zoom
    lat = np.linspace(lat_max, lat_min, 500)
    lon = np.linspace(lon_min, lon_max, 500)
    xx, yy = np.meshgrid(lon,lat)
    return xx, yy, normalize_height_field(data)


def main():
    # seed = 666
    xx, yy, data = make_global(seed)
    #xx_zoom, yy_zoom, data_zoom = make_zoom(seed,103,-49,20)
    #data_zoom = 10**-6*1900*np.loadtxt('49_zoom.asc')
    #lat_zoom = np.linspace(10.,-50., 1000)
    #lon_zoom = np.linspace(-70.,-10., 1000)
    #lat = np.linspace(90., -90., 5000)
    #lon = np.linspace(-180., 180., 10000)
    #lat = np.linspace(90., -90., 500)
    #lon = np.linspace(-180., 180., 1000)
    #xx, yy = np.meshgrid(lon,lat)
    #xx_zoom, yy_zoom = np.meshgrid(lon_zoom,lat_zoom)
    print("global min: %f, global max: %f" % (data.min(), data.max()))
    #print("global min: %f, global max: %f" % (data_zoom.min(), data_zoom.max()))

    # generate colormaps and norms for sea and land
    cmap = plt.get_cmap('terrain')
    cmap_land = truncate_colormap(cmap,0.225,1)
    levels_sea=[0.01-1,-5,-10,-20,-50,-100,-200,-500,-1000,-1500,-2000,-2500,-3000,-4000,-5000,-6000,-7000,-8000,-9000, -10000]
    levels_sea.reverse()
    levels_land=[0.0099,1,5,10,20,50,100,200,500,1000,1500,2000,2500,3000,4000,5000,6000,7000,8000]
    norm_sea = colors.BoundaryNorm(boundaries=levels_sea, ncolors=256)
    norm_land = colors.BoundaryNorm(boundaries=levels_land, ncolors=256)

    #fig, ax = plt.subplots(2,2,figsize=(8,8),dpi=150)
    fig, ax_global = plt.subplots(1,1, figsize=(32,32), dpi=160, 
        subplot_kw={'projection': ccrs.Stereographic( #)})
            central_longitude=-15.,central_latitude=-30.)}) #,
            # standard_parallels=(30.,50.))})
    #fig, ax_global = plt.subplots(1,1, figsize=(32,32), dpi=160, subplot_kw={'projection': ccrs.Robinson()})
    #fig, (ax_global, ax_zoom) = plt.subplots(2,1, figsize=(16,16), dpi=160, subplot_kw={'projection': ccrs.Robinson()})
    #gridspec.GridSpec(2,4)
    
    #ax_global = fig.add_subplot(2,1,1, projection=ccrs.Mollweide())
    cs = ax_global.contourf(xx,yy,data,levels=levels_sea, cmap='Blues_r',norm=norm_sea, transform=ccrs.PlateCarree(),extend="min")
    cs.cmap.set_under('k')
    cl = ax_global.contourf(xx,yy,data,levels=levels_land,cmap=cmap_land,norm=norm_land,transform=ccrs.PlateCarree(),extend="max")
    cs.cmap.set_over('k')
    ax_global.contour(xx,yy,data,levels=[0.],linewidths=0.5,colors='black',transform=ccrs.PlateCarree())
    ax_global.set_extent([-25.,-5.,-40.,-20.],ccrs.PlateCarree())
    ax_col_land = inset_axes(ax_global,
        width="49%",
        height="2.5%",
        loc="lower right",
        bbox_to_anchor=(0.,-0.08,1,1),
        bbox_transform=ax_global.transAxes,
        borderpad=0.1)
    ax_col_sea = inset_axes(ax_global,
        width="49%",
        height="2.5%",
        loc="lower left",
        bbox_to_anchor=(0.,-0.08,1,1),
        bbox_transform=ax_global.transAxes,
        borderpad=0.1)
    # ax_global.set_extent([-185,-105.,-80.,-25.],ccrs.PlateCarree())
    gl = ax_global.gridlines(crs=ccrs.PlateCarree(),#draw_labels=True,
                  linewidth=0.4, color='black')
    gl.xlocator = mticker.FixedLocator(np.arange(-180,190,30))
    gl.ylocator = mticker.FixedLocator(np.arange(-90,100,30))
    gl.n_steps = 200
    gl = ax_global.gridlines(crs=ccrs.PlateCarree(),#draw_labels=True,
                  linewidth=0.15, color='black')
    gl.xlocator = mticker.FixedLocator(np.arange(-180,190,5))
    gl.ylocator = mticker.FixedLocator(np.arange(-90,100,5))
    gl.n_steps = 200
    #plt.subplot2grid((2,4),(1,0),colspan=3)
    #ax_zoom = plt.subplot(2,1,2)
    # try:
    #     cs_zoom = ax_zoom.contourf(xx_zoom,yy_zoom,data_zoom,levels=levels_sea,cmap='Blues_r',norm=norm_sea)
    # except:
    #     print('no sea')
    # try:
    #     cl_zoom = ax_zoom.contourf(xx_zoom,yy_zoom,data_zoom,levels=levels_land,cmap=cmap_land,norm=norm_land)
    # except:
    #     print('no land')
    # try:
    #     ax_zoom.contour(xx_zoom,yy_zoom,data_zoom,levels=[0.],linewidths=0.5,colors='black')
    # except:
    #     print('no coastline')
    # plt.ylim((yy_zoom.min(),yy_zoom.max()))
    # plt.xlim((xx_zoom.min(),xx_zoom.max()))
    # gl = ax_zoom.gridlines(crs=ccrs.PlateCarree(),#draw_labels=True,
    #               linewidth=0.333, color='black')
    # gl.xlocator = mticker.FixedLocator(np.arange(-180,190,1))
    # gl.ylocator = mticker.FixedLocator(np.arange(-90,100,1))
    # # plt.subplot2grid((2,2),(1,1))
    scbar = fig.colorbar(cs, cax=ax_col_sea, orientation="horizontal")
    scbar.ax.tick_params(labelsize=25)
    lcbar = fig.colorbar(cl, cax=ax_col_land, orientation="horizontal")
    lcbar.ax.tick_params(labelsize=25)

    plt.savefig('SSS_'+str(seed).zfill(3)+'_XHR_coast.png')
    # plt.show()

parser = argparse.ArgumentParser()
parser.add_argument("seed", type=float, default=12345)
args = parser.parse_args()
seed = args.seed

if __name__ == '__main__':
	main()