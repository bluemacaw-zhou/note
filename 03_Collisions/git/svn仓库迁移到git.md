## 从项目release分支导出提交记录 并生成对应的.git目录

```shell
# 切换到合适的目录下执行
# 比如说D:\shzhou.michael\SVN\Src\git
git svn clone -r 1962485:HEAD http://techsrv.wind.com.cn:8080/svn/Src/Wind.IM.FixRelay/release/ Wind.IM.FixRelay
```

## 查看进度 (如果同步失败) 

```shell
git log -1 --all
```

# 从断点处从新同步

```shell
git svn fetch -r 2260125:2310124
git svn fetch -r 2610125:HEAD
```

## 创建本地分支

```txt
打开项目目录 D:\shzhou.michael\SVN\Src\git\Wind.IM.FixRelay
创建dev分支
```

## 设置git远端仓库地址
```shell
#切换到之前svn同步到git的目录
#如D:\shzhou.michael\SVN\Src\git\Wind.IM.FixRelay
# 设置一个叫wind的远端仓库
git remote add wind https://git.wind.com.cn/SRC/Wind.IM.FixRelay

# 执行fetch指令 让本地仓库感知到远端有那些分支
git fetch wind
```

## 关联分支

```shell
# svn同步到git时 默认有一个master分支 
# 后来我们本地创建了一个dev分支
# 现在我们需要将本地的master关联远端的release
# 本地的dev关联远端的dev
git branch -u wind/dev dev
```

## 强制同步远端代码

```shell
git pull wind dev --allow-unrelated-histories
```

## 上传代码

```shell
git push wind dev
```

