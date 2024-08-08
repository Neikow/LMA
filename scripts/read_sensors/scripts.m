ccc

load 'C:\Users\Vitaly\OneDrive\Bureau\LMA\results\simulated_dam_flat\traces\EE';

%% plot capteur n°
icap = 100;
plot(capteur(icap).Time,capteur(icap).Displ')

%% plot capteurs dans l'espace
for icap = 1 : numel(capteur)
    pos(icap,:) = capteur(icap).Pos;
end

figure
scatter3(pos(2:end,1),pos(2:end,2),pos(2:end,3))

%% plot FFT capteur n°
sq = fft(capteur(50).Displ,[],2)./fft(capteur(1).Displ,[],2);
plot(sq')