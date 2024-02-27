# ThenSync
thensync 是一个基于 Python 的备份工具，它可以将指定目录下的备份到另一个目录下。thensync 的特点是可以将备份到多个目录下。thensync 的使用非常简单，只需要在配置文件中指定需要同步的目录和文件类型即可。

## 要求
- Python 3.10+
- Linux

## 安装
运行 `python3 init.py --action install` 来初始化运行 thensync 所需的包。
> 如果你不使用系统自带的 Python，**请勿**使用 `init.py` 文件，需要手动安装下方列出的包。
```bash
pyyaml
boto3
```


## 使用
1. 复制 `config.yaml.example` 文件为 `config.yaml`。
2. 在 `config.yaml` 文件中配置需要同步的目录和文件类型。
3. 在定时任务（例如 cron）中运行 `thensync.py` 文件。
