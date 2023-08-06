# -*- coding: utf-8 -*-
"""PySAM default implementations."""
import json
import os
import pandas as pd
import PySAM.Pvwattsv5 as PySamPV5
import PySAM.Pvwattsv8 as PySamPV8
import PySAM.Pvsamv1 as PySamDetailedPV
import PySAM.Windpower as PySamWindPower
import PySAM.TcsmoltenSalt as PySamCSP
import PySAM.Swh as PySamSWH
import PySAM.TroughPhysicalProcessHeat as PySamTPPH
import PySAM.LinearFresnelDsgIph as PySamLDS
import PySAM.Lcoefcr as PySamLCOE
import PySAM.Singleowner as PySamSingleOwner
import PySAM.MhkWave as PySamMhkWave


DEFAULTSDIR = os.path.dirname(os.path.realpath(__file__))
DEFAULTSDIR = os.path.join(DEFAULTSDIR, 'defaults')


class DefaultPvWattsv5:
    """Class for default PVWattsv5"""

    @staticmethod
    def default():
        """Get the default PySAM pvwattsv5 object"""
        res_file = os.path.join(DEFAULTSDIR,
                                'USA AZ Phoenix Sky Harbor Intl Ap (TMY3).csv')
        config_file = os.path.join(DEFAULTSDIR, 'i_pvwattsv5.json')

        with open(config_file, 'r') as f:
            config = json.load(f)

        obj = PySamPV5.new()
        for k, v in config.items():
            if 'adjust:' not in k and 'file' not in k:
                obj.value(k, v)

        obj.AdjustmentFactors.constant = 0.0
        obj.SolarResource.solar_resource_file = res_file
        obj.execute()

        return obj


class DefaultPvWattsv8:
    """class for default PVWattsv7"""

    @staticmethod
    def default():
        """Get the default PySAM pvwattsv8 object"""
        res_file = os.path.join(DEFAULTSDIR,
                                'USA AZ Phoenix Sky Harbor Intl Ap (TMY3).csv')
        obj = PySamPV8.default('PVWattsNone')
        obj.SolarResource.solar_resource_file = res_file
        obj.execute()

        return obj


class DefaultPvSamv1:
    """class for default detailed PV"""

    @staticmethod
    def default():
        """Get the default PySAM Pvsamv1 object"""
        res_file = os.path.join(DEFAULTSDIR,
                                'USA AZ Phoenix Sky Harbor Intl Ap (TMY3).csv')
        obj = PySamDetailedPV.default('FlatPlatePVNone')
        obj.SolarResource.solar_resource_file = res_file
        obj.execute()

        return obj


class DefaultTcsMoltenSalt:
    """Class for default CSP"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        res_file = os.path.join(DEFAULTSDIR,
                                'USA AZ Phoenix Sky Harbor Intl Ap (TMY3).csv')
        obj = PySamCSP.default('MSPTSingleOwner')
        obj.SolarResource.solar_resource_file = res_file
        obj.execute()

        return obj


class DefaultWindPower:
    """Class for default windpower"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        res_file = os.path.join(DEFAULTSDIR, 'WY Southern-Flat Lands.csv')
        obj = PySamWindPower.default('WindPowerNone')
        obj.Resource.wind_resource_filename = res_file
        obj.execute()

        return obj


class DefaultSwh:
    """Class for default solar water heating"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        res_file = os.path.join(DEFAULTSDIR,
                                'USA AZ Phoenix Sky Harbor Intl Ap (TMY3).csv')
        obj = PySamSWH.default('SolarWaterHeatingNone')
        obj.Weather.solar_resource_file = res_file
        obj.execute()

        return obj


class DefaultTroughPhysicalProcessHeat:
    """Class for default parabolic trough process heat"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        res_file = os.path.join(DEFAULTSDIR,
                                'USA AZ Phoenix Sky Harbor Intl Ap (TMY3).csv')
        obj = PySamTPPH.default('PhysicalTroughIPHNone')
        obj.Weather.file_name = res_file
        obj.execute()

        return obj


class DefaultLinearFresnelDsgIph:
    """Class for default linear direct steam heat"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        res_file = os.path.join(DEFAULTSDIR, 'USA CA Daggett (TMY2).csv')
        obj = PySamLDS.default('DSGLIPHNone')
        obj.Weather.file_name = res_file
        obj.execute()

        return obj


class DefaultMhkWave:
    """Class for default mhkwave"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        data_dict = {}
        data_dict['lat'] = 40.8418
        data_dict['lon'] = 124.2477
        data_dict['tz'] = -7
        res_file = os.path.join(DEFAULTSDIR, 'US_Wave.csv')
        for var, data in pd.read_csv(res_file).iteritems():
            data_dict[var] = data.values.tolist()

        obj = PySamMhkWave.default('MEwaveLCOECalculator')
        obj.MHKWave.wave_resource_model_choice = 1
        obj.unassign('significant_wave_height')
        obj.unassign('energy_period')
        obj.MHKWave.wave_resource_data = data_dict
        obj.execute()

        return obj


class DefaultLCOE:
    """Class for default LCOE calculator"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        pv = DefaultPvWattsv5.default()
        obj = PySamLCOE.default('PVWattsLCOECalculator')
        obj.SimpleLCOE.annual_energy = pv.Outputs.annual_energy
        obj.execute()

        return obj


class DefaultSingleOwner:
    """class for default Single Owner (PPA) calculator"""

    @staticmethod
    def default():
        """Get the default PySAM object"""
        pv = DefaultPvWattsv5.default()
        obj = PySamSingleOwner.default('PVWattsSingleOwner')
        obj.SystemOutput.gen = pv.Outputs.ac
        obj.execute()

        return obj
