""" 
Example script to create a Campbell diagram with OpenFAST

Adapted from:
    https://github.com/OpenFAST/python-toolbox/blob/dev/pyFAST/linearization/examples/runCampbell.py

"""

import numpy as np
import pandas as pd
import os
import pyFAST.linearization.linearization as lin
import pyFAST.case_generation.runner as runner
import pyFAST.linearization.campbell as cmb

import matplotlib.pyplot as plt
from pyFAST.input_output import FASTInputDeck

if __name__=='__main__':

    # --- Parameters to generate linearization input files
    simulationFolder    = r'Campbell_Servo'  # Output folder for input files and linearization (will be created)
    templateFstFile     = r'Template_Servo\DTU_10MW_RWT.fst'  # Main file, used as a template
    operatingPointsFile = r'LinearizationPoints_Servo.csv'
    nPerPeriod       = 36   # Number of linearization per revolution

    # Main flags
    writeFSTfiles = True # Write OpenFAST input files based on template and operatingPointsFile
    runFast       = True # Run OpenFAST
    postproLin    = True # Postprocess the linearization outputs (*.lin)

    # --- Parameters to run OpenFAST
    fastExe = r'openfast_x64.exe' # Path to a FAST exe (and dll) 

    # --- Step 1: Write OpenFAST inputs files for each operating points 

    #From Jason: trimGainGenTorque = 1.5*tipradius^3/GBratio) and trimGainPitch = 0.1
    trimGainPitch = 0.0000001 #rad/(rad/s) for pitch 
    trimGainGenTorque = 200 #Nm/(rad/s) for torque 
    maxTrq = 199000.0000
    nPerPeriod = 36 #Usually 12 or 36
    tStart = 1000
    
    dt = 0.01
    baseDict={
            'CompAero': 2,
            'DT': dt, 
            'DT_OUT': dt, 
            'WrVTK': 3,
            'VTK_type': 1,
            'VTK_fields': True,
            'VTK_fps': 30,
            'EDFile|DT': dt,
            'ServoFile|DT': dt,
            'ServoFile|PCMode': 0,
            'ServoFile|VSContrl': 1, #Simple variable-speed generator
            'ServoFile|VS_RtGnSp': 480, #Rated generator speed (HSS) rpm
            'ServoFile|VS_RtTq': 200000, #Rated generator torque (HSS) Nm
            # 'ServoFile|VS_RtTq': 198943.6872, #Rated generator torque (HSS) Nm
            'ServoFile|VS_Rgn2K': 0.212, #Generator torque constant in Region 2 (HSS) N-m/rpm^2
            'ServoFile|VS_SlPc': 1, #Rated generator slip percentage in Region 2 1/2 for simple variable-speed generator control (%)
            
            } 
    FSTfilenames= lin.writeLinearizationFiles(templateFstFile, simulationFolder, operatingPointsFile, nPerPeriod=nPerPeriod, baseDict=baseDict, 
                                              tStart = tStart, trim=True, viz=False, 
                                              trimGainPitch = trimGainPitch, trimGainGenTorque = trimGainGenTorque, maxTrq= maxTrq, 
                                              LinInputs=1, LinOutputs=1)

    #Update file with 0 wind speed    
    for filepath in FSTfilenames: 
        if 'ws00.0' in filepath:
            deck = FASTInputDeck(filepath, ['ED'])
            fst = deck.fst
            ED  = deck.fst_vt['ElastoDyn'] 
            fst['CompServo'] = 0
            ED['GenDOF'] = False
            fst.write()
            ED.write()
        elif 'ws14.0' in filepath or 'ws20.0' in filepath:
            deck = FASTInputDeck(filepath, ['SrvD'])
            fst = deck.fst
            SD  = deck.fst_vt['ServoDyn']
            SD['VS_Rgn2K'] = 0.00001
            SD['VS_SlPc'] = 0.00001
            SD.write()
            

    print('Setting CompServo = 0 and GenDOF = False for ws = 0.0 m/s')
    

    # Create a batch script (optional)
    runner.writeBatch(os.path.join(simulationFolder,'_RUN_ALL.bat'), FSTfilenames, fastExe=fastExe)


    # --- Step 2: run OpenFAST 
    if runFast:
        runner.run_fastfiles(FSTfilenames, fastExe=fastExe, parallel=True, showOutputs=True, nCores=4)


    # --- Step 3: Run MBC, identify modes and generate XLS or CSV file
    if postproLin:
        OP, Freq, Damp, _, _, modeID_file = lin.postproCampbell(FSTfilenames)
        # Edit the modeID file manually to identify the modes
        print('[TODO] Edit this file manually: ',modeID_file)
        
    #%%
    import numpy as np
    import pandas as pd
    import os
    import pyFAST.linearization.linearization as lin
    import pyFAST.case_generation.runner as runner
    import pyFAST.linearization.campbell as cmb
    import matplotlib.pyplot as plt
    
    simulationFolder    = r'C:\OpenFAST_Workspace\DTU10MWRWT_FAST_v3.3.0\TestRuns\0Linearization\Campbell_Servo'  # Output folder for input files and linearization (will be created)
    # --- Step 4: Campbell diagram plot
    csvFile = os.path.join(simulationFolder, 'Campbell_ModesID_Manual.csv') # <<< TODO Change me if manual identification is done
    fig, axes, figName = cmb.plotCampbellDataFile(csvFile, ws_or_rpm='ws', ylim=[0,8])
    fig.savefig(figName+'.png')
    plt.show()