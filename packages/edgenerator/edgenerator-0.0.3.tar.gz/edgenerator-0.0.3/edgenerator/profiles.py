"""
This module contains profiles used for making energy diagrams.
"""

def get_profile(profile_name):
    """
    Returns a profile from the profiles dictionary.
    """
    return profiles[profile_name]

profiles = {
    "default": {
        "outputfile": "default_output", # name of output file
        "width" : 8, 
        "height": 8,
        "energy_type": 'G', # will be 'E', 'G' or 'H' from Excel file
        "energy_range": [-40,40],
        "energy_unit": "$\Delta \it{XXX}$  / kcal mol$^{-1}$", #XXX will be replaced'; please don't change 
        "font_size": 14,  
        "font_family": "arial", # "serif", "cursive", "fantasy", "monospace"
        "colour_list": ['black','blue','green','red'], # list of colours for pathways
        "hide_energy": True,   # display energy values or not in plot
        "normalise": [True, 1], # True/False and path number to normalise to; not used at the moment
        "delete_inputfile": True # delete input file after making diagram
    },

    "siebe": {
        "outputfile": "default_output", # name of output file
        "width" : 8, 
        "height": 8,
        "energy_type": 'G', # or 'G' or 'H'
        "energy_range": [-40,40],
        "energy_unit": "$\Delta \it{XXX}$  / kcal mol$^{-1}$",
        "font_size": 14,  
        "font_family": "monospace", # "serif", "cursive", "fantasy", "monospace"
        "colour_list": ['#000000','#0000FF','#008000','#FF0000', '#800080', 'yellow'], 
        "hide_energy": True,   
        "normalise": [True, 1],
        "delete_inputfile": True # delete input file after making diagram
    }
}