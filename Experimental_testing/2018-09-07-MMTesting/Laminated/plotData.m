clc
clear

%Read in from file
fid = fopen('laminated-averaged.txt','r');

data = textscan(fid, '%f %f %f','CommentStyle','*');
f = data{1};
dB = data{2};
fclose(fid);

%Solution data
ElmerFreqs = [
161.40
737.76
825.65
893.67
2188.59
2208.46

];

%Plot
figure(1)
p1 = semilogx(f,dB);
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('Laminate Sample - Frequency Spectrum')

for i = 1:length(ElmerFreqs)
   l1=  line([ElmerFreqs(i) ElmerFreqs(i)], [min(dB) max(dB)]);
   l1.Color = 'k';
   l1.LineWidth = 2;
   l1.LineStyle = '--';
end

legend([p1,l1],{'Data','Elmer Solutions'})
ylim([min(dB),max(dB)]);
xlim([min(f),max(f)]);

%fn vs n
figure(2)
plot(1:length(ElmerFreqs),ElmerFreqs,'--bo');
xlabel('Mode Number n')
ylabel('Natural Frequency [Hz]')
title('Laminate Sample - Natural Frequencies')
xticks([1,2,3,4,5,6])
legend('Elmer Solutions')