实验指导原文 : [https://blog.csdn.net/qq_51097294/article/details/142999211](https://blog.csdn.net/qq_51097294/article/details/142999211) 

前面的讲解就是书中[5.2]节内容 静态路由配置命令 :

```shell
ip route-static 目的网络地址 目的网络掩码  下一跳网络地址
```

---

本文无创新点

---

# 实验过程

## PC

按照图中配置

## 路由器配置

[注意要先启动]

```shell
# AR1
system-view
interface GigabitEthernet 0/0/0
ip address 192.168.10.254 24
q
interface GigabitEthernet 0/0/1
ip address 10.0.0.1 24
q

# AR2
system-view
interface GigabitEthernet 0/0/0
ip address 10.0.0.2 24
q
interface GigabitEthernet 0/0/1
ip address 10.0.1.2 24
q

# AR3
system-view
interface GigabitEthernet 0/0/0
ip address 10.0.1.1 24
q
interface GigabitEthernet 0/0/1
ip address 192.168.20.254 24
q
```

配置完成后应该检查是否配置成功 使用`Huawei`设备的命令

```shell
display ip interface brief

# AR1
*down: administratively down
^down: standby
(l): loopback
(s): spoofing
The number of interface that is UP in Physical is 3
The number of interface that is DOWN in Physical is 0
The number of interface that is UP in Protocol is 3
The number of interface that is DOWN in Protocol is 0

Interface                         IP Address/Mask      Physical   Protocol  
GigabitEthernet0/0/0              192.168.10.254/24    up         up        
GigabitEthernet0/0/1              10.0.0.1/24          up         up        
NULL0                             unassigned           up         up(s) 

# AR2
Interface                         IP Address/Mask      Physical   Protocol  
GigabitEthernet0/0/0              10.0.0.2/24          up         up        
GigabitEthernet0/0/1              10.0.1.2/24          up         up        
NULL0                             unassigned           up         up(s)     
[Huawei]

# AR3
Interface                         IP Address/Mask      Physical   Protocol  
GigabitEthernet0/0/0              10.0.1.1/24          up         up        
GigabitEthernet0/0/1              192.168.20.254/24    up         up        
NULL0                             unassigned           up         up(s)     
[Huawei]
```

此时直接`ping`会丢包 因为不是静态路由

```shell
PC>ping 192.168.20.1

Ping 192.168.20.1: 32 data bytes, Press Ctrl_C to break
Request timeout!
Request timeout!
Request timeout!

--- 192.168.20.1 ping statistics ---
  3 packet(s) transmitted
  0 packet(s) received
  100.00% packet loss
```

## 配置静态路由

```shell
<Huawei>display ip routing-table
```

发现没有到`10.0.0.1`的转发

配置静态路由，此步骤是将PC1的请求报文能够转发到AR2上

```shell
# AR1
<Huawei> system-view  # 从用户视图进入系统视图
Enter system view, return user view with Ctrl+Z.
[Huawei]  # 此时提示符变为 [ ]，表示进入系统视图
[Huawei]sysname AR1
[AR1] ip route-static 192.168.20.0 255.255.255.0 10.0.0.2  # 此时命令可正常执行

# AR2
# 从用户视图进入系统视图
<Huawei> system-view
Enter system view, return user view with Ctrl+Z.
[Huawei] sysname AR2
# 1. 访问PC1所在网段192.168.10.0/24，下一跳指向AR1的GE0/0/1接口（10.0.0.1）
[AR2] ip route-static 192.168.10.0 255.255.255.0 10.0.0.1

# 2. 访问PC2所在网段192.168.20.0/24，下一跳指向AR3的GE0/0/0接口（10.0.1.1）
[AR2] ip route-static 192.168.20.0 255.255.255.0 10.0.1.1

# AR3
<Huawei> system-view
Enter system view, return user view with Ctrl+Z.
[Huawei] sysname AR3

# 配置静态路由：
# 访问PC1所在网段192.168.10.0/24，下一跳指向AR2的GE0/0/1接口（10.0.1.2）
[AR3] ip route-static 192.168.10.0 255.255.255.0 10.0.1.2
```

配置完后检查

```
display ip routing-table
```

出现(对应的)

```shell
192.168.20.0/24  Static  60   0          RD   10.0.0.2        GigabitEthernet 0/0/1
```

说明配置成功

```shell
# 好像不能直接ping通 可能我是操作有问题
# 检查发现是AR1添加错误
192.168.20.0/24  Static  60   0          RD   10.0.0.2        GigabitEthernet 0/0/1
# 需要先删除再添加
undo ip route-static 192.168.20.0 255.255.255.0 10.0.0.2
ip route-static 192.168.20.0 255.255.255.0 10.0.1.1
```

## Final

```shell
ping 192.168.0.1
```

## Result

```shell
PC>ping 192.168.20.1

Ping 192.168.20.1: 32 data bytes, Press Ctrl_C to break
From 192.168.20.1: bytes=32 seq=1 ttl=125 time=47 ms
From 192.168.20.1: bytes=32 seq=2 ttl=125 time=31 ms
From 192.168.20.1: bytes=32 seq=3 ttl=125 time=32 ms
From 192.168.20.1: bytes=32 seq=4 ttl=125 time=31 ms
From 192.168.20.1: bytes=32 seq=5 ttl=125 time=31 ms

--- 192.168.20.1 ping statistics ---
  5 packet(s) transmitted
  5 packet(s) received
  0.00% packet loss
  round-trip min/avg/max = 31/34/47 ms
```

```shell
PC>ping 192.168.10.1

Ping 192.168.10.1: 32 data bytes, Press Ctrl_C to break
From 192.168.10.1: bytes=32 seq=1 ttl=125 time=47 ms
From 192.168.10.1: bytes=32 seq=2 ttl=125 time=31 ms
From 192.168.10.1: bytes=32 seq=3 ttl=125 time=47 ms
From 192.168.10.1: bytes=32 seq=4 ttl=125 time=31 ms
From 192.168.10.1: bytes=32 seq=5 ttl=125 time=31 ms

--- 192.168.10.1 ping statistics ---
  5 packet(s) transmitted
  5 packet(s) received
  0.00% packet loss
  round-trip min/avg/max = 31/37/47 ms
```

# 保存

很重要的一点是我之前都没有`save` .

# 直接写结果

-   `sys` 是有效指令，是 `system-view` 的缩写，用于进入系统视图
-   `q` 是华为设备（VRP 系统）中 **`quit` 命令的缩写**，核心作用是「退出当前视图，返回上一级视图」，是网络配置中高频使用的指令（类似文件管理器的 “返回上一级”）。

```shell
## AR1
system-view
interface GigabitEthernet 0/0/0
ip address 192.168.10.254 24
q
interface GigabitEthernet 0/0/1
ip address 10.0.0.1 24
q

# 如果需要 从用户视图进入系统视图 后面省略
# <Huawei> system-view
# Enter system view, return user view with Ctrl+Z.
# [Huawei]  # 此时提示符变为 [ ]，表示进入系统视图
# sysname AR1 (如果需要)
ip route-static 192.168.20.0 255.255.255.0 10.0.0.2

## AR2
system-view
interface GigabitEthernet 0/0/0
ip address 10.0.0.2 24
q
interface GigabitEthernet 0/0/1
ip address 10.0.1.2 24
q
# sysname AR2 (如果需要)
# 1. 访问PC1所在网段192.168.10.0/24，下一跳指向AR1的GE0/0/1接口（10.0.0.1）
ip route-static 192.168.10.0 255.255.255.0 10.0.0.1

# 2. 访问PC2所在网段192.168.20.0/24，下一跳指向AR3的GE0/0/0接口（10.0.1.1）
ip route-static 192.168.20.0 255.255.255.0 10.0.1.1

## AR3
system-view
interface GigabitEthernet 0/0/0
ip address 10.0.1.1 24
q
interface GigabitEthernet 0/0/1
ip address 192.168.20.254 24
q
# sysname AR3 (如果需要)
# 访问PC1所在网段192.168.10.0/24，下一跳指向AR2的GE0/0/1接口（10.0.1.2）
ip route-static 192.168.10.0 255.255.255.0 10.0.1.2
```

```shell
## 测试 (如果你前面直接复制 做的太快 开始可能会 `Request timeout!` ) 等几秒钟重试就好了
# 192.168.10.1->192.168.20.1
PC>ping 192.168.20.1

Ping 192.168.20.1: 32 data bytes, Press Ctrl_C to break
From 192.168.20.1: bytes=32 seq=1 ttl=125 time=47 ms
From 192.168.20.1: bytes=32 seq=2 ttl=125 time=31 ms
From 192.168.20.1: bytes=32 seq=3 ttl=125 time=32 ms
From 192.168.20.1: bytes=32 seq=4 ttl=125 time=31 ms
From 192.168.20.1: bytes=32 seq=5 ttl=125 time=31 ms

--- 192.168.20.1 ping statistics ---
  5 packet(s) transmitted
  5 packet(s) received
  0.00% packet loss
  round-trip min/avg/max = 31/34/47 ms
  
# 192.168.20.1->192.168.10.1
PC>ping 192.168.10.1

Ping 192.168.10.1: 32 data bytes, Press Ctrl_C to break
From 192.168.10.1: bytes=32 seq=1 ttl=125 time=47 ms
From 192.168.10.1: bytes=32 seq=2 ttl=125 time=31 ms
From 192.168.10.1: bytes=32 seq=3 ttl=125 time=47 ms
From 192.168.10.1: bytes=32 seq=4 ttl=125 time=31 ms
From 192.168.10.1: bytes=32 seq=5 ttl=125 time=31 ms

--- 192.168.10.1 ping statistics ---
  5 packet(s) transmitted
  5 packet(s) received
  0.00% packet loss
  round-trip min/avg/max = 31/37/47 ms
```

```shell
# 最后可以选择保存 在用户视图 like <AR1> , save 命令
save
  The current configuration will be written to the device. 
  Are you sure to continue? (y/n)[n]:y
  It will take several minutes to save configuration file, please wait.........
  Configuration file had been saved successfully
  Note: The configuration file will take effect after being activated
```

