clc
clear
close all
f = [54.67937101394212, 220.36092477902633, 349.3641691562582, 518.8326650938748, 710.5711234037525, 880.4627809405143];

SF = [1,2,3,4];

n = 1:6;

c = {'r','m','b','k'};
for i = 1:length(SF)
    scatter(n,f./SF(i),'x','Linewidth',1,'MarkerEdgeColor',c{i})
    hold on
    p = polyfit(n,f./SF(i),1);
    plot(n,polyval(p,n),strcat(c{i},'--'),'Linewidth',1,'DisplayName',sprintf('S = %i',SF(i)))
end

xlabel('Mode number n','Fontsize',12)
ylabel('Frequency [Hz]','Fontsize',12)
    set(gca,'xtick',[1 2 3 4 5 6])
    grid on
legend({},'Fontsize',12,'location','northwest')
