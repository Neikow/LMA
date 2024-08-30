load 'C:\Users\Vitaly\OneDrive\Bureau\LMA\results\21_08_dam_no_topo_big_domain\traces\EE';

Ncap = numel(capteur);

%% plot capteur n°
icap = 1000;
% plot(capteur(icap).Time,capteur(icap).Displ')

source(1,:) = tukeywin(size(capteur(1).Time, 2), 0.5)' .* capteur(1).Displ(1,:);
source(2,:) = tukeywin(size(capteur(1).Time, 2), 0.5)' .* capteur(1).Displ(2,:);
source(3,:) = tukeywin(size(capteur(1).Time, 2), 0.5)' .* capteur(1).Displ(3,:);


transformed(1,:) = tukeywin(size(capteur(icap).Time, 2), 0.5)' .* capteur(icap).Displ(1,:);
transformed(2,:) = tukeywin(size(capteur(icap).Time, 2), 0.5)' .* capteur(icap).Displ(2,:);
transformed(3,:) = tukeywin(size(capteur(icap).Time, 2), 0.5)' .* capteur(icap).Displ(3,:);

% hold on;
% plot(capteur(icap).Time,transformed)

%% plot capteurs dans l'espace
for i = 1 : Ncap
    pos(i,:) = capteur(i).Pos;

    if i == icap
        s(i) = 50;
    else
        s(i) = 10;
    end
end

for i = 1 : Ncap
    C(i,:) = [i / Ncap, 1 1];
end

C = hsv2rgb(C);

M = mean([pos(2:end,1), pos(2:end,3), pos(2:end,2)]);

figure(1);
hold on;
grid on;
axis equal;
scatter3(pos(2:end,1), pos(2:end,3), pos(2:end,2), s(2:end), C(2:end,:));
view(45, 25);
zlim([M(3) - 80 M(3) + 50]);
ylim([M(2) - 60 M(2) + 60]);
xlim([M(1) - 125 M(1) + 125]);

%% plot FFT capteur n° (1)

figure(1);
hold on;
cla;

pab = size(source, 2);

st = 4;

w = linspace(0, 1 / mean(diff(capteur(icap).Time)) / st, pab);

sq = fft(transformed(:,1:st:end), pab, 2) ./ fft(source(:,1:st:end), pab, 2);
plot(w, abs(sq)')

title('Displacement Response');
xlabel('Frequency (Hz)');
ylabel('|fft(Displacement)|');
legend('X (Lateral)', 'Y (Vertical)', 'Z (Depth)');
xlim([0.5 25])

%% plot FFT capteur n° (2)

figure(1);
hold on;

msk = w < 25;
max_H = max(sq(:,msk));

plot(w, 20 * log10(abs(sq') / max(max_H)))

title('Displacement Response');
xlabel('Frequency (Hz)');
ylabel('|fft(Displacement)|');
legend('X (Lateral)', 'Y (Vertical)', 'Z (Depth)');
xlim([0.5 25])

%% plot multiple

figure(1);
hold on;
cla;

pab = size(source, 2);
st = 4;
N = 200;

indexes = round(size(capteur, 2) .* rand(N, 1));

ffts = fft(source(:,1:st:end), pab, 2);

for i = 1 : numel(indexes)
    idx = indexes(i);
    dx = tukeywin(size(capteur(idx).Time, 2), 0.5)' .* capteur(idx).Displ(1,:);
    dy = tukeywin(size(capteur(idx).Time, 2), 0.5)' .* capteur(idx).Displ(2,:);
    dz = tukeywin(size(capteur(idx).Time, 2), 0.5)' .* capteur(idx).Displ(3,:);

    sqx = fft(dx(1:st:end), pab, 2) / ffts(1);
    sqy = fft(dy(1:st:end), pab, 2) / ffts(2);
    sqz = fft(dz(1:st:end), pab, 2) / ffts(3);

    % plot(w, abs(sqx)', 'red')
    % plot(w, abs(sqy)', 'green')
    % plot(w, abs(sqz)', 'blue')

    [pktx,lctx] = findpeaks(abs(sqx),w);
    [pkty,lcty] = findpeaks(abs(sqy),w);
    [pktz,lctz] = findpeaks(abs(sqz),w);

    scatter(lctx, pktx, 'or');
    scatter(lcty, pkty, 'og');
    scatter(lctz, pktz, 'ob');
end

title('Displacement Response');
xlabel('Frequency (Hz)');
ylabel('|fft(Displacement)|');
legend('X (Lateral)', 'Y (Vertical)', 'Z (Depth)');
xlim([0.5 25])
