# 伦文的学习笔记网站

这是一个基于 Material for MkDocs 的个人 Markdown 笔记网站模板，包含：

- 首页正方形笔记卡片
- Markdown 页面
- MathJax 数学公式
- 中文搜索
- 代码高亮与复制按钮
- 浅色/深色模式
- GitHub Pages 自动部署

## 一、本地运行

Windows PowerShell：

```powershell
cd lunwen-notes-site
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

然后访问：

```text
http://127.0.0.1:8000
```

## 二、增加一篇笔记

1. 在 `docs` 下创建 Markdown 文件，例如：

```text
docs/recommendation/din.md
```

2. 在 `mkdocs.yml` 的 `nav` 中增加：

```yaml
- DIN 论文笔记: recommendation/din.md
```

3. 在 `docs/index.md` 复制一个 `<a class="note-card">...</a>` 卡片，并修改链接和标题。

## 三、发布到 GitHub Pages

1. 在 GitHub 新建一个公开仓库，例如 `notes`。
2. 将整个项目推送到仓库的 `main` 分支。
3. 打开仓库 `Settings -> Pages`。
4. 确认发布来源为 `Deploy from a branch`，分支选择 `gh-pages` 和 `/ (root)`。
5. 第一次推送后，GitHub Actions 会自动生成 `gh-pages` 分支。

网站地址通常是：

```text
https://你的GitHub用户名.github.io/notes/
```

建议随后在 `mkdocs.yml` 中取消 `site_url` 的注释，并替换为真实地址。

## 四、公式写法

行内公式：

```markdown
设 $x\in\mathbb R^n$。
```

独立公式：

```markdown
$$
\min_x f(x)+\lambda\lVert x\rVert_1
$$
```
