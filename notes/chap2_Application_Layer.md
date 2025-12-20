# Chapter 2 Application Layer

The application layer is a particularly good place to start our study of protocols. It’s familiar ground. We’re acquainted with many of the applications that rely on the protocols we’ll study. It will give us a good feel for what protocols are all about and will introduce us to many of the same issues that we’ll see again when we study transport, network, and link layer protocols.

## 2.1 Principles of Network Applications

**At the core of network application development is writing programs that run on different end systems and communicate with each other over the network.**
处在开发网络应用程序核心地位的是 : 写出能够在不同的端系统通过网络彼此通信的程序 . 

### 2.1.1 Network Application Architectures

-   The application architecture is designed by the application developer and dictates how the application is structured over the various end systems. 

-   In choosing the application architecture, an application developer will likely draw on one of the **two predominant architectural paradigms** used in modern network applications: 
    -   the client-server architecture
    -   the peer-to-peer (P2P) architecture

#### client-server (CS) architecture

>   [!NOTE]
>
>   1.   有一台总是打开的主机--server
>   2.   客户之间不相互通信
>   3.   该服务器具有固定的 周知的 IP 地址 // 客户能够通过向该IP地址发送分组来与其联系
>   4.   服务的提供商同上会准备一个大型的数据中心

#### P2P architecture

仅依赖最小的服务器 , 甚至可以没有服务器 .

应用程序可以在主机间直接通信 这些主机被称为 `对等方 peers`.

P2P架构的一个重要特性是它的 **自扩展性 self-scalability** 

当然 P2P架构 也会面临安全性 性能 可靠性等挑战

![image-20250915105846364](./chap2_Application_Layer_pic/CS_and_P2P_arch.png)

>   [!CAUTION]
>
>   还有一些应用使用了混合的体系结构 :
>
>   -   使用服务器跟踪用户的IP地址
>   -   用户之间的报文传递使用P2P架构 无需通过中间服务器 直接发送

### 2.1.2 Processes Communicating

从操作系统的角度来说 真正进行信息通信的不是应用程序 而是应用程序中的一个进程 .

#### Client and Server Processes

对于进程而言 我们也可以把他们分为客户或者服务器 这与是否是SC架构无关 . 例如 :

-   对于Web程序而言 浏览器是一个 `client` 而Web服务器则是一个 `server` .
-   With P2P file sharing, the peer that is downloading the file is labeled as the client, and the peer that is uploading the file is labeled as the server.
-   当然 继续讨论P2P的话 一个P2P进程既能是 服务器 也可以是 客户 .

总之 , **the process that initiates the communication (that is, initially contacts the other process at the beginning of the session) is labeled as the client. The process that waits to be contacted to begin the session is the server.**

为了区分 有时候也会使用"应用程序的客户端/服务器端"这种说法 .

#### The Interface Between the Process and the Computer Network

Any message sent from one process to another must go through the underlying network .

进程通过`套接字-socket`软件接口向网络 发送 和 接收 Message .

>   [!NOTE]
>
>   **套接字是一个编程接口（API），它允许应用程序使用网络协议（如TCP/IP）进行通信。它是IP地址和端口号的组合。**
>
>   一个套接字可以用一个公式来定义：
>   $$
>   Socket = IP Address + Port Number
>   $$
>
>   例如，一个Web服务器的IP地址是 `142.251.42.206`，它使用80端口，那么与之通信的套接字就是 `142.251.42.206:80`。
>
>   ---
>
>   如果把网络通信迁移到电话通信上 **套接字就相当于电话插口** 电话机必须插到墙上的电话插座，才能连接到电话网络，听到拨号音 
>   **同样，一个网络应用程序必须创建一个套接字，才能连接到网络**

>   [!IMPORTANT]
>
>   **端口到底是什么 ? 和给IP地址增加一串数字有什么区别 ? **
>
>   一台计算机（一个IP地址）可以同时运行很多网络程序：比如你一边用浏览器上网（访问网页），一边用微信聊天，一边还在玩网络游戏。如果没有端口，计算机收到一个数据包，它根本不知道这个包是应该交给浏览器、微信还是游戏。
>
>   **端口的主要作用是“应用程序寻址”，它在一台计算机上唯一标识一个正在运行的网络应用程序或服务，确保数据包能被交给正确的程序。**
>
>   ---
>
>   一些规范 :
>
>   -   HTTP（网页服务）：端口 80
>   -   HTTPS（加密网页服务）：端口 443
>   -   FTP（文件传输）：端口 21
>   -   SSH（安全远程登录）：端口 22
>   -   SMTP（发送邮件）：端口 25
>
>   ---
>
>   **端口号的分类和范围**
>
>   端口号是一个16位的整数，范围是 **0 - 65535**。它们被分为三类：
>
>   | 类别              | 范围              | 说明                                                         | 例子                             |
>   | :---------------- | :---------------- | :----------------------------------------------------------- | :------------------------------- |
>   | **知名端口**      | **0 - 1023**      | 分配给系统级的重要服务。普通用户程序不应使用。               | 80 (HTTP), 443 (HTTPS), 21 (FTP) |
>   | **注册端口**      | **1024 - 49151**  | 分配给用户安装的某些应用程序或服务。                         | 3306 (MySQL), 3389 (远程桌面)    |
>   | **动态/私有端口** | **49152 - 65535** | **客户端使用的临时端口**。当客户端程序（如浏览器）发起连接时，操作系统会随机分配这个范围内的一个端口给它使用。 |                                  |

![image-20250915113736060](./chap2_Application_Layer_pic/socket_underlying_protocol.png)

#### Addressing Processes

这一段就是上面提到的IP地址和端口号的作用和区别 .

[第三章中会再详细学习端口号 等]

### 2.1.3 Transport Services Available to Applications

**应用层会使用运输层提供的服务** 因此我们有必要了解 运输层能够提供什么样的服务 / 应用层对所需要的服务有什么要求 .

1.   可靠数据传输
     -   有些数据十分重要 必须提供 `可靠数据传输reliable data transfer`
     -   也有一些 `可以容忍丢失的应用loss-tolerant application` 比如音视频数据 他们可以允许一定的损失
2.   吞吐量
     -   在沿着一条网络路径上的两个进程之间的通信会话场景中，**可用吞吐量就是发送进程能够向接收进程交付比特的速率**
     -   有一些应用是 弹性应用 有一些应用这是贷款敏感的应用
     -   但这一般都是最低的要求 我们永远是希望带宽越大越好 .
3.   定时
     - 有一些要求低时延的任务 如多方游戏 电话 都希望时延尽可能低
4.   安全性
     -   发送主机希望运输协议能够加密数据 接收主机希望能够解密数据
     -   还包括完整性和端点鉴别

### 2.1.4 Transport Services Provided by the Internet

计算机网络和因特网还是有一些差别 而我们提到因特网的时候一般指的就是 `TCP/IP 网络` 当然 这意味着因特网会为应用程序提供两个运输层协议 及 TCP 和 UDP .
**When an application developer create a new network application for the Internet, one of the first decisions you have to make is whether to use UDP or TCP.**

>   [!NOTE]
>
>   [!`deepseek`]
>
>   好的，我们用最简单的方式梳理这四个概念的关系：
>
>   1.  **计算机网络**：**总称**。任何连接多台计算机的系统都叫计算机网络。比如你家的Wi-Fi。
>
>   2.  **TCP/IP网络**：**一套规则**。指使用TCP/IP这套特定协议进行通信的网络。它是因特网的“语言”和“交通规则”。
>
>   3.  **因特网**：**最大的例子**。它是全球最大的、应用了TCP/IP规则的那个计算机网络。可以说，因特网就是一个全球性的TCP/IP网络。
>
>   4.  **UDP**：**规则里的一个工具**。它是TCP/IP这套规则中，与TCP并列的一个具体协议。它负责“快速但不可靠”的传输任务。
>
>   **一句话总结关系：**
>
>   **计算机网络**（如因特网）依靠 **TCP/IP** 这套规则 (fix:更准确的说法是协议栈) 运行，而 **TCP/IP** 规则中包含了 **UDP** 这种追求速度的传输工具。

#### TCP Services

The TCP service model includes a **connection-oriented service** and a **reliable data transfer service**. When an application invokes TCP as its transport protocol, the application receives both of these services from TCP.

-   **Connection-oriented service.** 
    TCP has the client and server exchange `transport-layer` control information with each other before the application-level messages begin to flow. This so-called handshaking procedure alerts the client and server, allowing them to prepare for an onslaught of packets. 
    首先会进行**第一次握手** 传输双方 (client and server) 会**交换运输层控制信息** 让它们**为大量分组的到来做好准备**
    After the handshaking phase, a TCP connection is said to exist between the sockets of the two processes. 
    握手阶段之后 , 一个TCP连接就在两个套接字之间建立了
    The connection is a **full-duplex** connection in that the two processes can send messages to each other over the connection at the same time. 

    >   [!NOTE]
    >
    >   **全双工** 是一种通信方式，允许数据在**同一时间、双向**传输。这意味着通信的双方可以同时发送和接收数据 。
    >
    >   它的英文是 **Full-Duplex**，常缩写为 **FDX**。
    >
    >   ---
    >
    >   -   **单工**：像一条单行道，所有车只能朝一个方向开。
    >   -   **半双工**：像一条狭窄的单车道桥梁，车可以双向通行，但在任何一刻，只能有一个方向的车在行驶，需要交通灯或对讲机来协调谁先走。
    >   -   **全双工**：像一条宽阔的**双车道高速公路**，一条车道专门用于A到B的流量，另一条车道专门用于B到A的流量。两边的车可以**同时、互不干扰地**飞速对向行驶。

    When the application finishes sending messages, it must **tear down(拆除)** the connection. 
    `In Chapter 3 we'll discuss connection-oriented service in detail and examine how it is implemented.`

-   **Reliable data transfer service.**
     The communicating processes can rely on TCP to **deliver all data sent without error and in the proper order**. When one side of the application passes a stream of bytes into a socket, it can count on TCP to deliver the same stream of bytes to the receiving socket, without missing or duplicate bytes.

>   [!NOTE]
>
>   TCP协议还具有拥塞控制机制，这种服务不一定能为通信进程带来直接好处，但能为因特网带来整体好处。当发送方和接收方之间的网络出现拥塞时，TCP的拥塞控制机制会抑制发送进程（客户或服务器）。如我们将在第3章中所见，TCP拥塞控制也试图限制每个TCP连接，使它们达到公平共享网络带宽的目的。

>   [!CAUTION]
>
>   **关于安全性** :
>
>   1. **TCP 与 UDP 缺乏加密机制** 
>      发送进程传入套接字的数据会以明文形式在网络上传输，可能被中间链路嗅探。
>   2. **SSL 的作用** 
>      SSL（安全套接字层）是对 TCP 的加强，提供加密、数据完整性和端点鉴别等安全服务。
>   3. **SSL 的实现方式** 
>      - **SSL 位于应用层**，不是独立的传输协议。 
>      - **应用程序需在客户端和服务器端集成 SSL 代码（使用现有库）**。 
>      - SSL 提供自己的套接字 API，与传统 TCP 套接字 API 类似。
>   4. **SSL 的工作流程** 
>      发送端：明文 → SSL 加密 → TCP 套接字 → 网络传输 
>      接收端：网络 → TCP 套接字 → SSL 解密 → 明文数据传递给接收进程

#### UDP Services

**UDP是一种不提供不必要服务的轻量级运输协议，它仅提供最小服务。**UDP是无连接的，因此在两个进程通信前没有握手过程。UDP协议提供一种不可靠数据传送服务，也就是说，当进程将一个报文发送进UDP套接字时，UDP协议并不保证该报文将到达接收进程。不仅如此，到达接收进程的报文**也可能是乱序到达**的。
UDP**没有包括拥塞控制机制**，所以UDP的发送端可以用它选定的任何速率向其下层（网络层）注入数据。
然而，值得注意的是实际端到端吞吐量可能小于该速率，这可能是因为中间链路的带宽受限或因为拥塞而造成的。

#### Services Not Provided by Internet Transport Protocols

前文提到了运输协议服务要求的4个特征：可靠数据传输、吞吐量、定时、安全性。

TCP和UDP提供了这些服务中的哪些呢？我们已经注意到TCP提供了可靠的端到端数据传送。并且我们也知道TCP在应用层可以很容易地用SSL来加强以提供安全服务。但在我们对TCP和UDP的简要描述中，明显地漏掉了对吞吐量或定时保证的讨论，即这些服务目前的因特网运输协议并没有提供。**[目前的因特网运输协议并不能保证 吞吐量 和 定时]**

但是多年的发展下来 有很多好的设计来保证这两点 详细见 第九章 . 尽管在时延过大或端到端吞吐量受限时，再好的设计也不能保证上面两点 .

**总之，今天的因特网通常能够为时间敏感应用提供满意的服务，但它不能提供任何定时或带宽保证。**

>   [!NOTE]
>
>   不同的应用会采取不同的应用层协议 运输层协议也有差别 
>   值得注意的是 例如网上及时通信的过程中 主要会使用 UDP 但是也会用 TCP 作为备份
>
>   |     应用     |                    应用层协议                     | 支撑的运输协议 |
>   | :----------: | :-----------------------------------------------: | :------------: |
>   |   电子邮件   |                  SMTP [RFC 5321]                  |      TCP       |
>   | 远程终端访问 |                 Telnet [RFC 854]                  |      TCP       |
>   |     Web      |                  HTTP [RFC 2616]                  |      TCP       |
>   |   文件传输   |                   FTP [RFC 959]                   |      TCP       |
>   |  流式多媒体  |                HTTP（如 YouTube）                 |      TCP       |
>   |  因特网电话  | SIP [RFC 3261]、RTP [RFC 3550] 或专用（如 Skype） |   UDP 或 TCP   |

### 2.1.5 Application-Layer Protocols

**An application-layer protocol defines how an application’s processes, running on different end systems, pass messages to each other.** 

In particular, an application-layer protocol defines: 

1.   The types of messages exchanged, for example, request messages and response messages 
2.   The syntax of the various message types, such as the fields in the message and how the fields are delineated(规定/描述)
3.   The semantics of the fields, that is, the meaning of the information in the fields 
4.   Rules for determining when and how a process sends messages and responds to messages

>   [!NOTE]
>
>   以下是对这段文字的整理总结：
>
>   ---
>
>   ### 一、应用层协议的定义与作用
>
>   应用层协议定义了运行在不同端系统上的应用程序如何通过网络交换报文，具体包括：
>
>   - **报文类型**：如请求报文和响应报文；
>   - **报文语法**：字段结构及其描述方式；
>   - **字段语义**：字段中信息的含义；
>   - **通信规则**：进程何时发送报文、如何响应等。
>
>   ---
>
>   ### 二、应用层协议的分类
>
>   - **公开协议**：由 RFC 文档定义，如 HTTP（Web）、SMTP（电子邮件），可供公共使用；
>   - **私有协议**：如 Skype 使用的协议，不对外开放。
>
>   ---
>
>   ### 三、应用层协议与网络应用的关系
>
>   - **应用层协议只是网络应用的一部分**，尽管是关键部分；
>   - **Web 应用**包括：
>     - 文档格式（HTML）；
>     - 浏览器与服务器软件；
>     - 应用层协议（HTTP）；
>   - **电子邮件应用**包括：
>     - 邮件服务器与客户端；
>     - 报文格式标准；
>     - 应用层协议（如 SMTP）。
>
>   ---
>
>   ### 四、总结
>
>   应用层协议是实现网络通信的规则集合，它指导进程如何构造和交换报文。理解协议有助于深入掌握网络应用的工作原理，但协议本身只是整个应用系统中的一个组成部分。

### 2.1.6 Network Applications Covered in This Book

因特网应用的种类繁多 本书只讨论五种重要的应用

>   [!NOTE]
>
>   以下是对这段文字的整理总结：
>
>   ---
>
>   ### 一、五种重要的网络应用
>
>   本部分将详细讨论以下五种关键的网络应用：
>
>   1. **Web 应用**  
>      - 最流行、使用广泛；  
>      - 应用层协议 HTTP 简单易懂，是入门的良好示例。
>
>   2. **文件传输**（如 FTP）  
>      - 用于在不同主机之间传输文件；  
>      - 将在后续内容中介绍。
>
>   3. **电子邮件**  
>      - 是互联网上最早流行的应用之一；  
>      - 相比 Web 更复杂，涉及多个应用层协议（如 SMTP、POP3、IMAP）。
>
>   4. **目录服务（DNS）**  
>      - 提供域名到 IP 地址的解析服务；  
>      - 用户通常间接使用（如通过 Web、邮件等应用）；  
>      - 体现了网络核心功能（名字解析）如何在应用层实现。
>
>   5. **流式视频 与 P2P 文件共享**  
>      - 包括按需视频流（如通过内容分发网络 CDN）；  
>      - P2P 应用强调用户之间的直接资源共享；  
>      - 流式视频和 P2P 是现代网络流量和应用的重要组成部分。
>
>   ---
>
>   ### 二、学习顺序说明
>
>   - 从 **Web（HTTP）** 开始，因其简单直观；
>   - 接着学习 **电子邮件**，理解多协议协作；
>   - 然后深入 **DNS**，掌握网络基础服务机制；
>   - 最后探讨 **P2P 和流式视频**，理解现代内容分发与共享方式。
>
>   ---
>
>   ### 三、总结
>
>   这五种应用代表了互联网的核心功能和服务类型。通过逐一学习它们的工作原理和协议机制，可以全面理解应用层在网络通信中的作用。后续章节还将涉及如 VoIP、视频会议等多媒体应用。

## 2.2 The Web and HTTP

直到1994年 万维网(World Wide Web)才从学校走向世界 之前基本不为学术界和研究界之外所知 . Web的优点数不胜数 .

### 2.2.1 Overview of HTTP

The **HyperText Transfer Protocol (HTTP)**, the **Web’s application-layer protocol**,  is at the heart of the Web . It is defined in [RFC 1945], [RFC 7230] and [RFC 7540].  

**HTTP is implemented in two programs: a client program and a server program. The  client program and server program, executing on different end systems, talk to each other by exchanging HTTP messages.**

 **HTTP defines the structure of these messages  and how the client and server exchange the messages.** 

![image-20250917185119016](./chap2_Application_Layer_pic/HTTP_request_and_response.png)

>   **上图就是`HTTP`的主要作用 "defines how Web clients request Web pages from Web servers and how  servers transfer Web pages to clients. "定义了client如何请求server以及server如何将Web网页发送给client .**

---

Before explaining HTTP in  detail, we should review some Web terminology(术语).

**A Web page** (also called a document) consists of objects. An **object** is  simply a file—such as an HTML file, a JPEG image, a Javascrpt file, a CCS  style sheet file, or a video clip—that is addressable by a single URL. Most Web  pages consist of a **base HTML file** and several referenced objects.

---

1. **传输方式**：HTTP基于TCP协议，而非UDP。客户端先与服务器建立TCP连接，然后通过套接字接口发送和接收HTTP请求与响应。

2. **可靠性**：TCP为HTTP提供可靠的数据传输，确保请求和响应报文完整送达，HTTP本身无需处理数据丢失或乱序问题。

3. **无状态性**：HTTP服务器不保存客户端的状态信息，每次请求都被独立处理，即使同一客户端短时间内重复请求同一资源，服务器也会重新响应。[像这样的协议可以称作是 **无状态协议 stateless protocol**]

4. **架构特点**：Web采用客户端-服务器架构，服务器始终在线，拥有固定IP地址，能同时处理大量来自不同浏览器的请求。

### 2.2.2 Non-Persistent and Persistent Connections

这段内容的核心是对比**非持续连接（non-persistent connection）**与**持续连接（persistent connection）**在TCP通信中的应用，特别是在HTTP协议中的使用场景与权衡。

---
- 在**长时间交互**的互联网应用中，客户端与服务器之间会进行**多次请求-响应**的通信。
- 这些请求可以是**周期性**或**间歇性**的。
- 通信基于**TCP协议**，因此需要决定：**每个请求/响应对是否使用独立的TCP连接**。

---

| 类型           | 定义说明                                       |
| -------------- | ---------------------------------------------- |
| **非持续连接** | 每个请求/响应对都通过**一个新的TCP连接**完成。 |
| **持续连接**   | 所有请求和响应都通过**同一个TCP连接**完成。    |

---

- HTTP协议**默认使用持续连接**。
- 但HTTP也**支持配置为非持续连接**，根据需求灵活选择。

---

#### 非持续链接的HTTP

在非持续连接的HTTP中 , 每个TCP在服务器发送完成一个对象后就会关闭 , 不会持续 .
而每一个TCP连接也只会传输一个请求和一个响应报文 . 比如我按顺序有11个文件需要从server获取 那么就要产生11个TCP请求 .

值得注意的是 这个过程还可以并行执行 . 事实上 , 现代浏览器可以控制连接的并行度(一般会默认打开5-10个并行的TCP连接,每个连接处理一个响应事务).当然 用户也可以把最大连接并行数设置为1,这样就回到串行了.

>   [!NOTE]
>
>   **往返时间 Round-Trip Time RTT**
>
>   这个时间指一个短分组从客户端到服务器然后再返回客户端所花费的时间 . RTT 也包括了分组传播时延 , 分组在中间路由器和交换机的排队时延以及分组处理等所有的时延 . 
>
>   ![image-20250919115540694](./chap2_Application_Layer_pic/RTT.png)
>
>   图中三条细一些的箭头表示了**三次握手**的过程 其中 前两次占据了一个完整的RTT .
>   **粗略的讲 总的响应时间就是两个RTT加上一个传输时间**

#### 持续连接的HTTP

**非持续连接有一些缺点。**

-   第一，<u>必须为每一个请求的对象建立和维护一个全新的连接</u>。对于每个这样的连接，在客户和服务器中都要分配 TCP 的缓冲区和保持 TCP 变量，这给 Web 服务器带来了严重的负担，因为一台 Web 服务器可能同时服务于数以百计不同的客户的请求。
-   第二，就像我们刚描述的那样，每一个对象经受<u>两倍 RTT 的交付时延</u>，即一个 RTT 用于创建 TCP，另一个 RTT 用于请求和接收一个对象。

在采用 HTTP 1.1 持续连接的情况下，服务器在发送响应后保持该 TCP 连接打开。在相同的客户与服务器之间，后续的请求和响应报文能够通过相同的连接进行传送。特别是，一个完整的 Web 页面（上例中的 HTML 基本文件加上 10 个图形）可以用单个持续 TCP 连接进行传送。更有甚者，位于同一台服务器的多个 Web 页面在从该服务器发送给同一个客户时，可以在单个持续 TCP 连接上进行。对对象的这些请求可以一个接一个地发出，而不必等待对未决请求（流水线）的回答。

一般来说，如果一条连接经过一定时间间隔（一个可配置的超时间隔）仍未被使用，HTTP 服务器就关闭该连接。HTTP 的默认模式是使用带流水线的持续连接。最近，HTTP/2 [RFC 7540] 是在 HTTP 1.1 基础上构建的，它允许在相同连接中多个请求和回答交错，并增加了在该连接中优化 HTTP 报文请求和回答的机制。

>   [!NOTE]
>
>   我们把量化比较持续连接和非持续连接性能的任务留作第 2、3 章的课后习题。鼓励读者阅读文献 `[Heidemann 1997；Nielsen 1997；RFC 7540]`。

---

### 2.2.3 HTTP Message Format

The HTTP specifications [RFC 1945; RFC 7230; RFC 7540] include the definitions  of the HTTP message formats.

所有的HTTP报文都可以分为两种 : **请求报文** 和 **响应报文** .

#### HTTP Request Message

Below we provide typical HTTP request messages(GET and POST):

```http
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
[这里是一个换行符]
```

```http
POST /api/login HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 42
User-Agent: Mozilla/5.0

{"username": "john_doe", "password": "secret123"}
```

HTTP请求报文的格式非常标准，遵循一个清晰的结构。它主要由四个部分组成：

1.  **请求行 (Request Line)**
2.  **首部行 (Headers Lines)**
3.  **空行 (Blank Line)**
4.  **实体 体 (Entity Body)** - 可选
    -  **GET**, **HEAD**, **DELETE** 等通常不携带实体的请求，报文到空行就结束了。
    - **POST**, **PUT**, **PATCH** 等请求通常会用请求体来发送数据。

![image-20250919150958860](./chap2_Application_Layer_pic/http请求报文.png)

>   [!NOTE]
>
>   [这里可能会有一些翻译问题]
>
>   ### 1. 请求行 (Request Line)
>
>   请求行是报文的第一行，它包含三个基本部分，用空格分隔：
>
>   -   **请求方法 (HTTP Method)**： 表示要对资源执行的操作。常见的方法有：
>       -   `GET`： 请求获取指定的资源。
>       -   `POST`： 向指定资源提交数据（例如提交表单或上传文件）。
>       -   `PUT`： 替换指定资源的所有当前表示。
>       -   `DELETE`： 删除指定的资源。[出于安全考虑，大多数公共网站不会允许普通用户直接使用DELETE方法，删除操作通常通过一个POST请求来触发后端程序执行。]
>       -   `HEAD`： 与GET相同，但服务器只返回响应头，不返回响应体。
>       -   `PATCH`： 对资源进行部分修改。
>   -   **请求目标 (Request Target)**： 通常是URL的路径和查询部分（例如 `/api/users?id=123`），有时也可以是绝对URL（在代理请求中常见）。
>   -   **HTTP版本 (HTTP Version)**： 声明使用的HTTP协议版本，例如 `HTTP/1.1` 或 `HTTP/2`。
>
>   **格式：**
>   `<方法> <请求目标> <HTTP版本>`
>
>   **示例：**
>   `GET /index.html HTTP/1.1`
>
>   ------
>
>   ### 2. 请求头 (Request Headers)
>
>   请求头是从第二行开始，一直到遇到一个空行为止。它们是以键值对（`Key: Value`）的形式出现的，每行一个。
>
>   请求头为服务器提供了关于客户端、请求本身以及期望的响应方式的额外信息。常见的请求头包括：
>
>   -   **Host**： (HTTP/1.1 **必须要有**) 指定请求的服务器的域名和端口号。
>       -   `Host: www.example.com`
>   -   **User-Agent**： 告诉服务器客户端的软件信息（浏览器类型、操作系统等）。
>       -   `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`
>   -   **Accept**： 声明客户端可以处理的媒体类型（MIME类型）。
>       -   `Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8`
>   -   **Accept-Language**： 声明客户端偏好的语言。
>       -   `Accept-Language: en-US,en;q=0.5`
>   -   **Accept-Encoding**： 声明客户端可以理解的压缩编码。
>       -   `Accept-Encoding: gzip, deflate, br`
>   -   **Content-Type**： (用于有Body的请求，如POST/PUT) 声明请求体的媒体类型。
>       -   `Content-Type: application/json`
>       -   `Content-Type: application/x-www-form-urlencoded`
>   -   **Content-Length**： (用于有Body的请求) 声明请求体的长度（以字节为单位）。
>       -   `Content-Length: 348`
>   -   **Authorization**： 包含用于服务器验证客户端身份的凭据（如Token或用户名密码）。
>       -   `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
>   -   **Cookie**： 将之前服务器通过Set-Cookie头发送过来的Cookie返回给服务器。
>       -   `Cookie: sessionId=abc123; username=john_doe`
>   -   **Connection**： 控制本次请求/响应完成后连接是否保持。
>       -   `Connection: keep-alive`
>
>   ------
>
>   ### 3. 空行 (Empty Line)
>
>   这是一个**必须存在**的部分。它就是一个回车换行符（`\r\n`），用来告诉服务器请求头部分已经结束。空行之后的内容（如果有）就全部是请求体了。
>
>   ------
>
>   ### 4. 请求体 (Request Body)
>
>   请求体是可选的，并不是所有请求都有。它用于携带需要发送给服务器的数据。
>
>   -   **GET**, **HEAD**, **DELETE** 等通常不携带请求体的请求，报文到空行就结束了。
>   -   **POST**, **PUT**, **PATCH** 等请求通常会用请求体来发送数据。
>
>   请求体中数据的格式由 `Content-Type` 头来指定。常见格式：
>
>   -   **表单数据**： `Content-Type: application/x-www-form-urlencoded`
>       -   格式： `key1=value1&key2=value2`
>   -   **JSON数据**： `Content-Type: application/json`
>       -   格式： `{"username": "john", "age": 30}`
>   -   **表单数据（带文件上传）**： `Content-Type: multipart/form-data; boundary=---something`
>   -   **纯文本/XML等**： 其他任何格式。

>   [!CAUTION]
>
>   **澄清一个常见的误解（表单必须用POST）**
>
>   [此处看原文可能会看不懂 , 实际上惊为天人]
>
>   HTML表单（`<form>`）的默认方法其实是GET，而不是POST。
>
>   -   **工作原理:** 当表单使用 `method="GET"` 时，用户输入的数据会被**附加到URL的末尾**，以一个问号`?`开始，用`&`符号连接多个字段。这被称为“查询字符串”或“URL参数”。
>   -   **举例:**
>       -   一个表单有两个字段：`animal` 和 `food`。
>       -   用户在第一栏输入 `monkeys`，在第二栏输入 `bananas`。
>       -   点击提交后，生成的URL会是：`www.somesite.com/animalsearch?animal=monkeys&food=bananas`
>       -   服务器接收到这个URL后，可以从 `?` 后面的部分解析出用户提交的数据。
>
>   -   **GET vs POST 在表单中的选择:**
>       -   **用 GET:** 适用于**获取数据**的请求，如搜索、筛选。数据在URL中可见，有长度限制，可被收藏为书签。
>       -   **用 POST:** 适用于**修改数据**或**提交敏感信息**的请求，如登录、注册、付款。数据在请求体内，不可见，长度限制更大。

#### HTTP Response Message

Below we provide a typical HTTP response message. This response message could  be the response to the example request message just discussed.

```http
HTTP/1.1 200 OK
Connection: close
Date: Tue, 18 Aug 2015 15:44:04 GMT
Server: Apache/2.2.3 (CentOS)
Last-Modified: Tue, 18 Aug 2015 15:11:03 GMT
Content-Length: 6821
Content-Type: text/html

(data data data data data ...)
```

![image-20250919154919512](./chap2_Application_Layer_pic/http_response_message.png)

[有了请求报文的阅读经验 这一段实际上也非常好懂 这里这描述一些感兴趣/不同的部分]

-   第一行 叫做状态行
    -   `HTTP/1.1 200 OK`
    -   In this example, the status  line indicates that the server is using HTTP/1.1 and that everything is OK (that is, the  server has found, and is sending, the requested object).
    -   200 表示状态码 可能是内部的约定
-   Now let’s look at the header lines. 
    -   The server uses the **Connection: close** header line to tell the client that it is going to close the TCP connection after sending  the message. 
    -   The **Date**: header line indicates the time and date when the HTTP  response was created and sent by the server. Note that this is not the time when  the object was created or last modified; it is the time when the server retrieves the  object from its file system, inserts the object into the response message, and sends the  response message. 
    -   The **Server**: header line indicates that the message was generated by an Apache Web server; it is analogous to the User-agent: header line in  the HTTP request message. 
    -   The **Last-Modified**: header line indicates the time  and date when the object was created or last modified. **The Last-Modified: header, which we will soon cover in more detail, is critical for object caching, both  in the local client and in network cache servers (also known as proxy servers).**
    -   The  Content-Length: header line indicates the number of bytes in the object being  sent. The Content-Type: header line indicates that the object in the entity body  is HTML text. (The object type is officially indicated by the Content-Type: header and not by the file extension.)

>   [!NOTE]
>
>   这个状态码的部分也非常的有意思
>
>   - **200 OK**：请求成功，信息在返回的响应报文中。
>   - **301 Moved Permanently**：请求的对象已经被永久转移了，新的 URL 定义在响应报文的 Location 首部行中。客户软件将自动获取新的 URL。
>   - **400 Bad Request**：一个通用差错代码，指示该请求不能被服务器理解。
>   - **404 Not Found**：被请求的文档不在服务器上。
>   - **505 HTTP Version Not Supported**：服务器不支持请求报文使用的 HTTP 协议版本。

---

这里书中提供了自己尝试看到真实的HTTP响应报文的方法 使用`telnet`工具 

但是由于安全原因，现代 Windows 系统默认不安装 Telnet (甚至在WSL中也没有)。你需要先启用它。

推荐直接使用`curl`工具 .

```shell
curl -I http://www.google.com  # 只显示响应头（包含状态行和首部）
```

```http
HTTP/1.1 200 OK
Transfer-Encoding: chunked
Cache-Control: private
Connection: keep-alive
Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-su0WELEtOhMDEUT2mNKGkQ' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
Content-Type: text/html; charset=ISO-8859-1
Date: Fri, 19 Sep 2025 08:06:32 GMT
Expires: Fri, 19 Sep 2025 08:06:32 GMT
Keep-Alive: timeout=4
P3p: CP="This is not a P3P policy! See g.co/p3phelp for more info."
Proxy-Connection: keep-alive
Server: gws
Set-Cookie: AEC=AaJma5u27rlMFYQ7oiPVWnruo5RIQb8V-TvvU_Q9q1TerrQ14dt1cQHEWO8; expires=Wed, 18-Mar-2026 08:06:32 GMT; path=/; domain=.google.com; Secure; HttpOnly; SameSite=lax
Set-Cookie: NID=525=laTKRQz9QOfdP8hQrQR3A17iUqvA32stT-msuj0jVSUIgSuIoWyfYOGeRzwumQUG2rYkDX84doBeiZp_JXVsv5iLtc_vFynRlNV1pxEYUYhterrliSo9HEQh1Ad1q-Tc4ODPxmztt21gBL2-rYYAJlEPVXTCHoitZmtzlcCA6qM7cH6-djTfv5nKGguneW3gWML3qjwyDhVJZKQ; expires=Sat, 21-Mar-2026 08:06:32 GMT; path=/; domain=.google.com; HttpOnly
X-Frame-Options: SAMEORIGIN
X-Xss-Protection: 0
```

```shell
curl -I https://www.cug.edu.cn
```

```http
HTTP/1.1 200 Connection established

HTTP/1.1 200 OK
Date: Fri, 19 Sep 2025 08:10:48 GMT
Server: Apache
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer-when-downgrade
X-Download-Options: noopen
X-Permitted-Cross-Domain-Policies: master-only
Upgrade: h2c,h2
Connection: Upgrade
Last-Modified: Fri, 19 Sep 2025 06:50:37 GMT
Accept-Ranges: bytes
Content-Length: 118087
Vary: User-Agent,Accept-Encoding
Cache-Control: private, max-age=600
Expires: Fri, 19 Sep 2025 08:20:48 GMT
ETag: "1cd47-63f21e31e7f75-gzip"
Content-Type: text/html
Content-Language: zh-CN
```

上面使用`-I`只会显示**响应头**这样更清晰 

>   [!CAUTION]
>
>   如果使用 `curl -v https://www.cug.edu.cn`  , 可以自行尝试一下 .

### 2.2.4 User-Server Interaction: Cookies

HTTP服务器是无状态的 服务器设计因此变得很简单 但是一个Web站点有时候需要设别用户 这就需要用到 **Cookie** . 使用 Cookie 服务器就可以跟踪它的 users .

![image-20250920091405312](pic_networking\chap2pic\cookie.png)

上图是cookie的一个例子 , 展示了cookie的工作原理 , 可以看到 一个用户的cookie就像是他的一个 id 

后台可以只储存这个用户的id 而不必储存其他私密信息 [当然cookie也有严重的侵犯隐私方面的问题].

 cookie technology has four components: (1) a cookie  header line in the HTTP response message; (2) a cookie header line in the HTTP  request message; (3) a cookie file kept on the user’s end system and managed by  the user’s browser; and (4) a back-end database at the Web site.

### 2.2.5 Web Caching

网络缓存（也称为代理服务器）是一种代表原始网络服务器处理HTTP请求的网络实体。该网络缓存拥有自身的磁盘存储系统，并将近期请求过的对象副本保存于此。如图2.11所示，用户浏览器可配置为将所有HTTP请求首先指向网络缓存[RFC 7234]。一旦完成浏览器配置，每个针对对象的浏览器请求都会首先导向网络缓存。以浏览器请求`http://www.someschool.edu/campus.gif`对象为例，具体过程如下：

1. 浏览器与网络缓存建立TCP连接，并向其发送针对该对象的HTTP请求
2. 网络缓存检查本地是否存储该对象副本。若存在，则通过HTTP响应消息将对象返回客户端浏览器
3. 若网络缓存未存储该对象，则向原始服务器（即`www.someschool.edu`）建立TCP连接。随后通过网络缓存至服务器的TCP连接发送HTTP请求。原始服务器接收请求后，通过HTTP响应将对象发送至网络缓存
4. 当网络缓存接收到对象时，会在本地存储副本的同时，通过客户端浏览器与网络缓存之间的现有TCP连接，以HTTP响应消息形式将副本发送至客户端浏览器

需要注意的是，缓存同时兼具服务器和客户端**双重身份**：当它接收浏览器请求并返回响应时作为服务器；当它向原始服务器发送请求并接收响应时则作为客户端。

**通常网络缓存由互联网服务提供商（ISP）购买和部署。**例如，大学可能在校园网内安装缓存，并将所有校园浏览器配置指向该缓存；或大型居民区ISP, 可能在其网络中安装一个或多个缓存，并预先配置出厂浏览器指向这些缓存。

网络缓存在互联网中的部署主要基于**两大优势**:

-   它能**显著降低客户端请求的响应时间**——当客户端与原始服务器之间的瓶颈带宽远低于客户端与缓存之间的带宽时尤为明显。若客户端与缓存之间存在高速连接（这种情况十分常见），且缓存存有请求对象，则能快速向客户端交付对象
-   正如后续示例将说明的，网络缓存**能大幅减少机构互联网接入链路上的流量**。通过降低流量，机构（如企业或大学）可延缓带宽升级需求从而节约成本。此外，网络缓存还能整体减少互联网中的Web流量，进而提升所有应用的性能表现。

>   [!NOTE]
>
>   可以在很大程度上将Web Cache(Proxy Server)看作计算机组成原理中的Cache .

![image-20250920105956178](./chap2_Application_Layer_pic/web_cache(proxy_server).png)

Through the use of Content Distribution Networks (CDNs), Web caches are  increasingly playing an important role in the Internet. A CDN company installs many  geographically distributed caches throughout the Internet, thereby localizing much of  the traffic. There are shared CDNs (such as Akamai and Limelight) and dedicated CDNs  (such as Google and Netflix). We will discuss CDNs in more detail in Section 2.6.

#### The Conditional GET

[此处第八版和第七版有所不同 标题序号以第八版为准]

使用缓存的方法(无论是缓存到本地还是缓存到代理服务器)都可能会遇到缓存内容过期的问题 . 

“条件GET”是HTTP协议中的一种优化机制，**允许客户端（通常是浏览器或缓存服务器）向服务器验证其本地存储的缓存副本是否仍然是最新的**。如果副本没有更改，服务器会返回一个极小的 `304 Not Modified` 响应，而不是完整的请求对象，从而显著节省网络带宽和加载时间。

该机制依赖于HTTP头域中几个特定的字段来实现。

1.   首次请求（缓存未命中时）
     当缓存（或浏览器）第一次向原始服务器请求一个对象时，服务器会在返回响应（状态码 `200 OK`）的同时，在响应头中附带一个校验器（Validator），通常是：
     *   `Last-Modified`： 指示该对象最后被修改的日期和时间。
     *   `ETag`（实体标签）： 一个唯一标识对象版本的字符串（类似于指纹或哈希值）。如果对象被修改，即使内容不变（例如被重新上传），`ETag` 通常也会改变，它比 `Last-Modified` 更精确。

服务器响应示例：
```http
HTTP/1.1 200 OK
Date: Sat, 08 Oct 2022 15:26:48 GMT
Server: Apache
Last-Modified: Wed, 05 Oct 2022 08:23:17 GMT  <-- 校验器
ETag: "a7f64-s1w3-ec85d3e86c9c0"             <-- 校验器
Content-Length: 83254
...（这里是对象数据）
```
缓存服务器会存储这个对象，并**同时保存这些校验器信息**。

2. 后续请求（验证缓存时）
当缓存需要再次请求同一个对象（例如，缓存副本已过期）时，它不会直接请求完整对象，而是发起一个“条件GET”请求。它会将之前服务器发来的校验器信息放入**请求头**中发送给服务器，用于询问“我持有的这个版本是否仍然有效？”。

常用的请求头有两个：
    -  `If-Modified-Since` 头：
        缓存会发送：`If-Modified-Since: <Last-Modified的值>`
        意思是：“如果自这个日期时间之后对象被修改过，请返回新对象。”
        -  `If-None-Match` 头：
            	缓存会发送：`If-None-Match: <ETag的值>`
            	意思是：“如果我提供的ETag与服务器上当前版本的ETag不匹配，请返回新对象。”（`None-Match` 即“不匹配”）

`ETag` 的优先级通常高于 `Last-Modified`。现代Web服务器更倾向于使用 `If-None-Match`。

3.   服务器验证并响应
     服务器收到条件GET请求后，会将其携带的校验器与当前服务器上该对象的校验器进行比对。结果有两种：

*   **情况一：对象未修改（缓存有效）**
    如果服务器判断 `If-None-Match` 的ETag匹配，或者 `If-Modified-Since` 的时间晚于或等于对象的最后修改时间，则说明客户端的缓存仍然是最新的。
    服务器会返回一个极简的响应：**`304 Not Modified`**。这个响应没有消息体（body），只包含一些头信息。
    ```http
    HTTP/1.1 304 Not Modified
    Date: Sat, 08 Oct 2022 16:00:32 GMT
    Server: Apache
    （消息体为空，节省了大量带宽）
    ```
    缓存收到 `304` 响应后，知道其本地副本是新鲜的，于是会更新该缓存条目的过期时间等信息，并将副本返回给客户端。

*   **情况二：对象已修改（缓存失效）**
    如果校验器不匹配（ETag不同或对象在指定时间后被修改过），则说明缓存副本已经过期。
    服务器会像处理普通GET请求一样，忽略条件头，返回一个完整的 **`200 OK`** 响应，并在消息体中包含最新的对象内容。同时，响应头中会带有新的 `Last-Modified` 和 `ETag` 值。
    缓存会丢弃旧的副本，存储新的对象和新的校验器，然后将其返回给客户端。

---

**条件GET的核心优势：**

*   **大幅减少网络带宽消耗**：`304` 响应没有消息体，体积非常小，避免了重复传输未被修改的完整内容。
*   **降低服务器负载**：服务器无需为未修改的资源重新生成完整的响应。
*   **加快用户感知的加载速度**：缓存可以快速验证并返回本地资源，无需等待完整的数据传输。

这正是Web缓存能够高效工作、提升性能并减少流量的关键技术之一。

### 2.2.6 HTTP/2

HTTP/2 [RFC 7540], standardized in 2015, was the first new version of HTTP since  HTTP/1.1, which was standardized in 1997. Since standardization, HTTP/2 has  taken off, with over 40% of the top 10 million websites supporting HTTP/2 in 2020  [W3Techs]. Most browsers also support HTTP/2. 

**The primary goals for HTTP/2 are to reduce perceived(可感知的) latency by enabling request  and response multiplexing over a single TCP connection, provide request prioritization  and server push, and provide efficient compression of HTTP header fields.** 

**HTTP/2  does not change HTTP methods, status codes, URLs, or header fields. Instead, HTTP/2  changes how the data is formatted and transported between the client and server.**

To motivate the need for HTTP/2, recall that HTTP/1.1 uses persistent TCP  connections, allowing a Web page to be sent from server to client over a single TCP  connection. By having only one TCP connection per Web page, the number of sockets at the server is reduced and each transported Web page gets a fair share of the  network bandwidth (as discussed below). But developers of Web browsers quickly  discovered that sending all the objects in a Web page over a single TCP connection has a **Head of Line (HOL) blocking problem**. To understand HOL blocking,  consider a Web page that includes an HTML base page, a large video clip near the  top of Web page, and many small objects below the video. Further suppose there is  a low-to-medium speed bottleneck link (for example, a low-speed wireless link) on  the path between server and client. Using a single TCP connection, the video clip  will take a long time to pass through the bottleneck link, while the small objects are  delayed as they wait behind the video clip; that is, the video clip at the head of the  line blocks the small objects behind it. HTTP/1.1 browsers typically work around this  problem by opening multiple parallel TCP connections, thereby having objects in the  same web page sent in parallel to the browser. This way, the small objects can arrive  at and be rendered in the browser much faster, thereby reducing user-perceived delay. 

TCP congestion(拥堵) control, discussed in detail in Chapter 3, also provides browsers an unintended incentive to use multiple parallel TCP connections rather than a  single persistent connection. Very roughly speaking, TCP congestion control aims to  give each TCP connection sharing a bottleneck link an equal share of the available  bandwidth of that link; so if there are n TCP connections operating over a bottleneck  link, then each connection approximately gets 1/n th of the bandwidth. By opening  multiple parallel TCP connections to transport a single Web page, the browser can  “cheat” and grab a larger portion of the link bandwidth. Many HTTP/1.1 browsers  open up to six parallel TCP connections not only to circumvent HOL blocking but  also to obtain more bandwidth. **One of the primary goals of HTTP/2 is to get rid of (or at least reduce the number of) parallel TCP connections for transporting a single Web page.** This not only  reduces the number of sockets that need to be open and maintained at servers, but  also allows TCP congestion control to operate as intended. But with only one TCP  connection to transport a Web page, HTTP/2 requires carefully designed mechanisms to avoid HOL blocking.

>   [!NOTE]
>
>   研究人员很早就发现了HOL(Head Of Line 队头)阻塞问题 , HTTP1.1的解决方案是并行的开多个TCP连接 . 但是考虑到浏览器的TCP连接数限制 很有可能被一个网页占据了所有的TCP连接通道 . 而且每个通道的传输能力是均分的 .
>
>   HTTP2 的主要目的就是消除/减少用于单个网页的并行TCP连接 这减少了服务器上需要打开和维护的套接字数量 当然 这需要精心的设计

#### HTTP/2 Framing 帧机制

>   [!NOTE]
>
>   The HTTP/2 solution for HOL blocking is to break each message into small frames, and  interleave the request and response messages on the same TCP connection. 
>   HTTP/2解决队头阻塞（HOL）的方法是将每条消息分解为小帧，并在同一TCP连接上交错传输请求和响应消息。

假设某网页包含一个大型视频剪辑和8个较小对象。服务器会收到浏览器想要获取该网页时发出的9个并发请求。针对每个请求，服务器需要向浏览器发送9条竞争的HTTP响应消息。假设所有帧均为固定长度，视频剪辑包含1000帧，每个较小对象包含两帧。通过帧交错传输，在发送视频剪辑的一帧后，会发送每个小对象的第一帧。接着在发送视频剪辑的第二帧后，再发送每个小对象的最后一帧。因此，所有较小对象在总共发送18帧后即可传输完成。若不使用交错传输，较小对象需在发送1016帧之后才能被传输。由此可见，HTTP/2的帧机制能显著降低用户可感知的延迟。

The ability to break down an HTTP message into independent frames, interleave them, and then reassemble them on the other end is the single most important  enhancement of HTTP/2. The framing is done by the framing sub-layer of the  HTTP/2 protocol. When a server wants to send an HTTP response, the response  is processed by the framing sub-layer, where it is broken down into frames. The  header field of the response becomes one frame, and the body of the message is  broken down into one for more additional frames. The frames of the response are  then interleaved by the framing sub-layer in the server with the frames of other  responses and sent over the single persistent TCP connection. As the frames arrive  at the client, they are first reassembled into the original response messages at the  framing sub-layer and then processed by the browser as usual. Similarly, a client’s  HTTP requests are broken into frames and interleaved. 

In addition to breaking down each HTTP message into independent frames, the  framing sublayer also binary encodes the frames. Binary protocols are more efficient  to parse, lead to slightly smaller frames, and are less error-prone.

#### Response Message Prioritization and Server Pushing

**Message prioritization allows developers to customize the relative priority of  requests to better optimize application performance.**
**消息优先级设定允许开发者自定义请求的相对优先级，从而更好地优化应用性能。**

 As we just learned, the framing sub-layer organizes messages into parallel streams of data destined to the same  requestor. When a client sends concurrent requests to a server, it can prioritize the  responses it is requesting by assigning a weight between 1 and 256 to each message.  The higher number indicates higher priority. Using these weights, the server can  send first the frames for the responses with the highest priority. In addition to this,  the client also states each message’s dependency on other messages by specifying  the ID of the message on which it depends. 

**Another feature of HTTP/2 is the ability for a server to send multiple responses  for a single client request.**
**HTTP/2的另一项特性是服务器能够针对单个客户端请求发送多个响应。** 

That is, in addition to the response to the original request,  the server can push additional objects to the client, without the client having to  request each one. This is possible since the HTML base page indicates the objects  that will be needed to fully render the Web page. So instead of waiting for the  HTTP requests for these objects, the server can analyze the HTML page, identify  the objects that are needed, and send them to the client before receiving explicit  requests for these objects. Server push eliminates the extra latency due to waiting  for the requests.

#### HTTP/3 

>   [!NOTE]
>
>   **QUIC** is a "transport" layer network protocol developed by Google to enhance **network speed and security**. It operates over **UDP** and integrates **TLS 1.3** for improved data transmission efficiency.

QUIC, discussed in Chapter 3, is a new “transport” protocol that is implemented in  the application layer over the bare-bones UDP protocol. QUIC has several features  that are desirable for HTTP, such as message multiplexing (interleaving), per-stream  flow control, and low-latency connection establishment. 

HTTP/3 is yet a new HTTP  protocol that is designed to operate over QUIC. As of 2020, HTTP/3 is described  in Internet drafts and has not yet been fully standardized. Many of the HTTP/2 features (such as message interleaving) are subsumed(将...归入 \ 纳入) by QUIC, allowing for a simpler,  streamlined design for HTTP/3.

>   [!NOTE]
>
>   **QUIC到底是运输层协议还是应用层协议**
>
>   最准确的回答是：QUIC是一个传输层协议，但它被设计为在用户空间（Application Space）中实现，并直接集成在应用层协议（HTTP/3）中，这模糊了传统的网络分层界限。

## 2.3 Electronic Mail in the Internet

电子邮件主要有三个组成部分 : 1. 用户代理(user agent) 2. 邮件服务器(mail server) 3. 简单邮件传输协议(SMTP)

接下来我们考虑一个情景 Alice 给 Bob 发送邮件 .

**When Alice is  finished composing her message, her user agent sends the message to her mail server,  where the message is placed in the mail server’s outgoing message queue. When Bob  wants to read a message, his user agent retrieves the message from his mailbox in his  mail server.**

**Mail servers** form the core of the e-mail infrastructure. Each recipient(接收方), such  as Bob, has a mailbox located in one of the mail servers. Bob’s mailbox manages  and maintains the messages that have been sent to him. **A typical message starts its  journey in the sender’s user agent, then travels to the sender’s mail server, and then travels to the recipient’s mail server, where it is deposited in the recipient’s mailbox.**  When Bob wants to access the messages in his mailbox, the mail server containing  his mailbox authenticates Bob (with his username and password). 

**Alice’s mail server  must also deal with failures in Bob’s mail server.** If Alice’s server cannot deliver  mail to Bob’s server, Alice’s server holds the message in a message queue and  attempts to transfer the message later. Reattempts are often done every 30 minutes or so; if there is no success after several days, the server removes the message and  notifies the sender (Alice) with an e-mail message.

### 2.3.1 SMTP

SMTP 是因特网电子邮件中主要的应用层协议。它使用 TCP 可靠数据传输服务，从**发送方的邮件服务器**向**接收方的邮件服务器**发送邮件。也就是说 STMP 协议是作用于两个邮件服务器的 .

像大多数应用层协议一样，SMTP 也有两个部分：运行在发送方邮件服务器的客户端和运行在接收方邮件服务器的服务器端。每台邮件服务器上既运行 SMTP 的客户端也运行 SMTP 的服务器端。当一个邮件服务器向其他邮件服务器发送邮件时，它就表现为 SMTP 的客户；当邮件服务器从其他邮件服务器上接收邮件时，它就表现为一个 SMTP 的服务器。

![image-20250921113852473](./chap2_Application_Layer_pic/Alice_sends_a_message_to_Bob.png)

>   [!IMPORTANT]
>
>   SMTP的一个重要特性是 它不会经过中间服务器 即使两个服务器在地球的两端 SMTP 下 , 也只会把邮件直接发送到对方的服务器
>
>   因此 如果对方的服务器没有开机 那么该报文就会保留在发送方的邮件服务器上并等待新的尝试 **不会经过第三方服务器** .

>   [!NOTE]
>
>   **SMTP与HTTP的对比**
>
>   这两个协议**都用于从一台主机向另一台主机传送文件**：HTTP从Web服务器向Web客户（通常是一个浏览器）传送文件（也称为对象）；SMTP从一个邮件服务器向另一个邮件服务器传送文件（即电子邮件报文）。当进行文件传送时，持续的HTTP和SMTP都使用**持续连接**。因此，这两个协议有一些共同特征。
>
>   然而，两者之间也有一些重要的区别。
>
>   -   首先，HTTP主要是一个**拉协议（pull protocol）**，即在方便的时候，某些人在Web服务器上装载信息，用户使用HTTP从该服务器拉取这些信息。特别是TCP连接是由想接收文件的机器发起的。另一方面，SMTP基本上是一个**推协议（push protocol）**，即发送邮件服务器把文件推向接收邮件服务器。特别是，这个TCP连接是由要发送该文件的机器发起的。
>
>   -   第二个区别就是我们前面间接地提到过的，SMTP要求每个报文（包括它们的体）采用7比特ASCII码格式。如果某报文包含了非7比特ASCII字符（如具有重音的法文字符）或二进制数据（如图形文件），则该报文必须按照7比特ASCII码进行编码。HTTP数据则不受这种限制。
>
>   -   第三个重要区别是如何处理一个既包含文本又包含图形（也可能是其他媒体类型）的文档。如我们在2.2节知道的那样，HTTP把每个对象封装到它自己的HTTP响应报文中，而SMTP则把所有报文对象放在一个报文之中。

### 2.3.2 Mail Message Formats

Every header must have

-   From: header line 

-   To: header line

-   a header may include a Subject: header line as well as other optional header  lines. 

这些内容或许与SMTP命令很像 但是他们是绝对不同的 . 

The commands in that section were part of the  SMTP handshaking protocol; the header lines examined in this section are part of  the mail message itself. A typical message header looks like this: 

```shell
From: alice@crepes.fr 
To: bob@hamburger.edu 
Subject: Searching for the meaning of life.
```

也就是说:

**SMTP 命令（如 MAIL FROM、RCPT TO）是传输协议层面的，用于服务器之间握手和传递邮件。**
**邮件头部（如 From:、To:、Subject:）是邮件内容的一部分，属于邮件消息本身的元数据。**

After the message header, a blank line follows; then the message body (in ASCII)  follows.

### 2.3.3 Mail Access Protocols

#### 1. **邮件传输过程（SMTP）**

-   邮件从 Alice 发送到 Bob，**不是直接从 Alice 的电脑到 Bob 的电脑**。
-   而是：
    -   Alice 的用户代理（比如 Outlook）→ 她的邮件服务器（SMTP）
    -   她的邮件服务器 → Bob 的邮件服务器（SMTP）
-   这样做的好处是：**即使 Bob 的邮件服务器暂时离线，Alice 的服务器可以反复尝试发送**，直到成功。

#### 2. **邮件访问过程（POP3 / IMAP / HTTP）**

-   Bob 的邮件已经在他自己的邮件服务器上了，但他**不能用 SMTP 来取邮件**，因为 SMTP 是“推”协议（只负责发，不负责收）。
-   所以 Bob 需要用**邮件访问协议**把邮件从服务器“拉”到自己的设备上：
    -   **POP3**：简单，下载邮件后通常从服务器删除。
    -   **IMAP**：更强大，邮件保留在服务器上，支持多设备同步。
    -   **HTTP**：比如通过网页邮箱（如 Gmail 网页版）访问邮件。

## 2.4 DNS—The Internet’s Directory Service

主机名如`www.google.com`或者`www.eurecom.fr`这类主机名字几乎没有提供主机在因特网中的位置信息 可能我们只能从`.fr`或者`.cn`中看出其所在国家的名字 .

>   [!NOTE]
>
>   `.com``.cn``.ai``.xyz` 都是 **顶级域名（TLD, Top-Level Domain）**
>
>   ### ✅ 常见顶级域名含义表：
>
>   | 域名后缀 |     全称/来源      |               含义/用途                |                备注                |
>   | :------: | :----------------: | :------------------------------------: | :--------------------------------: |
>   |  `com`   |     commercial     |           商业用途（最通用）           |      全球最流行，任何人可注册      |
>   |   `cn`   |       China        |            中国国家顶级域名            |  由中国政府管理，适合中国本土网站  |
>   |   `ai`   | Anguilla（安圭拉） | 原本是加勒比小国域名，现被AI公司“抢注” |  人工智能（AI）行业最爱，价格较贵  |
>   |  `xyz`   | 字母表最后三个字母 |         通用、年轻化、创意域名         | 便宜、好记，适合个人项目或创业公司 |

所以我们接下来会简单讨论一下IP地址 . 每个IP地址由四个字节组成 这样每个字节就表示`0~255`的十进制数字 . 

### 2.4.1 Services Provided by DNS

人类擅长记忆主机名字而计算机适合记忆IP地址 , 所以需要使用DNS(Domain Name System)进行转换 . 

DNS（Domain Name System，域名系统）是互联网的核心服务之一，它的主要作用是将人类可读的域名（如 `www.example.com`）转换为机器可识别的 IP 地址（如 `192.0.2.1`），从而让用户的设备能够找到并访问目标服务器。**它是一个帮助主机查询分布式数据库的应用层协议(尽管它不直接与用户打交道)** . 其主机通常运行BIND(Berkeley Internet Name Domain)软件 . 报文通过UDP协议 53号端口收发 .

---

#### DNS 的核心功能
|     功能     |                             说明                             |
| :----------: | :----------------------------------------------------------: |
| **域名解析** |          将域名解析为 IP 地址（A 记录、AAAA 记录）           |
| **反向解析** |               将 IP 地址解析为域名（PTR 记录）               |
| **邮件路由** |                  通过 MX 记录指定邮件服务器                  |
| **负载均衡** | DNS也用于在冗余的服务器（如允余的Web服务器<br/>等）之间进行负载分配。紧忙的站点（如cnn.com）被允余分布在多台服务器上，<br/>每台服务器均运行在不同的端系统上，每个都有着不同的IP地址。由于这些允余<br/>的Web服务器，一个IP地址集合因此与同一个规范主机名相联系。DNS数据库中<br/>存储着这些IP地址集合。当客户对映射到某地址集合的名字发出一个DNS请求<br/>时，该服务器用IP地址的整个集合进行响应，但在每个回答中循环这些地址次<br/>序。因为客户通常总是向IP地址排在最前面的服务器发送HTTP请求报文，所以<br/>DNS就在所有这些允余的Web服务器之间循环分配了负载。DNS的循环同样可以<br/>用于邮件服务器，因此，多个邮件服务器可以具有相同的别名。 |
| **别名设置** | 使用 CNAME 将一个域名指向另一个域名<br />(这里包括邮箱名称的别名和网站域名的别名) |

---

#### 一次 DNS 查询的典型流程
1. 用户在浏览器输入 `www.example.com\index.html`,浏览器会从中抽取出主机名称`www.example.com`并传递给DNS应用的客户端 .
2. 操作系统检查本地缓存 → 没有
3. 会从客户端向服务器端发送一个包含主机名的请求
4. 客户端最终会收到一份回答报文 其中含有对应与该主机名的IP地址
5. 便能够向位于该IP地址的80端口的HTTP服务器进程发起一个TCP连接

很显然这个过程会带来客观的时延 所以我们尽量把常用或者全部的IP地址放在一个附近的DNS服务器中 .

---

#### 常用 DNS 记录类型
| 类型  | 含义                         | 示例                                                   |
| ----- | ---------------------------- | ------------------------------------------------------ |
| A     | 域名 → IPv4 地址             | `www.example.com → 93.184.216.34`                      |
| AAAA  | 域名 → IPv6 地址             | `www.example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| CNAME | 别名                         | `blog.example.com → www.example.com`                   |
| MX    | 邮件服务器                   | `example.com → mail.example.com`                       |
| TXT   | 文本记录（用于验证、SPF 等） | `example.com → "v=spf1 include:_spf.google.com ~all"`  |
| NS    | 权威域名服务器               | `example.com → ns1.example.net`                        |

### 2.4.2 Overview of How DNS Works

每一个域名的IP地址查询都需要访问一个数据库(服务器) 提供这个服务的黑盒子非常复杂 它由分布在全球的大量的DNS服务器以及定义了DNS服务器与查询主机通信方式的应用层组成 . [显然 只设置一个集中的服务器是不好的 所以DNS的服务器是一个精彩的在因特网上实现的分布式数据库的范例 ]

实际上 没有一台DNS服务器含有全部的数据 而是以层次方式组织 具体有 : 根服务器 顶级域服务器 和 权威DNS服务器 .

![image-20250923200930963](./chap2_Application_Layer_pic/DNS服务器的分层结构.png)

-   **根 DNS 服务器**。有 400 多个根名字服务器遍及全世界。这些根名字服务器由 13 个不同的组织管理。根名字服务器的全部清单连同管理它们的组织及其 IP 地址可在 [ Root Servers2016 ] 中找到。根名字服务器提供 TLD 服务器的 IP 地址。
-   **顶级域 (TLD) 服务器**。对于每个顶级域（如 `com、org、net、edu` 和 `gov`）和所有国家的顶级域（如 `uk、fr、ca` 和` jp`），都有 TLD 服务器（或服务器集群）。支持 TLD 的网络基础设施可能是大而复杂的。所有顶级域的列表参见 [ TLD List 2016 ] 。
    **TLD 服务器提供了权威 DNS 服务器的 IP 地址。**
-   **权威 DNS 服务器**。在因特网上具有公共可访问主机（如 Web 服务器和邮件服务器）的每个组织机构必须提供公共可访问的 DNS 记录，这些记录将这些主机的名字映射为 IP 地址。一个组织机构的权威 DNS 服务器收藏了这些 DNS 记录。一个组织机构能够选择实现它自己的权威 DNS 服务器以保存这些记录；另一种方法是，该组织能够支付费用，让这些记录存储在某个服务提供商的一个权威 DNS 服务器中。多数大学和大公司实现和维护它们自己基本和辅助（备份）的权威 DNS 服务器。

根、TLD 和权威 DNS 服务器都处在该 DNS 服务器的层次结构中，如[图 2-17] 所示。

还有另一类重要的 DNS 服务器，称为**本地 DNS 服务器 (local DNS server)**。严格说来，一个本地 DNS 服务器并不属于该服务器的层次结构，但它对 DNS 层次结构是至关重要的。每个 ISP（如一个居民区的 ISP 或一个机构的 ISP）都有一台本地 DNS 服务器（也叫默认名字服务器）。当主机与某个 ISP 连接时，该 ISP 提供一台主机的 IP 地址，该主机具有一台或多台其本地 DNS 服务器的 IP 地址（通常通过 DHCP，将在第 4 章中讨论）。通过访问 Windows 或 UNIX 的网络状态窗口，用户能够容易地确定他的本地 DNS 服务器的 IP 地址。主机的本地 DNS 服务器通常“邻近”本主机。对某机构 ISP 而言，本地 DNS 服务器可能就与主机在同一个局域网中；对于某居民区 ISP 来说，本地 DNS 服务器通常与主机相隔不超过几台路由器。当主机发出 DNS 请求时，该请求被发往本地 DNS 服务器，它起着代理的作用，并将该请求转发到 DNS 服务器层次结构中，我们下面将更为详细地讨论。

#### 递归查询和迭代查询 "原则"

![image-20250923204210274](chap2_Application_Layer_pic/Interaction_DNS.png)

The example shown in Figure 2.19 makes use of both **recursive queries** and  **iterative queries**. The query sent from `cse.nyu.edu` to `dns.nyu.edu` is a  recursive query, since the query asks `dns.nyu.edu` to obtain the mapping on its  behalf. However, the subsequent three queries are iterative since all of the replies  are directly returned to dns.nyu.edu. In theory, any DNS query can be iterative or recursive. For example, Figure 2.20 shows a DNS query chain for which all  of the queries are recursive. In practice, **the queries typically follow the pattern in  Figure 2.19: The query from the requesting host to the local DNS server is recursive,  and the remaining queries are iterative.**

![image-20250923204635579](./chap2_Application_Layer_pic/全递归查询.png)

>   [!NOTE]
>
>   ### DNS缓存机制
>
>   实际上 在本地的DNS服务器中 会经常缓存常用的主机名/IP地址对 (一般超过两天就会丢弃这个缓存信息)
>
>   DNS缓存可以**减少时延**并**减少在因特网上到处传输的DNS报文数量**
>
>   事实上 因为缓存 大量的DNS查询得以绕过根服务器

### 2.4.3 DNS Records and Messages

The DNS servers that together implement the DNS distributed database store  resource records (RRs), including RRs that provide hostname-to-IP address mappings . 
每一个资源记录Resource Record(RRs)都保存了主机名到IP的映射对 这些RR实际上是一个四元组 : 

```
(Name, Value, Type, TTL)
```

-   Name:主机名 如 `www.example.com`
-   Value:它的具体含义完全由 Type 字段决定，这是理解RR的关键。
    -   如果 `Type=A`，那么 `Value` 就是一个 **IPv4 地址**（例如 `192.0.2.1`）。
    -   如果 `Type=NS`，那么 `Value` 就是一个 **权威DNS服务器的主机名**（例如 `dns.example.com`）。
    -   如果 `Type=CNAME`，那么 `Value` 就是一个 **别名指向的规范名称**（例如 `example.com`）。
    -   如果 `Type=MX`，那么 `Value` 就是 **邮件服务器的主机名**（例如 `mail.example.com`）。
-    Type: 这是资源记录中**最重要的字段**，它定义了 `Value` 字段的数据类型以及这条记录的用途。
    -   见上表中的类型 [2.4.1 / 常用 DNS 记录类型]
-    TTL (Time To Live，存活时间)
    -   **含义**： 这条记录在**非权威DNS服务器（如本地DNS服务器）的缓存中应该被保存多久**。单位通常是秒。
    -   **功能**： 平衡DNS查询的效率和数据的一致性。TTL时间长，可以减少对权威服务器的查询，响应更快；TTL时间短，可以更快地获取到域名记录的最新变更。
    -   **示例**： `TTL=3600` 表示这条记录可以在缓存中保留1小时（3600秒）。

#### DNS Messages

DNS只有查询和回答这两种报文 且这两种报文的格式相同 如下 :

![image-20250923210012291](./chap2_Application_Layer_pic/DNS报文格式.png)

- **首部区域**（前12个字节）：包含多个字段。
  - **标识符**（16位）：用于标识查询，会被复制到回答报文中，以便匹配请求和回答。
  - **标志字段**：包含若干标志位：
    - **查询/回答**（1位）：指示报文是查询（0）还是回答（1）。
    - **权威的**（1位）：若 DNS 服务器是所请求名字的权威服务器，则在回答报文中置位。
    - **希望递归**（1位）：若客户希望服务器执行递归查询，则置位。
    - **递归可用**（1位）：若 DNS 服务器支持递归查询，则在回答报文中置位。
  - **数量字段**（4个）：指出后续4类数据区域的出现数量。

- **问题区域**：包含查询信息。
  - **名字字段**：被查询的主机名。
  - **类型字段**：询问的问题类型（如 A、MX 等）。

- **回答区域**（在回答报文中）：包含对最初请求名字的资源记录（RR），每条记录包含 Type、Value、TTL 等。可包含多条 RR（如一个主机名对应多个 IP 地址）。

- **权威区域**：包含其他权威服务器的记录。

- **附加区域**：包含其他有帮助的记录。例如，对 MX 请求的回答可能包含邮件服务器的规范主机名（回答区域），而附加区域则提供该主机名的 IP 地址（A 记录）。

有一些程序可以帮助查看DNS报文 书中给出的是`nslookup`程序 但是考虑到本书比较老 应该自行上网先看看有没有更好的程序 . 以免出现之前的`telnet`不如`curl`的现象.

>   [!CAUTION]
>
>   亲测可以在`powershell`上直接使用
>
>   ```shell
>   nslookup www.bilibili.com
>   服务器:  dns1.cug.edu.cn
>   Address:  202.114.200.252
>   
>   非权威应答:
>   名称:    www.bilibili.com
>   Addresses:  240e:978:90d:1000::76
>            240e:978:90d:1000::70
>            61.147.236.102
>            175.4.62.128
>            114.230.222.139
>            61.147.236.101
>            61.147.236.104
>            183.131.147.48
>   ```
>   这是一个非常标准的 `nslookup` 命令输出，它查询了域名 `www.bilibili.com` 对应的 IP 地址。我们来逐部分解读：
>
>   ### 1. 本地使用的 DNS 服务器
>   ```
>   服务器:  dns1.cug.edu.cn
>   Address:  202.114.200.252
>   ```
>   *   **解读**： 你的电脑在进行域名解析时，向指定的 DNS 服务器发出了查询请求。
>   *   **`dns1.cug.edu.cn`**： 这是你使用的 DNS 服务器的域名，从名字可以看出这是 **中国地质大学（武汉）** 的 DNS 服务器。
>   *   **`202.114.200.252`**： 这是上述域名对应的 IP 地址。所有查询请求都发往这个地址。
>
>   ### 2. 查询结果
>   ```
>   非权威应答:
>   名称:    www.bilibili.com
>   Addresses:  ...
>   ```
>   *   **非权威应答**： 这是一个关键术语。它意味着你查询的 DNS 服务器（`dns1.cug.edu.cn`）并不是 `bilibili.com` 这个域名的官方管理者。它只是从自己的缓存中，或者向上级 DNS 服务器查询后，将结果返回给你。如果它是 B站 自己的 DNS 服务器，那么返回的结果就是“权威应答”。
>   *   **名称**： 你查询的域名。
>   *   **Addresses**： 下面列出的就是 `www.bilibili.com` 这个域名当前解析出的所有 IP 地址。
>
>   ### 3. IP 地址列表
>   ```
>   Addresses:
>     240e:978:90d:1000::76
>     240e:978:90d:1000::70
>     61.147.236.102
>     175.4.62.128
>     114.230.222.139
>     61.147.236.101
>     61.147.236.104
>     183.131.147.48
>   ```
>   这部分列出了 B站 网站服务器的 IP 地址，有两种类型：
>
>   *   **IPv6 地址**（以 `240e:` 开头的）：
>       *   `240e:978:90d:1000::76`
>       *   `240e:978:90d:1000::70`
>       *   **解读**： 这是新一代的互联网协议地址，长度更长，可以提供更多的地址数量。如果你的网络环境支持 IPv6，你的设备可能会优先尝试通过 IPv6 地址来访问 B站，这通常速度更快。
>
>   *   **IPv4 地址**（以数字和点组成的，如 `61.147.236.102`）：
>       *   后面列出的所有其他地址都是 IPv4 地址。
>       *   **解读**： 这是目前最广泛使用的互联网协议地址。
>
>   **为什么有这么多 IP 地址？**
>   这体现了大型网站常用的 **负载均衡** 技术。当成千上万的用户同时访问 `www.bilibili.com` 时，如果只有一个服务器和一个 IP 地址，服务器肯定会不堪重负。通过将一个域名解析到多个 IP 地址，DNS 服务器可以轮询或智能地将用户请求分发到不同的后端服务器上，从而：
>   1.  **分担流量压力**，避免单台服务器过载。
>   2.  **提高网站的可用性**，如果其中一台服务器出现故障，请求可以被自动导向其他正常的服务器，用户可能完全感知不到。
>
>   ### 总结
>
>   这个 `nslookup` 结果的简单解读是：
>
>   **你通过中国地质大学（武汉）的 DNS 服务器查询到，B站 的官方网站 `www.bilibili.com` 背后有多个服务器在同时工作，其中包含 2 个 IPv6 地址和 6 个 IPv4 地址。这样做是为了保证网站的高性能和稳定性。**
>
>   你可以尝试再运行一次 `nslookup www.bilibili.com`，可能会发现返回的 IP 地址顺序变了，这就是负载均衡策略的一个简单体现。

#### Inserting Records into the DNS Database

[需要注册]

>   [!NOTE]
>
>   ### DNS 面临的攻击类型
>
>   #### 1. **DDoS 带宽洪泛攻击**
>   - **攻击方式**：向 DNS 服务器 , 如根服务器或顶级域名服务器(通常对顶级域名服务器伤害更大) , 发送大量无效请求，使其无法响应合法查询。
>   - **实例**：2002 年 10 月对 13 个 DNS 根服务器的 DDoS 攻击。
>   - **结果**：由于分组过滤器和缓存机制，实际影响很小。
>
>   #### 2. **针对顶级域名服务器的 DDoS 攻击**
>   - 攻击目标转向处理具体域名的服务器（如 `.com` 服务器）。
>   - 此类攻击更难过滤，但可通过本地 DNS 缓存缓解。
>
>   #### 3. **中间人攻击**
>   - 攻击者截获 DNS 查询并返回伪造的响应，将用户引导至恶意网站。
>
>   #### 4. **DNS 缓存投毒**
>   - 攻击者向 DNS 服务器发送伪造记录，污染其缓存，影响后续查询结果。
>
>   - **中间人攻击**和**缓存投毒**需要拦截或控制网络流量或服务器，技术难度较高。
>
>   ---
>
>   ### 结论
>   - DNS 尽管存在多种潜在攻击方式，但因其具备**缓存机制、分组过滤、分布式架构**等防护手段，表现出**较强的抗攻击能力**。
>   - 至今尚未出现导致 DNS 服务大规模瘫痪的成功攻击。
>

## 2.5 Peer-to-Peer File Distribution

我们也不能忽略成对间歇连接的主机是用户自己的`PCs, laptops, and  smartphones`的P2P连接 .

我们考虑的一个模型是 从单一服务器向大量主机(peers 对等方)分发一个大文件 容易看出 这个操作对服务器的带宽需求极大 . 当前最为流行的P2P协议是`BitTorrent`.

### Scalability of P2P Architectures

![image-20250924083124692](./chap2_Application_Layer_pic/P2P分发.png)

我们在理想情况下考虑分发时间(distribution time) 用 , 也就是 $N$ 个Peers 得到该文件所需的时间 . 我们定义$u_i$表示接收方上传速率 , $d_i$表示接收方下载速率 , $u_s$表示服务器上传速率 , 文件总大小是 F .

**对于服务器-客户端体系** , $D_{cs}$表示分发时间 , 分别考虑上传和下载的最大限制 得到 
$$
D_{cs} \geq max \{ \frac{N F}{u_s} , \frac{F}{d_{min}}\}
\\
d_{min} = min \{ d_1,d_2 \cdots d_{N} \}
$$
可以看到受N的影响 当N很大的时候 $D_{cs}$ 非常大 .

**对于P2P体系** , $D_{cs}$表示分发时间 , 分别考虑上传和下载的最大限制 得到 
$$
D_{p2p} \geqslant \max\left\{ \frac{F}{\mu_s}, \frac{F}{d_{\min}}, \frac{NF}{u_s + \sum_{i=1}^N u_i} \right\}
$$
其中 第三项考虑的限制是 整个体系需要总共会分发出$NF$的文件 总文件速率就是${u_s + \sum_{i=1}^N u_i}$.

我们考虑$N$为自变量 可以发现在N大于一定值时成为主要的影响因素 D取到N相关项 假设我们假设 $u_{i} = \frac{u_s}{10}$ 会看到下图的增长效果 :

![image-20250924090416476](./chap2_Application_Layer_pic/P2P和CS体系的分发时长.png)

### BitTorrent

这一段书上写的不是很好 参考`deepseek`.

>   [!NOTE]
>
>   好的，这是一份关于 BitTorrent 的详细介绍。我将从基本概念、工作原理、技术组件、优缺点以及常见用途等方面进行全面阐述。
>
>   ### 一、BitTorrent 是什么？
>
>   BitTorrent（简称 BT）是一种**基于点对点（P2P）网络协议的文件分发技术**。与传统的“客户端-服务器”模式（如 HTTP 或 FTP 下载）不同，BitTorrent 的核心思想是 **“人人为我，我为人人”**。
>
>   *   **传统模式**：所有下载者都从一个中央服务器获取文件。服务器带宽成为瓶颈，下载人数越多，每个人的速度就越慢。
>   *   **BitTorrent 模式**：下载者在下载文件的同时，也在为其他下载者上传自己已经拥有的文件部分。参与下载的用户越多，整体的分发效率反而越高。
>
>   BitTorrent 本身不是一个软件，而是一个协议规范。遵循这个协议开发的客户端软件（如 qBittorrent、μTorrent 等）才是用户直接使用的工具。
>
>   ---
>
>   ### 二、核心工作原理：它是如何工作的？
>
>   BitTorrent 的工作流程可以概括为以下几个关键步骤和角色：
>
>   #### 关键角色
>
>   1.  **种子文件（.torrent file）或磁力链接（Magnet Link）**
>       *   **种子文件**：一个很小的文件，它不包含实际内容，只包含了文件的元数据，例如：目标文件的名称、大小、分块情况以及最重要的——**Tracker 服务器的地址**。
>       *   **磁力链接**：一串以 `magnet:?xt=urn:btih:` 开头的字符串，其本质是一个内容标识符（哈希值）。它包含了足够的信息让客户端找到对等节点，无需依赖种子文件，更加方便。
>
>   2.  **Tracker 服务器**
>       *   一个中央的协调服务器（但**不存储**实际文件）。
>       *   它的作用是记录当前有哪些**Peer**（ peer 对等端）正在下载或分享同一个文件。
>       *   当你的 BT 客户端启动时，它会向 Tracker “注册”，并获取一份正在参与该文件分享的 Peer 列表。
>
>   3.  **Peer（对等端/节点）**
>       *   网络上任何一个正在下载或上传该文件的用户，都是一个 Peer。也就是你我这样的普通用户。
>
>   4.  **Seeder（做种者）**
>       *   指那些已经拥有**完整文件**并在上传的 Peer。Seeder 是下载速度的源泉。一个 Torrent 的健康度取决于 Seeders 的数量。
>
>   5.  **Leecher（下载者 直译可作吸血鬼）**
>       *   指那些还没有下载完成，正在下载同时也在上传的 Peer。有时这个词也带有一点贬义，特指那些下载完成后就立刻关闭程序停止上传的自私用户。
>
>   #### 工作流程
>
>   1.  **开始**：用户获得一个 `.torrent` 文件或磁力链接，并用 BT 客户端打开它。
>   2.  **连接 Tracker**：客户端连接到 `.torrent` 文件中指定的 Tracker 服务器，告知“我要下载这个文件”。
>   3.  **获取 Peer 列表**：Tracker 返回一个当前正在参与该文件共享的 Peer（包括 Seeder 和 Leecher）的 IP 地址列表。
>   4.  **连接 Peer**：你的客户端开始直接与列表中的其他 Peer 建立连接。
>   5.  **交换数据块**：
>       *   文件被分割成许多个小**数据块**（例如 256KB 或 1MB）。
>       *   你的客户端会分析所有连接的 Peer 各自拥有哪些数据块。
>       *   采用一种名为 **“最稀缺优先”** 的算法：优先下载在整个网络中副本最少的那个数据块。这确保了稀有数据块能被快速复制，提高整个网络的健壮性。
>       *   同时，你的客户端也会将你已经下载好的数据块上传给其他需要的 Peer。
>   6.  **完成下载**：当所有数据块都下载完毕并校验通过后，文件就下载完成了。
>   7.  **做种**：此时你从一个 Leecher 变成了一个 Seeder。保持客户端开启，继续为他人上传，分享精神就在这里体现。
>
>   ---
>
>   ### 三、关键技术机制
>
>   1.  **choking / unchoking（阻塞/解阻塞）**
>       *   这是一种**激励机制**。你的客户端不会无限制地上传给所有 Peer。
>       *   它会优先为那些给你上传速度最快的 Peer 提供上传（解阻塞），而暂时忽略那些只下载不上传的 Peer（阻塞）。
>       *   这鼓励了用户保持上传，贡献自己的带宽。
>
>   2.  **Piece Selection（数据块选择策略）**
>       *   **最稀缺优先**：如上所述，优先下载稀缺块，优化整体网络效率。
>       *   **随机第一块**：在刚开始下载时，随机选择一些块下载，以便尽快地拥有一些可上传的内容，与其他 Peer 进行交换。
>
>   3.  **Endgame Mode（终局模式）**
>       *   当下载即将完成，只剩最后几个数据块时，客户端会向所有连接的 Peer 请求这些缺失的块。
>       *   一旦从任何一个 Peer 那里收到该块，就会向其他 Peer 取消请求，以避免带宽浪费。
>
>   ---
>
>   ### 四、BitTorrent 的优缺点
>
>   #### 优点
>
>   *   **高效分发**：下载者越多，总带宽越大，下载速度可能越快。非常适合分发大型、热门文件（如 Linux 系统镜像）。
>   *   **服务器负载低**：原始发布者（初始 Seeder）只需提供很小的初始带宽，后续主要靠 Peer 之间相互分发。
>   *   **健壮性**：没有单点故障。即使原始服务器关闭，只要网络上还有 Seeder，文件就依然可以下载。
>   *   **校验机制**：所有数据块都通过哈希校验，确保下载文件的完整性。
>
>   #### 缺点
>
>   *   **依赖做种**：如果没有人做种（即 Seeder 为 0），那么文件将无法下载。
>   *   **隐私问题**：你的 IP 地址会暴露给所有连接到的 Peer 以及 Tracker 服务器。
>   *   **版权问题**：由于其匿名性和高效性，BitTorrent 被广泛用于传播盗版内容，这使其在法律上颇具争议。
>   *   **速度不稳定**：冷门文件可能速度极慢；网络环境（如ISP限制、防火墙/NAT）也可能影响连接性。
>
>   ---
>
>   ### 五、合法与常见用途
>
>   尽管 BitTorrent 常与盗版关联，但它有许多完全合法的、重要的用途：
>
>   1.  **开源软件分发**：如 Ubuntu、Linux Mint 等大型开源操作系统主要通过 BitTorrent 分发，为官方服务器节省了大量带宽。
>   2.  **游戏更新**：像暴雪（Blizzard）的战网客户端就使用 P2P 技术来分发《魔兽世界》、《守望先锋》等游戏的大型更新包。
>   3.  **学术数据共享**：研究机构用它来共享大型数据集，例如天文望远镜数据、基因序列数据等。
>   4.  **内容分发网络（CDN）**：一些商业CDN会集成P2P技术来加速大型文件或直播流的传输。
>   5.  **独立艺术家**：音乐家、电影制作人可以使用 BitTorrent 来直接向粉丝分发作品，避免中间商。
>
>   ### 总结
>
>   BitTorrent 是一项革命性的 P2P 技术，它通过将下载者转变为上传者，巧妙地解决了大规模文件分发的效率瓶颈。其核心在于**去中心化**和**协作共享**的精神。
>
>   在使用时，请选择优秀的客户端（如 **qBittorrent**（免费开源无广告）），并务必注意：
>   *   **尊重版权**，下载合法内容。
>   *   **保持做种**，在下载完成后继续上传一段时间，回馈社区。
>   *   考虑使用 **VPN** 来保护你的隐私。

我们简要地提一下另一种 P2P 应用——分布式散列表 (DHT) 来结束我们的讨论。分布式散列表是一种简单的数据库，其数据库记录分布在一个 P2P 系统的多个对等方上。DHT 得到了广泛实现 (如在 BitTorrent 中) ，并成为大量研究的主题。在配套网站的 Video Note 中对 DHT 进行了概述。

## 2.6 Video Streaming and Content Distribution  Networks

视频流媒体等是ISP中的流量主体 他们的实现方式是 使用应用层协议和类似高速缓存的方式运行的服务器 . 第九章中会更加详细的讨论 . 

### 2.6.1 Internet Video

Many Internet companies today provide streaming video,  including, Netflix, YouTube (Google), Amazon, and TikTok.`ed = 8th , language = en`

许多因特网公司现在提供流式视频 , 包括 Netflix, YouTube (Google), Amazon, and 优酷.`ed = 7th , language = zh`

视频数据的一个重要特征是它能够被压缩(也需要被压缩) , 因而可以用比特率来权衡视频质量 . 如今的压缩算法支持把视频压缩成任何希望的比特率 当然比特率越高视频的图像质量越好 . 传输视频(尤其是高质量的流式视频 比特率可以达到3Mbps甚至10Mbps)消耗巨大的流量的存储 . 对于网络而言 最重要的性能度量就是**平均端到端吞吐量** .

这段中文翻译太烂 看英文 : In order to provide continuous playout, the network must provide  an average throughput to the streaming application that is at least as large as the bit  rate of the compressed video.

现在的普遍做法则是 把同一个视频压缩成多种比特率 用户依据网速决定自己看什么质量的视频 .

>   [!NOTE]
>
>   我有点不太理解六视频中的比特率 故 :
>   ask : 我大概理解比特率的是一种网速 但是在流视频领域中 它怎么衡量流视频的质量 和1080p 720p这种有关系吗 ?
>
>   ---
>
>   好的，直接讲核心关系。
>
>   **1. 比特率是质量的直接决定因素。**
>   比特率代表“每秒钟用于描述画面的数据量”。数据量越高，保留的细节越多，画质越清晰，压缩瑕疵（如马赛克）越少。
>
>   **2. 分辨率是质量的容器上限。**
>   1080p只是一个“画布尺寸”，规定了有207万个像素点需要被填充颜色。比特率就是用于填充这些颜色的“颜料量”。
>
>   **3. 两者的直接关系是：比特率必须匹配分辨率。**
>   *   用低比特率去填充高分辨率（如1080p），每个像素分到的“颜料”不足，结果就是画面模糊、出现大块色块和马赛克。
>   *   用高比特率去填充低分辨率（如720p），每个像素都能获得充足甚至过量的“颜料”，画面会非常干净、锐利，但无法超越720p的细节极限。
>
>   **结论：**
>   在流媒体中，**比特率是衡量实际观感的直接指标**。平台通过提供不同分辨率下、比特率匹配的多个视频文件，来适应你的网速。你看到的“1080p”选项，背后对应的是一个能满足1080p清晰度的**高比特率**文件。如果网速不够，平台会给你一个**低比特率**的1080p文件（导致画质差）或直接切换到一个**比特率匹配的720p**文件（保证画质干净流畅）。

### 2.6.2 HTTP Streaming and DASH

#### HTTP Streaming
- 视频以普通文件形式存储在 HTTP 服务器上，每个视频有唯一的 URL。
- 客户端通过 TCP 连接发送 HTTP GET 请求获取视频。
- 服务器尽可能快地发送视频数据，客户端接收并缓存数据。
- 当缓存数据达到一定阈值时，客户端开始播放视频，同时继续缓存后续内容。

**缺陷：**
- 所有客户端接收相同编码的视频，无法适应不同客户端的带宽差异。

#### DASH（Dynamic Adaptive Streaming over HTTP）
- 将视频编码为多个不同比特率（质量）的版本。
- 视频被切分为若干个小段（chunk），每段几秒钟。
- 客户端根据当前带宽动态选择不同版本的视频段进行请求和播放。

**工作流程：**
1. 客户端首先请求**告示文件（manifest file）**，获取所有可用版本的 URL 和比特率信息。
2. 客户端根据当前网络状况（如缓存量、实测带宽）选择合适版本的视频段。
3. 通过 HTTP GET 请求指定 URL 和字节范围，逐段下载视频。
4. 客户端持续测量带宽并动态调整下一次请求的视频质量。

**优势：**
- 适应不同网络环境（如 3G、光纤）和带宽波动。
- 特别适合移动网络用户，能应对带宽变化。
- 客户端可自主切换视频质量，提升用户体验。

### 2.6.3 Content Distribution Networks

**challenge:** how to stream content (selected from millions of videos) to hundreds of thousands of simultaneous users?

-   option 1 : 建立单一的大规模数据中心 在数据中心存储其所有视频 然后直接从这个数据中心向所有用户分发视频
    -   单点故障
    -   如果客户远离数据中心 会经过多个ISP 时延可能很大
    -   消耗大量网络带宽
-   option 2 : 内容分发网络 Content Distribution Network CDN 在多个地理位置的服务器(可以是专用的CDN 也可以借用第三方CDN)中储存视频的副本

这些都应该类比cache机制 不是所有的集群都会保存所有的资料数据 可能会有地方差异

**邀请做客**的机制 好于 **深入**的机制(深入的目标事靠近用户端 用来降低时延和吞吐量 但是这种高度分布式的设计 维护和管理任务成为挑战)

[pass]

### 2.6.4 Case Studies: Netflix and YouTube

[pass]

## 2.7 Socket Programming: Creating Network Applications

Now that we’ve looked at a number of important network applications, let’s explore how network application programs are actually created. Recall from Section 2.1 that **a typical network application consists of a pair of programs—a client program and a server program—residing in two different end systems**. When these two programs  are executed, a client process and a server process are created, and these processes communicate with each other by reading from, and writing to, **sockets**. 

**When creating a network application, the developer’s main task is therefore to write the code for both the client and server programs.**

>   [!NOTE]
>
>   网络应用程序主要有两类 : 
>
>   1. **开放协议型网络应用程序**
>
>       - 定义：<u>基于公开标准协议（如 RFC 或其他标准文档）</u>实现的应用程序。
>       - 特点：协议规则公开透明，任何人都可以查阅 ; 客户端和服务器程序必须严格遵守协议规范。
>       - 示例：HTTP 协议（RFC 2616）：如 Chrome 浏览器与 Apache Web 服务器的通信 ;  BitTorrent 协议：客户端与跟踪器之间的通信。
>       - 优势：不同开发者可以独立开发兼容的客户端和服务器程序 ;  具有良好的互操作性。
>
>   2. **专用网络应用程序**
>
>       - 定义：使用<u>私有、未公开的应用层协议</u>的应用程序。
>
>       - 特点：协议规范不公开发布，仅由开发团队内部掌握 ; 客户端和服务器程序由同一团队开发和控制。
>
>       - 示例：某些企业内部的专用系统 ; 特定厂商的封闭式网络服务。
>
>       - 局限性：其他开发者无法开发与之交互的程序 ; 缺乏开放性和扩展性。
>
>   ---
>
>   研发开放网络应用程序时 应当使用与这个协议关联的端口号 ; 私有协议则要避免使用周知的端口号 .

### 2.7.1 Socket Programming with UDP

In this subsection, we’ll write simple client-server programs that use UDP .

![image-20250925160843689](pic_networking/chap2pic/UDP_workflow.png)

>   [!CAUTION]
>
>   代码 : `.\code_chap2\2.7.1_Socket_Programming_with_UDP`

```python
# UDPClient.py

from socket import *

# serverName = 'hostname'  # 服务器主机名（需改为实际IP或主机名）
serverName = 'localhost'  # 改为localhost或127.0.0.1
serverPort = 12000       # 服务器端口号
clientSocket = socket(AF_INET, SOCK_DGRAM)  # 创建UDP socket

message = input('Input lowercase sentence:')  # 获取用户输入 书中的raw_input是python2的写法
# 发送消息到服务器
# 会先用'encode()'方法把字符串类型转换成字节类型
# 会把源地址(自己的地址)自动附上 不通过用户显式附上
clientSocket.sendto(message.encode(), (serverName, serverPort))

# 接收服务器返回的消息（最多2048字节）
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())  # 打印转换后的消息
clientSocket.close()  			 # 关闭socket 然后关闭了该进程
```

```python
# UDPServer.py

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)  # 创建UDP socket
serverSocket.bind(('', serverPort))  # 绑定到所有网络接口的12000端口
print("The server is ready to receive")

while True:
    # 接收客户端消息
    message, clientAddress = serverSocket.recvfrom(2048)
    # 将消息转换为大写
    modifiedMessage = message.decode().upper()
    # 将处理后的消息发回客户端
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```

### 2.7.2 Socket Programming with TCP

in this subsection, we’ll write similar programs that use TCP.

TCP与UDP的不同之处在于 : 

-   TCP 需要先进行一次握手来创立一个TCP连接(全双工) .
-   UDP协议需要为每一个分组附上一个目的地地址 ; TCP协议只需要通过套接字把数据丢进TCP连接中 .

#### TCP服务器

1.   TCP服务器需要在客户发起接触操作前运行起来
2.   TCP服务器必须有一个特殊的套接字 用来"欢迎"任意客户进程上的某种初始接触 . 

####  Details in TCP

With the server process running, the **client process can initiate a TCP connection to the server**. This is done in the client program by creating a TCP socket. When the client creates its TCP socket, **client process specifies the address of the welcoming socket in the server**, namely, the IP address of the server host and the port number of the socket.  After creating its socket, **the client initiates a three-way handshake and establishes a  TCP connection with the server.** 

>   [!IMPORTANT]
>
>   **The three-way handshake**, which takes place within  the transport layer, is completely invisible to the client and server programs.
>
>   During the three-way handshake, the client process knocks on the welcoming door of the server process. When the server “hears” the knocking, it creates a  new door—more precisely, a new socket that is dedicated to that particular client.  In our example below, the welcoming door is a TCP socket object that we call  **`serverSocket`**; the newly created socket dedicated to the client making the connection is called **`connectionSocket`**. 
>
>   ---
>
>   Students who are encountering TCP sockets for the first time sometimes confuse the welcoming socket (which is the initial  point of contact for all clients wanting to communicate with the server), and each  newly created server-side connection socket that is subsequently created for communicating with each client.
>
>   ---
>
>   TCP连接可以提供可靠的服务 保证彼此(注意是全双工)按顺序接收到数据

![image-20250925191128479](pic_networking/chap2pic/TCP协议.png)

#### TCP Code

![image-20250925194051190](pic_networking/chap2pic/TCP_workflow.png)

>   [!CAUTION]
>
>   代码 : `.\code_chap2\2.7.2_Socket_Programming_with_TCP`

```python
# TCPClient.py

from socket import *

serverName = 'localhost'  							# 修改为'localhost'或'127.0.0.1'
serverPort = 12000
# 创建套接字 直接用于通信
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()
```

```python
# TCPServer.py
# 这里在原来的基础上增加了退出代码 (仅仅可用而已)

from socket import *

serverPort = 12000							# 服务器在12000端口上监听客户端的连接请求。服务地址

# 创建欢迎套接字
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))			# 12000(ServerPort是欢迎端口)绑定到端口
serverSocket.listen(1)						# 开始监听欢迎套接字
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()		# 等待阻塞 不阻塞的话 会自动分配一个端口用于TCP连接给connectionSocket
    sentence = connectionSocket.recv(1024).decode()

    # 检查是否收到退出命令
    if sentence.lower() == 'shutdown':
        print('收到关闭命令，服务器正在停止...')
        connectionSocket.send('服务器已关闭'.encode())
        connectionSocket.close()
        break

    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()

serverSocket.close()
print('服务器已关闭')
```

>   [!CAUTION]
>
>   是的，在 TCP 连接过程中，客户端和服务器需要保持一致的是服务器的欢迎端口（Welcome Port）。以下是具体说明：
>
>   -   欢迎端口（如你的代码中的 12000）是服务器端监听客户端连接请求的固定端口。客户端通过明确指定服务器的 IP 地址和这个欢迎端口（例如 clientSocket.connect((serverName, serverPort)) 中的 serverPort = 12000）来发起连接。
>   -   客户端和服务器必须在欢迎端口上达成一致，否则客户端无法正确连接到服务器。例如，如果服务器在 12000 端口监听，而客户端尝试连接到 13000 端口，连接会失败。
>   -   连接端口（用于实际数据通信的端口）则不需要双方显式一致：
>       -   客户端的连接端口是操作系统动态分配的临时端口（ephemeral port），服务器无需知道具体是哪个端口。
>       -   服务器端的 `connectionSocket` 也会使用一个新的套接字（可能绑定到临时端口）来处理与客户端的通信，但这对客户端是透明的。

# Homework

R12 P4 P5 P7 P8 P22





