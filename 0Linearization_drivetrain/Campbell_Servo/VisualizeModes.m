%Script for visualizing mode shapes from linearization in OpenFAST. 

%Based on the following description: https://github.com/OpenFAST/r-test/blob/main/glue-codes/openfast/5MW_Land_ModeShapes/vtk-visualization.md
%And example: https://github.com/OpenFAST/r-test/tree/main/glue-codes/openfast/5MW_Land_ModeShapes

%% run OpenFAST (saves checkpoint file)
% system([ openFASTexe ' ' RootName 'fst']);
% I typically do this manually in the command window


%% after running OpenFAST linearization
%addpath( genpath('C:\matlabPackages\matlab-toolbox') )
clc

RootNames = {'ws00.0.', 'ws04.0.', 'ws07.0.', 'ws10.0.', 'ws14.0.', 'ws20.0.'};
nModes = 13; %Drivetrain torsion not included in visualization
%%
for iRoot = 1:length(RootNames)
    RootName = RootNames{iRoot};
    if strcmp(RootName,'ws20.0.')
        LinFileNames = strcat( RootName, strrep( cellstr(num2str( (1:36)' )), ' ', ''), '.lin' );
    else
        LinFileNames = strcat( RootName, strrep( cellstr(num2str( (1:1)' )), ' ', ''), '.lin' );
    end
    ModesVizNameBase = 'EigenvectorsForModeShapeVTK.bin';
    ModesVizName = strcat( RootName, '_', ModesVizNameBase);

    [MBC] = fx_mbc3( LinFileNames, ModesVizName ); 
    disp(LinFileNames)
end

%% restart OpenFAST to generate vtk/.vtp files
% system([ openFASTexe ' -VTKLin ElastoDyn-Modes_ws00.0.viz']); Remember to use the
% correct windspeed
% Remember to check ElastoDyn-Modes.viz that the right checkpoint file is
% used. 
% I typically do this manually in the command window

%% after running plotModeShapes.py
% convert avi to gif files and fix issue with pvpython not saving th
% correct frame rate in the avi file (was an issue in 5.5, but appears to be
% fixed in 5.7)
RootNames = {'ws04.0.', 'ws07.0.', 'ws10.0.', 'ws14.0.', 'ws20.0.'};
for i=1:nModes
    for iRoot = 1:length(RootNames)
        RootName = RootNames{iRoot};
        fileName = [RootName 'Mode' num2str(i) ];
        avi2gif( [fileName '.avi'], [fileName '.gif'], 1, 30 );
    end
end