# 构建镜像

构建 python2.7、python3.6 的基础和运行镜像。

## 登录 Docker 仓库

```
$ make login DOCKER_USERNAME=<账号> DOCKER_PASSWORD=<密码>
$ make build ENVIRONMENT=basic
$ make build ENVIRONMENT=basic PY_VERSION=python2.7
$ make build ENVIRONMENT=basic PY_VERSION=python3.6
```

## 模型运行镜像

```
$ make build ENVIRONMENT=build
$ make build ENVIRONMENT=build PY_VERSION=python2.7
$ make build ENVIRONMENT=build PY_VERSION=python3.6
```

# 推送镜像

推送镜像到 https://docker.io 的 BGE 团队。

## 基础环境镜像

```
$ make push ENVIRONMENT=basic
$ make push ENVIRONMENT=basic PY_VERSION=python2.7
$ make push ENVIRONMENT=basic PY_VERSION=python3.6
```

## 模型运行镜像

```
$ make push ENVIRONMENT=build
$ make push ENVIRONMENT=build PY_VERSION=python2.7
$ make push ENVIRONMENT=build PY_VERSION=python3.6
```

# 启动容器

退出容器后自动删除。

```
make run ENVIRONMENT=build PY_VERSION=python2.7
make run ENVIRONMENT=build PY_VERSION=python3.6
```

# 后端运行容器

退出容器后，自动不会自动删除，将在后端继续运行。

```
make run ENVIRONMENT=build PY_VERSION=python2.7
make run ENVIRONMENT=build PY_VERSION=python3.6
```


# 删除无用镜像

```
make clean
```