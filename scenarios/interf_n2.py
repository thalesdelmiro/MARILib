'''
Created on May 23, 2019

@author: Thales DELMIRO
'''


from copy import deepcopy
from os.path import join, dirname

from marilib.aircraft_model.airplane import viewer as show
from gems.api import configure_logger
from gems.api import generate_n2_plot, create_scenario, create_design_space
from gems.core.chain import MDOChain
from gems.core.coupling_structure import MDOCouplingStructure
from gems.utils.gems_interface_generator\
    import get_accessed_props_dict, MARILIBdisc, set_ac_data, to_numbers_dict, \
           get_ac_data, to_arr_dict, generate_disciplines, clean_dkeys, flatten
from gems.utils.xdsmizer import XDSMizer
from scenarios.module_split_n2 import *

OUTPUTS_DIR = join(dirname(__file__), "outputs/n2")
configure_logger("GEMS", "INFO")



aircraft = Aircraft()
n_pax_ref = 150                     # Reference number of passengers
design_range = unit.m_NM(3000)      # Design range
cruise_mach = 0.78                  # Nominal cruise mach number
propu_config = 1    # 1: turbofan, 2: partial turbo electric
n_engine = 2        # Number of engine
aircraft_initialization(aircraft, n_pax_ref, design_range, cruise_mach, propu_config, n_engine)
fuselage_design(aircraft)
predesign_initialization(aircraft)

disc_funcs = [lifting_plane_design, propulsion, aircraft_aerodynamics, aircraft_mass,
              handling_quality_analysis, nominal_mission, performance_analysis, criteria]
disciplines = generate_disciplines(aircraft, disc_funcs)



design_space = create_design_space()
design_space.add_variable("turbofan_engine/reference_thrust", size=1, l_b=50000., u_b=150000., value=140000.)
design_space.add_variable("wing/area", size=1, l_b=50., u_b=200., value=100.)
design_space.add_variable("wing/x_root", size=1, l_b=10., u_b=15., value=13.)
design_space.add_variable("horizontal_tail/area", size=1, l_b=30., u_b=50., value=40.)
design_space.add_variable("vertical_tail/area", size=1, l_b=15., u_b=30., value=25.)


scenario = create_scenario(disciplines, "MDF", "economics/direct_operating_cost",
                            design_space, maximize_objective=False,
                            tolerance=1e-14,
                               max_mda_iter=20)
constraints = ["weights/mass_constraint_1",
               "weights/mass_constraint_2",
               "weights/mass_constraint_3",
               "center_of_gravity/cg_constraint_1",
               "center_of_gravity/cg_constraint_2",
               "center_of_gravity/cg_constraint_3",
               "high_speed/perfo_constraint_1",
               "high_speed/perfo_constraint_2",
               "high_speed/perfo_constraint_3",
               "low_speed/perfo_constraint_1",
               "low_speed/perfo_constraint_2",
               "low_speed/perfo_constraint_3"]

omags = [1e4,  1e4,  1e4,
         10.,10.,10.,
         1e1,1e1,1e1,
         1e2,1e1,1e-2]


for cstr, mag in zip(constraints,omags):
    scenario.add_constraint(cstr, 'ineq',positive=True)
    #scenario.formulation.opt_problem.constraints[-1]*=1/mag

scenario.formulation.opt_problem.objective-=15000.
scenario.formulation.opt_problem.objective*=0.01

run_inputs = {'max_iter': 90,
                  'algo': "NLOPT_COBYLA",
                  'algo_options': {"ftol_rel": 1e-14,"ftol_abs": 1e-14,"xtol_rel": 1e-14,"xtol_abs": 1e-14,
                                   "ineq_tolerance": 1e-2,
                                   "normalize_design_space": True}}

mda=scenario.formulation.mda
mda.set_jacobian_approximation(jac_approx_type=mda.FINITE_DIFFERENCES,
                                   jax_approx_step=1e-7,
                                   jac_approx_n_processes=6)

# Execute scenario
scenario.execute(run_inputs)
# Print execution metrics
scenario.print_execution_metrics()
# Outputs
file_path = join(OUTPUTS_DIR, "mdf")
# N2 diagram
generate_n2_plot(disciplines,file_path=join(OUTPUTS_DIR,"n2.pdf"))
# XDSM diagram
scenario.xdsmize(outdir=OUTPUTS_DIR)
# Plot residual history
scenario.formulation.mda.plot_residual_history(filename=file_path)
# Plot optimization history
scenario.post_process("OptHistoryView", save=True, show=False,
                      file_path=file_path)
# Write variables output to ini file
for disc in disciplines:
    set_ac_data(to_numbers_dict(disc.get_output_data()), aircraft)
aircraft.export_to_ini_file("".join([file_path,"_output_variables.ini"]))
