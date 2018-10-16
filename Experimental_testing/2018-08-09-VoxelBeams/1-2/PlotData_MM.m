clc
clear
close all

inplane = [1,2,3,4,5,6];
ooplane = [1,2,3,4,5,6];
torsional = [1,2,3,4,5,6];


%Stiffest
f_stiff = [60.002722232496275, 157.60452743310026, 300.52659439992505, 468.25063955917915, 659.4540462378267, 822.1547541479205];

%Flexible
f_flex = [56.34109712861741, 147.21773735688788, 281.91430942993316, 438.995582491605, 615.6145293037536, 770.5098288025011];

%Nominal freqs
fnominal = [
58.13;
152.24;
290.98;
453.22;
636.81;
795.62]';


%Read in in-plane from file
fid = fopen('InPlane-averaged.txt','r');

data = textscan(fid, '%f %f %f','CommentStyle','*');
f = data{1};
dB = data{2};
fclose(fid);

%Truncate data for linear scale
[~,maxind] = max(find(f<=1000));
f = f(1:maxind);
dB = dB(1:maxind);

%Plot - inplane
figure(1)
subplot(2,2,1)
plot(f,dB,'Linewidth',2);
hold on
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('Voxel Beam Solution 1-2 - In-Plane Excitation')


xlim([min(f),max(f)]);
ymin = -90;
ymax = 80;
ylim([ymin,ymax])
hold on
for i = 1:length(inplane)
    t = text(f_stiff(inplane(i))+30,-30,['n = ',num2str(inplane(i))],'Interpreter','Latex','Fontsize',16);
    set(t,'Rotation',90);
    r = rectangle('Position',[f_flex(inplane(i)),ymin,f_stiff(inplane(i))-f_flex(inplane(i)),ymax-ymin],'FaceColor',[0 0 0 0.5],'Edgecolor',[0 0 0 0.5]);
end

%Read in out-of-plane from file
fid = fopen('OoPlane-averaged.txt','r');

data = textscan(fid, '%f %f %f','CommentStyle','*');
f = data{1};
dB = data{2};
fclose(fid);

%Truncate data for linear scale
[~,maxind] = max(find(f<=1000));
f = f(1:maxind);
dB = dB(1:maxind);

%Plot - ooplane
figure(1)
subplot(2,2,2)
plot(f,dB,'Linewidth',2);
hold on
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('Voxel Beam Solution 1-2 - Out-of-Plane Excitation')

xlim([min(f),max(f)]);
ymin = -90;
ymax = 80;
ylim([ymin,ymax])
hold on
for i = 1:length(ooplane)
    t = text(f_stiff(ooplane(i))+30,-30,['n = ',num2str(ooplane(i))],'Interpreter','Latex','Fontsize',16);
    set(t,'Rotation',90);
    r = rectangle('Position',[f_flex(ooplane(i)),ymin,f_stiff(ooplane(i))-f_flex(ooplane(i)),ymax-ymin],'FaceColor',[0 0 0 0.5],'Edgecolor',[0 0 0 0.5]);
end


%Read in torsional from file
fid = fopen('Torsional-averaged.txt','r');

data = textscan(fid, '%f %f %f','CommentStyle','*');
f = data{1};
dB = data{2};
fclose(fid);

%Truncate data for linear scale
[~,maxind] = max(find(f<=1000));
f = f(1:maxind);
dB = dB(1:maxind);

%Plot - torsional
figure(1)
subplot(2,2,3)
plot(f,dB,'Linewidth',2);
hold on
xlabel('Frequency [Hz]')
ylabel('SPL [dB]')
title('Voxel Beam Solution 1-2 - Torsional Excitation')

xlim([min(f),max(f)]);
ymin = -90;
ymax = 80;
ylim([ymin,ymax])
hold on
for i = 1:length(torsional)
    t = text(f_stiff(torsional(i))+30,-30,['n = ',num2str(torsional(i))],'Interpreter','Latex','Fontsize',16);
    set(t,'Rotation',90);
    r = rectangle('Position',[f_flex(torsional(i)),ymin,f_stiff(torsional(i))-f_flex(torsional(i)),ymax-ymin],'FaceColor',[0 0 0 0.5],'Edgecolor',[0 0 0 0.5]);
end

p = polyfit(1:6,fnominal,1);
x = 0:0.01:6;

subplot(2,2,4)
%scatter(1:6,fnominal,'MarkerFaceColor',[0 0.4470 0.7410])
errorbar(1:6,fnominal,fnominal-f_flex,f_stiff-fnominal,'o')
hold on
plot(x,polyval(p,x))
ylabel('Frequency [Hz]')
xlabel('Mode Number n')
title('Natural Frequency Profile')
xlim([0,6.1])