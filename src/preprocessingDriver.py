#modules from this thing needed to work...
import geomAnalyzer
import NICSInp
import readFile

import os
import argparse #used for parsing commandline arguments

orcaBqSymbol = 'DA'
gaussianBqSymbol = 'Bq'


def prepare_nics_1_calc(xyzInputFn, xyzOutputFn,bqSymbol=gaussianBqSymbol):
    #read xyz file
    atomList, geomList = readFile.read_xyz(xyzInputFn)
    conMatrix, bndAtom = geomAnalyzer.get_connectivity(geomList)
    spBqList = []
    #find all monocycles
    spMonoCycles = geomAnalyzer.find_monocycle(bndAtom)
    for cpCycle in spMonoCycles:
        #use 1.0 as height, this is assuming we only want
        #to do nics(1)zz calculations for now
        bq1x, bq1y, bq1z, bq2x, bq2y, bq2z = NICSInp.calCoor(cpCycle, 1.0, geomList)
        spBqList.append(['Bq', bq1x, bq1y, bq1z])
        spBqList.append(['Bq', bq2x, bq2y, bq2z])
    #write xyz file (need to write this one meself)
    write_xyz_file(geomList,spBqList,xyzOutputFn,bqSymbol)

def write_xyz_file(geomList,spBqList,xyzFilename,bqSymbol=gaussianBqSymbol):
    numAtoms = len(geomList) + len(spBqList)
    with open (xyzFilename,'w') as xyzFile:
        xyzFile.write(f'{numAtoms}\n')
        xyzFile.write('\n')
        for geomRou in geomList:
            xyzFile.write(f'{geomRou[0]}  {geomRou[1]:.6f}  {geomRou[2]:.6f}  {geomRou[3]:.6f}\n')
        for bqSpAtm in spBqList:			
            xyzFile.write(f'{bqSymbol}  {bqSpAtm[1]:.6f}  {bqSpAtm[2]:.6f}  {bqSpAtm[3]:.6f}\n')
        xyzFile.write('\n')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple driver program for NICS preprocessing")
    parser.add_argument("input_file", type=str, help="Path to the input .xyz file")  # Positional argument
    parser.add_argument("-o", "--output", type=str, default="NICS.xyz", help="Path to the output .xyz file")  # Optional argument
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")  # Flag (True/False)
    parser.add_argument("-p", "--program" , type=str, default="Gaussian", help="Program to use dummy atom syntax for (options are ORCA or Gaussian {default})")

    args = parser.parse_args()

    inputFile = args.input_file
    outputFile = args.output
    program = args.program
    verbose = args.verbose

    if program.lower() == 'gaussian':
        bqSymbol = gaussianBqSymbol
    elif program.lower() == 'orca':
        bqSymbol = orcaBqSymbol
    else:
        raise ValueError("unsupported job type")

    if verbose:
        print(f"input file path: {os.path.abspath(inputFile)}")
        print(f"output file path: {os.path.abspath(outputFile)}")
        
    if not os.path.exists(inputFile):
        raise ValueError("input file does not exist")
    
    prepare_nics_1_calc(inputFile,outputFile,bqSymbol)

    if not os.path.exists(outputFile):
        raise RuntimeError("Failed to write output file")

    print("pyAroma terminated normally.")
    


    

    
