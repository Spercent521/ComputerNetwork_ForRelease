# Computer Network Course Repository

本仓库包含《计算机网络：自顶向下方法》课程的学习资料、代码实现和实验文档。

## 目录结构

- **code_chap2/**: 第2章应用层编程示例（UDP/TCP Socket编程）
- **lab/**: 实验配置与文档（eNSP网络模拟器）
- **notes/**: 各章节学习笔记（Markdown格式）
- **Programming_Assignments/**: 编程作业（Web服务器、UDP Pinger、SMTP客户端、视频流）
- **期末复习集合/**: 期末复习资料和思维导图
- **知识点思维导图/**: 各章节知识点思维导图

## 大文件说明

以下工具安装包因超过 GitHub 文件大小限制而被忽略，请从官方渠道下载：

| 文件名 | 官方下载链接 | 版本 | 大小 | 说明 |
| --- | --- | --- | --- | --- |
| lab/Wireshark-win64-3.4.8.exe | [Wireshark官网](https://www.wireshark.org/download.html) | v3.4.8 | 68.07 MB | 网络协议分析工具 |
| lab/VirtualBox-5.2.30-130521-Win.exe | [VirtualBox旧版本](https://www.virtualbox.org/wiki/Download_Old_Builds_5_2) | v5.2.30 | 110.53 MB | 虚拟机软件 |
| lab/eNSP_SetupV100R003C00SPC100.exe | [华为官网](https://support.huawei.com/enterprise/zh/tool/ensp) | V100R003C00SPC100 | 542.42 MB | 华为eNSP网络模拟器 |
| lab/WinPcap_4_1_3.exe | [WinPcap官网](https://www.winpcap.org/install/) | v4.1.3 | ~1 MB | Wireshark依赖的数据包捕获库 |

## 课程设计

-   见 [Spercent521/network-curriculum_design-CUG: CUG 计算机网络课程设计](https://github.com/Spercent521/network-curriculum_design-CUG)

## 使用说明

1. Clone 本仓库后，根据上表下载所需的工具安装包
2. Python 代码示例位于 `code_chap2/` 和 `Programming_Assignments/` 目录
3. 实验配置文件为 eNSP 格式（`.topo` 文件），需配合 eNSP 使用

## 注意事项

- 本仓库不包含任何个人敏感信息
- 所有大型安装包均已从版本控制中移除，请从官方渠道下载
- 实验报告等个人文件已通过 `.gitignore` 排除
