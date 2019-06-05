#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 23:22:21 2019

@author: DRUOT Thierry : original Scilab implementation
         ROCHES Pascal : portage to Python
"""

import numpy

from marilib.earth import environment as earth


#===========================================================================================================
def turbofan_sfc(aircraft,pamb,tamb,mach,rating,nei):
    """
    Bucket SFC for a turbofan
    """

    engine = aircraft.turbofan_engine

    sfc = ( 0.4 + 1/engine.bpr**0.895 )/36000

    return sfc


#===========================================================================================================
def turbofan_thrust(aircraft,Pamb,Tamb,Mach,rating,nei):
    """
    Calculation of thrust for pure turbofan airplane
    Warning : ALL engine thrust returned
    """

    engine = aircraft.turbofan_engine
    nacelle = aircraft.turbofan_nacelle

    factor = engine.rating_factor       # [MTO,MCN,MCL,MCR,FID]

    kth =  0.475*Mach**2 + 0.091*(engine.bpr/10)**2 \
         - 0.283*Mach*engine.bpr/10 \
         - 0.633*Mach - 0.081*engine.bpr/10 + 1.192

    (rho,sig) = earth.air_density(Pamb,Tamb)

    fn0 = factor[int(rating)]*kth*engine.reference_thrust*sig**0.75

    fn_core = fn0 * engine.core_thrust_ratio        # Core thrust

    fn_fan0 = fn0 * (1-engine.core_thrust_ratio)    # Fan thrust

    Vsnd = earth.sound_speed(Tamb)
    Vair = Vsnd*Mach

    shaft_power0 = fn_fan0*Vair/nacelle.efficiency_prop   # Available total shaft power for one engine

    fn = fn0*(engine.n_engine - nei)        # All turbofan thrust

    data = (fn_core,fn_fan0,fn0,shaft_power0)   # Data for ONE turbofan engine

    return fn,data


#===========================================================================================================
def turbofan_nacelle_drag(aircraft,nacelle,Re,Mach):
    """
    Turbofan nacelle drag
    WARNING : All nacelle drag returned
    """

    wing = aircraft.wing

    fac = (1 + 0.126*Mach**2)

    # All nacelle drag
    nac_nwa = nacelle.net_wetted_area

    nac_cxf =   1.15*((0.455/fac)*(numpy.log(10)/numpy.log(Re*nacelle.length))**2.58)*nac_nwa/wing.area

    return nac_cxf,nac_nwa


#===========================================================================================================
def turbofan_oei_drag(aircraft,nacelle,pamb,tamb):
    """
    Inoperative engine drag coefficient
    """

    wing = aircraft.wing

    dCx = 0.12*nacelle.width**2 / wing.area

    return dCx



