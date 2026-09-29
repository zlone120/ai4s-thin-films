import numpy as np
from tmm_core import generate_dataset

seed = 6
print(f"正在生成数据集 (seed={seed})...")
thicknesses, spectra, wavelengths = generate_dataset(5000, seed=seed)

np.savez('dataset.npz',
         thicknesses=thicknesses,
         spectra=spectra,
         wavelengths=wavelengths)

np.savez('train.npz', x=thicknesses[:4000], y=spectra[:4000])
np.savez('val.npz', x=thicknesses[4000:4500], y=spectra[4000:4500])
np.savez('test.npz', x=thicknesses[4500:], y=spectra[4500:])

print("数据已生成并保存！")
print(f"厚度范围: {thicknesses.min():.1f} ~ {thicknesses.max():.1f} nm")
print(f"光谱形状: {spectra.shape}")
print(f"训练集: 4000, 验证集: 500, 测试集: 500")
