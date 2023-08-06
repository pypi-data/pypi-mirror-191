# vim: ts=4:sts=4:sw=4
#
# @date 2021-01-13
#
# This file is part of IDF converter, a set of tools to convert satellite,
# in-situ and numerical model data into Intermediary Data Format, making them
# compatible with the SEAScope application.
#
# Copyright (C) 2014-2022 OceanDataLab
#
# IDF converter is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# IDF converter is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IDF converter. If not, see <https://www.gnu.org/licenses/>.

"""
"""

import os
import numpy
import numpy.typing
import typing
import netCDF4
import logging
import idf_converter.lib
import idf_converter.readers.netcdf_grid_yx
from idf_converter.lib.types import InputOptions, OutputOptions, ReaderResult

logger = logging.getLogger()

DATA_MODEL = idf_converter.readers.netcdf_grid_yx.DATA_MODEL


def help() -> typing.Tuple[str, str]:
    """Describe options supported by this reader.

    Returns
    -------
    str
        Description of the supported options
    """
    in_msg, out_msg = idf_converter.readers.netcdf_grid_yx.help()
    return (in_msg, out_msg)


def mask_where_no_ice(var_dicts: typing.Dict[str, typing.Any],
                      var_id: str
                      ) -> numpy.typing.NDArray:
    """Build mask for ice concentration.

    Parameters
    ----------
    var_dicts: dict
        Dictionary containing the values for each variable

    Returns
    -------
    numpy.ndarray
        Array with cells set to True where values should be masked , i.e. NaN
        or no ice.
    """
    var_dict = var_dicts[var_id]
    values = var_dict['array']
    values._sharedmask = False
    nan_mask = (numpy.isnan(values))
    values[numpy.where(nan_mask)] = -1.0
    zero_mask = (values <= 0.0)
    _mask = (nan_mask | zero_mask)
    result: numpy.typing.NDArray = numpy.ma.getdata(_mask)
    return result


def read_data(input_opts: InputOptions,
              output_opts: OutputOptions
              ) -> typing.Iterator[ReaderResult]:
    """Read input file, extract data and metadata, store them in a Granule
    object then prepare formatting instructions to finalize the conversion to
    IDF format.

    Parameters
    ----------
    input_opts: dict
        Options and information related to input data
    output_opts: dict
        Options and information related to formatting and serialization to IDF
        format

    Returns
    -------
    tuple(dict, dict, idf_converter.lib.Granule, list)
        A tuple which contains four elements:

        - the input_options :obj:dict passed to this method

        - the output_options :obj:dict passed to this method

        - the :obj:`idf_converter.lib.Granule` where the extracted information
          has been stored

        - a :obj:list of :obj:dict describing the formatting operations that
          the converter must perform before serializing the result in IDF
          format
    """
    _input_path = input_opts.get('path', None)
    if _input_path is None:
        raise idf_converter.readers.netcdf_grid_yx.InputPathMissing()
    input_path = os.path.normpath(_input_path)

    f_handler = netCDF4.Dataset(input_path, 'r')
    platform = f_handler.platform_name
    sensor = f_handler.instrument_type
    proj4_str = f_handler.variables['Polar_Stereographic_Grid'].proj4_string
    f_handler.close()

    input_opts['time_variable'] = 'time'
    input_opts['x_variable'] = 'xc'
    input_opts['y_variable'] = 'yc'
    input_opts['time_coverage_relative_start'] = '-86400'
    input_opts['time_coverage_relative_end'] = '0'
    input_opts['spatial_resolution'] = 10000
    input_opts['projection'] = f'+units=km {proj4_str}'  # noqa
    input_opts['variables'] = 'ice_conc,confidence_level'
    input_opts['variable_overrides_ice_conc'] = 'valid_min:0.0,valid_max:100.0'

    grid_yx = idf_converter.readers.netcdf_grid_yx
    result = grid_yx.read_data(input_opts, output_opts)
    input_opts, output_opts, granule, transforms = next(result)

    granule.meta['platform'] = platform
    granule.meta['sensor'] = sensor

    # Remove variables that were required only to compute mask
    transforms.append(('remove_vars', {'targets': ('confidence_level',)}))

    # add mask where confidence level is too low
    qc_mask = (2 > granule.vars['confidence_level']['array'])
    transforms.insert(0, ('static_common_mask', {'targets': ('ice_conc',),
                                                 'mask': qc_mask}))

    # add mask where there is no ice
    mask_methods = {'ice_conc': mask_where_no_ice}
    transforms.insert(0, ('mask_methods', {'targets': ('ice_conc',),
                                           'methods': mask_methods}))
    yield (input_opts, output_opts, granule, transforms)
