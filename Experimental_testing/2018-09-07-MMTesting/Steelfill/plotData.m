clc
clear

%Read in from file
fid = fopen('steelfill-averaged-2.txt','r');

data = textscan(fid, '%f %f %f','CommentStyle','*');
f = data{1};
dB = data{2};
fclose(fid);

%Solution data
ElmerFreqs = [
198.74
902.68
1092.24
1216.99
3310.83
3391.18
];

InPlane = [
194.1039648
1216.433475
3405.307017
];
%Plot
figure(1)
p1 = semilogx(f,dB);
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('Steelfill Frequency Spectrum')

for i = 1:length(ElmerFreqs)
   l1=  line([ElmerFreqs(i) ElmerFreqs(i)], [min(dB) max(dB)]);
   l1.Color = 'k';
   l1.LineWidth = 2;
   l1.LineStyle = '--';
end

for i = 1:length(InPlane)
   l2=  line([InPlane(i) InPlane(i)], [min(dB) max(dB)]);
   l2.Color = 'r';
   l2.LineWidth = 2;
   l2.LineStyle = '--';
end
legend([p1,l1,l2],{'Data','Elmer Solutions','Analytic Solutions'})
ylim([min(dB),max(dB)]);
xlim([min(f),max(f)]);

%fn vs n
figure(2)
plot(1:length(ElmerFreqs),ElmerFreqs,'--bo');
hold on
plot([1,4,5],InPlane,'*r','Linewidth',2);
xlabel('Mode Number n')
ylabel('Natural Frequency [Hz]')
title('Steelfill - Natural Frequencies')
xticks([1,2,3,4,5,6])
legend('Elmer Solutions','In-Plane Bending Analytic Solutions')