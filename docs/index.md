---
hide:
  - navigation
  - toc
---

# 伦文的学习笔记

记录推荐算法、优化理论、TensorFlow 与工程工具。点击卡片进入对应 Markdown 笔记。

<div class="note-grid">

<a class="note-card" href="recommendation/dcin/">
  <span class="note-card__category">推荐算法 · 论文</span>
  <h2>DCIN</h2>
  <p>决策上下文建模、CIU、AIAU 与历史页面兴趣聚合。</p>
  <span class="note-card__link">查看笔记 →</span>
</a>

<a class="note-card" href="recommendation/dlf/">
  <span class="note-card__category">推荐算法 · 论文</span>
  <h2>DLF</h2>
  <p>低阶显式、高阶显式与隐式特征交互。</p>
  <span class="note-card__link">查看笔记 →</span>
</a>

<a class="note-card" href="recommendation/mmoe/">
  <span class="note-card__category">推荐算法 · 基础</span>
  <h2>MMoE</h2>
  <p>专家网络、任务门控与多任务学习的基本结构。</p>
  <span class="note-card__link">查看笔记 →</span>
</a>

<a class="note-card" href="mathematics/optimization/">
  <span class="note-card__category">数学 · 最优化</span>
  <h2>优化理论</h2>
  <p>近端算法、约束优化与谱聚类研究笔记。</p>
  <span class="note-card__link">查看笔记 →</span>
</a>

<a class="note-card" href="tensorflow/tf1/">
  <span class="note-card__category">工程 · 深度学习</span>
  <h2>TensorFlow 1.x</h2>
  <p>工业代码中常见的变量域、张量形状与 Mask。</p>
  <span class="note-card__link">查看笔记 →</span>
</a>

<a class="note-card" href="tools/git/">
  <span class="note-card__category">工具 · Git</span>
  <h2>Git 操作</h2>
  <p>分支切换、提交、推送与代码回退。</p>
  <span class="note-card__link">查看笔记 →</span>
</a>

</div>

## 数学公式测试

行内公式：设当前商品表示为 $\mathbf{x}_t\in\mathbb{R}^{D}$。

独立公式：

$$
\operatorname{Attention}(Q,K,V)
=
\operatorname{Softmax}\left(\frac{QK^\top}{\sqrt d}\right)V.
$$
