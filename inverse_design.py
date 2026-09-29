import numpy as np
import torch
from tmm_core import calc_reflectance
from train_mlp import MLP

# 加载归一化参数
norm_params = np.load('norm_params.npz')
d_min, d_max = norm_params['d_min'], norm_params['d_max']

model = MLP()
model.load_state_dict(torch.load('mlp_best.pth', weights_only=True))
model.eval()

# 从测试集中随机选一些真实光谱作为目标
test_data = np.load('test.npz')
np.random.seed(7)  # design_seed

# 选 100 个不同的真实光谱
n_targets = 100
indices = np.random.choice(len(test_data['x']), n_targets, replace=False)
target_thicknesses = test_data['x'][indices]
target_spectra = test_data['y'][indices]

print(f"正在进行逆向设计预测 (使用 {n_targets} 个真实光谱作为目标)...")
with torch.no_grad():
    predicted_thickness_norm = model(torch.FloatTensor(target_spectra)).numpy()

# 反归一化
predicted_thickness = predicted_thickness_norm * (d_max - d_min) + d_min
predicted_thickness = np.clip(predicted_thickness, 40, 180)

wavelengths = np.arange(400, 810, 10)

print("正在用 TMM 验证预测结果...")
actual_spectra = np.zeros((n_targets, 41))
for i in range(n_targets):
    for j, wl in enumerate(wavelengths):
        actual_spectra[i, j] = calc_reflectance(predicted_thickness[i], wl)

errors = np.mean((actual_spectra - target_spectra) ** 2, axis=1)
top_k_idx = np.argsort(errors)[:10]

print("\n===== Top 10 最佳逆向设计结果 =====")
for rank, idx in enumerate(top_k_idx):
    orig_idx = indices[idx]
    print(f"\nRank {rank+1}:")
    print(f"  真实厚度: [{target_thicknesses[idx][0]:.1f}, {target_thicknesses[idx][1]:.1f}, {target_thicknesses[idx][2]:.1f}, {target_thicknesses[idx][3]:.1f}] nm")
    print(f"  预测厚度: [{predicted_thickness[idx][0]:.1f}, {predicted_thickness[idx][1]:.1f}, {predicted_thickness[idx][2]:.1f}, {predicted_thickness[idx][3]:.1f}] nm")
    print(f"  MSE 误差: {errors[idx]:.6f}")

np.savez('inverse_results.npz',
         predicted_thickness=predicted_thickness,
         target_thicknesses=target_thicknesses,
         target_spectra=target_spectra,
         actual_spectra=actual_spectra,
         errors=errors)
print("\n结果已保存为 inverse_results.npz")
