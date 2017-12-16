clear all, clc

number_of_files = 17;
figure(1), clf(1), hold on
for k = 1:number_of_files
  myfilename = sprintf('output/csv/1_%d.txt', k);
  data = importdata(myfilename);
  plot3(data(:,1),data(:,2),data(:,3))
end
hold off

textFiles = dir('*.txt'); 
numfiles = length(textFiles);

figure(2), clf(2), hold on
for k = 1:numfiles 
  data = importdata(textFiles(k).name); 
  plot3(data(:,1),data(:,2),data(:,3))
end