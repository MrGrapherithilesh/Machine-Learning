% Helper idea for MATLAB users:
% Generate small folders of synthetic images if you do not want to draw data manually.
% This is intentionally simple because the Python side already generates the real demo.

function makeSyntheticCyberDataset(outputFolder)
    if nargin == 0
        outputFolder = fullfile(pwd, "dataset");
    end

    labels = ["neon_square", "pulse_ring", "diagonal_strike"];
    for label = labels
        folder = fullfile(outputFolder, label);
        if ~exist(folder, "dir")
            mkdir(folder);
        end
    end

    disp("Use the Python generator for the full dataset:");
    disp("python -m vision_cyberlab.cli run --output outputs");
    disp("Then export images if required for MATLAB training.");
end
