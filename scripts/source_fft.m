%% load file
usds_th = readtable('C:\Users\Vitaly\OneDrive\Bureau\LMA\Accelerograms.xlsx', Sheet='USDS-TH');
ud_th = readtable('C:\Users\Vitaly\OneDrive\Bureau\LMA\Accelerograms.xlsx', Sheet='UD-TH');
cross_str = readtable('C:\Users\Vitaly\OneDrive\Bureau\LMA\Accelerograms.xlsx', Sheet='CROSS-STR');


%% plot accelerogram
figure(1);
cla;
hold on;

plot(usds_th.Time_s_, usds_th.x_cm_s_s_);
A1 = 'USDS\_TH';
plot(ud_th.Time_s_, ud_th.x_cm_s_s_);
A2 = 'UD\_TH';
plot(cross_str.Time_s_, cross_str.x_cm_s_s_);
A3 = 'CROSS\_STR';

title('Accelerogram');
xlabel('Time (s)');
ylabel('Acceleration (cm.s^{-2})');
legend(A1, A2, A3);

%% plot fft
figure(1);
cla;
hold on;

T = usds_th.Time_s_(2) - usds_th.Time_s_(1);    % Sampling period
Fs = 1 / T;                                     % Sampling frequency                                       
L = size(usds_th.Time_s_, 1);                   % Length of signal
t = (0:L-1)*T;                                  % Time vector

plot(Fs/L*(0:L-1), abs(fft(usds_th.x_cm_s_s_)));
A1 = 'USDS\_TH';
plot(Fs/L*(0:L-1), abs(fft(ud_th.x_cm_s_s_)));
A2 = 'UD\_TH';
plot(Fs/L*(0:L-1), abs(fft(cross_str.x_cm_s_s_)));
A3 = 'CROSS\_STR';

title('Accelerogram');
xlabel('Frequency (Hz)');
ylabel('|fft(Acceleration)|');
legend(A1, A2, A3);