import os
from .energy_leveler import ReadInput
from .read_excel import read_excelfile
from .prepare_input import overwrite_settings, assign_colour_to_pathways, make_links, make_inputfile

def run_edgenerator(excel_path, workdir_path):
    """
    Runs the program
    Arguments:
        Absolute path to the excel file
        Absolute path of the output folder
    Output:
        A png file (or pdf) with the energy diagram
    """

    print(f"\nReading Excel file (path {excel_path}...)")
    
    data_dic = read_excelfile(excel_path)
    
    print("Loading profile for profiles.py...")
    
    full_dic = overwrite_settings(data_dic)
    
    print("Making inputfile for energyleveler.py...")
      
    assign_colour_to_pathways(full_dic)
    make_links(full_dic["paths"])
    inputfile = make_inputfile(workdir_path, full_dic)
    
    print("Running energyleveler.py...\n")

    diagram = ReadInput(inputfile)
    diagram.MakeLeftRightPoints()
    diagram.Draw()
    if full_dic["delete_inputfile"] == True:
        print("Removing inputfile...")
        os.remove(inputfile)

    print("Finished!\n")
    
    print("o=======================================================o")
    print(f"{full_dic['outputfile']}.png is made in {workdir_path}!")
    print("o=======================================================o")
