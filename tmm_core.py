import numpy as np


def calc_reflectance(d, wavelength, n_H=2.30, n_L=1.45, n_s=1.52):
    """
    用传输矩阵法(TMM)计算多层薄膜的反射率
    d: 4层厚度 [d1, d2, d3, d4]，单位 nm
    wavelength: 波长，单位 nm
    返回: 反射率 R (0~1)
    结构: Air / H / L / H / L / Glass
    """
    n_list = [1.0, n_H, n_L, n_H, n_L, n_s]
    d_list = [np.inf] + list(d) + [np.inf]

    # 每层的光学厚度（相位）
    delta = []
    for i in range(1, len(d_list) - 1):
        delta.append(2 * np.pi * n_list[i] * d_list[i] / wavelength)

    # 构建传输矩阵
    # 从最后一层开始往前乘
    M = np.array([[1, 0], [0, 1]], dtype=complex)

    for i in range(len(d_list) - 2, 0, -1):
        n = n_list[i]
        # 界面矩阵
        if i < len(d_list) - 1:
            n_next = n_list[i + 1]
        else:
            n_next = n_list[-1]

        # 传输矩阵 = 界面矩阵 × 传播矩阵
        # 界面矩阵 (从 n 到 n_next)
        r = (n - n_next) / (n + n_next)
        t = 2 * n / (n + n_next)
        D = np.array([[1, r], [r, 1]], dtype=complex) / t

        # 传播矩阵
        P = np.array([
            [np.exp(-1j * delta[i - 1]), 0],
            [0, np.exp(1j * delta[i - 1])]
        ], dtype=complex)

        M = D @ P @ M

    # 最外层界面
    n0 = n_list[0]
    n1 = n_list[1]
    r01 = (n0 - n1) / (n0 + n1)
    t01 = 2 * n0 / (n0 + n1)
    D0 = np.array([[1, r01], [r01, 1]], dtype=complex) / t01

    M_total = D0 @ M

    # 反射系数
    r_total = M_total[1, 0] / M_total[0, 0]
    R = np.abs(r_total) ** 2
    return R


def generate_dataset(n_samples, seed):
    """生成 n_samples 个随机样本"""
    np.random.seed(seed)
    wavelengths = np.arange(400, 810, 10)

    thicknesses = np.random.uniform(40, 180, size=(n_samples, 4))
    spectra = np.zeros((n_samples, 41))

    for i in range(n_samples):
        for j, wl in enumerate(wavelengths):
            spectra[i, j] = calc_reflectance(thicknesses[i], wl)

    return thicknesses, spectra, wavelengths
