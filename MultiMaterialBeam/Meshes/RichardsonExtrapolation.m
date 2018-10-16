function [f_extrap,p] = RichardsonExtrapolation(h_coarse,h_med,h_fine,f_coarse,f_med,f_fine)
%Performs Richardson extrapolation on a quantity f, using a fine and medium
%mesh. Coarse mesh is included so that apparent order of convergence can be
%estimated
%Also returns the apparent order of convergence

%Mesh grid sizing ratios
r32 = h_coarse/h_med;
r21 = h_med/h_fine;

%Differences in estimates
e32 = f_coarse - f_med;
e21 = f_med - f_fine;

%Evaluate constants to estimate apparent order of convergence
s = (e32*e21)/abs(e32*e21);

apparent_order = @(p) 1/log(r21) * abs( log(abs(e32/e21) ) + log( (r21^p - s)/(r32^p - s) ) ) - p;

%Use an initial guess of 1 for order of convergence -> linear order schemes
p = fzero(apparent_order, 1);

%Use richardson extrapolation with apparent order of convergence
f_extrap = (r21^p * f_fine - f_med)/(r21^p - 1);


end

