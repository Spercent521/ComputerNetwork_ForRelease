`eNSP`中启动路由器发生`40`报错

-   直接原因是`eNSP`中的网络依赖于`VirtualBox`创建的虚拟网卡 并且只能使用名称为`VirtualBox Host-Only Network`的网卡
-   深层原因是 如果你之前使用过`VirtualBox`这个默认网卡估计已经被占用了 并且由于各种安全原因或者乱七八糟的原因(笔者用过很多虚拟机 双系统 各种各样的环境 以及 `Tailscale`等等 )(这里真的想夸`Tailscale` 后面也会说明)无法直接通过重命名的方法改成想要的(也就是下图展示的在`网络连接`或者`VirtualBox`直接重命名 这也是网上最容易搜索到的方法)
-   anyway 笔者的电脑管理还是太混乱了
-   甚至在注册表中直接修改`\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\NetworkSetup2`也被拒绝访问了

最有启发的工作来自 [Windows 10系统升级后VirtualBox虚拟网卡消失问题解决]([Windows 10系统升级后VirtualBox虚拟网卡消失问题解决_virtualbox host-only network #2-CSDN博客](https://blog.csdn.net/weixin_43113691/article/details/104322205)) 

![3119ad32283eaec07b9391ffa990a19a](./eNSP配置全网独家(并非)_pic/3119ad32283eaec07b9391ffa990a19a.png)

1.   按照他们的提示 下载[RunAsTI]([jschicht/RunAsTI: Launch processes with TrustedInstaller privilege](https://github.com/jschicht/RunAsTI))工具以后 运行`RunAsTI64.exe`默认你是64位操作系统 输入`regedit`打开`注册表编辑器` 这样你就可以访问上文中的`NetworkSetup2`了

2.   这时候你会看到下面的样子 让会你会照着教程删除所有的`Kernel`注册表 如果你没有注意看右边的信息的话

     **理论上应该仅仅删除命名为Virtualbox Host-Only Network Adapter的残留网卡信息**

     ![image-20251125021411793](./eNSP配置全网独家(并非)_pic/image-20251125021411793.png)

3.   但是如果你像笔者一样被这个东西折磨到凌晨两点 神志大概已经不清 删掉所有的`Kernel`并重启电脑的话 你应该已经断开了互联网 因为你删掉了所有的网卡注册表 只有坚强的`Tailscale`和万恶的`VirtualBox Host-Only Network #2`还在支撑
4.   不用担心 下面是本文的创新点 我们使用基于attention 机制的 LLM(手机版) 得到下面的结果
     1.   按 `Win` + `I` 打开设置
     2.   进入"**网络和 Internet**" > "**高级网络设置**"
     3.   找到并点击"**网络重置**"
     4.   重启
     5.   之后你的网络就好了
5.   这样你肯定删掉了`VirtualBox Host-Only Network`就能正常在`控制面板`和`VirtualBox Host-Only Network`中重命名了
6.   回到`eNSP`运行`demo`成功
     ![image-20251125022527704](./eNSP配置全网独家(并非)_pic/image-20251125022527704.png)

>   [!IMPORTANT]
>
>   如果只是希望有一个虚拟的网络端口的 为什么要依赖`VirtualBox` 为什么依赖`VirtualBox`只允许默认配置端口 我们的教育却有问题

