clc
clear
close all
%Main script for generation of mesh sensitivity analysis plots
n = 6;
%fn - nSols x nGrids matrix
nGrids = 3;
nSols = 5;
h = [2e-3,1e-3,(2/3)*1e-3,0.5e-3];
N = [1200, 8000, 28800, 64000];
N = N(2:end);
%Solution 1
f1 = [56.19	55.47	55.21];
f2 = [147.55	146.82	146.55];
f3 = [282.67	277.71	275.82];
f4 = [440.07	434.75	432.76];
f5 = [616.36	613.59	612.60];
f6 = [774.11	760.65	755.61];

%Solution 2
f1 = [57.77	57.08	56.83];
f2 = [190.78	190.16	189.92];
f3 = [313.18	308.99	307.46];
f4 = [511.06	506.54	504.90];
f5 = [702.07	691.22	687.17];
f6 = [838.20	834.35	832.92];

%Solution 3
f1 = [53.26	51.93	51.39];
f2 = [163.81	161.92	161.12];
f3 = [320.14	314.36	312.15];
f4 = [501.07	493.03	489.69];
f5 = [690.40	685.72	683.87];
f6 = [870.61	851.94	844.60];

%Solution 4
f1 = [56.68	56.01	55.78];
f2 = [173.73	173.04	172.79];
f3 = [320.18	316.23	314.83];
f4 = [505.15	499.97	498.22];
f5 = [689.69	686.68	685.62];
f6 = [849.55	838.27	834.15];

%Solution 5
f1 = [53.94	52.92	52.53];
f2 = [214.12	212.91	212.41];
f3 = [342.38	337.97	336.36];
f4 = [509.19	502.06	499.20];
f5 = [698.26	686.74	682.36];
f6 = [853.31	850.69	849.74];



f1 = [59.40	56.19	55.47	55.21;
    60.96	57.77	57.08	56.83;
    57.36	53.26	51.93	51.39;
    59.74	56.68	56.01	55.78;
    0 53.94	52.92	52.53];

f1 = f1(:,2:end);

f2 = [150.13	147.55	146.82	146.55;
    193.03	190.78	190.16	189.92;
    168.10	163.81	161.92	161.12;
    176.06	173.73	173.04	172.79;
    0 214.12	212.91	212.41];
f2 = f2(:,2:end);

f3 = [300.81	282.67	277.71	275.82;
    330.77	313.18	308.99	307.46;
    341.17	320.14	314.36	312.15;
    337.86	320.18	316.23	314.83;
    0 342.38	337.97	336.36];
f3 = f3(:,2:end);

f4 = [456.54	440.07	434.75	432.76;
    526.96	511.06	506.54	504.90;
    523.09	501.07	493.03	489.69;
    523.64	505.15	499.97	498.22;
    0 509.19	502.06	499.20];
f4 = f4(:,2:end);

f5 = [625.78	616.36	613.59	612.60;
    742.86	702.07	691.22	687.17;
    703.89	690.40	685.72	683.87;
    700.29	689.69	686.68	685.62;
    0 698.26	686.74	682.36];
f5 = f5(:,2:end);

f6 = [822.27	774.11	760.65	755.61;
    850.19	838.20	834.35	832.92;
    932.74	870.61	851.94	844.60;
    896.89	849.55	838.27	834.15;
    0 853.31	850.69	849.74];
f6 = f6(:,2:end);

fn = cat(3,f1,f2,f3,f4,f5,f6);
%fn(a,b,c) = frequency c for grid a and solution b

%Solutions to keep
solns = [4,5];

f_extrap_matrix = zeros(length(solns),n);
cnt = 1;
bin = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0;
    1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0];

%bin = bin(1,:);
for k = 1:nSols
    figure(k);
    for i = 1:n
        subplot(2,3,i);
        %Richardson extrap estimate
        [f_extrap,p] = RichardsonExtrapolation(h(end-2),h(end-1),h(end),fn(k,end-2,i),fn(k,end-1,i),fn(k,end,i));
        plot(0,f_extrap,'ro');
        hold on
        plot(N.^(-p),fn(k,:,i),'-bo');
        xlabel('1/N^p')
        ylabel(sprintf('f_%i [Hz]',i))
        grid on
        legend({'Richardson Extrapolation','Numerical Solutions'},'Location','Northwest')
        title(sprintf('f_%i Convergence, p = %.2f',i,p));
        
        if ismember(k,solns)
            f_extrap_matrix(cnt,i) = f_extrap;
        end
    end
    a = axes;
    %t1 = title(sprintf('Voxel Beam Solution Number %i - Mesh Convergence Plots',k));
    t1 = title(sprintf('Voxel Beam Solution Number %i - Mesh Convergence Plots',k), 'Units', 'normalized', 'Position', [0.5, 1.05, 0]); % Set Title with correct Position
    a.Visible = 'off'; % set(a,'Visible','off');
    t1.Visible = 'on'; % set(t1,'Visible','on');
    t1.FontSize = 18;
    
        if ismember(k,solns)
            cnt = cnt + 1;
        end
end

for i = 1:(cnt-1)
    figure(i+8)
    for j = 1:n
        %plot(N.^(-2),fn(solns(i),:,j)./f_extrap_matrix(i,j),'--o','Linewidth',1,'DisplayName',['n = ',num2str(j)])
        plot(N.^(-2),abs((fn(solns(i),:,j)-f_extrap_matrix(i,j))./f_extrap_matrix(i,j)),'--o','Linewidth',1,'DisplayName',['n = ',num2str(j)])
        hold on
        xlabel('1/N^2','Fontsize',12)
        ylabel('$$\varepsilon_n$$','Interpreter','Latex','Fontsize',18)
        grid on
        title(sprintf('Voxel beam solution number %i convergence',solns(i)),'Fontsize',12);
    end
            legend({},'Fontsize',12,'location','northwest')
end
p = polyfit(1:6,reshape(fn(solns(i),3,:),[1,n]),1);

 for i = 1:length(solns)
     figure(i + 10);
     %subplot(1,2,1)
     plot(1:n,reshape(fn(solns(i),3,:),[1,n]),'bo','DisplayName','N = 28800','Linewidth',1);
     error = norm(reshape(fn(solns(i),3,:),[1,n])-polyval(p,1:6),2);
    % text(2,700,['||\epsilon||_2 = ', sprintf('%.2f%',error),'Hz'],'Fontsize',12);
     hold on
     refline(p(1),p(2));
     xlabel('Mode number n','Fontsize',24)
     set(gca,'xtick',[1 2 3 4 5 6])
     ylabel('Frequency [Hz]','Fontsize',24)
     ylim([0,inf])
     title(sprintf('Voxel beam solution %i',solns(i)-3),'Fontsize',24); 
     grid on
     pbaspect([1 1 1])
     figure(i + 15)
     imagesc((reshape(bin(i,:),[4,10])));
     set(gca,'xtick',[])
    set(gca,'xticklabel',[])
         set(gca,'ytick',[])
    set(gca,'yticklabel',[])
    pbaspect([10 4 1])
 end