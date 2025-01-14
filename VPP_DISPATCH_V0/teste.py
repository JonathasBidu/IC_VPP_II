import numpy as np

M = np.array([[13.996+10.998j, -(1+1j)], [-(1+1j), 13.996+10.998j]])
M1 = np.array([[120, -(1+1j)],[-60-103.923j, 13.996+10.998j]])
M2 = np.array([[13.996+10.998j, 120], [-(1+1j), -60-103.923j]])
x = np.array([200, -100-173.21j])
det_M = np.linalg.det(M)
det_M1 = np.linalg.det(M1)
det_M2 = np.linalg.det(M2)
print(M)
print(M1)
print(M2)
print(f'{det_M:.2f}')
print(f'{det_M1:.2f}')
print(f'{det_M2:.2f}')
I1 = det_M1/det_M
I2 = det_M2/det_M
print(f'I1 = {I1:.2f} = {np.abs(I1):.2f}/_{np.degrees(np.angle(I1)):.2f}°')
print(f'I2 = {I2:.2f} = {np.abs(I2):.2f}/_{np.degrees(np.angle(I2)):.2f}°')
# print(x)
# print(f'{np.degrees(np.angle(det_M)):.2f}')
# y = np.linalg.solve(M, x)
# print(f'I_1 = {y[0]:.2f} = {np.abs(y[0]):.2f}/_{np.degrees(np.angle(y[0])):.2f}')
# print(f'I_2 = {y[1]:.2f} = {np.abs(y[1]):.2f}/_{np.degrees(np.angle(y[1])):.2f}')