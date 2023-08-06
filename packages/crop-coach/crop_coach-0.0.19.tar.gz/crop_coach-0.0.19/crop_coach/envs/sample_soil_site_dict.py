import random, time


def sample_water_retention_dict():
    random.seed(time.time())
    # SMW intervale : soil moisture content at wilting point [cm3/cm3]
    SMW = random.uniform(0.1, 0.5)
    # SMFCF intervale : soil moisture content at field capacity [cm3/cm3]
    SMFCF = random.uniform(0., 0.3)
    # SM0 intervale : soil moisture content at saturation [cm3/cm3]
    SM0 = random.uniform(0.1, 0.2)
    # CRAIRC intervale : crop root area index reduction coefficient
    CRAIRC = random.uniform(0.01, 0.1)

    # SMTB_list intervale :
    SMTB_list = []
    for i in range(20):
        SMTB_list.append(random.uniform(0.1, 0.9))

    # create water_retention_dict :
    return {
        "SMTB_list": SMTB_list,
        "SMW": SMW,
        "SMFCF": SMFCF,
        "SM0": SM0,
        "CRAIRC": CRAIRC
    }




def sample_hydraulic_conductivity_dict():

    random.seed(time.time())
    # CONTAB_list intervale :
    CONTAB_list = []
    for i in range(10):
        CONTAB_list.append(random.uniform(0.1, 0.9))

    # RDMSOL intervale :
    RDMSOL = random.uniform(0.1, 0.9)

    # K0 intervale :
    K_0 = random.uniform(0.1, 0.9)

    # SOPE intervale :
    SOPE = random.uniform(0.1, 0.9)

    # KSUB intervale :
    KSUB = random.uniform(0.1, 0.9)

    # create hydraulic_conductivity_dict :
    hydraulic_conductivity_dict = {
        "CONTAB_list": CONTAB_list,
        "RDMSOL": RDMSOL,
        "K0": K_0,
        "SOPE": SOPE,
        "KSUB": KSUB
    }

    return hydraulic_conductivity_dict


def sample_workability_parameters_dict():
    """
    "SPADS"    :   0.050,
        "SPODS"    :   0.025,
        "SPASS"    :   0.100,
        "SPOSS"    :   0.040,
        "DEFLIM"   :  -0.300,
    }
    """
    random.seed(time.time())
    # SPADS intervale :
    SPADS = random.uniform(0.01, 0.1)
    # SPODS intervale :
    SPODS = random.uniform(0.01, 0.1)
    # SPASS intervale :
    SPASS = random.uniform(0.01, 0.1)
    # SPOSS intervale :
    SPOSS = random.uniform(0.01, 0.1)
    # DEFLIM intervale :
    DEFLIM = random.uniform(0.01, 0.1)

    # create workability_parameters_dict :
    workability_parameters_dict = {
        "SPADS": SPADS,
        "SPODS": SPODS,
        "SPASS": SPASS,
        "SPOSS": SPOSS,
        "DEFLIM": DEFLIM
    }

    return workability_parameters_dict



def sample_soil_dict():
    return {

        "water_retention_dict": sample_water_retention_dict(),
        "hydraulic_conductivity_dict": sample_hydraulic_conductivity_dict(),
        "workability_parameters_dict": sample_workability_parameters_dict()
        }




def sample_gene_site_dict():
    random.seed(time.time())
    # SMLIM intervale :
    SMLIM = random.uniform(0.01, 0.1)
    # IFUNRN intervale :
    IFUNRN = random.uniform(0.01, 0.1)
    # SSMAX intervale :
    SSMAX = random.uniform(0.01, 0.1)
    # SSI intervale :
    SSI = random.uniform(0.01, 0.1)
    # WAV intervale :
    WAV = random.uniform(0.01, 0.1)
    # NOTINF intervale :
    NOTINF = random.uniform(0.01, 0.1)

    # create gene_site_dict :
    return {
        "SMLIM": SMLIM,
        "IFUNRN": IFUNRN,
        "SSMAX": SSMAX,
        "SSI": SSI,
        "WAV": WAV,
        "NOTINF": NOTINF
    }


def sample_n_site_dict():

    random.seed(time.time())
    # BG_N_SUPPLY intervale :
    BG_N_SUPPLY = random.uniform(0.01, 0.1)
    # NSOILBASE intervale :
    NSOILBASE = random.uniform(0.01, 0.1)
    # NSOILBASE_FR intervale :
    NSOILBASE_FR = random.uniform(0.01, 0.1)

    # create n_site_dict :
    return {
        "BG_N_SUPPLY": BG_N_SUPPLY,
        "NSOILBASE": NSOILBASE,
        "NSOILBASE_FR": NSOILBASE_FR
    }

def sample_p_site_dict():

    random.seed(time.time())
    # BG_P_SUPPLY intervale :
    BG_P_SUPPLY = random.uniform(0.01, 0.1)
    # PSOILBASE intervale :
    PSOILBASE = random.uniform(0.01, 0.1)
    # PSOILBASE_FR intervale :
    PSOILBASE_FR = random.uniform(0.01, 0.1)

    # create p_site_dict :
    return {
        "BG_P_SUPPLY": BG_P_SUPPLY,
        "PSOILBASE": PSOILBASE,
        "PSOILBASE_FR": PSOILBASE_FR
    }


def sample_k_site_dict():

    random.seed(time.time())
    # BG_K_SUPPLY intervale :
    BG_K_SUPPLY = random.uniform(0.01, 0.1)
    # KSOILBASE intervale :
    KSOILBASE = random.uniform(0.01, 0.1)
    # KSOILBASE_FR intervale :
    KSOILBASE_FR = random.uniform(0.01, 0.1)

    # create k_site_dict :
    return {
        "BG_K_SUPPLY": BG_K_SUPPLY,
        "KSOILBASE": KSOILBASE,
        "KSOILBASE_FR": KSOILBASE_FR
    }

def sample_site_dict():
    return {
        "gene_site_dict": sample_gene_site_dict(),
        "n_site_dict": sample_n_site_dict(),
        "p_site_dict": sample_p_site_dict(),
        "k_site_dict": sample_k_site_dict()
    }
    