import os

def generate_site_header():
  return """**\n** Site characteristics file for Running WOFOST N/P/K\n** Derived from management data file for use with LINTUL model (May 2011)\n**"""



def generate_site_fpart(gene_site_dict):
  return f"""SMLIM = {gene_site_dict["SMLIM"]}  ! Limiting amount of volumetric moisture in upper soil layer [-]\nIFUNRN = {gene_site_dict["IFUNRN"]}   ! Rain infiltration as function of storm size [0/1]\nSSMAX = {gene_site_dict["SSMAX"]}   ! Maximum surface storage [cm]\nSSI = {gene_site_dict["SSI"]}      ! Initial surface storage [cm]\nWAV = {gene_site_dict["WAV"]}     ! Initial amount of soil water [cm]\nNOTINF = {gene_site_dict["NOTINF"]}   ! Not infiltrating fraction of rainfall [0..1]"""



def generate_site_npart(n_site_dict):
  return f"""* Background supply of N [kg/ha/day]\nBG_N_SUPPLY = {n_site_dict["BG_N_SUPPLY"]}\n* Soil N mineralization\nNSOILBASE   = {n_site_dict["NSOILBASE"]}    ! total mineral soil N available at start of growth period [kg N/ha]\nNSOILBASE_FR  = {n_site_dict["NSOILBASE_FR"]}  ! fraction of soil mineral coming available per day [day-1]"""



def generate_site_ppart(p_site_dict):
  return f"""* Background supply of P [kg/ha/day]\nBG_P_SUPPLY = {p_site_dict["BG_P_SUPPLY"]}\n* Soil P mineralization\nPSOILBASE   = {p_site_dict["PSOILBASE"]}    ! total mineral soil N available at start of growth period [kg P/ha]\nPSOILBASE_FR  = {p_site_dict["PSOILBASE_FR"]}  ! fraction of soil mineral coming available per day [day-1]"""

def generate_site_kpart(k_site_dict):
  return f"""* Background supply of K [kg/ha/day]\nBG_K_SUPPLY = {k_site_dict["BG_K_SUPPLY"]}\n* Soil K mineralization\nKSOILBASE   = {k_site_dict["KSOILBASE"]}    ! total mineral soil N available at start of growth period [kg K/ha]\nKSOILBASE_FR  = {k_site_dict["KSOILBASE_FR"]}  ! fraction of soil mineral coming available per day [day-1]"""


def generate_site_cab(gene_site_dict, n_site_dict, p_site_dict, k_site_dict):
# get the current file dir
  dir_to_save = os.path.join(os.path.dirname(__file__), "step_data", "step_site.cab")
  # print(os.path.dirname(__file__))
  step_data = os.path.join(os.path.dirname(__file__), "step_data")
  if not os.path.exists(step_data):
      os.makedirs(step_data)
  with open(dir_to_save, "w") as f:
    f.write(generate_site_header())
    f.write("\n\n")
    f.write(generate_site_fpart(gene_site_dict))
    f.write("\n\n")
    f.write(generate_site_npart(n_site_dict))
    f.write("\n\n\n")
    f.write(generate_site_ppart(p_site_dict))
    f.write("\n\n\n")
    f.write(generate_site_kpart(k_site_dict))
    f.write("\n\n")
  return dir_to_save

# Remove a file
def remove_file():
    dir_to_save = os.path.join(os.path.dirname(__file__), "step_data", "step_site.cab")
    os.remove(dir_to_save)


if __name__ == "__main__":
  gene_site_dict = {
      "SMLIM": 0.5,
      "IFUNRN": 1,
      "SSMAX": 0.0,
      "SSI": 0.0,
      "WAV": 0.0,
      "NOTINF": 0.0
  }
  n_site_dict = {
      "BG_N_SUPPLY": 0.0,
      "NSOILBASE": 0.0,
      "NSOILBASE_FR": 0.0
  }
  p_site_dict = {
      "BG_P_SUPPLY": 0.0,
      "PSOILBASE": 0.0,
      "PSOILBASE_FR": 0.0
  }
  k_site_dict = {
      "BG_K_SUPPLY": 0.0,
      "KSOILBASE": 0.0,
      "KSOILBASE_FR": 0.0
  }
  generate_site_cab(gene_site_dict, n_site_dict, p_site_dict, k_site_dict)