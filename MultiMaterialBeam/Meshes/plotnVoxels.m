clc
clear
close all

load nVoxelsData.mat;

scatter(nVoxels,CPUTime,'rs','Linewidth',1,'DisplayName','CPU Time')
text(150,6.1,sprintf('$$\\hat{t}_C = %.2f$$s, $$\\sigma_C = %.2f$$s',mean(CPUTime),std(CPUTime)),'Interpreter','Latex','Fontsize',12)

hold on
scatter(nVoxels,WallTime,'bo','Linewidth',1,'DisplayName','Wall-clock Time')
xlabel('nVoxels')
ylabel('Time (s)')

h = refline(0,mean(WallTime));
h.LineStyle = '--';
h.LineWidth = 2;
h.Color = [0.6 0.6 0.6];
text(150,3.2,sprintf('$$\\hat{t}_W = %.2f s, \\sigma_W = %.2f s$$',mean(WallTime),std(WallTime)),'Interpreter','Latex','Fontsize',12)
h = refline(0,mean(CPUTime));
h.LineStyle = '--';
h.LineWidth = 2;
h.Color = [0.6 0.6 0.6];
legend({},'Fontsize',12)