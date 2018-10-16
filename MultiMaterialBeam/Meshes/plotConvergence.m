clc
clear
close all

load convergenceData.mat

n = [1,3,5]; %Indices for in-plane solutions

f_analytic = [71.9104494;
450.656832;
1261.577311]; %analytic solutions

%Grid sizes
N = [1200,8000,28800,64000];

%Linear elements convergence
figure(1)
plot(N,LinearSolns(n,:)./f_analytic,'o-','Linewidth',1);
xlabel('$N$','Interpreter','Latex','Fontsize',14)
ylabel('$$f_n/f^{exact}_n$$','Interpreter','Latex','Fontsize',14)
hold on
h = refline(0,1);
h.LineStyle = '--';
h.LineWidth = 2;
h.Color = 'k';
legend({'n = 1', 'n = 3', 'n = 5','$$f_n = f^{exact}_n$$'},'Interpreter','Latex','Fontsize',14)
title('Linear Elements')

%Quadratic elements convergence
figure(2)
plot(N(1:3),QuadSolns(n,:)./f_analytic,'x-','Linewidth',1);
xlabel('$N$','Interpreter','Latex','Fontsize',14)
ylabel('$$f_n/f^{exact}_n$$','Interpreter','Latex','Fontsize',14)
hold on
h = refline(0,1);
h.LineStyle = '--';
h.LineWidth = 2;
h.Color = 'k';
legend({'n = 1', 'n = 3', 'n = 5','$$f_n = f^{exact}_n$$'},'Interpreter','Latex','Fontsize',14)
title('Quadratic Elements')

figure(3)
%Wall time / CPU time Wall clock time achieved per unit CPU time
plot(N,LinearTimes(:,2)./LinearTimes(:,1),'k-o','Linewidth',1,'DisplayName','Linear Elements')
hold on
plot(N(1:3),QuadTimes(:,2)./QuadTimes(:,1),'k--s','Linewidth',1,'DisplayName','Quadratic Elements')
legend({},'Fontsize',14)
xlabel('$N$','Interpreter','Latex','Fontsize',14)
ylabel('T_W/T_C')
%plot(N,LinearTimes(:,2),'b--o','Linewidth',2)
%plot(N(1:3),QuadTimes(:,2),'b--o','Linewidth',2)