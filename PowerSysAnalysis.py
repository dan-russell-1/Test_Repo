import numpy as np
import matplotlib.pyplot as plt

# print table for latex
def print_latex_table(zload, zline, Vmag, Vphase, S):
    zldr = 1        # zload round number
    zlnr = 2        # zline round number
    Pr = 3          # power rounding
    Qr = 3          # Q rounding

    S = S / 1e3         # convert s to kW/kVAr

    print("\\begin{table}[ht]")
    print("\\centering")
    print("\\caption{The units are $\\Omega$, $V$, degrees, $\\text{kW}$ and $\\text{kVAr}$.}")
    print("\\label{tab:}")
    print("\\begin{tabular}{|c|c|c|c|c|}")
    print("\\hline")
    print("$Z_2$ & $Z_4$ & $Z_6$ & $Z_8$ & $Z_{10}$ \\\\")
    print(f"{np.round(zload[0],zldr)} & {np.round(zload[1],zldr)} & {np.round(zload[2],zldr)} & {np.round(zload[3],zldr)} & {np.round(zload[4],zldr)} \\\\")
    print("\\hline")
    print("$Z_1$ & $Z_3$ & $Z_5$ & $Z_7$ & $Z_9$ \\\\")
    print(f"{np.round(zline[0],zlnr)} & {np.round(zline[1],zlnr)} & {np.round(zline[2],zlnr)} & {np.round(zline[3],zlnr)} & {np.round(zline[4],zlnr)} \\\\")
    print("\\hline")
    print("$|V_2|$ & $|V_3|$ & $|V_4|$ & $|V_5|$ & $|V_6|$ \\\\")
    print(f"{np.round(Vmag[0], 2)} & {np.round(Vmag[1], 2)} & {np.round(Vmag[2], 2)} & {np.round(Vmag[3], 2)} & {np.round(Vmag[4], 2)} \\\\")
    print("\\hline")
    print("$\\angle V_2$ & $\\angle V_3$ & $\\angle V_4$ & $\\angle V_5$ & $\\angle V_6$ \\\\")
    print(f"{np.round(Vphase[0], 2)} & {np.round(Vphase[1], 2)} & {np.round(Vphase[2], 2)} & {np.round(Vphase[3], 2)} & {np.round(Vphase[4], 2)} \\\\")
    print("\\hline")
    print("$P_2$ & $P_3$ & $P_4$ & $P_5$ & $P_6$ \\\\")
    print(f"{np.round(S[0].real, Pr)} & {np.round(S[1].real, Pr)} & {np.round(S[2].real, Pr)} & {np.round(S[3].real, Pr)} & {np.round(S[4].real, Pr)} \\\\")
    print("\\hline")
    print("$Q_2$ & $Q_3$ & $Q_4$ & $Q_5$ & $Q_6$ \\\\")
    print(f"{np.round(S[0].imag, Qr)} & {np.round(S[1].imag, Qr)} & {np.round(S[2].imag, Qr)} & {np.round(S[3].imag, Qr)} & {np.round(S[4].imag, Qr)} \\\\")
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")


def compute_voltages(zline, zload, Vs):
    z = np.column_stack((zline, zload)).ravel()  # Combine line and load impedances
    y = 1 / z  # Admittance
    Y = np.array([  [y[0]+y[1]+y[2], -y[2],           0,              0,              0],
                    [-y[2],           y[2]+y[3]+y[4], -y[4],          0,              0],
                    [0,               -y[4],          y[4]+y[5]+y[6], -y[6],          0],
                    [0,               0,              -y[6],          y[6]+y[7]+y[8], -y[8]],
                    [0,               0,              0,              -y[8],          y[8]+y[9]]])  # Admittance matrix
    i = np.array([Vs * y[0], 0, 0, 0, 0])  # Current vector
    V = np.linalg.inv(Y) @ i  # Solve for voltages
    Vmag = np.abs(V)  # Magnitude of voltages
    Vphase = np.degrees(np.angle(V))  # Phase of voltages
    return V, Vmag, Vphase


## Set up / constants
showprint = False
np.random.seed(41)
Vs = 240 + 0*1j  # Source voltage
zline = np.random.uniform(3e-2, 7e-2, size=(5)) + 1j * np.random.uniform(3e-2, 7e-2, size=(5))  # Random complex impedances
print(zline)

## Ex2 in the paper - values set to get realistic loads ######################################
## Before load change
# initial loads
zload = np.random.uniform(20, 40, size=(5)) + 1j * np.random.uniform(5, 10, size=(5))        # Random complex loads with reasonable power factor
# compute voltages
V, Vmag, Vphase = compute_voltages(zline, zload, Vs)
# Calculate power
S = abs(V)**2 / zload.conjugate()

## After load change
# initial loads
zload2 = zload * np.array([1, 1, 0.5, 1, 1])
V2, Vmag2, Vphase2 = compute_voltages(zline, zload2, Vs)
S2 = abs(V2)**2 / zload2.conjugate()


## Ex3 in paper - add a capacitor to ex2
# initial loads
Xc = (Vmag[2])**2 / np.imag(S[2])               # compute Xc value
zc = 0 - 1j*Xc                                  # define capacitor impedance
z_eq3 = (zload[2] * zc) / (zload[2] + zc)       # find equivalent impedance with capacitor in parallel
zload3 = zload.copy()                           # initialize new load same as first load
zload3[2] = z_eq3                               # replace with capacitor load
# compute voltages
V3, Vmag3, Vphase3 = compute_voltages(zline, zload3, Vs)
# Calculate power
S3 = abs(V3)**2 / zload3.conjugate()

print(Xc)

## After load change
# initial loads
zld2 = 0.5*zload[2]
z_eq4 = (zld2 * zc) / (zld2 + zc)               # find equivalent impedance with capacitor in parallel
zload4 = zload.copy()                           # initialize new load same as first load
zload4[2] = z_eq4                               # replace with capacitor load
# compute voltages
V4, Vmag4, Vphase4 = compute_voltages(zline, zload4, Vs)
# Calculate power
S4 = abs(V4)**2 / zload4.conjugate()

## Plot the voltage profiles ###############################
Vmagp = np.insert(Vmag, 0, 240)     # Insert the source voltage at the beginning
Vmagp2 = np.insert(Vmag2, 0, 240)   # Insert the source voltage at the beginning
Vmagp3 = np.insert(Vmag3, 0, 240)   # Insert the source voltage at the beginning
Vmagp4 = np.insert(Vmag4, 0, 240)   # Insert the source voltage at the beginning
plt.figure(figsize=(10, 5))
plt.plot(Vmagp/240, marker='o', label='|V| t=1, no cap', color='royalblue')
plt.plot(Vmagp2/240,'--', marker='o', label='|V| t=2, no cap', color='lightskyblue')
plt.plot(Vmagp3/240, marker='o', label='|V| t=1, w/ cap', color='firebrick')                # comment to show pre-load-change
plt.plot(Vmagp4/240,'--', marker='o', label='|V| t=2, w/ cap', color='lightcoral')          # comment to show pre-load-change
plt.xlabel('Node')
plt.ylabel('Voltage Magnitude (p.u.)')
plt.title('Voltage Magnitudes Before and After Load Change')
plt.xticks(ticks=np.arange(6), labels=[f'Node {i+1}' for i in range(6)])
plt.legend()
plt.grid()


# print results in latex table form for the paper
if showprint: 
    print("=1=1=1=1=1=1=1=1=1=1=1=1= TABLE FOR EX2 BEFORE LOADING CHANGE =1=1=1=1=1=1=1=1=1=1=1=1=1=1=1=")
    print_latex_table(zload, zline, Vmag, Vphase, S)
    print("=1=1=1=1=1=1=1=1=1=1=1=1= TABLE FOR EX2 AFTER LOADING CHANGE =1=1=1=1=1=1=1=1=1=1=1=1=1=1=1=")
    print_latex_table(zload2, zline, Vmag2, Vphase2, S2)
    print("=1=1=1=1=1=1=1=1=1=1=1=1= TABLE FOR EX3 BEFORE LOADING CHANGE =1=1=1=1=1=1=1=1=1=1=1=1=1=1=1=")
    print_latex_table(zload3, zline, Vmag3, Vphase3, S3)
    print("=1=1=1=1=1=1=1=1=1=1=1=1= TABLE FOR EX3 AFTER LOADING CHANGE =1=1=1=1=1=1=1=1=1=1=1=1=1=1=1=")
    print_latex_table(zload4, zline, Vmag4, Vphase4, S4)
    
plt.show()