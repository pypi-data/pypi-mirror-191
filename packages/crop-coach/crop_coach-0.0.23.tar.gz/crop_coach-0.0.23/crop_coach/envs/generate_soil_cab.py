import os


def generate_soil_header():
    return """** $Id: ec4.new 1.2 1997/09/18 17:33:54 LEM release $\n**\n** SOIL DATA FILE for use with WOFOST Version 5.0, June 1990\n**\n** EC-4 fine\n\nSOLNAM='EC4-fine'"""



def generate_soil_fpart(water_retention_dict):
    return f"""** physical soil characteristics\n\n** soil water retention\nSMTAB    =  {water_retention_dict["SMTB_list"][0]},   {water_retention_dict["SMTB_list"][1]},    ! vol. soil moisture content
            {water_retention_dict["SMTB_list"][2]},   {water_retention_dict["SMTB_list"][3]},    ! as function of pF [log (cm); cm3 cm-3]
            {water_retention_dict["SMTB_list"][4]},   {water_retention_dict["SMTB_list"][5]},
            {water_retention_dict["SMTB_list"][6]},  {water_retention_dict["SMTB_list"][7]},
            {water_retention_dict["SMTB_list"][8]},   {water_retention_dict["SMTB_list"][9]},
            {water_retention_dict["SMTB_list"][10]},   {water_retention_dict["SMTB_list"][11]},
            {water_retention_dict["SMTB_list"][12]},   {water_retention_dict["SMTB_list"][13]},
            {water_retention_dict["SMTB_list"][14]},   {water_retention_dict["SMTB_list"][15]},
            {water_retention_dict["SMTB_list"][16]},   {water_retention_dict["SMTB_list"][17]},
            {water_retention_dict["SMTB_list"][18]},   {water_retention_dict["SMTB_list"][19]}\nSMW     =   {water_retention_dict["SMW"]}  !  soil moisture content at wilting point [cm3/cm3]\nSMFCF    =   {water_retention_dict["SMFCF"]}  !  soil moisture content at field capacity [cm3/cm3]\nSM0      =   {water_retention_dict["SM0"]}  !  soil moisture content at saturation [cm3/cm3]\nCRAIRC   =   {water_retention_dict["CRAIRC"]}  ! critical soil air content for aeration [cm3/cm3]"""

def generate_soil_spart(hydraulic_conductivity_dict):
    return f"""** hydraulic conductivity\nCONTAB    =  {hydraulic_conductivity_dict["CONTAB_list"][0]},   {hydraulic_conductivity_dict["CONTAB_list"][1]},    ! 10-log hydraulic conductivity
            {hydraulic_conductivity_dict["CONTAB_list"][2]},   {hydraulic_conductivity_dict["CONTAB_list"][3]},    ! as function of pF [log (cm); cm3 cm-3]
            {hydraulic_conductivity_dict["CONTAB_list"][4]},   {hydraulic_conductivity_dict["CONTAB_list"][5]},
            {hydraulic_conductivity_dict["CONTAB_list"][6]},  {hydraulic_conductivity_dict["CONTAB_list"][7]},
            {hydraulic_conductivity_dict["CONTAB_list"][8]},   {hydraulic_conductivity_dict["CONTAB_list"][9]},
            {hydraulic_conductivity_dict["CONTAB_list"][10]},   {hydraulic_conductivity_dict["CONTAB_list"][11]},
            {hydraulic_conductivity_dict["CONTAB_list"][12]},   {hydraulic_conductivity_dict["CONTAB_list"][13]},
            {hydraulic_conductivity_dict["CONTAB_list"][14]},   {hydraulic_conductivity_dict["CONTAB_list"][15]},
            {hydraulic_conductivity_dict["CONTAB_list"][16]},   {hydraulic_conductivity_dict["CONTAB_list"][17]},
            {hydraulic_conductivity_dict["CONTAB_list"][18]},   {hydraulic_conductivity_dict["CONTAB_list"][19]},
            {hydraulic_conductivity_dict["CONTAB_list"][20]},   {hydraulic_conductivity_dict["CONTAB_list"][21]},
            {hydraulic_conductivity_dict["CONTAB_list"][22]},   {hydraulic_conductivity_dict["CONTAB_list"][23]},
            {hydraulic_conductivity_dict["CONTAB_list"][24]},   {hydraulic_conductivity_dict["CONTAB_list"][25]}\n\nRDMSOL = {hydraulic_conductivity_dict["RDMSOL"]}       ! soil maximum rootable depth\nK0       =  {hydraulic_conductivity_dict["K0"]}  ! hydraulic conductivity of saturated soil [cm day-1]\nSOPE     =   {hydraulic_conductivity_dict["SOPE"]}   ! maximum percolation rate root zone[cm day-1]\nKSUB     =   {hydraulic_conductivity_dict["KSUB"]}   ! maximum percolation rate subsoil [cm day-1]"""

def generate_soil_cpart(workability_parameters_dict):
    return f"""** soil workability parameters\nSPADS    =   {workability_parameters_dict["SPADS"]}  !  1st topsoil seepage parameter deep seedbed\nSPODS    =   {workability_parameters_dict["SPODS"]}  !  2nd topsoil seepage parameter deep seedbed\nSPASS    =   {workability_parameters_dict["SPASS"]}  !  1st topsoil seepage parameter shallow seedbed\nSPOSS    =   {workability_parameters_dict["SPOSS"]}  !  2nd topsoil seepage parameter shallow seedbed\nDEFLIM   =  {workability_parameters_dict["DEFLIM"]}  !  required moisture deficit deep seedbed"""



# generate_soil_cab that uses all functions above to generate the soil cab file
def generate_soil_cab(water_retention_dict, hydraulic_conductivity_dict, workability_parameters_dict):
    # get the current file dir
    dir_to_save = os.path.join(os.path.dirname(__file__), "step_data", "step_soil.cab")
    # create a dir
    step_data = os.path.join(os.path.dirname(__file__), "step_data")
    if not os.path.exists(step_data):
        os.makedirs(step_data)
    with open(dir_to_save, "w") as f:
        f.write(generate_soil_header())
        f.write("\n\n")
        f.write(generate_soil_fpart(water_retention_dict))
        f.write("\n\n")
        f.write(generate_soil_spart(hydraulic_conductivity_dict))
        f.write("\n\n")
        f.write(generate_soil_cpart(workability_parameters_dict))
    return dir_to_save

# Remove a file
def remove_file():
    dir_to_save = os.path.join(os.path.dirname(__file__), "step_data", "step_soil.cab")
    os.remove(dir_to_save)


# test in main :
if __name__ == "__main__":


    water_retention_dict = {
        "SMTB_list": [-1.000, 0.570, 1.000, 0.533,1.300,   0.524,1.491, 0.515,2.000, 0.486,2.400, 0.451,2.700,   0.420,3.400, 0.350,4.204, 0.300, 6.000, 0.270],
        "SMW": 0.300,
        "SMFCF": 0.460,
        "SM0": 0.570,
        "CRAIRC": 0.050
    }

    hydraulic_conductivity_dict = {
        "CONTAB_list": [1.000,  -0.824, 1.300,  -1.155,1.491,  -1.398,1.700,  -1.523, 2.000,  -1.959, 2.400,  -2.495, 2.700,  -2.886, 3.000,  -3.276, 3.400,  -3.770, 3.700,  -4.131, 4.000,  -4.481, 4.204,  -4.745, 3.700,  -4.131, 4.000,  -4.481, 4.204,  -4.745],
        "RDMSOL": 120.,
        "K0": 10.789,
        "SOPE": 0.55,
        "KSUB": 0.37
    }


    workability_parameters_dict = {
        "SPADS"    :   0.050,
        "SPODS"    :   0.025,
        "SPASS"    :   0.100,
        "SPOSS"    :   0.040,
        "DEFLIM"   :  -0.300,
    }

    generate_soil_cab(water_retention_dict, hydraulic_conductivity_dict, workability_parameters_dict)

