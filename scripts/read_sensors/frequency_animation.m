figure(1);
hold on;
pause on;
axis equal;
cla;

pab = size(source, 2);
st = 4;
Ncap = numel(capteur);

nframes = 40;

w = linspace(0, 1 / mean(diff(capteur(icap).Time)) / st, pab);

ffts = fft(source(:,1:st:end), pab, 2);

% select frequency
f = 10.2;

normalize = 1 / 10;


filename = sprintf('animation_f_%.2f.gif', f);

for i = 1 : Ncap
    dx = tukeywin(size(capteur(i).Time, 2), 0.5)' .* capteur(i).Displ(1,:);
    dy = tukeywin(size(capteur(i).Time, 2), 0.5)' .* capteur(i).Displ(2,:);
    dz = tukeywin(size(capteur(i).Time, 2), 0.5)' .* capteur(i).Displ(3,:);

    % asqx(i,:) = abs(fft(dx(1:st:end), pab, 2) / ffts(1));
    % asqy(i,:) = abs(fft(dy(1:st:end), pab, 2) / ffts(2));
    % asqz(i,:) = abs(fft(dz(1:st:end), pab, 2) / ffts(3));

    asqx(i,:) = real(fft(dx(1:st:end), pab, 2) / ffts(1));
    asqy(i,:) = real(fft(dy(1:st:end), pab, 2) / ffts(2));
    asqz(i,:) = real(fft(dz(1:st:end), pab, 2) / ffts(3));


    Ax(i) = interp1(w, asqx(i,:), f);
    Ay(i) = interp1(w, asqy(i,:), f);
    Az(i) = interp1(w, asqz(i,:), f);
end

t = 0;
dt = 2 * pi / f / nframes;

for i = 1 : Ncap
    ipos(i,:) = capteur(i).Pos;
end

M = mean([ipos(2:end,1), ipos(2:end,3), ipos(2:end,2)]);

view(45, 25);


title(sprintf('Sensors position in time (f = %.2f Hz)', f))
xlabel('X Position (m)');
ylabel('Z Position (m)');
zlabel('Y Position (m)')

j = 1;

while 1
    cla;

    xlim([M(1) - 125 M(1) + 125]);
    ylim([M(2) - 60 M(2) + 60]);
    zlim([M(3) - 80 M(3) + 50]);
    
    for i = 1 : Ncap
        pos(i,:) = ipos(i,:) + normalize * [Ax(i), Ay(i), Az(i)] * cos(f * t);
    end

    scatter3(pos(2:end,1), pos(2:end,3), pos(2:end,2));

    drawnow

    frame = getframe(1);
    im = frame2im(frame);
    [imind,cm] = rgb2ind(im,256);
    if j <= nframes
        if j == 1
             imwrite(imind,cm,filename,'gif', 'Loopcount',inf,"DelayTime",dt);
        else
             imwrite(imind,cm,filename,'gif','WriteMode','append',"DelayTime",dt);
        end
    end

    t = t + dt;
    j = j + 1;
    pause(dt);
end