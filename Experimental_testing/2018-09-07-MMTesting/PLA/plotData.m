clc
clear

%Read in from file
fid = fopen('PLA-averaged.txt','r');

data = textscan(fid, '%f %f %f','CommentStyle','*');
f = data{1};
dB = data{2};
fclose(fid);

%Solution data
ElmerFreqs = [
225.08
1022.31
1236.99
1378.27
3749.59
3840.58
];

InPlane = [
219.8272345
1377.639076
3856.589045
];
%Plot
figure(1)
p1 = semilogx(f,dB);
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('PLA Frequency Spectrum')

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
title('PLA - Natural Frequencies')
xticks([1,2,3,4,5,6])
legend('Elmer Solutions','In-Plane Bending Analytic Solutions')