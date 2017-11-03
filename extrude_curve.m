%% Imports a layer of 3D part and extrudes along it
clear all, clc

q = linspace(0,2*pi,33);
base = 0.2*[cos(q); sin(q)];   % Base curve is a circle (radius = 0.2)

number_of_files = 17;
figure(1), clf(1), hold on
for k = 1:number_of_files
  myfilename = sprintf('1_%d.txt', k);
  exportname = sprintf('1_%d.stl', k);
  data = importdata(myfilename);
  [X,Y,Z] = extrude(base,data');
  surf(X,Y,Z)
  surf2stl(exportname,X,Y,Z)
end
hold off
