% Deep Learning for Computer Vision using MATLAB
% This is the MATLAB side of my Python cyber vision project.
% Put image folders as:
% dataset/neon_square, dataset/pulse_ring, dataset/diagonal_strike

clear; clc; close all;

imageSize = [40 40 3];
dataFolder = fullfile(pwd, "dataset");

imds = imageDatastore(dataFolder, ...
    "IncludeSubfolders", true, ...
    "LabelSource", "foldernames");

[trainDs, testDs] = splitEachLabel(imds, 0.75, "randomized");

layers = [
    imageInputLayer(imageSize, "Name", "input")
    convolution2dLayer(3, 16, "Padding", "same", "Name", "conv_1")
    batchNormalizationLayer("Name", "bn_1")
    reluLayer("Name", "relu_1")
    maxPooling2dLayer(2, "Stride", 2, "Name", "pool_1")
    convolution2dLayer(3, 32, "Padding", "same", "Name", "conv_2")
    batchNormalizationLayer("Name", "bn_2")
    reluLayer("Name", "relu_2")
    maxPooling2dLayer(2, "Stride", 2, "Name", "pool_2")
    fullyConnectedLayer(64, "Name", "dense")
    reluLayer("Name", "relu_dense")
    dropoutLayer(0.25, "Name", "dropout")
    fullyConnectedLayer(numel(categories(imds.Labels)), "Name", "class_head")
    softmaxLayer("Name", "softmax")
    classificationLayer("Name", "output")
];

options = trainingOptions("adam", ...
    "InitialLearnRate", 1e-3, ...
    "MaxEpochs", 12, ...
    "MiniBatchSize", 32, ...
    "Shuffle", "every-epoch", ...
    "ValidationData", testDs, ...
    "Verbose", false, ...
    "Plots", "training-progress");

net = trainNetwork(trainDs, layers, options);
predicted = classify(net, testDs);
accuracy = mean(predicted == testDs.Labels);

fprintf("Cyber Vision MATLAB accuracy: %.2f%%\n", accuracy * 100);
figure;
confusionchart(testDs.Labels, predicted);
title("Cyber Vision Confusion Matrix");
