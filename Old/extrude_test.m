      q = linspace(0,2*pi,33);
      base = 0.2*[cos(q); sin(q)];   % Base curve is a circle (radius = 1)
      q = linspace(0,2*pi,101);
      traj = 5*[cos(q); sin(q); 0*q]; %Trajectory is a circle (radius = 5)

      [X,Y,Z] = extrude(base,test);
      figure; surf(X,Y,Z); axis equal;