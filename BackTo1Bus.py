import numpy as np

Vs = 234.95 + 0j       # source voltage
z1 = 0.02372565+0.00229018j
Sl = abs(Vs)**2 / z1.conjugate()
print("Sl",Sl)
Ql = np.imag(Sl)
print("Ql",Ql)
Qc = -1*Ql
Xc = abs(Vs)**2 / Qc
print("Xc",Xc)

zc = 0 + 1j*Xc
z_eq = (z1 * zc) / (z1 + zc)
Sfix = Sl = abs(Vs)**2 / z_eq.conjugate()

print(Sfix)