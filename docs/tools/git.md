# Git 常用操作

## 查看分支

```powershell
PS> git branch
  pv_ctr_model
* pv_ctr_model_fumilun
```

星号表示当前所在分支。

## 提交并推送

```powershell
git add .
git commit -m "update notes"
git push
```

## 查看提交历史

```powershell
git log --oneline --decorate --graph -10
```
