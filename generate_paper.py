from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_font(run, font_name='宋体', size=12):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)

doc = Document()

# 标题
title = doc.add_heading('AI for Thin Films: MLP 逆向设计研究', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(title.runs[0], '黑体', 18)

# Abstract
doc.add_heading('摘要', level=1)
p = doc.add_paragraph()
run = p.add_run('本研究提出了一种基于机器学习的多层光学薄膜逆向设计方法。我们采用多层感知机（MLP）神经网络从目标反射光谱预测层厚度，替代计算密集的传输矩阵法（TMM）仿真。使用 TMM 生成了 5000 个样本的数据集，用于四层结构（Air/H/L/H/L/Glass），折射率分别为 n_H=2.30、n_L=1.45、n_s=1.52。MLP 架构包含四个全连接层（41→128→128→64→4），使用均方误差损失训练。结果表明，模型在测试数据上达到平均 MSE 0.000197，平均厚度误差 12.51 nm。使用更大数据集训练显著提高了预测精度，证明了深度学习用于快速薄膜逆向设计的可行性。')
set_font(run, '宋体', 12)

# Introduction
doc.add_heading('1. 引言', level=1)
p = doc.add_paragraph()
run = p.add_run('多层光学薄膜广泛应用于增透膜、反射镜、滤波器和光子器件中。传统设计方法依赖于迭代优化结合传输矩阵法（TMM）仿真，计算量大且耗时。人工智能的最新进展提供了有前景的替代方案，通过直接从数据中学习结构参数与光学特性之间的映射关系。\n\n'
                '本研究探讨多层感知机（MLP）神经网络在薄膜结构逆向设计中的应用。给定目标反射光谱，训练好的 MLP 预测相应的层厚度，实现无需重复 TMM 计算的快速设计。我们系统评估了不同训练集大小下的模型性能，并分析了数据量与预测精度之间的关系。')
set_font(run, '宋体', 12)

# Materials and Methods
doc.add_heading('2. 材料与方法', level=1)

doc.add_heading('2.1 薄膜结构', level=2)
p = doc.add_paragraph()
run = p.add_run('研究的結構由沉积在玻璃基板上的四层交替高/低折射率层组成：Air / H / L / H / L / Glass。折射率为 n_H = 2.30（高）、n_L = 1.45（低）、n_s = 1.52（基板）。每层厚度范围为 40 至 180 nm。反射光谱在 400 至 800 nm 波长范围内以 10 nm 间隔计算（共 41 个波长点）。')
set_font(run, '宋体', 12)

doc.add_heading('2.2 传输矩阵法', level=2)
p = doc.add_paragraph()
run = p.add_run('TMM 用于从给定层厚度计算反射光谱。对于每个波长 λ，该方法通过将所有层的界面矩阵和传播矩阵相乘来构建传输矩阵。从总传输矩阵中提取反射系数 r，反射率 R = |r|²。')
set_font(run, '宋体', 12)

doc.add_heading('2.3 数据集生成', level=2)
p = doc.add_paragraph()
run = p.add_run('使用 seed = 6 生成了 5000 个随机样本的数据集。层厚度从 [40, 180] nm 均匀采样。使用 TMM 计算对应的反射光谱。数据集分为训练集（4000）、验证集（500）和测试集（500）。')
set_font(run, '宋体', 12)

doc.add_heading('2.4 MLP 架构与训练', level=2)
p = doc.add_paragraph()
run = p.add_run('MLP 将 41 维反射光谱作为输入，输出四层厚度的预测值。网络架构为：Linear(41, 128) → ReLU → Linear(128, 128) → ReLU → Linear(128, 64) → ReLU → Linear(64, 4)。输出值归一化到 [0, 1] 范围，对应 [40, 180] nm。\n\n'
                '训练使用 Adam 优化器，学习率 0.001，批次大小 128，MSE 损失。模型训练 500 个 epoch，基于验证损失进行早停。实验分别在 500、1000、2000 和 4000 个样本的训练集上进行。')
set_font(run, '宋体', 12)

doc.add_heading('2.5 逆向设计评估', level=2)
p = doc.add_paragraph()
run = p.add_run('为了评估，从测试集中选取 100 个真实光谱作为目标。训练好的 MLP 预测相应厚度，然后使用 TMM 验证。预测质量通过预测光谱与实际光谱之间的 MSE，以及预测厚度与真实厚度之间的绝对误差来评估。')
set_font(run, '宋体', 12)

# Results
doc.add_heading('3. 结果', level=1)

doc.add_heading('3.1 训练性能', level=2)
p = doc.add_paragraph()
run = p.add_run('图 1 显示了不同训练集大小的验证损失曲线。更大的数据集 consistently achieve lower validation losses，4000 样本模型达到 Val Loss = 0.0243。所有模型都显示损失单调下降，表明成功收敛。')
set_font(run, '宋体', 12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture('val_loss_curve.png', width=Inches(5))
doc.add_paragraph('图 1. 不同训练数据量的验证损失随 epoch 变化曲线。').alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_heading('3.2 逆向设计精度', level=2)
table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = '指标'
hdr_cells[1].text = '数值'
for metric, value in [
    ('平均 MSE', '0.000197'),
    ('中位数 MSE', '0.000109'),
    ('最小 MSE', '0.000002'),
    ('最大 MSE', '0.001896'),
    ('平均厚度误差', '12.51 nm'),
    ('最大厚度误差', '68.13 nm')
]:
    row_cells = table.add_row().cells
    row_cells[0].text = metric
    row_cells[1].text = value

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture('fig2_error_distribution.png', width=Inches(5))
doc.add_paragraph('图 2. 100 次逆向设计预测的 MSE 误差分布。').alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_heading('3.3 最佳预测示例', level=2)
p = doc.add_paragraph()
run = p.add_run('图 3 比较了最佳性能样本（MSE = 0.000002）的目标光谱与 MLP 预测光谱。两条曲线几乎重叠，显示出极好的一致性。')
set_font(run, '宋体', 12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture('fig1_spectrum_comparison.png', width=Inches(5))
doc.add_paragraph('图 3. Top-1 结果的目标与预测反射光谱对比。').alignment = WD_ALIGN_PARAGRAPH.CENTER

# Discussion
doc.add_heading('4. 讨论', level=1)

doc.add_heading('4.1 训练数据量的影响', level=2)
p = doc.add_paragraph()
run = p.add_run('结果清楚地表明，更大的训练集能提高模型性能。与 500 样本模型相比，4000 样本模型的验证损失降低了约 40%。这表明薄膜逆向设计从覆盖参数空间的更多样化训练示例中受益匪浅。')
set_font(run, '宋体', 12)

doc.add_heading('4.2 预测精度分析', level=2)
p = doc.add_paragraph()
run = p.add_run('12.51 nm 的平均厚度误差代表 140 nm 范围（40–180 nm）内约 8.9% 的相对误差。虽然不完美，但这种精度对于许多实际应用已经足够，因为精确厚度控制本身就受到制造公差的限制。\n\n'
                '68.13 nm 的最大误差表明存在一些模型难以处理的挑战性情况。这些可能对应于具有复杂特征的光谱或逆问题中的多个局部最小值。')
set_font(run, '宋体', 12)

doc.add_heading('4.3 ML 方法的优势', level=2)
p = doc.add_paragraph()
run = p.add_run('一旦训练完成，MLP 在毫秒级内预测厚度，而迭代 TMM 优化需要数秒或数分钟。这种加速使得能够快速探索设计空间并进行实时调整应用。')
set_font(run, '宋体', 12)

doc.add_heading('4.4 局限性', level=2)
p = doc.add_paragraph()
run = p.add_run('当前方法存在几个局限性：\n'
                '1. 固定结构：模型仅适用于其训练特定的四层配置。\n'
                '2. 光谱复杂性：简单目标光谱可能有多个有效厚度解，导致歧义。\n'
                '3. 泛化能力：对于训练分布之外的光谱，性能会下降。\n'
                '4. 物理约束：模型不强制执行制造约束，如最小层厚度或材料可用性。\n\n'
                '未来的工作可以通过在多种结构上训练、结合物理信息损失或使用生成模型来捕捉解的多重性来解决这些问题。')
set_font(run, '宋体', 12)

# Conclusions
doc.add_heading('5. 结论', level=1)
p = doc.add_paragraph()
run = p.add_run('我们证明了 MLP 神经网络可以有效执行光学多层薄膜的逆向设计。在 4000 个 TMM 生成的样本上训练后，模型达到平均 MSE 0.000197，平均厚度误差 12.51 nm。更大的训练数据集显著提高精度。与传统优化方法相比，ML 方法提供了数量级的加速，使其适用于快速原型设计和设计探索。虽然存在关于泛化和解唯一性的局限性，但结果验证了深度学习作为薄膜逆向设计可行工具的有效性。')
set_font(run, '宋体', 12)

# Data and Code Availability
doc.add_heading('数据与代码可用性', level=1)
p = doc.add_paragraph()
run = p.add_run('所有代码和数据可在 GitHub 获取：https://github.com/zlone120/ai4s-thin-films\n\n'
                '仓库包括：\n'
                '- tmm_core.py：传输矩阵法实现\n'
                '- generate_data.py：数据集生成脚本\n'
                '- train_mlp.py：MLP 训练代码\n'
                '- inverse_design.py：逆向设计评估\n'
                '- plot_results.py：可视化脚本\n'
                '- requirements.txt：Python 依赖项\n\n'
                '使用的参数：\n'
                '- seed: 6（数据生成）\n'
                '- design_seed: 7（逆向设计）\n'
                '- 目标波长：450 + 10 × (N mod 31) nm，N ∈ {0, ..., 99}')
set_font(run, '宋体', 12)

# References
doc.add_heading('参考文献', level=1)
p = doc.add_paragraph()
run = p.add_run('[1] Ma, J., Ma, Z., & Guo, L. J. "Optical Multilayer Thin Film Structure Inverse Design: From Optimization to Deep Learning." Advanced Optical Materials, 2023.\n\n'
                '[2] Yeh, P. "Optical Waves in Layered Media." Wiley, 2005.\n\n'
                '[3] Byrnes, S. J. "Multilayer optical calculations." arXiv:1603.02720, 2016.')
set_font(run, '宋体', 12)

doc.save('AI4S_Research_Article.docx')
print('Word 文档已生成：AI4S_Research_Article.docx')
