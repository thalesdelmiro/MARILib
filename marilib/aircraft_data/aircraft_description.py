#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 23:22:21 2019

@author: DRUOT Thierry, GALLARD Francois, DELMIRO Thales
"""

from collections import OrderedDict

from marilib.aircraft_data.operational_performances \
    import DesignDriver, LowSpeed, HighSpeed, MaxPayloadMission, \
           NominalMission, MaxFuelMission, ZeroPayloadMission, \
           CostMission, Economics, Environmental_Impact

from marilib.aircraft_data.physical_performances \
    import Aerodynamics, Propulsion, CharacteristicWeight, CenterOfGravity

from marilib.airplane.airframe.airframe_data \
    import Cabin, Payload, Fuselage, Wing, Tanks, LandingGears, \
           Systems, HorizontalTail, VerticalTail

from marilib.airplane.propulsion.turbofan.turbofan_data \
    import TurbofanPylon, TurbofanNacelle, TurbofanEngine

from marilib.airplane.propulsion.hybrid_pte1.hybrid_pte1_data \
    import PowerElectricChain, Battery, ElectricNacelle, ElectricEngine

#--------------------------------------------------------------------------------------------------------------------------------
class Aircraft(object):
    """
    Assembling all aircraft data branches
    """
    def __init__(self, name = None):
        """
        Constructor :
            Data structure branches, no ramification
        """
        self.name = name
        self.design_driver = DesignDriver()
        self.low_speed = LowSpeed()
        self.high_speed = HighSpeed()
        self.max_payload_mission = MaxPayloadMission()
        self.nominal_mission = NominalMission()
        self.max_fuel_mission = MaxFuelMission()
        self.zero_payload_mission = ZeroPayloadMission()
        self.cost_mission = CostMission()
        self.economics = Economics()
        self.environmental_impact = Environmental_Impact()

        self.aerodynamics = Aerodynamics()
        self.propulsion = Propulsion()
        self.weights = CharacteristicWeight()
        self.center_of_gravity = CenterOfGravity()

        self.cabin = Cabin()
        self.payload = Payload()
        self.fuselage = Fuselage()
        self.wing = Wing()
        self.landing_gears = LandingGears()
        self.horizontal_tail = HorizontalTail()
        self.vertical_tail = VerticalTail()
        self.tanks = Tanks()
        self.systems = Systems()

        self.turbofan_pylon = TurbofanPylon()
        self.turbofan_nacelle = TurbofanNacelle()
        self.turbofan_engine = TurbofanEngine()

        self.electric_nacelle = ElectricNacelle()
        self.electric_engine = ElectricEngine()
        self.power_elec_chain = PowerElectricChain()
        self.battery = Battery()


    def export_to_ini_file(self, out_file_path = "Aircraft.ini", def_order = True,\
                           user_format = True):
        """
        Build  ini file :
            Data tree file
            :param out_file_path: File path - default value "Aircraft.ini"
            :param def_order: parameters' order - default value True for class definition order
                                                  alternative value False for alphabetical order
        """

        from configobj import ConfigObj
        out_parser = ConfigObj(indent_type="    ")
        out_parser.filename = out_file_path

        if def_order: # class definition order
            data_dict = self.get_ordered_data_dict()
            write_ordered_data_dict_to_ini(data_dict, 'Aircraft', out_parser, user_format)
        else: # alphabetical order
            data_dict = self.get_data_dict()
            write_data_dict_to_ini(data_dict, 'Aircraft', out_parser, user_format)
            
        out_parser.write()
        

    def get_data_dict(self):

        return get_data_dict(self, "Aircraft", {})


#--------------------------------------------------------------------------------------------------------------------------------
def write_data_dict_to_ini(data_dict, section, out_parser):

    for key in sorted(data_dict.keys()):

        value = data_dict[key]

        if isinstance(value, dict):

            out_parser[key] = {}

            write_data_dict_to_ini(value, key, out_parser[key])

        else:

            out_parser[key] = value


#--------------------------------------------------------------------------------------------------------------------------------
def is_basetype(obj):

    if obj is None or not hasattr(obj, "__dict__"):

        return True

    return False


#--------------------------------------------------------------------------------------------------------------------------------
def get_data_dict(obj, obj_name, data_dict):

    curr_data_d = {}

    data_dict[obj_name] = curr_data_d

    if not hasattr(obj, "__dict__"):

        return

    for attr_name in obj.__dict__.keys():

        attribute = getattr(obj, attr_name)

        if is_basetype(attribute):

            curr_data_d[attr_name] = attribute

        else:

            get_data_dict(attribute, attr_name, curr_data_d)

    return data_dict
