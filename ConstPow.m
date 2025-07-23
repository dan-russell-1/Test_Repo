%% Testing Constant Power Loads
% for Dan Russell Comp Exam Follow-Up
clc; clear; close all;


%% init
vmag = ones(6,4);      % store voltage magnitudes

%% No Cap:
% before load increase
mpc_nocap = loadcase(case5);
res = runpf(mpc_nocap);
vmag(:,1) = res.bus(:,8);
% after load increase
mpc_nocap.bus(4,3:4) = 2*mpc_nocap.bus(4,3:4);
res = runpf(mpc_nocap);
vmag(:,2) = res.bus(:,8);

%% With Cap:
% before load increase
mpc_nocap = loadcase(case5);
mpc_nocap.bus(4,6) = 0.625 / 1e3;   % cap bank - static b value in MVAr
res = runpf(mpc_nocap);
vmag(:,3) = res.bus(:,8);
% after load increase
mpc_nocap.bus(4,3:4) = 2*mpc_nocap.bus(4,3:4);
res = runpf(mpc_nocap);
vmag(:,4) = res.bus(:,8);

%% Plot:
linesty = {'-','--','-','--'};
linecol = {'b','c','r',[1 0.5 0.8]};
ledg = {'|V|, t=1, no cap','|V|, t=2, no cap','|V|, t=1, w/ cap','|V|, t=2, w/ cap'};

figure;
hold on
for ii = 1:4
    plot(1:6, vmag(:,ii),'Color',linecol{ii},'LineStyle',linesty{ii},'LineWidth',2,'DisplayName',ledg{ii},'Marker','o');
end
xlabel('Nodes','FontSize',14)
xticks(1:6);
ylabel('Voltage Magnitude (p.u.)','FontSize',14)
legend('FontSize',14)
grid on
hold off
