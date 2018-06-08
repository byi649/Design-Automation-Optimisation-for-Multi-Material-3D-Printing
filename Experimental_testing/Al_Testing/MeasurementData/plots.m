clc
clear

%Load textfile data
load data.mat

%Solver frequencies from Elmer
ElmerFreqs = [169.2935102,
,1057.808456
,1582.881646
,1595.960663
,2959.547684
,4844.400919];

%Analytic solutions
InPlane = [163.9150733
,1027.242191
,2875.681338
,5636.448197];

%plots

%Torsional modes
figure(1)
p1 = semilogx(Measurement3Tor(:,1),Measurement3Tor(:,2),'Linewidth',2)
hold on
for i = 1:length(ElmerFreqs)
   l1=  line([ElmerFreqs(i) ElmerFreqs(i)], [min(Measurement3Tor(:,2)) max(Measurement3Tor(:,2))]);
   l1.Color = 'k';
   l1.LineWidth = 2;
   l1.LineStyle = '--';
end

for i = 1:length(InPlane)
   l2=  line([InPlane(i) InPlane(i)], [min(Measurement3Tor(:,2)) max(Measurement3Tor(:,2))]);
   l2.Color = 'r';
   l2.LineWidth = 2;
   l2.LineStyle = '--';
end
legend([p1,l1,l2],{'Data','Elmer Solutions','Analytic Solutions'})
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('Frequency Spectrum - Torsional Excitation Testing')


%In-plane bending
figure(2)
p1 = semilogx(Measurement2(:,1),Measurement2(:,2),'Linewidth',2)
hold on
for i = 1:length(ElmerFreqs)
   l1=  line([ElmerFreqs(i) ElmerFreqs(i)], [min(Measurement3Tor(:,2)) max(Measurement3Tor(:,2))]);
   l1.Color = 'k';
   l1.LineWidth = 2;
   l1.LineStyle = '--';
end

for i = 1:length(InPlane)
   l2=  line([InPlane(i) InPlane(i)], [min(Measurement3Tor(:,2)) max(Measurement3Tor(:,2))]);
   l2.Color = 'r';
   l2.LineWidth = 2;
   l2.LineStyle = '--';
end
legend([p1,l1,l2],{'Data','Elmer Solutions','Analytic Solutions'})
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('Frequency Spectrum - In-Plane Excitation Testing')
