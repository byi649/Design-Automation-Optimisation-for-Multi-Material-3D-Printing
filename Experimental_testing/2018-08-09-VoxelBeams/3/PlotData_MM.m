clc
clear
close all

inplane = [1,2,3,4,5,6];
ooplane = [1,2,3,4,5,6];
torsional = [1,2,3,4,5,6];


%Stiffest
f_stiff = [56.11779370476488, 174.22545578605053, 340.45615803610025, 529.0265779277128, 737.6926898633982, 922.0595991228488];

%Flexible
f_flex = [52.63475586761726, 162.93945421747765, 319.5702852809374, 496.4571292356812, 689.386208484303, 865.197948810865];

%Nominal freqs
fnominal = [
54.33;
168.41;
329.75;
512.32;
712.77;
892.89]';


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
title('Voxel Beam Solution 3 - In-Plane Excitation')


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
title('Voxel Beam Solution 3 - Out-of-Plane Excitation')

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
title('Voxel Beam Solution 3 - Torsional Excitation')

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