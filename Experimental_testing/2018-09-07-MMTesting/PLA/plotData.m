clc
clear

%Read in from file
fid = fopen('steelfill-averaged.txt','r');

data = textscan(fid, '%f %f %f','CommentStyle','*');
f = data{1};
dB = data{2};
fclose(fid);

%Solution data
ElmerFreqs = [
    185.33
841.76
1018.52
1134.85
3087.36
3162.29
];

InPlane = [
    181.002880438105
1134.33006416419
3175.46516708348
];
%Plot
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