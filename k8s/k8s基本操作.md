## 查看集群状态

```shell
kubectl get nodes -owide
```

## 查看事件

```shell
kubectl get events -n test
```

## 查看 pod

```shell
kubectl describe pod/nfs-client-provisioner-75b96b58b8-7pbb5 -n nfs-storage
```


## 查看 pod 运行日志

```shell
kubectl logs pod/nfs-client-provisioner-75b96b58b8-7pbb5 -n nfs-storage
```

## Json 格式输出 pod 的详细信息

```shell
kubectl get pod/calico-node-sc222 -n kube-system -o json
```

## 编辑当前的 pod

```shell
kubectl edit pod/calico-node-sc222 -n kube-system
```


## 查看命名空间

```shell
kubectl config view --minify --output 'jsonpath={..namespace}'
```

## 切换命名空间

```shell
kubectl config set-context --current --namespace=monitoring
```

## 执行 yaml 资源清单

```shell
kubectl apply -f create-namespace.yaml
```


## 删除资源清单中创建的所有组件

```shell
kubectl delete -f create-namespace.yaml
```
