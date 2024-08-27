figure(1);
hold on;
pause on;
axis equal;
cla;

st = 4;
Ncap = numel(capteur);

filename = 'animation_displacement.gif';

for i = 1 : Ncap
    ipos(i,:) = capteur(i).Pos;
end

M = mean([ipos(2:end,1), ipos(2:end,3), ipos(2:end,2)]);

view(45, 25);

xlabel('X Position (m)');
ylabel('Z Position (m)');
zlabel('Y Position (m)')

t = 0;
dt = 0.1;
nframes = max(capteur(i).Time) / dt;
step = floor(size(capteur(i).Time, 2) / nframes);

for i = 1 : Ncap
    max_displ(i,:) = max(capteur(i).Displ');
end

for j = 1 : step : size(capteur(i).Time, 2)
    cla;

    xlim([M(1) - 125 M(1) + 125]);
    ylim([M(2) - 60 M(2) + 60]);
    zlim([M(3) - 80 M(3) + 50]);
    
    for i = 1 : Ncap
        pos(i,:) = capteur(i).Pos + [30, 30, 30] .* capteur(i).Displ(j) ./ max_displ(i);
    end

    scatter3(pos(2:end,1), pos(2:end,3), pos(2:end,2));

    title(sprintf('Sensors position in time (t = %.2f s)', t))

    drawnow

    frame = getframe(1);
    im = frame2im(frame);
    [imind,cm] = rgb2ind(im,256);
    if j == 1
         imwrite(imind,cm,filename,'gif', 'Loopcount',inf,"DelayTime",dt);
    else
         imwrite(imind,cm,filename,'gif','WriteMode','append',"DelayTime",dt);
    end

    t = t + dt;
    pause(dt);
end