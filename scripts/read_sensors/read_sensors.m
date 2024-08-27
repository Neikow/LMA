close all
clear all
clc

% load the files...
folder = 'C:\Users\Vitaly\OneDrive\Bureau\LMA\results\21_08_dam_no_topo_big_domain\traces';
matname = 'EE';


files = dir([folder filesep 'capteurs*.h5']);

%% load the data
for ifile = 1 : numel(files)
    h5name = [files(ifile).folder filesep files(ifile).name];
    info = h5info(h5name);
    for j = 1 : numel(info.Datasets)
        j/numel(info.Datasets)
        if(strcmp(info.Datasets(j).Name, 'Variables'))
            labels = h5read(h5name, '/Variables');
        elseif strcmp(info.Datasets(j).Name(end-3:end), '_pos')
            name = info.Datasets(j).Name;
            cap = regexp(name,'_','split');
            Pos(str2double(cap{2})+1,:) = h5read(h5name,['/' name])';
        else
            name = info.Datasets(j).Name;
            cap = regexp(name,'_','split');
            capName{str2double(cap{2})+1} = name;
            Data(str2double(cap{2})+1,:,:) = h5read(h5name,['/' name]);
        end
    end
end
%% create capteur structure
subs = 1;
for ic = 1 : size(Data,1)
    ic/size(Data,1)
    capteur(ic).Name = capName{ic};
    capteur(ic).Pos = Pos(ic,:);
    aux = squeeze(Data(ic,:,:));
    capteur(ic).Time = aux(1,1:subs:end);
    aux(1,:) = [];

    if any(labels == "EnergyP    1")
        capteur(ic).EnergyP = aux(1,1:subs:end);
        aux(1,:) = [];
    end
    if any(labels == "EnergyS    1")
        capteur(ic).EnergyS = aux(1,1:subs:end);
        aux(1,:) = [];
    end
    if any(labels == "Eps Vol    1")
        capteur(ic).EpsVol = aux(1,1:subs:end);
        aux(1,:) = [];
    end
    if any(labels == "Displ      1")
        capteur(ic).Displ = aux(1:3,1:subs:end);
        aux(1:3,:) = [];
    end
    if any(labels == "Veloc      1")
        capteur(ic).Veloc = aux(1:3,1:subs:end);
        aux(1:3,:) = [];
    end
    if any(labels == "Accel      1")
        capteur(ic).Accel = aux(1:3,1:subs:end);
        aux(1:3,:) = [];
    end
    if any(labels == "Pressure   1")
        capteur(ic).Pressure = aux(1,1:subs:end);
        aux(1,:) = [];
    end
    if any(labels == "Eps Dev    1")
        capteur(ic).EpsDev = aux(1:6,1:subs:end);
        aux(1:6,:) = [];
    end
    if any(labels == "Stress Dev 1")
        capteur(ic).StressDev = aux(1:6,1:subs:end);
        aux(1:6,:) = [];
    end

%     for ifields = 1 : numel(labels)
%         aux = split(labels(ifields));
%         capteur(ic).(aux(1)) = [];
%     end
end

save([folder filesep matname '.mat'],'capteur','-v7.3')

return
%%
a = hfigure;
pad = 4*2048;
hold all
for ic = 2:numel(capteur)
    %hfigure(ic);
    %subplot(2,1,2)
    %hold all

    plot(capteur(ic).Time,(capteur(ic).Pressure),'DisplayName',[num2str(capteur(ic).Pos),' r=',num2str(norm(capteur(ic).Pos)) ])
    %plot(capteur(ic).Time,abs(hilbert(capteur(ic).Pressure)),'--','DisplayName',num2str(capteur(ic).Pos))

    %plot(capteur(ic).Time,capteur(ic).StressDev)
    %title(sprintf('Pressure Sdev - Pos x:%f y:%f z:%f',capteur(ic).Pos))
    aa(ic,:) = fft(capteur(ic).Pressure,pad);
end
fa = 1/mean(diff(capteur(ic).Time));
w = linspace(0,fa,pad);
xlabel('Time [s]')
ylabel('Pressure [Pa]')
xlim([0 0.15])
grid on
box on
set(gca,'FontSize',18)

saveas(a,[folder filesep 'PressureTime.png'])
%
b = hfigure;
plot(w,abs(aa)./max(abs(aa(:))))
xlim([0 2000])
wave = WaveformRickersClass (63, fa, 2/63);
wave.Generate
hold all
W = fft(wave.Tone,pad);
W = 2*pi*W.*w';
%plot(w,abs(W/max(W(1:end/2))))
xlim([0 w(end)/2])
xlim([0 1500])
xlabel('Frequency [Hz]')
ylabel('Normalised Pressure [Pa/Pa]')
grid on
box on
set(gca,'FontSize',18)
saveas(b,[folder filesep 'PressureFreq.png'])


return
%saveas(a,[folder filesep 'time.png'])
%saveas(b,[folder filesep 'freq.png'])

%%
close all
    hfigure(ic);
for ic = 1:numel(capteur)
    %subplot(2,1,1)
    hold all
    plot(capteur(ic).Time,capteur(ic).EnergyP,'DisplayName',num2str(capteur(ic).Pos))
    %plot(capteur(ic).Time,capteur(ic).EnergyS,'DisplayName',num2str(capteur(ic).Pos))
    title(sprintf('Energy P - Pos x:%f y:%f z:%f',capteur(ic).Pos))
end

    hfigure(ic);
for ic = 1:numel(capteur)
    %subplot(2,1,1)
    %plot(capteur(ic).Time,capteur(ic).EnergyP,'DisplayName',num2str(capteur(ic).Pos))
    hold all
    plot(capteur(ic).Time,capteur(ic).EnergyS,'DisplayName',num2str(capteur(ic).Pos))
    title(sprintf('Energy S - Pos x:%f y:%f z:%f',capteur(ic).Pos))
end
%%
hfigure;

for ic = 1:numel(capteur)
    %hfigure(ic);
    %subplot(2,1,2)
    %hold all
    hold all
    plot(capteur(ic).Time,capteur(ic).Veloc,'DisplayName',num2str(capteur(ic).Pos))
    %plot(capteur(ic).Time,capteur(ic).StressDev)
    %title(sprintf('Pressure Sdev - Pos x:%f y:%f z:%f',capteur(ic).Pos))
end
xlabel('Time [s]')
ylabel('Velocity [m/s]')
%%
close all
hfigure;

for ic = 1:numel(capteur)
    %hfigure(ic);
    %subplot(2,1,2)
    %hold all
    hold all
    [peakmax(ic), peakpos(ic)] = max(abs(hilbert(capteur(ic).Pressure)));
    plot(capteur(ic).Time,abs(hilbert(capteur(ic).Pressure)),'DisplayName',num2str(capteur(ic).Pos))
    %plot(capteur(ic).Time,capteur(ic).StressDev)
    %title(sprintf('Pressure Sdev - Pos x:%f y:%f z:%f',capteur(ic).Pos))
end

save("/Volumes/GoogleDrive/Mon Drive/PosDoc/ComparacaoEnergiaAcustica/semAcoustic.mat","capteur");

sd = peakpos - peakpos(1)+4;
vp = 6300;
sd*vp/fa
%%
for ic = 1:numel(capteur)
    for i = 1 :size(capteur(ic).StressDev(1,:) ,2)
        sigmadev = [capteur(ic).StressDev(1,i) capteur(ic).StressDev(4,i) capteur(ic).StressDev(6,i);
            capteur(ic).StressDev(1,i) capteur(ic).StressDev(2,i) capteur(ic).StressDev(5,i);
            capteur(ic).StressDev(6,i) capteur(ic).StressDev(5,i) capteur(ic).StressDev(3,i)];
        sigma = sigmadev - capteur(ic).Pressure(i)*eye(3);
        capteur(ic).Poynting(i,:) = 0.5*(sigma*capteur(ic).Veloc(:,i));
    end
end
%%

for ic = 1:numel(capteur)
    hfigure;
    plot(capteur(ic).Time,capteur(ic).Poynting)
    title(sprintf('Umov - Poynting - Pos x:%f y:%f z:%f',capteur(ic).Pos))
    legend('x','y','z')
end
