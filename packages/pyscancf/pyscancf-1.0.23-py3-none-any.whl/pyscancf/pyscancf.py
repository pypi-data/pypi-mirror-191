"""
#!/usr/bin/env python
# coding: utf-8
# Author: Syed Hamid Ali - hamidsyed37@gmail.com
"""
import warnings
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from netCDF4 import num2date
import glob
import re
import os
import pathlib
import pyart
from pyart.config import get_metadata
from matplotlib import axes
from matplotlib.ticker import NullFormatter
import cartopy.crs as ccrs
import cartopy.feature as feat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

warnings.filterwarnings('ignore')
tstart = dt.datetime.now()


def plot_cappi(grid, prod, **kwargs):
    ''' Plots CAPPI
    grid: pyart grid object,
    prod(str): radar product e.g., "REF", "VELH", "WIDTH", or "ALL"
    '''
    max_c = grid.fields[prod]['data'].max(axis=0)
    max_x = grid.fields[prod]['data'].max(axis=1)
    max_y = grid.fields[prod]['data'].max(axis=2).T
    trgx = grid.x['data']
    trgy = grid.y['data']
    trgz = grid.z['data']

    if prod == 'REF':
        cmap = 'pyart_NWSRef'
        levels = range(10, 60)
        stitle = 'Max-Z'
        munit = 'dBZ'

    if prod == 'VELH':
        cmap = 'pyart_NWSVel'
        levels = range(-30, 31)
        stitle = 'Max-V'
        munit = 'm/s'

    if prod == 'WIDTH':
        cmap = 'pyart_NWS_SPW'
        levels = np.linspace(0, 5, 9)
        stitle = 'Max-W'
        munit = 'm/s'

    print('Generating Figures of Max-CAPPI, please be patient!')
    fig = plt.figure(figsize=(10.3, 10))
    # define axes
    left, bottom, width, height = 0.1, 0.1, 0.6, 0.2
    left, bottom, width, height = 0.1, 0.1, 0.6, 0.2
    ax_xy = plt.axes((left, bottom, width, width),
                     projection=ccrs.AzimuthalEquidistant(
                         grid.origin_longitude['data'][0],
                         grid.origin_latitude['data'][0]))
    ax_x = plt.axes((left, bottom + width, width, height))
    ax_y = plt.axes((left + width, bottom, height, width))
    ax_cnr = plt.axes((left+width, bottom + width, left+left, height))
    ax_cb = plt.axes((left + width + height + 0.02, bottom, 0.02, width))

    # set axis label formatters
    ax_x.xaxis.set_major_formatter(NullFormatter())
    ax_y.yaxis.set_major_formatter(NullFormatter())
    ax_cnr.yaxis.set_major_formatter(NullFormatter())
    ax_cnr.xaxis.set_major_formatter(NullFormatter())

    # label axes
    # ax_xy.set_xlabel("Longitude [°E]",fontsize=15)
    # ax_xy.set_ylabel("Latitude [°N]",fontsize=15)
    # ax_x.set_xlabel("")
    ax_x.set_ylabel("Height AMSL (km)", fontsize=15)
    # ax_y.set_ylabel("")
    ax_y.set_xlabel("Height AMSL (km)", fontsize=15)

    # draw CAPPI
    plt.sca(ax_xy)
    xy = ax_xy.contourf(trgx, trgy, max_c, cmap=cmap, levels=levels, **kwargs)
    gl = ax_xy.gridlines(
        crs=ccrs.PlateCarree(),
        linewidth=1, color='black', alpha=0.5,
        linestyle='--', draw_labels=True
                        )
    gl.xlabels_top = False
    gl.ylabels_left = True
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    # gl.xlabel_style = {'weight': 'bold'}
    # gl.ylabel_style = {'weight': 'bold'}

    # ax_xy.add_feature(shape_feature)
    ax_xy.add_feature(feat.COASTLINE, alpha=0.5)
    ax_xy.add_feature(feat.BORDERS, alpha=0.5)

    [ax_xy.plot(r * np.cos(np.arange(0, 360) * np.pi / 180),
                r * np.sin(np.arange(0, 360) * np.pi / 180),
                'k--', linewidth=1,
                alpha=0.5) for r in np.arange(5e4, 30e4, 5e4)]

    ax_xy.set_xlim(-2.5e5, 2.5e5)
    ax_xy.set_ylim(-2.5e5, 2.5e5)
    ax_xy.plot([0, 0], [-10e3, 10e3],)  # 'w-')
    ax_xy.plot([-10e3, 10e3], [0, 0],)  # 'w-')

    # draw colorbar
    cb = plt.colorbar(xy, cax=ax_cb)
    cb.set_label(munit, fontsize=15)

    plt.sca(ax_x)
    plt.contourf(trgx/1e3, trgz/1e3, max_x, cmap=cmap, levels=levels)
    # plt.ylim(0,20)
    # plt.yticks([0,5,10,15,20])
    # plt.grid(axis='y')
    ax_x.set_xlim(-250, 250)

    plt.sca(ax_y)
    plt.contourf(trgz/1e3, trgy/1e3, max_y, cmap=cmap, levels=levels)
    # plt.xlim(0,20)
    ax_y.set_xticks([5, 10, 15, 20])
    # plt.grid(axis='x')
    ax_y.set_ylim(-250, 250)

    plt.sca(ax_cnr)
    plt.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        left=False,
        right=False,
        labelbottom=False)
    # labels along the bottom edge are off
    plt.text(0.34, 0.8, stitle, size=14, weight='bold')
    plt.text(0.09, 0.65, 'Max Range: 250 km', fontsize=12)
    plt.text(0.12, 0.5, 'VPR Height: 20 km', fontsize=12)
    plt.text(0.15, 0.3, num2date(
        grid.time['data'], grid.time['units']
        )[0].strftime('%H:%M:%S Z'), weight='bold', fontsize=17)
    plt.text(0.06, 0.15, num2date(
        grid.time['data'], grid.time['units']
        )[0].strftime('%d %b, %Y UTC'), fontsize=14)

    ax_xy.set_aspect('auto')
    plt.savefig(stitle+'_'+grid.metadata['instrument_name'] +
                num2date(grid.time['data'],
                grid.time['units'])[0].strftime('%Y%m%d%H%M%S')+'.jpg',
                dpi=100, bbox_inches='tight')
    print('Figures saved')


def get_grid(radar, grid_shape=(30, 500, 500), height=15, length=250):
    """
    Returns grid object from radar object.
    grid_shape=(60, 500, 500), no. of bins of z,y,x respectively.
    height:(int) = 15, height in km
    length:(int) = 250, horizontal length in km
    """
    grid = pyart.map.grid_from_radars(
        radar, grid_shape=grid_shape,
        grid_limits=((radar.altitude['data'][0], height * 1e3),
                     (-length * 1e3, length * 1e3),
                     (-length * 1e3, length*1e3)),
        fields=radar.fields.keys(),
        weighting_function='Barnes2',
        min_radius=length)
    return grid

def natural_sort_key(s, _re=re.compile(r'(\d+)')):
    return [int(t) if i & 1 else t.lower() for i, t in enumerate(_re.split(s))]

def cfrad(input_dir, output_dir, scan_type="B", dualpol=False, gridder=False, plot=None,nf=None):
    '''
        input_dir(str): Enter path of single sweep data directory,
        output_dir(str): Enter the path for output data,
        scan_type(str): "B", "C". B is for short range PPI, & C is for long range PPI.
        dualpol(bool): True, False. (If the data contains dual-pol products e.g., ZDR, RHOHV),
        gridder(bool): True, False,
        plot(str): 'REF', 'VELH', 'WIDTH', 'ALL',
        nf(int): Number of files to group together
    '''
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    in_dir = input_dir
    out_dir = output_dir
    files_list = glob.glob(os.path.join(in_dir, "*nc*"))
    files = sorted(files_list, key=natural_sort_key)
    print('Number of files: ', len(files))
    bb = list()
    if scan_type == "B":
        if nf is None:
            nf = 10
        for i in range(0, len(files), nf):
            bb.append(files[i:i+nf])
    elif scan_type == "C":
        if nf is None:
            nf = 2
        for i in range(0, len(files), nf):
            bb.append(files[i:i+nf])
    print('Total number of files will be created: ', len(bb))
    print('Merging all scans in one file')
    for i in range(0, len(bb)):
        en = []
        a1 = []
        t1 = []
        e1 = []
        Z1 = []
        # T1 = []
        V1 = []
        W1 = []
        ZDR1 = []
        KDP1 = []
        PHIDP1 = []
        SQI1 = []
        RHOHV1 = []
        HCLASS1 = []
        nyquist = []
        unambigrange = []
        for j in range(0, nf):
            ds = Dataset(bb[i][j])
            az = ds.variables['radialAzim'][:]
            time = ds.variables['radialTime'][:]
            ele = ds.variables['radialElev'][:]
            Z = ds.variables['Z'][:]
            # T = ds.variables['T'][:]
            V = ds.variables['V'][:]
            W = ds.variables['W'][:]
            EN = ds.variables['elevationNumber'][:]
            a1.extend(az)
            t1.extend(time)
            e1.extend(ele)
            Z1.extend(Z)
            # T1.extend(T)
            V1.extend(V)
            W1.extend(W)
            en.append(EN)
            nyquist.append(ds.variables['nyquist'][:])
            unambigrange.append(ds.variables['unambigRange'][:])
            if dualpol:
                ZDR = ds.variables['ZDR'][:]
                PHIDP = ds.variables['PHIDP'][:]
                KDP = ds.variables['KDP'][:]
                SQI = ds.variables['SQI'][:]
                RHOHV = ds.variables['RHOHV'][:]
                HCLASS = ds.variables['HCLASS'][:]
                ZDR1.extend(ZDR)
                KDP1.extend(KDP)
                PHIDP1.extend(PHIDP)
                SQI1.extend(SQI)
                RHOHV1.extend(RHOHV)
                HCLASS1.extend(HCLASS)

        fname = os.path.basename(bb[i][0]).split(".nc")[0]

        radar = pyart.testing.make_empty_ppi_radar(
            ds.dimensions['bin'].size, ds.dimensions['radial'].size*nf, 1)
        radar.nsweeps = nf
        radar.time['data'] = np.array(t1)
        # 'seconds since 1970-01-01T00:00:00Z'
        radar.time['units'] = ds.variables['radialTime'].units
        radar.latitude['data'] = np.array([ds.variables['siteLat'][:]])
        radar.longitude['data'] = np.array([ds.variables['siteLon'][:]])
        radar.altitude['data'] = np.array([ds.variables['siteAlt'][:]])
        radar.range['data'] = np.arange(
            0,
            ds.dimensions['bin'].size*ds.variables['gateSize'][:].data,
            int(ds.variables['gateSize'][:].data))

        radar.fixed_angle['data'] = ds.variables['elevationList']

        radar.sweep_number['data'] = np.array(en)

        radar.sweep_start_ray_index['data'] = np.arange(
            0,
            ds.dimensions['radial'].size*nf,
            ds.dimensions['radial'].size)

        radar.sweep_end_ray_index['data'] = np.arange(
            ds.dimensions['radial'].size-1,
            ds.dimensions['radial'].size*nf,
            ds.dimensions['radial'].size)

        radar.azimuth['data'] = np.ma.array(a1)
        radar.elevation['data'] = np.ma.array(e1)
        radar.metadata['instrument_name'] = fname[:3]
        radar.init_gate_altitude()
        radar.init_gate_longitude_latitude()
        ref_dict = get_metadata('reflectivity')
        ref_dict['data'] = np.ma.array(Z1)
        ref_dict['units'] = 'dBZ'
        VELH_dict = get_metadata('velocity')
        VELH_dict['data'] = np.ma.array(V1)
        VELH_dict['units'] = 'm/s'
        W_dict = get_metadata('spectrum_width')
        W_dict['data'] = np.ma.array(W1)
        W_dict['units'] = 'm/s'
        radar.instrument_parameters = {}
        radar.instrument_parameters['nyquist_velocity'] = {
            'units': 'm/s',
            'comments': 'Unambiguous velocity',
            'meta_group': 'instrument_parameters',
            'long_name': 'Nyquist velocity'}
        radar.instrument_parameters['nyquist_velocity']['data'] = np.ma.array(nyquist)
        radar.instrument_parameters['unambiguous_range'] = {
            'units': 'meters', 
            'comments': 'Unambiguous range', 
            'meta_group': 'instrument_parameters',
            'long_name': 'Unambiguous range'}
        radar.instrument_parameters['unambiguous_range']['data'] = np.ma.array(unambigrange)

        if dualpol:
            ZDR_dict = get_metadata('differential_reflectivity')
            ZDR_dict['data'] = np.ma.array(ZDR1)
            PHIDP_dict = get_metadata('differential_phase')
            PHIDP_dict['data'] = np.ma.array(PHIDP1)
            KDP_dict = get_metadata('specific_differential_phase')
            KDP_dict['data'] = np.ma.array(KDP1)
            RHOHV_dict = get_metadata('cross_correlation_ratio')
            RHOHV_dict['data'] = np.ma.array(RHOHV1)
            SQI_dict = get_metadata('normalized_coherent_power')
            SQI_dict['data'] = np.ma.array(SQI1)
            HCLASS_dict = get_metadata('radar_echo_classification')
            HCLASS_dict['data'] = np.ma.array(HCLASS1)
        if dualpol is False:
            radar.fields = {'REF': ref_dict,
                            'VELH': VELH_dict,
                            'WIDTH': W_dict}
        else:
            radar.fields = {'REF': ref_dict, 'VELH': VELH_dict,
                            'WIDTH': W_dict, 'ZDR': ZDR_dict,
                            'KDP': KDP_dict, 'PHIDP': PHIDP_dict,
                            'SQI': SQI_dict, 'RHOHV': RHOHV_dict,
                            'HCLASS': HCLASS_dict}
        
        out_file = f"cfrad_{fname}.nc"
        out_path = os.path.join(out_dir, out_file)
        pyart.io.write_cfradial(out_path, radar, format='NETCDF4')
        
        if gridder:
            grid = get_grid(radar)
            if plot is not None:
                if plot == 'REF':
                    plot_cappi(grid, 'REF')
                if plot == 'VELH':
                    plot_cappi(grid, 'VELH')
                if plot == 'WIDTH':
                    plot_cappi(grid, 'WIDTH')
                if plot == 'ALL':
                    plot_cappi(grid, 'REF')
                    plot_cappi(grid, 'VELH')
                    plot_cappi(grid, 'WIDTH')
            else:
                pass
            out_file = f"grid_{fname}.nc"
            out_path = os.path.join(out_dir, out_file)
            pyart.io.write_grid(out_path, grid)
            del radar, grid
        else:
            pass
    print('Data merging done \nTotal Time Elapsed: ', dt.datetime.now()-tstart)