function mpc = case5
%CASE5
% designed for comp exam study
% 5 nodes, just loads, no inverters

%% MATPOWER Case Format : Version 2
mpc.version = '2';

%%-----  Power Flow Data  -----%%
%% system MVA base
mpc.baseMVA = 0.001;    % values specified in kW

%% bus data
%	bus_i	type	Pd	Qd	Gs	Bs	area	Vm	Va	baseKV	zone	Vmax	Vmin

mpc.bus = [
	1	3	0	    0	    0	0	1	1	0	240	1	1	1;
	2	1	2.038	0.409	0	0	1	1	0	240	1	1.1	0.9;
	3	1	1.959	0.651	0	0	1	1	0	240	1	1.1	0.9;
	4	1	2.152	0.596	0	0	1	1	0	240	1	1.1	0.9;
	5	1	1.868	0.619	0	0	1	1	0	240	1	1.1	0.9;
	6	1	1.741	0.411	0	0	1	1	0	240	1	1.1	0.9
    ];
% next % % % 
% put in shunt capacitance, in MVAr (or convert it down below)


%% generator data
%	bus	Pg	Qg	Qmax	Qmin	Vg	mBase	status	Pmax	Pmin	Pc1	Pc2	Qc1min	Qc1max	Qc2min	Qc2max	ramp_agc	ramp_10	ramp_30	ramp_q	apf
mpc.gen = [
	1	0	0	100	    -100	1	100	1	100	    0	0	0	0	0	0	0	0	0	0	0	0;
];

%% branch data
%	fbus	tbus	r	x	b	rateA	rateB	rateC	ratio	angle	status	angmin	angmax
mpc.branch = [
	1	2	0.04003694	0.05415463	0	0	0	0	0	0	1	-360	360;
	2	3	0.03184383	0.03763723	0	0	0	0	0	0	1	-360	360;
	3	4	0.05707265	0.05674063	0	0	0	0	0	0	1	-360	360;
	4	5	0.03173878	0.06669791	0	0	0	0	0	0	1	-360	360;
	5	6	0.03465695	0.0467512	0	0	0	0	0	0	1	-360	360
    ];


%%-----  OPF Data  -----%%
%% generator cost data
%	1	startup	shutdown	n	x1	y1	...	xn	yn
%	2	startup	shutdown	n	c(n-1)	...	c0
mpc.gencost = [
	2	0	0	3	0	1	0
];

%% convert branch impedances from Ohms to p.u.
[PQ, PV, REF, NONE, BUS_I, BUS_TYPE, PD, QD, GS, BS, BUS_AREA, VM, ...
    VA, BASE_KV, ZONE, VMAX, VMIN, LAM_P, LAM_Q, MU_VMAX, MU_VMIN] = idx_bus;
[F_BUS, T_BUS, BR_R, BR_X, BR_B, RATE_A, RATE_B, RATE_C, ...
    TAP, SHIFT, BR_STATUS, PF, QF, PT, QT, MU_SF, MU_ST, ...
    ANGMIN, ANGMAX, MU_ANGMIN, MU_ANGMAX] = idx_brch;
Vbase = mpc.bus(1, BASE_KV);            %% in Volts
Sbase = mpc.baseMVA * 1e6;              %% in VA
mpc.branch(:, [BR_R BR_X]) = mpc.branch(:, [BR_R BR_X]) / (Vbase^2 / Sbase);

%% convert loads from kW to MW
mpc.bus(:, [PD, QD]) = mpc.bus(:, [PD, QD]) / 1e3;