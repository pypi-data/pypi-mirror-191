from profiles import profiles

# o=======================================================o
#                        Functions                     
# o=======================================================o
        
def overwrite_settings(data_dic) -> dict:
    """
    Collects the settings from profiles.py and overwrites the settings found in the excel file
    Input: 
        data_dic = dictionary with the data from the excel file
    Output: 
        data_dic = dictionary with more settings obtained from the chosen profile
    """
    profile_dic = profiles[data_dic["profile"]] # importing from profiles.py
    
    # Merging the two dictionaries. Note: the data dic contains the most up-to-date settings
    # Thus, the profile_dic is overwritten by the data_dic
    profile_dic = profile_dic | data_dic
    # [print(f"{key} - {value}") for key, value in profile_dic.items()]
    
    return profile_dic        

def assign_colour_to_pathways(profile_dic):
    """
    Loops over pathways found in the profile_dic and assigns a colour to each of them
    The colours are defined in the profiles.py with the associated profile
    """
    if len(profile_dic["colour_list"]) < len(profile_dic["paths"]):
        raise IndexError(f"Error: not enough colours defined in profile: {profile_dic['profile']}")
    
    for i,path in enumerate(profile_dic["paths"]):
        path.add_colour(profile_dic["colour_list"][i])
    
def make_links(paths):
    for path in paths:
        for i,state in enumerate(path.states):
            state.linksTo = path.states[i+1].label if i < len(path.states)-1 else None      
    
def make_inputfile(output_path, dic):
    """
    Makes the input file for the energyleveler.py script
    All the information should be present in the dic (dictionary)
    This is the merged dictionary with the data from the excel file and the specified profile
    """
    outfile = f"{output_path}/{dic['outputfile']}.inp"
    with open(outfile, 'w') as output:
        output.write(f"output-file     = {dic['outputfile']}.png"
        f"\nwidth           = {dic['width']}"
        f"\nheight          = {dic['height']}"
        f"\nenergy-units    = {dic['energy_unit'].replace('XXX', dic['energy_type'])}"
        f"\nenergy range    = {dic['energy_range'][0]},{dic['energy_range'][1]}"
        f"\nfont size       = {dic['font_size']}"           
        f"\nfont            = {dic['font_family']}"  
        
        "\n\n#   This is a comment. Lines that begin with a # are ignored."
        "\n#   Available colours are those accepted by matplotlib "
        "\n\n#   Now begins the states input")
        
        for i,path in enumerate(dic["paths"]):
            output.write(f"\n\n#-------  Path {i+1}: {path.name} ----------\n")         
            for j,state in enumerate(path.states):
                output.write("\n{") 
                output.write(f"\n\ttext-colour = {path.colour}")
                output.write(f"\n\tname        = {state.label}")
                output.write(f"\n\tcolumn      = {j+1}")
                output.write(f"\n\tenergy      = {float(state.energy) :2.1f}")
                output.write(f"\n\tlabelColour = {path.colour}")
                
                # conditional prints
                if i==0: 
                    output.write(f"\n\tlabel       = {state.label.split('_')[1]}")
                    
                if j==0: 
                    output.write(f"\n\tlegend       = {path.name}")
                    
                if dic["hide_energy"] == True:
                    output.write("\n\tHIDE ENERGY")
                    
                if state.linksTo != None:
                    output.write(f"\n\tlinksto     = {state.linksTo}:{path.colour}")
                    
                output.write("\n}\n")    
        return outfile
                     
                     
    
