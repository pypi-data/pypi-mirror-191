# vim: ts=4:sts=4:sw=4
#
# @date 2019-09-25
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

import numpy
import typing
import logging
import numpy.typing
import scipy.interpolate
from idf_converter.lib.types import InputOptions, OutputOptions, Granule
from idf_converter.lib.types import FormatterResult, NumValuesDict, AtmCorrData

logger = logging.getLogger(__name__)


class IncompatibleLUTSize(ValueError):
    """Error raised when the number of entries in the LUT is not a multiple of
    (number of observation zenith angles * number of zenithal deltas)."""
    def __init__(self, lut_size: int, lut_size_factor: float) -> None:
        """"""
        self.lut_size = lut_size
        self.lut_size_factor = lut_size_factor
        _msg = ('The size of the LUT does not match the hardcoded '
                'parameters: the number of lines per sza value should '
                f'be {lut_size_factor}')
        super(IncompatibleLUTSize, self).__init__(_msg)


def interp_tie_ac(tie_values_list: typing.List[numpy.typing.NDArray],
                  tie_ac_factor: int,
                  ac_index: numpy.typing.NDArray
                  ) -> typing.List[numpy.typing.NDArray]:
    """"""
    # Linear interpolation over across-track dimension
    tie_ac_index = numpy.arange(tie_values_list[0].shape[1],
                                dtype='float32') * tie_ac_factor
    indint = numpy.clip(numpy.searchsorted(tie_ac_index, ac_index) - 1,
                        0, tie_ac_index.size - 2)
    indratio = (ac_index - tie_ac_index[indint]) / \
               (tie_ac_index[indint + 1] - tie_ac_index[indint])
    indratio = indratio[numpy.newaxis, :]
    int_values = []
    for val in tie_values_list:
        ac_diff = val[:, indint + 1] - val[:, indint]
        int_val = val[:, indint] + ac_diff * indratio
        int_values.append(int_val)
    return int_values


def get_atmospheric_rho(targets: typing.Iterable[str],
                        atm_corr_data: AtmCorrData) -> NumValuesDict:
    """Compute atmospheric correction from LUT"""
    sza_lut = atm_corr_data['SZA_LUT']
    oza_lut = atm_corr_data['OZA_LUT']
    delta_lut = atm_corr_data['DELTA_LUT']
    rho_lut = numpy.array(atm_corr_data['RHO_LUT'])

    oza_resol = 5
    # sza_resol = 5
    delta_resol = 10
    ntot_delta = 360 / delta_resol + 1
    ntot_oza = 90 / oza_resol + 1

    sza = atm_corr_data['SZA'].astype('float32')
    saa = atm_corr_data['SAA'].astype('float32')
    oza = atm_corr_data['OZA'].astype('float32')
    oaa = atm_corr_data['OAA'].astype('float32')

    bands_index = atm_corr_data['bands_index']

    # Check the size of the LUT
    lut_size = len(rho_lut)
    lut_size_factor = ntot_oza * ntot_delta
    if 0 != (lut_size % lut_size_factor):
        raise IncompatibleLUTSize(lut_size, lut_size_factor)

    # Interpolate atmospheric correction according to angles
    delta = numpy.mod(saa - oaa, 360.)
    _points = numpy.array((sza.flatten(), oza.flatten(),
                           delta.flatten())).transpose()
    sza_lut = numpy.unique(numpy.array(sza_lut, dtype='float32'))
    oza_lut = numpy.unique(numpy.array(oza_lut, dtype='float32'))
    delta_lut = numpy.unique(numpy.array(delta_lut, dtype='float32'))
    lut_points = (sza_lut, oza_lut, delta_lut)

    result = {}
    interpolator = scipy.interpolate.RegularGridInterpolator
    lut_shape = (sza_lut.size, oza_lut.size, delta_lut.size)
    for var_id in targets:
        band_index = bands_index[var_id]
        lut_values = numpy.array(rho_lut[:, band_index],
                                 dtype='float32').reshape(lut_shape)
        lut_func = interpolator(lut_points, lut_values, method='linear',
                                bounds_error=False, fill_value=None)
        band_rho = lut_func(_points).reshape(sza.shape).astype('float32')
        result[var_id] = band_rho
    return result


def studpdf(z: numpy.typing.NDArray,
            wind: float,
            n: float
            ) -> numpy.typing.NDArray:
    """
    """
    # Magic numbers, yeah!
    mss = 0.003 + 5.12e-3 * wind
    p_denom = (1. + (2. * z ** 2. / mss) / (n - 1.)) ** (n / 2. + 1)
    p: numpy.ndarray = n / (n - 1.) / (numpy.pi * mss) / p_denom  # type:ignore
    return p


def brightness_contrast(input_opts: InputOptions,
                        output_opts: OutputOptions,
                        granule: Granule,
                        *args: typing.Iterable[typing.Any],
                        targets: typing.Iterable[str],
                        atm_corr_data: AtmCorrData) -> FormatterResult:
    """"""
    sza = atm_corr_data['SZA'].astype('float32')
    saa = atm_corr_data['SAA'].astype('float32')
    oza = atm_corr_data['OZA'].astype('float32')
    oaa = atm_corr_data['OAA'].astype('float32')

    # Extra-terrestrial solar irradiance
    solar_flux = atm_corr_data['solar_flux']

    ac_subsampling = atm_corr_data['ac_subsampling']
    ncell = atm_corr_data['ncell']

    cos_sza = numpy.cos(numpy.deg2rad(sza))
    sin_sza = numpy.sin(numpy.deg2rad(sza))
    cos_saa = numpy.cos(numpy.deg2rad(saa))
    sin_saa = numpy.sin(numpy.deg2rad(saa))
    cos_oza = numpy.cos(numpy.deg2rad(oza))
    sin_oza = numpy.sin(numpy.deg2rad(oza))
    cos_oaa = numpy.cos(numpy.deg2rad(oaa))
    sin_oaa = numpy.sin(numpy.deg2rad(oaa))

    tie_zx = -1 * (sin_sza * cos_saa + sin_oza * cos_oaa) / (cos_sza + cos_oza)
    tie_zy = -1 * (sin_sza * sin_saa + sin_oza * sin_oaa) / (cos_sza + cos_oza)

    tie_nrow, tie_ncell = numpy.shape(sza)
    ac_index = numpy.arange(0, ncell, dtype='float32')
    _oza = oza * numpy.sign(sin_oaa)
    _values_list = [tie_zx, tie_zy, sza, _oza]
    zx, zy, interp_sza, interp_oza = interp_tie_ac(_values_list,
                                                   ac_subsampling, ac_index)
    zx_sqr: numpy.typing.ArrayLike = zx ** 2.
    zy_sqr: numpy.typing.ArrayLike = zy ** 2.
    z = numpy.sqrt(zx_sqr + zy_sqr)
    del zx, zy
    interp_oza = numpy.abs(interp_oza)

    # Magic numbers, yeah!
    offset = 0.008263
    k = 0.859117
    w = 6.766508
    n = 4.878770

    # More magic numbers in formula, yeah!
    _stu_pdf = studpdf(z, w, n)
    cos_interp_sza = numpy.cos(numpy.deg2rad(interp_sza))
    cos_interp_oza = numpy.cos(numpy.deg2rad(interp_oza))
    rho_back_numerator = k * _stu_pdf * numpy.pi * 0.022 * (1. + z ** 2.) ** 2
    rho_back_denominator = 4. * cos_interp_sza * cos_interp_oza
    rho_back = offset + rho_back_numerator / rho_back_denominator

    rho_atm = get_atmospheric_rho(targets, atm_corr_data)

    for var_id in targets:
        _band_rho_atm = rho_atm[var_id]
        band_rho_atm = interp_tie_ac([_band_rho_atm], ac_subsampling,
                                     ac_index)[0]
        band_rho_back = rho_back + band_rho_atm

        band = granule.vars[var_id]['array']

        # 10**(-3) variation for solar flux is neglectable so we consider the
        # mean
        es = numpy.mean(solar_flux[var_id])

        rho_band = band * numpy.pi
        rho_band = rho_band / cos_interp_sza
        rho_band = rho_band / es
        result = rho_band / band_rho_back

        var_id_bc = f'{var_id}_bc'
        granule.vars[var_id_bc]['array'] = result

    return input_opts, output_opts, granule
