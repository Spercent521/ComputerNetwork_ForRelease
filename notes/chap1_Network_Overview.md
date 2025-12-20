# chap1 : Computation network and Internet

## 1.1 what is network

In this book, we’ll use the public Internet(公用互联网), a specific computer network, as our principal vehicle(主要载体) for discussing computer networks and their protocols.

 But what is the Internet? There are a couple of ways to answer this question. 

-   First, we can describe the [nuts and bolts](https://zhidao.baidu.com/question/5654469.html) of the Internet, that is, the **basic hardware and software components** that make up the Internet. 
-   Second, we can describe the Internet in terms of a networking infrastructure that provides services to distributed applications.

### 1.1.1 A Nuts-and-Bolts Description

Indeed, the term <u>computer network</u> is beginning to sound a bit dated, given the many nontraditional devices that are being hooked up to the Internet. In Internet jargon(术语), all of these devices are called hosts(主机) or end systems(端系统). 

![image-20250710222907069](chap1_Network_Overview_pic\NetworkOverview.png)

End systems are connected together by a network of **communication links(通信链路)** and **packet switches(分组交换机)** . The types of communication links include coaxial cable, copper wire, optical fiber, and radio spectrum. Different links can transmit data at different rates, with the **transmission rate(传输速率) of a link measured in bits/second**. When one end system has data to send to another end system, the sending end system segments the data and adds header bytes to each segment. The resulting packages of information, known as **packets(分组/数据包)** in the jargon of computer networks, are then sent through the network to the destination end system, where they are reassembled into the original data.

**A packet switch takes a packet arriving on one of its incoming communication links and forwards that packet on one of its outgoing communication links.** Packet switches come in many shapes and flavors, but the two most prominent types in today’s Internet are **routers** and **link-layer switches**. Both types of switches forward packets toward their ultimate destinations. 

-   Link-layer switches are typically used in access networks, while routers are typically used in the network core.

The sequence of communication links and packet switches traversed by a packet from the sending end system to the receiving end system is known as a **route** or **path** through the network.

通过的这一系列的通信链路和分组交换机(一个packet从发送端到接收端)就是route/path。

---

端系统通过**因特网服务提供商 ISP Internet Service Provider**接入因特网。这个名称不是太好 可能翻译成“提供者”更好。

**每个ISP自身就是一个由多台分组交换机和多段通信链路组成的网络。**

**ISP的作用**主要包括：

1.   提供端系统接入互联网的服务
2.   分配IP地址 。 ISP会为每一个联网设备静态或者动态的分配一个IP地址 
3.   提供域名解析服务DNS 。ISP会将网站域名www.google.com翻译成难记的IP地址,如`142.251.42.206`. 
4.   数据中转 数据通常要经过**你的ISP**转到**多个骨干ISP**转到**目标网站的ISP**

These lower-tier ISPs are inter-connected through national and international upper-tier ISPs. An upper-tier ISP consists of high-speed routers interconnected with high-speed fiber-optic links. Each ISP network, whether upper-tier or lower-tier, is 21 managed independently, runs the IP protocol (see below), and conforms to certain naming and address conventions.

---

End systems, packet switches, and other pieces of the Internet run **protocols** that control the sending and receiving of information within the Internet. 

网络中的任何设备都要运行一系列协议 这些协议控制着网络中信息的接收和发送。

**The Transmission Control Protocol (TCP,传输控制协议)** and **the Internet Protocol (IP,网络协议)** are two of the most important protocols in the Internet. The IP protocol specifies the format of the packets that are sent and received among routers and end systems. The Internet’s principal protocols are collectively known as TCP/IP. 

因特网中最重要的两个协议是**TCP协议**和**IP协议**,我们可以简称为**TCP/IP**协议。

**IP协议定义了在路由器和端系统之间接收和发送信息的分组格式。**

---

每个人都应该认同、理解和遵守这些协议,这样人们就能创造协同工作的系统和产品。

---

### 1.1.2 A Services Description 

互联网的另一个作用就是为各种**分布式应用程序**提供网络服务,因为这些应用程序都是在端系统上运行的。具体的场景就是你的作品怎样发送给其他设备。

这就需要用到**套接字接口socket interface**,这个接口规定了运行在一个端系统上的程序,通过因特网基础设施,向另一个在端系统上的特定目的地程序交付数据的方式。可以类比邮政系统发送信件来理解。

### 1.1.3 What Is a Protocol?

只有使用同一套协议(这里不考虑兼容的情况)的人才能交互,比如讲礼貌的人和不讲礼貌的人可能就很难交互上。

the exchange of messages and the actions taken when these messages are sent and received are the key defining elements of a protocol: 

协议的主要作用是定义了message在传送(接收和发送)中的一系列行为。

>   [!NOTE]
>
>   A protocol defines the format and the order of messages exchanged between two or more communicating entities, as well as the actions taken on the transmission and/or receipt of a message or other event. 

The Internet, and computer networks in general, make extensive use of protocols. Different protocols are used to accomplish different communication tasks. As you read through this book, you will learn that some protocols are simple and straightforward, while others are complex and intellectually deep. 

**Mastering the field of computer networking is equivalent to understanding the what, why, and how of networking protocols.**

掌握计算机网络领域知识的过程就是理解网络协议的构成、原理和工作方式的过程。

>   [!IMPORTANT]
>
>   下面的讲述逻辑是从网络边缘的设备逐步介绍到网络核心的设备。
>
>   -   网络边缘 ：端系统和运行在端系统上的应用 离用户端最近 是数据的起点或终点。
>
>   -   网络核心 = 运营商的骨干网 + 路由器/交换机等基础设施,负责把边缘产生的数据高效地搬来搬去。
>
>       ​		 =  核心设备 离用户端最远 一般不跑用户端的应用程序 而是专门负责转发和选择链路

## 1.2 The Network Edge

端系统之所以被称为端系统 是因为他们位于因特网的边缘 。 他们具体包括了桌面计算机(个人计算机)、服务器和移动计算机,另外越来越多的物品正作为端系统与因特网相连。

**端系统也称为主机(host),因为它们运行应用程序。**

主机也会进一步分为客户端(client)和服务器(server)。服务器集群可以被称作为**数据中心**,例如,谷歌有若干个数据中心用来提供搜索服务,每个数据中心都有几万台以上的服务器。

### 1.2.1 Access Networks

Access Networks(接入网)不是一种行为,而是将端系统**物理**连接到其**边缘路由器edge router**的网络。

**边缘路由器edge router**是端系统到任何其他远程端系统的路径上的**第一台路由器**。

>   [!NOTE]
>
>   【这个分类有些过时】接入链路和使用接入网的几种环境：
>
>   1.   家庭接入：DSL、电缆、FTTH、拨号和卫星
>   2.   企业和家庭接入：以太网和WiFi
>   3.   广域无线接入：对应我们使用的流量 在基站一定范围内就可以使用。

在越来越多的环境中 使用**局域网LAN**是主要的将端系统连接到边缘路由器的方式。

两种最广泛的局域网技术就是：以太网 和 无线LAN技术-WiFi

### 1.2.2 Physical Media

**物理媒介Physical Medium**分为两种类型：**引导型媒体Guided Media**和**非引导型媒体Unguided Media**。

【物理链路的材料成本是相当便宜的】

【双绞铜线 同轴电缆 光纤 陆地无线电信道 卫星无线电信道】

- **双绞铜线**：一种由两根绝缘铜导体按特定扭距绞合而成的有线传输媒介,通过差分电信号在百米级距离内实现局域网数字通信。  
- **同轴电缆**：由中心铜导体、绝缘介质、屏蔽铜网及外护套构成的同轴结构,利用受控阻抗传输高频电信号,广泛应用于有线电视与宽带接入。  
- **光纤**：以高纯度石英玻璃为纤芯、包层折射率差异实现全内反射,通过激光或 LED 的光信号在长距离、高带宽、低衰减条件下完成大容量数据传送。  
- **陆地无线电信道**：基于地面基站与移动终端之间的射频电磁波传播,依托蜂窝或局域无线协议,在数百米至数十千米范围内提供移动或固定无线接入。  
- **卫星无线电信道**：利用地球同步轨道或其他轨道卫星作为中继转发节点,通过上行/下行微波链路实现跨洲际、跨海洋的超视距无线通信。

## 1.3 The Network Core

### 1.3.1 Packet Switching

为了从源端系统向目的端系统发送Message,源端系统将长报文划分为较小的数据块,这个过程称为**分组Packet**。

在源端系统和目的地之间 **每个分组都通过通信链路和分组交换机传送**。

分组交换机Packet Switch分为两类 **路由器Router**和**链路层交换机Link-layer Switch**.

分组传送的速率就是该链路的最大传送速率。

So, if a source end system or a packet switch is sending a packet of L bits over a link with transmission rate R bits/sec, then the time to transmit the packet is L /R seconds.

If one of the links is congested because other packets need to be transmitted over the link at the same time, then the packet will have to wait in a buffer at the sending side of the transmission link and suffer a delay. 

**The Internet makes its best effort to deliver packets in a timely manner, but it does not make any guarantees.**

#### 存储转发传输

多数分组交换机在链路的输入端使用**存储转发传输store-and-forward transmission**机制。

就是指：在交换机能够开始发送该分组的第一个比特之前、必须接收到整个分组。

通过计算,如果一个分组通过由N条速率均为R的链路组成的路径,那么,所有数据都会通过$N-1$台路由器；那么,总延迟就是：
$$
d_{end\_to\_end} = N\times \frac{L}{R}
$$
如果扩展到P个分组呢？
$$
d_{end\_to\_end} = N\times \frac{L}{R}+(P-1) \times \frac{L}{R}
$$

#### 排队延时和分组丢失

每台分组交换机有多条链路与之相连,对于每条链路,该分组交换具有一个**缓存输出output buffer/输出队列output queue**,用于存储路由器准备发往那条链路的分组。
如果到达的分组需要传输到某条链路,而这条链路正忙于传输其他分组,该到达的分组必须在传输缓存中等待。这个等待的过程被称作排队**延迟queuing delay**。如果队列大小被用尽,那么新到达的或者已经到达分组就会被丢失,称为**分组丢失packet loss**。

#### 转发表和路由选择协议

>   [!NOTE]
>
>   路由器可以决定信息转发的方向。
>
>   【实际上在不同的计算机网络中有不同的方式 下面主要介绍的时因特网中的转发方式】

**在因特网中,每个端系统都具有一个IP地址。当源主机要想目的端系统发送一个分组时,源就在该分组的首部包含了目的地的IP地址。当每一个分组到达网络中的路由器时,路由器就检查该分组的一部分,并向一台相邻路由器转发该分组。**

**这个过程再具体一些,每台路由器都具有一个转发表Forwarding Table,用于将目的地址或者目的地址的一部分映射成输出链路。路由器通过差表就可以找到对应的输出链路。**

---

可以举一个生动的例子：

我现在拿到一个目的地地址`佛罗里达州奥兰多市的Lakeside Drive街156号`。
那么因为我要去佛罗里达,所以第一个引路人告诉我要先去一条州际公路；
进入佛罗里达后,第二个引路人看到我要去奥兰多,所以告诉我要沿着某条公路继续走到奥兰多；
到达奥兰多以后,第三个引路人看到我要去某某街,于是又告诉我要怎么走；
最后到了这条街,我问了最后一个路人,他告诉我156号在哪里。
最后我到了目的地`佛罗里达州奥兰多市的Lakeside Drive街156号`。

---

1.   至于转发表是如何设置的,会在`chap5`中详细介绍。一个用来启发的关键词是：路由选择协议。
2.   `linux` 中可以使用`routetrace`工具查看具体的路由路径。`windows`中可以用内置的`tracert`平替一下。
3.   在`docker`中可以使用`nali`工具解析IP地址属地。

### 1.3.2 Circuit Switching

通过网络链路和交换机移动数据有两种基本方式：**电路交换**和**分组交换**。

电路交换古老但没有完全过时,应该把电路交换和分组交换提升到**同等重要**的地位上。

#### Multiplexing in Circuit-Switched Networks

有线链路中的电路是通过 **频分复用** 或 **时分复用** 来实现的。

>   [!NOTE]
>
>   此外也需要注意：**码分复用(CDM - Code Division Multiplexing)**,特别是在网络中广泛应用的**码分多址(CDMA - Code Division Multiple Access)**
>
>   -   **FDM(频分复用)**：像把大厅分成几个小房间,每个房间里的人用一种语言(如中文、英文、法文)交谈,互不干扰。
>   -   **TDM(时分复用)**：像所有人都在一个大房间里,但大家轮流说话,一个人说完下一个人再说。
>   -   **CDMA(码分复用)**：**像所有人都在同一个大房间里同时说话,但每对交谈者使用一种独一无二的语言(比如一对用中文,一对用英文,一对用日文)。** 尽管环境很嘈杂,但只要你懂你的伙伴说的那种语言,你就能从一片噪声中清晰地听懂他/她在说什么,而其他对话对你来说只是背景噪音。

#### 频分复用 FDM

![image-20250913225929480](chap1_Network_Overview_pic\FDM_P20.png)

-   频分复用应该想象成把一条大道(**频谱**)划分成多个小车道(**信道**),每个车道(**信道**)的宽度就是它的带宽.
-   例子:FM收音机听到的广播
    -   调频无线电台通常会共享`88MHz-108MHz`的频谱,而其中每一个电台,都只会共享其中的一个特定的频段
-   传输速度:
    -   传输速度主要取决于 1. 信道宽度(相当于车道宽度) 2. 调制方式 更先进的调制方式传输的速率越高
    -   而其中心频率,如88MHz或者说108MHz,只决定了这条车道的位置
    -   **数据速率(单位：bps)基本上直接由“车道宽度”(带宽)决定。** 带宽越宽,能承载的数据速率就越高。这就是著名的**香农定理**的核心思想之一。

#### 时分复用 TDM

![image-20250913230917707](chap1_Network_Overview_pic\TDM_P20.png)

时分复用就是把时间划分成固定的帧`frame`,每个帧又划分成固定的时间间隔.

-   图中标号相同的一系列帧被一个连接所共用 [如图所示]
-   速率计算
    -   一条电路的传输速率 = 帧速率 $\times$ 一个时间空隙中的比特数量
    -   For example, if the link transmits 8,000 frames per second and each slot consists of 8 bits, then the transmission rate of each circuit is 64 kbps.

>   [!IMPORTANT]
>
>   **为什么要选择分组交换 分组交换有哪些优点 ?**
>
>   1.   电路交换在静默期时 , 专用电路会空闲 不够经济
>   2.   实现线路选择连接等是复杂的

>   [!CAUTION]
>
>   **题目**
>
>   Let us consider how long it takes to send a file of 640,000 bits from Host A to Host B over a circuit-switched network. Suppose that all links in the network use TDM with 24 slots and have a bit rate of 1.536 Mbps. Also suppose that it takes 500 msec to establish an end-to-end circuit before Host A can begin to transmit the file. How long does it take to send the file? Each circuit has a transmission rate of so it takes seconds to transmit the file. To this 10 seconds we add the circuit establishment time, giving 10.5 seconds to send the file. 
>
>   **Note that the transmission time is independent of the number of links: The transmission time would be 10 seconds if the end-to-end circuit passed through one link or a hundred links.**

#### Packet Switching Versus Circuit Switching

在很多场景下 分组交换都更有优势 

-   比如突然产生了大量的单点通信需求 Suppose there are 10 users and that one user suddenly generates one thousand 1,000-bit packets, while other users remain quiescent and do not generate packets. 分组交换允许它使用更多的流量 .
-    或者在一个长期需求中又有空闲 比如client和server产生了连接 但是某些时候在查看数据而没有请求传输 这样无论是时分复用还是频分复用 都会有很大的空闲 像是被进程锁锁住了一样

现在大的趋势是转向 分组交换 . 在一些电话网络负责海外通信(昂贵)时 都在使用分组交换 .

### 1.3.3 A Network of Networks

端系统必须先进入`ISP`才能与因特网相连接 . 而这些`ISP`也不是直接相连的 , 而是 `hierarchical` 的.

接入`ISP`的是`customer`而提供`ISP`服务的则是`provider`.

有一些内容提供商 为了避免向顶层`ISP`交费 , 还会自行组建`内容提供商网络 content provider network` . 比如"谷歌".这些内容提供商也对 其服务内容最终如何交付给端用户有了更多的控制 .

![image-20250914151410690](chap1_Network_Overview_pic\ISP的互联.png)

**总之 , 较高层(上层/顶层)的ISP彼此互联 , 较低层的ISP是较高层ISP的客户 .** 

## 1.4 Delay, Loss, and Throughput in Packet-Switched Networks

本章主要来研究分组交换网络中的时延/丢包/吞吐量

### 1.4.1 Delay

>   [!NOTE]
>
>   时延的主要类型有:
>
>   1.   节点处理时延 nodal processing delay
>   2.   排队时延 queuing delay
>   3.   传输时延 transmission delay
>   4.   传播时延 propagation delay
>
>   这些时延加起来就是 **节点总时延 total nodal delay**

-   处理时延
    -   **检查分组首部和决定该分组导向何处所需要的时间是 处理时延 的重要部分** .
    -   还包括处理比特级别的差错所需要的时间
    -   高速路由器的处理时延低至微秒甚至更低的级别
-   排队时延
    -   At the queue, the packet experiences a queuing delay **as it waits to be transmitted onto the link**.
    -   The length of the queuing delay of a specific packet will depend on the number of earlier-arriving packets
        that are queued and waiting for transmission onto the link.
    -   We will see shortly that the number of packets that an arriving packet might expect to find is a function of the intensity and nature of the traffic arriving at the queue.
        而一个队列里面的数据包数量 和 队列目前的流量和转发效率等属性有关
    -   排队时延一般在毫秒级别 , 甚至更低 .
-   传输时延
    -   是从路由器节点推上传输链路的时间
    -   $\frac{L}{R}$
-   传播时延
    -   取决于路由器A和路由器B之间的物理媒体
    -   也就是前面计算过的 从 路由器A 到 路由器B 的时间

$$
d_{nodal}=d_{proc}+d_{queue}+d_{trans}+d_{prop}
$$

### 1.4.2 Queuing Delay and Packet Loss

#### 定义 流量强度

我们假定

-   从路由器中推到链路上的速率是 $\mathbf{R}$ 单位是 `bps`
-   所有分组都是`L 比特`组成
-   分组的平均到达速率是`a 分组/秒`

所以流量强度`Traffic Intensity`就是
$$
\frac{L \times a}{R}
$$
If Traffic Intensity > 1, then the average rate at which bits arrive at the queue exceeds the rate at which the bits can be transmitted from the queue. 

In this unfortunate situation, the queue will tend to increase without bound and the queuing delay will approach infinity!

**Therefore, one of the golden rules in traffic engineering is: Design your system so that the traffic intensity is no greater than 1.**

即使流量强度小于1 也不意味着万事大吉 如果突然有很大的传输需求 这是的平均排队延时也很高

#### Packet Loss

**丢包**[这里真的想吐槽一些这本书的编排 至少第一章的顺序十分让人感到困惑]

### 1.4.3 End-to-End Delay

这里会建议你使用`linux`系统自带的`traceroute`程序 , 如果是`windows`可以使用`tracert`代替

或者访问 http://www.traceroute.org 

后面还会讨论其他类型的时延

### 1.4.4 Throughput in Computer Networks

>   [!IMPORTANT]
>
>   三大计算机网络中的性能指标 : 时延 / 丢包率 / 端到端吞吐量

吞吐量就是我们常说的网速 也分为 **瞬时吞吐量** 和 **平均吞吐量** .

有时候也会遇到一种 **瓶颈链路** . 此时他们的近似传输速率就是
$$
\frac{F}{\min\{R_1,R_2,\cdots,R_n\}}
$$
其中 F 是假象的一个超大文件的总比特数 .

当然 瓶颈也可能出现在在发送端 比如一个服务器的最大发送速率是 $5Mbps$现在同时发送10个文件 那么它所能提供的最大传输速率就是$5kbps$ . 此时整体吞吐量不会超过$5kbps$ .

**其他扰动因素的影响后面会讲到** .

## 1.5 Protocol Layers and Their Service Models

### 1.5.1 Layered Architecture

显然 分层考虑一个系统是一种简单而有效的方法 .

#### Protocol Layering

上一协议层会对下一协议层提出 Request , 而下一层则是对上一层提供 Service . 

这些服务可能通过软件实现 , 也可能通过硬件实现 , 又或者要依靠两者来实现 .

>   [!CAUTION]
>
>   也有一些研究人员激烈的反对分层 :
>
>   -   因为这样会设计出一些冗余的较低层
>       -   一个例子是 几乎所有的协议层中都重复的增加冗余来恢复差错
>   -   第二个问题是 有些层要求其他层的信息才能工作 违反了层次分离的目标
>
>   在我看来 一个系统在不断更新的时候会越来越朝着屎山的方向发展 就算不分层也很难避免

Definition : 各个层次的所有协议都被称为 **协议栈 protocol stack**

>   [!TIP]
>
>   $\mathbf{Deepseek}$
>
>   **协议栈是所有这些分层协议的集合,以及它们之间协同工作的整个系统**

最早的分层是 OSI 模型 比因特网分层多了 **表示层** 和 **会话层** 仅在应用层下方 .

后来的因特网分层将选择是否含有这两层的权利给了应用程序 , 由应用程序决定是否需要这两成的功能 .

#### Internet's 5 Layers

##### 1. 应用层

这是最顶层,直接与用户和应用程序交互。

-   **功能**：为特定的应用程序提供通信服务,定义数据格式和交互规则。例如,浏览器如何向Web服务器请求页面,邮件客户端如何发送邮件。
-   **协议**：
    -   **HTTP**：用于万维网(WWW)的数据传输。
    -   **HTTPS**：安全的HTTP。
    -   **FTP**：用于文件传输。
    -   **SMTP**：用于发送电子邮件。
    -   **POP3/IMAP**：用于接收电子邮件。
    -   **DNS**：将域名(如 `www.google.com`)解析为IP地址。
    -   **WebSocket**：用于全双工通信。
-   **数据单位**：**报文**。
-   **类比**：就像你要寄一封信,**应用层**就是信的具体**内容**(你写的文字)和**类型**(是一封私人信件还是一份商业合同)。

------

##### 2. 传输层

负责为两台主机上的**应用程序**提供端到端的通信。

-   **功能**：
    -   **进程到进程的通信**：通过端口号来标识不同的应用程序(如80端口对应Web服务,25端口对应邮件服务)。
    -   **可靠性**：确保数据完整、有序地到达(如TCP)。
    -   **流量控制**：控制发送方的数据发送速率,以免淹没接收方。
-   **协议**：
    -   **TCP**：提供**面向连接的、可靠的**数据传输。速度慢,但保证数据准确送达。用于Web浏览、邮件、文件传输等。
    -   **UDP**：提供**无连接的、不可靠的**数据传输。速度快,但不保证数据一定送达。用于视频通话、在线游戏、DNS查询等。
-   **数据单位**：**段**(TCP段或UDP数据报)。
-   **类比**：**传输层**负责把你的信**打包**成一个标准的信封,并在信封上写上**发件人和收件人的具体门牌号(端口号)**,而不仅仅是街道地址。

------

##### 3. 网络层

负责将数据包从源主机**跨网络**传输到目标主机。

-   **功能**：
    -   **逻辑寻址**：为每台设备分配一个唯一的**IP地址**。
    -   **路由**：选择数据包从源到目的地所经过的最佳路径。路由器就是工作在这一层的关键设备。
    -   **分组和转发**：将传输层的段封装成**数据包**,并根据IP地址进行转发。
-   **协议**：
    -   **IP**：核心协议,提供不可靠、无连接的数据报传送服务。
    -   **ICMP**：用于网络诊断和错误报告,如 `ping` 命令。
    -   **路由协议**：如OSPF, BGP,用于路由器之间交换路由信息。
-   **数据单位**：**数据包**。
-   **类比**：**网络层**的工作是根据**收件人的街道地址(IP地址)**,规划信件的运输路线,决定它应该经过哪个中转站(路由器)。

------

##### 4. (数据)链路层

负责在**同一个局域网**内,通过物理网络连接的两个设备之间传输数据帧。

-   **功能**：
    -   **物理寻址**：为网络设备定义一个唯一的**MAC地址**(也叫硬件地址)。
    -   **帧的组装和拆解**：将网络层的数据包封装成**帧**,添加帧头和帧尾。
    -   **差错检测**：通过帧尾的校验码(如CRC)来检测数据在传输过程中是否出错。
    -   **介质访问控制**：控制设备如何在共享介质(如以太网)上发送数据,避免冲突。交换机工作在这一层。
-   **协议**：**以太网**、**Wi-Fi**、**PPP**。
-   **数据单位**：**帧**。
-   **类比**：**数据链路层**负责在一条具体的街道上,将信件从**一个邮箱(MAC地址)传递到下一个邮箱(MAC地址)**。它不关心最终目的地,只关心下一站去哪。

------

##### 5. 物理层

负责在物理介质上传输原始的比特流。

-   **功能**：
    -   定义物理特性：如接口的形状、针脚的数量、电压的大小、光线的波长等。
    -   传输比特流：将数据链路层的帧转换成**1**和**0**的比特流,通过网线、光纤、无线电波等物理介质进行传输。
-   **设备**：集线器、中继器、网线、光纤、无线接入点。
-   **数据单位**：**比特**。
-   **类比**：**物理层**就是**运送信件的卡车和公路**。它不关心信的内容和地址,只负责把装着信件的箱子(比特流)从一个地方 physically 移动到另一个地方。

### 1.5.2 Encapsulation

封装性 每一层都只处理接受到的数据 就像把数据放到了信封中 而邮递员只用看信封上的信息来运送信件即可 

![image-20250914200820481](chap1_Network_Overview_pic\Encapsulation_layers.png)

## 1.6 Networks Under Attack

网络安全是本书的核心之一 . 

书里面提到网络攻击的一些思路和原理 : 

>   [!IMPORTANT]
>
>   1.   The Bad Guys Can Put Malware into Your Host Via the Internet
>        - 植入有害程序
>   2.   The Bad Guys Can Attack Servers and Network Infrastructure
>        -  DDoS 系列
>   3.   The Bad Guys Can Sniff Packets
>        -   相当于是被动的监听 , 因为没有主动的发送信息等 , 所以很难主动探测到
>   4.   The Bad Guys Can Masquerade as Someone You Trust
>        -   IP 哄骗 / IP spoofing

## 1.7 History of Computer Networking and the Internet

...

## 1.8 Summary

...

























































