import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt


class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(41, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 4)
        )

    def forward(self, x):
        return self.net(x)


def train(model, X_train, y_train, X_val, y_val, epochs=500, batch_size=128, lr=0.001):
    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    train_losses, val_losses = [], []
    best_val = float('inf')
    best_state = None

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for xb, yb in loader:
            pred = model(xb)
            loss = criterion(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        train_losses.append(epoch_loss / len(loader))

        model.eval()
        with torch.no_grad():
            val_loss = criterion(model(X_val), y_val).item()
        val_losses.append(val_loss)

        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}

        if (epoch + 1) % 100 == 0:
            print(f"  Epoch {epoch+1}/{epochs} | Train: {train_losses[-1]:.6f} | Val: {val_losses[-1]:.6f}")

    if best_state is not None:
        model.load_state_dict(best_state)
        print(f"  已恢复最佳模型 (Val Loss: {best_val:.6f})")

    return train_losses, val_losses


if __name__ == '__main__':
    train_data = np.load('train.npz')
    val_data = np.load('val.npz')

    # 归一化：厚度缩放到 0~1
    d_min, d_max = 40.0, 180.0
    y_train_norm = (train_data['x'] - d_min) / (d_max - d_min)
    y_val_norm = (val_data['x'] - d_min) / (d_max - d_min)

    X_train = torch.FloatTensor(train_data['y'])
    y_train = torch.FloatTensor(y_train_norm)
    X_val = torch.FloatTensor(val_data['y'])
    y_val = torch.FloatTensor(y_val_norm)

    data_sizes = [500, 1000, 2000, 4000]
    results = {}

    for size in data_sizes:
        print(f"\n===== 训练数据量: {size} =====")
        model = MLP()
        train_losses, val_losses = train(model, X_train[:size], y_train[:size], X_val, y_val)
        results[size] = {'train_losses': train_losses, 'val_losses': val_losses}

    plt.figure(figsize=(10, 6))
    for size in data_sizes:
        plt.plot(results[size]['val_losses'], label=f'{size} samples')
    plt.xlabel('Epoch')
    plt.ylabel('Validation MSE Loss (normalized)')
    plt.title('MLP Validation Loss vs Training Data Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('val_loss_curve.png', dpi=150)
    print("\n训练曲线已保存为 val_loss_curve.png")

    # 用全部数据训练最终模型
    print("\n===== 用全部 4000 条数据训练最终模型 =====")
    model = MLP()
    train(model, X_train, y_train, X_val, y_val, epochs=500)
    torch.save(model.state_dict(), 'mlp_best.pth')

    # 保存归一化参数
    np.savez('norm_params.npz', d_min=d_min, d_max=d_max)
    print("最佳模型已保存为 mlp_best.pth")
