import numpy as np
import matplotlib.pyplot as plt

results = np.load('inverse_results.npz')
wavelengths = np.arange(400, 810, 10)

best_idx = np.argmin(results['errors'])

plt.figure(figsize=(10, 6))
plt.plot(wavelengths, results['target_spectra'][best_idx], 'r--', label='Target (real spectrum)', linewidth=2)
plt.plot(wavelengths, results['actual_spectra'][best_idx], 'b-', label='MLP + TMM prediction', linewidth=2)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title(f'Top-1 Inverse Design Result')
plt.legend()
plt.grid(True)
plt.savefig('fig1_spectrum_comparison.png', dpi=150)
print("图1已保存: fig1_spectrum_comparison.png")

plt.figure(figsize=(10, 6))
plt.hist(results['errors'], bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('MSE Error')
plt.ylabel('Count')
plt.title(f'Error Distribution of {len(results["errors"])} Inverse Designs')
plt.grid(True)
plt.savefig('fig2_error_distribution.png', dpi=150)
print("图2已保存: fig2_error_distribution.png")

mean_error = np.mean(results['errors'])
median_error = np.median(results['errors'])
print(f"\n误差统计:")
print(f"  平均 MSE: {mean_error:.6f}")
print(f"  中位数 MSE: {median_error:.6f}")
print(f"  最小 MSE: {np.min(results['errors']):.6f}")
print(f"  最大 MSE: {np.max(results['errors']):.6f}")

# 计算厚度预测的误差
thickness_errors = np.abs(results['predicted_thickness'] - results['target_thicknesses'])
mean_thick_err = np.mean(thickness_errors)
max_thick_err = np.max(thickness_errors)
print(f"\n厚度预测误差:")
print(f"  平均绝对误差: {mean_thick_err:.2f} nm")
print(f"  最大绝对误差: {max_thick_err:.2f} nm")
