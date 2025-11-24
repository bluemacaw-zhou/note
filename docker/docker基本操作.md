## 公司拉取镜像

```shell
docker pull 10.100.6.129:8987/<image url>
```

## 打包镜像

```shell
docker save -o pause.tar 6270bb605e12
```

## 导入镜像

```shell
docker load < pause.tar
```

## 镜像打标签

```
docker tag 6270bb605e12 registry.aliyuncs.com/google_containers/pause:3.6 
```
