from paraview.simple import * #For this to work, add paraviews site-package/paraview to PYTHONPATH in environment variables. I removed it because it crashed some of my environments
import os 

"""Warning. Some of the animations just show blank animations. They still work when loading the state in the GUI in Paraview.
But perhaps this script is just tine consuming and useless at the moment"""

mainDirName =  os.getcwd() + '\\Campbell_Servo\\vtk\\'
fileRootFmt = 'ws{ws}.Mode{mode:d}.' # keep the format specifier {:d} for the mode number
#%%
wsLst = ['00.0', '04.0', '07.0', '10.0', '14.0', '20.0']


nModes = 13  # number of modes to visualize
fps = 30 # frames per second (rate to save in the .avi file)

StructureModule = 'ED'
BladeMesh = "AD_Blade"

for ws in wsLst:
    if ws == '00.0':
        pass #Haven't gotten the correct pvsm-format for 0.00 yet (varies between 0.0001 and 0.001)
    else: 
        print('')
        print(ws)
        print('')
        for iMode in range(nModes):  # iMode starts at 0, so add 1
           #fileRootName = fileRoot + str(iMode+1) + '.LinTime1.' #.LinTime1 depends on visualization options
           fileRootName = fileRootFmt.format(ws = ws, mode = iMode+1)
           print('***' + fileRootName + '***')
           print(fileRootName + 'avi')
           
           stateFile = 'ED_Surfaces_ws{ws}Mode{mode:d}.pvsm'
           
           # determine number of leading zeros in this mode shape
           nLeadingZeros = 0
           exists = False
           while (not exists) and nLeadingZeros < 6:
              nLeadingZeros = nLeadingZeros + 1
              txt = '{:0' + str(nLeadingZeros) + 'd}'
              fileLeadingZeros = txt.format(1)
              Blade1File = mainDirName + fileRootName + BladeMesh + '1.' + fileLeadingZeros + '.vtp'
              exists = os.path.isfile(Blade1File)
        
           if not exists:
              print('  Could not find files to load.')
           else:
              LoadState(stateFile.format(ws = ws, mode = iMode+1))
        
              #####
              SetActiveView(GetRenderView()) 
              view = GetActiveView() 
              # layout = GetLayout()
            
              # SaveAnimation(fileRootName + 'avi', viewOrLayout=layout, FrameRate=fps ) 
            
              SaveAnimation(fileRootName + 'avi', viewOrLayout=view, FrameRate=fps, ImageResolution=(1544,784) ) 
              # this .pvsm file defaults to (2734,1178) without ImageResolution arguments, resulting in a bunch of warnings
              # For some reason, ParaView is ignoring the FrameRate argument and always uses a value of 1.
            
              print('  Saved animation file.')


