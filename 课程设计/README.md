# 计算机网络构建系列实验项目文档
## 一、术语概念释义
在开展实验前，先明确文档中涉及的核心概念，避免因术语混淆影响实验推进：

### （一）硬件相关概念
1. **USB转串口接口卡（含自收发型）**：一种硬件转接设备，用于将计算机的USB接口转换为传统串口（常见为RS-232接口）。串口是计算机早期用于数据传输的物理接口，而现代电脑多取消串口，通过该转接卡可实现传统串口通信功能。其中“自收发型”指接口卡自身可完成收发端的连接测试（无需额外设备即可验证接口是否正常工作），常用于单机串口调试实验。
2. **通信线**：用于连接串口设备的传输线缆，核心为RS-232串口线，两端通常为DB9接头（对应串口接口），需根据设备引脚定义选择直连或交叉线（双机通信需使用交叉线，即PC1的接收端连接PC2的发送端，PC2的接收端连接PC1的发送端）。
3. **拓扑结构**：计算机网络中设备的连接方式，实验涉及的类型包括：
   - 星型拓扑：以一台设备为中心，其他设备均直接连接到中心设备；
   - 环形拓扑：设备依次连接形成闭合回路，数据沿回路传输；
   - 树形拓扑：星型拓扑的延伸，形成层级化连接（如中心设备连接次级设备，次级设备再连接终端设备）；
   - 多链路拓扑：设备间存在多条可达路径，支持路由选择（如6台PC间形成含2跳以上的复杂连接）。

### （二）软件与接口相关概念
1. **COM口（串行通信端口）**：计算机中用于串行通信的物理或虚拟端口，Windows系统中以“COM+数字”命名（如COM4、COM5）。USB转串口接口卡连接电脑后，系统会自动分配唯一的COM口编号，需通过设备管理器查询确认（实验核心操作接口）。
2. **串口调试助手**：用于测试串口通信的工具软件，支持配置COM口参数（波特率、数据位等）、手动发送数据、实时接收数据，核心作用是验证硬件连接是否正常，为编程实现提供基础测试环境（常见工具如SecureCRT、SSCOM）。
3. **C/S模式**：即客户端/服务器（Client/Server）模式，是网络应用的基础架构：
   - 服务器（Server）：持续运行并提供服务的设备/程序，可接收多个客户端的请求并响应；
   - 客户端（Client）：主动向服务器发起请求，获取服务或传输数据的设备/程序。
4. **链路层/网络层/运输层/应用层**：计算机网络OSI七层模型或TCP/IP四层模型中的核心层级，实验按层级递进实现功能：
   - 物理层：负责硬件连接（如串口引脚定义、信号传输）；
   - 链路层：负责相邻设备间的数据帧传输（如拓扑适配、帧校验）；
   - 网络层：负责跨链路的路由选择（如路径规划、设备标识）；
   - 运输层：负责端到端的可靠传输（如重传机制、流量控制）；
   - 应用层：提供具体网络服务（如ping、traceroute等网络管理功能）。
5. **可靠传输**：确保数据从发送端完整、无差错地传输到接收端的机制，核心技术包括：
   - 数据校验：通过校验码（如CRC、奇偶校验）检测数据是否出错；
   - 确认（ACK）：接收端收到正确数据后向发送端反馈确认信息；
   - 超时重传：发送端未在规定时间内收到确认，自动重新发送数据；
   - 滑动窗口：允许发送端连续发送多个数据帧，无需等待每个帧的确认，提升传输效率。
6. **路由算法**：用于在多链路拓扑中选择最优路径的算法，分为：
   - 静态路由：手动配置路径信息，适用于拓扑稳定的网络；
   - 动态路由：设备通过交互链路状态（如是否连通）或距离向量（如跳数），自动更新路径信息，适用于拓扑动态变化的网络（实验推荐洪泛法实现链路状态交互）。
7. **ping**：应用层网络测试工具，通过发送ICMP回声请求包，验证目标设备是否可达，同时测量往返时间（RTT），核心原理是基于网络层的数据包转发与响应机制。
8. **traceroute/tracert**：应用层网络测试工具，用于追踪数据从源设备到目标设备的传输路径，通过发送含TTL（生存时间）的数据包，逐步发现路径中的每一跳设备，核心原理是利用TTL超时机制与ICMP差错报告。

### （三）编程相关概念
1. **多线程技术**：允许程序同时执行多个任务（线程）的编程技术，串口通信中常用“接收线程”（持续监听串口数据）和“发送线程”（独立处理数据发送），避免收发操作相互阻塞。
2. **心跳机制**：设备间定期发送的检测数据包（如每隔1秒发送固定格式数据），用于确认对方是否在线，核心作用是动态更新网络拓扑（如检测设备断开/接入）。
3. **洪泛法**：网络中设备将收到的数据包转发到所有相邻设备的方式，适用于链路状态信息的交互（如动态路由中设备向全网广播自身连接状态）。

## 二、项目概述
### （一）项目目标
本项目通过6个递进式实验，从物理层到应用层逐步构建计算机网络，掌握网络分层架构的核心原理与实现方法，最终实现多设备、跨链路、可靠的网络通信及网络管理功能。

### （二）适用环境
1. 硬件环境：Windows系统计算机（数量按实验要求配置）、USB转串口接口卡、RS-232通信线；
2. 软件环境：Windows操作系统、串口调试助手（如SSCOM）、编程工具（支持Python或C++，如PyCharm、Visual Studio）；
3. 团队要求：实验一/二为单人实验，实验三（4人组队）、实验四/五/六（6人组队）。

### （三）分数占比与提交要求
| 项目内容 | 分数占比 | 验收/提交要求 |
|----------|----------|---------------|
| 实验一：单机串口通信 | 10% | 上机验收 |
| 实验二：双机C/S模式通信 | 15% | 上机验收 |
| 实验三：多机链路层通信 | 20% | 上机验收 |
| 实验四：跨链路网络层通信 | 30% | 上机验收（含图形化界面5%） |
| 实验报告 | 20% | 电子版+纸质版（详见报告要求） |

#### 提交时间节点
1. 电子版材料（报告完整版+源代码）：以“班级-学号-姓名”命名压缩包，个人提交给学委，学委汇总后于2025年1月28日前发送至对应老师QQ邮箱；
2. 纸质版报告：打印核心内容（不超过10页），于2025年2月17日（开学第一周周一）提交至学院410办公室；
3. 实验验收：所有实验需在上机时间内完成验收。

## 三、实验详情
### 实验一：单机串口实验
#### （一）实验目标
1. 理解串口通信的物理层原理（含COM口配置、收发端连接逻辑）；
2. 掌握USB转串口接口卡的硬件连接方法；
3. 实现串口的基础功能（打开/关闭串口、数据发送/接收）。

#### （二）实验器材
| 器材名称 | 数量 | 备注 |
|----------|------|------|
| Windows系统计算机 | 1台 | 需支持USB接口 |
| USB转串口接口卡（自收发型） | 1块 | 含驱动程序（需提前安装） |
| RS-232通信线 | 1根 | 适配接口卡的DB9接头 |

#### （三）实验软件
1. 操作系统：Windows 10/11；
2. 调试工具：串口调试助手（如SSCOM V5.13）；
3. 编程工具：Python 3.x或C++（推荐Visual Studio 2019+）。

#### （四）实验步骤
1. **硬件连接**：
   - 将USB转串口接口卡插入计算机USB接口，安装驱动程序；
   - 使用通信线连接接口卡的“发送端（TX）”与“接收端（RX）”（自收发连接，用于单机测试）。
2. **软件调试**：
   - 打开Windows设备管理器（右键“此电脑”→“管理”→“设备管理器”→“端口（COM和LPT）”），查询接口卡分配的COM口编号（如COM4）；
   - 打开串口调试助手，配置参数：选择查询到的COM口、波特率9600、数据位8、停止位1、无校验位、无流控；
   - 点击“打开串口”，在发送区输入测试数据（如“test”），点击“发送”，观察接收区是否能正常接收相同数据（验证硬件与接口正常）。
3. **程序编写**：
   - 核心功能：实现串口的打开/关闭、数据发送、数据接收；
   - 参数要求：支持配置COM口编号、波特率（默认9600）、数据位（默认8）、停止位（默认1）、校验位（默认无）；
   - 输出要求：接收数据实时打印，发送数据需反馈发送状态（成功/失败）。
4. **拓展任务**：
   - 实时检测消息到达：通过监听串口缓冲区数据量（如Python的serial.in_waiting）实现消息到达触发接收；
   - 最大发送速率测试：在保证接收无差错的前提下，逐步提高发送频率，记录最大稳定发送速率；
   - 长消息收发：测试并实现最大无差错收发的消息长度（需处理数据分包/粘包问题）。

### 实验二：双机通信实验
#### （一）实验目标
1. 掌握双机串口通信的物理层连接方法（交叉连接）；
2. 理解C/S模式的通信逻辑（请求/响应机制）；
3. 实现双机间的双向数据传输。

#### （二）实验器材
| 器材名称 | 数量 | 备注 |
|----------|------|------|
| Windows系统计算机 | 2台 | 分别命名为PC1、PC2，均支持USB接口 |
| USB转串口接口卡 | 2块 | 每台电脑1块，含驱动程序 |
| RS-232交叉通信线 | 1根 | 确保PC1_TX→PC2_RX、PC2_TX→PC1_RX |

#### （三）实验软件
同实验一。

#### （四）实验步骤
1. **硬件连接**：
   - 两台电脑分别插入USB转串口接口卡，安装驱动并查询各自的COM口编号（如PC1为COM4，PC2为COM5）；
   - 使用交叉通信线连接两块接口卡：PC1接口卡的TX引脚连接PC2接口卡的RX引脚，PC2接口卡的TX引脚连接PC1接口卡的RX引脚。
2. **软件调试**：
   - 两台电脑均打开串口调试助手，按相同参数配置（波特率9600、数据位8等），分别选择各自的COM口并打开；
   - PC1发送测试数据（如“Hello PC2”），观察PC2接收区是否正常接收；反之，PC2发送数据，验证PC1接收功能（确认双机连接正常）。
3. **程序编写**：
   - 基于实验一的串口功能代码，扩展C/S模式逻辑；
   - 服务器端（Server）功能：监听指定COM口，接收客户端请求，处理后返回响应（如接收“请求时间”则返回当前系统时间）；
   - 客户端（Client）功能：连接服务器端对应的COM口，发送请求数据，接收并显示服务器响应；
   - 交互流程：客户端发起请求→服务器端接收并解析→服务器端返回响应→客户端显示响应（支持多次请求/响应）。
4. **拓展任务**：
   - 服务器拒绝请求：实现基于请求类型（如非法指令）或客户端权限的请求拒绝机制（返回拒绝响应）；
   - 客户端超时处理：当服务器无响应时，客户端设置超时时间（如5秒），超时后提示“请求超时”并可重新发起请求；
   - 客户端断开检测：服务器端通过心跳机制（定期接收客户端状态包）或超时检测，判断客户端是否已断开连接，释放资源。

### 实验三：简单拓扑的多机通信实验（链路层）
#### （一）实验目标
1. 理解链路层的帧传输原理；
2. 掌握树形拓扑的硬件连接方法；
3. 实现多机（4台）间任意两台的直接数据交付。

#### （二）实验器材
| 器材名称 | 数量 | 备注 |
|----------|------|------|
| Windows系统计算机 | 4台 | 分别命名为PC1~PC4，4人组队，每人1台 |
| USB转串口接口卡 | 12块 | 每台电脑3块（用于连接其他设备） |
| RS-232通信线 | 若干 | 按树形拓扑需求配置（确保相邻设备交叉连接） |

#### （三）实验软件
同实验一。

#### （四）实验步骤
1. **硬件连接**：
   - 按树形拓扑连接4台PC：选择1台PC作为根节点（如PC1），其余3台作为叶子节点（PC2~PC4）；
   - 根节点PC1通过3块接口卡分别连接PC2~PC4（每块接口卡对应1台叶子节点），连接方式为交叉连接（PC1_TX→PC2_RX，PC2_TX→PC1_RX，以此类推）；
   - 所有设备安装接口卡驱动，查询各自用于连接的COM口编号（如PC1连接PC2用COM4，连接PC3用COM5，连接PC4用COM6）。
2. **软件调试**：
   - 每台PC打开串口调试助手，配置所有已连接的COM口参数（波特率9600等）；
   - 测试相邻设备通信：PC1向PC2发送数据，验证PC2接收；PC3向PC1发送数据，验证PC1接收（确保所有链路连接正常）。
3. **程序编写**：
   - 基于实验二的双机通信代码，扩展多串口管理功能（每台PC需支持同时管理多个COM口）；
   - 核心功能：任意两台PC间可直接发送数据（如PC2向PC3发送数据，需通过根节点PC1转发，链路层自动处理帧转发逻辑）；
   - 设备标识：为每台PC分配唯一标识（如ID001~ID004），数据帧中需包含源ID、目标ID；
   - 转发逻辑：根节点接收数据帧后，根据目标ID转发至对应叶子节点；叶子节点仅接收目标ID为自身的数据帧。
4. **拓展任务**：
   - 自动发现可达设备：通过洪泛法（每台设备定期广播自身ID和连接状态），实现无需人工干预的可达设备列表更新；
   - 故障容错：当某台叶子节点（如PC2）断开连接时，确保其他设备（PC3~PC4）间的通信不受影响；当根节点断开时，需提示网络中断（树形拓扑无备用路径）。

### 实验四：跨链路的多机通信实验（网络层）
#### （一）实验目标
1. 理解网络层的路由选择原理；
2. 掌握多链路拓扑的构建方法（含2跳以上路径）；
3. 实现动态/静态路由，支持设备的动态接入/退出。

#### （二）实验器材
| 器材名称 | 数量 | 备注 |
|----------|------|------|
| Windows系统计算机 | 6台 | 分别命名为PC1~PC6，6人组队，每人1台 |
| USB转串口接口卡 | 18块 | 每台电脑3块（用于连接其他设备） |
| RS-232通信线 | 若干 | 按多链路拓扑需求配置（交叉连接） |

#### （三）实验软件
同实验一。

#### （四）实验步骤
1. **硬件连接**：
   - 构建多链路拓扑：要求任意两台PC间存在至少两条可达路径，且包含2跳以上链路（如PC1→PC2→PC3→PC6，PC1→PC4→PC5→PC6）；
   - 示例拓扑：PC1连接PC2、PC4；PC2连接PC1、PC3；PC3连接PC2、PC6；PC4连接PC1、PC5；PC5连接PC4、PC6；PC6连接PC3、PC5（每台设备通过接口卡实现交叉连接）；
   - 所有设备查询并记录自身用于连接的COM口编号及对应连接的设备ID。
2. **软件调试**：
   - 每台PC打开串口调试助手，配置所有连接用COM口参数；
   - 测试直接连接设备的通信（如PC1与PC2、PC1与PC4），确保链路正常；
   - 测试跨链路通信（如PC1向PC6发送数据），通过调试助手观察数据转发过程（验证路径可达）。
3. **程序编写**：
   - 基于实验三的多串口管理功能，加入路由算法；
   - 设备标识：每台PC分配唯一ID（如ID001~ID006），并维护路由表（记录目标ID、下一跳设备ID、链路状态）；
   - 路由实现：支持静态路由（手动配置路由表）或动态路由（通过洪泛法交互链路状态，自动更新路由表）；
   - 动态适配：当某台设备接入/退出网络时，路由表自动更新，确保剩余设备间通信正常（通过心跳机制检测设备状态）；
   - 核心要求：任意两台PC间可通过最优路径（如跳数最少）实现数据交付。
4. **拓展任务**：
   - 多应用通信支持：为每台PC的不同应用分配唯一端口号（如应用1用端口8080，应用2用端口8081），数据帧中加入端口字段，实现同一设备上不同应用的独立通信。

### 实验五：多机可靠传输实验（运输层）
#### （一）实验目标
1. 理解运输层可靠传输的核心原理（停等协议、重传机制）；
2. 掌握数据校验、超时重传、确认机制的实现方法；
3. 实现多机间的无差错数据传输（支持模拟出错/超时场景）。

#### （二）实验器材
同实验四。

#### （三）实验软件
同实验一。

#### （四）实验步骤
1. **硬件连接**：
   - 沿用实验四的多链路拓扑（确保含2跳以上路径）；
   - 确认所有设备的COM口连接正常，链路通信稳定。
2. **软件调试**：
   - 使用串口调试助手模拟数据出错场景（手动修改发送数据），验证基础通信链路的容错性（未实现可靠传输时会出现数据错误）；
   - 模拟超时场景（断开某条链路后快速恢复），观察数据传输是否中断。
3. **程序编写**：
   - 基于实验四的路由功能，加入可靠传输机制（基于停等协议）；
   - 数据帧格式定义：帧头（源ID、目标ID、源端口、目标端口、帧序号、校验码、帧类型（数据/确认））+ 数据载荷；
   - 核心机制：
     - 数据校验：使用CRC32或奇偶校验计算校验码，接收端验证，校验失败则丢弃并请求重传；
     - 停等协议：发送端发送一帧后，等待接收端的确认帧（ACK），收到ACK后再发送下一帧；
     - 超时重传：发送端设置超时时间（如3秒），未在超时内收到ACK则自动重传该帧；
     - 确认机制：接收端正确接收数据帧后，立即发送对应序号的ACK帧；若接收重复帧，丢弃数据但重新发送ACK；
   - 模拟测试：手动触发数据出错（修改校验码）、超时（延迟发送ACK），验证程序是否能正确重传并接收正确数据。
4. **拓展任务**：
   - 滑动窗口协议实现：将停等协议扩展为滑动窗口（如窗口大小为3），支持连续发送多个帧后再等待ACK，提升传输效率；
   - 窗口大小优化：测试不同窗口大小（1~5）下的传输速率，确定最优窗口大小。

### 实验六：简单网络管理实验（应用层）
#### （一）实验目标
1. 理解ping和traceroute工具的核心原理；
2. 掌握应用层网络管理功能的实现方法；
3. 实现多机网络的可达性检测与路径追踪。

#### （二）实验器材
同实验四。

#### （三）实验软件
同实验一。

#### （四）实验步骤
1. **硬件连接**：
   - 沿用实验四的多链路拓扑；
   - 确保所有设备的路由功能正常（基于实验四实现）。
2. **软件调试**：
   - 使用Windows系统自带的ping命令（如ping 目标IP，实验中替换为设备ID）测试设备可达性；
   - 使用tracert命令（如tracert 目标IP）测试路径追踪，记录实际路径（跳数、设备ID）。
3. **程序编写**：
   - 基于实验四的路由功能和实验五的可靠传输机制，实现ping和traceroute功能；
   - ping功能实现：
     - 客户端（发起ping的设备）向目标设备发送ICMP回声请求帧（含请求标识、序列号、发送时间戳）；
     - 目标设备收到后，立即返回ICMP回声响应帧（携带相同标识和序列号、接收时间戳）；
     - 客户端计算往返时间（RTT=接收时间戳-发送时间戳），并统计丢包率（未收到响应的请求数/总请求数）；
     - 输出要求：显示目标设备是否可达、RTT平均值、丢包率。
   - traceroute功能实现：
     - 客户端向目标设备发送含TTL（生存时间）的测试帧，TTL初始值为1；
     - 每一跳设备收到帧后，TTL减1，若TTL=0则返回ICMP超时帧（包含自身ID）；
     - 客户端收到超时帧后，记录该跳设备ID，将TTL加1后继续发送测试帧；
     - 当测试帧到达目标设备时，目标设备返回ICMP响应帧，客户端停止测试并输出完整路径（所有跳数的设备ID）；
     - 输出要求：按跳数顺序显示路径中的设备ID、每跳的RTT。
4. **拓展任务**：
   - 批量ping测试：实现同时向多个目标设备发送ping请求，批量输出可达性结果；
   - traceroute路径优化：结合实验四的路由算法，显示最优路径与备选路径的追踪结果。

## 四、课设报告要求
### （一）报告结构
报告需按实验分章（共6章实验+1章总结），每章结构如下：
1. **功能要求**：简述对应实验的核心目标、需实现的功能点、预期效果（如“实现双机C/S模式通信，支持客户端请求与服务器响应，无数据丢失”）；
2. **实现思路**：
   - 硬件拓扑：绘制清晰的设备连接图（标注设备ID、COM口编号、链路类型）；
   - 功能流程：使用流程图描述核心逻辑（如串口打开流程、可靠传输流程、ping请求/响应流程）；
   - 协议定义：明确数据帧格式、交互规则（如请求/响应的字段定义、ACK确认机制）；
3. **模块设计**：
   - 模块划分：按功能拆分核心模块（如串口操作模块、路由模块、可靠传输模块）；
   - 调用关系：使用模块调用图描述各模块间的交互逻辑；
   - 接口定义：明确模块间的数据交互格式（如函数参数、返回值、数据结构）；
4. **功能实现**：
   - 核心代码：粘贴关键模块的代码（需添加注释），说明核心逻辑（如校验码计算、路由表更新、超时重传判断）；
   - 实现效果：附实验测试截图（如数据收发成功界面、ping结果界面、traceroute路径显示界面）；
   - 性能分析：分析实验结果（如传输速率、丢包率、RTT平均值），说明影响性能的因素及优化方向。

### （二）总结与感想
1. 总结整个课设的核心收获（如对网络分层架构的理解、编程能力的提升、问题解决经验）；
2. 分析实验中遇到的主要问题及解决方案（如硬件连接错误、数据粘包、路由表更新异常）；
3. 对实验设计的改进建议或拓展方向（如增加无线通信模块、实现更复杂的路由算法）。

### （三）提交要求
1. 电子版：
   - 包含报告完整版（Word或PDF格式）、源代码（按实验分文件夹存放，含编译/运行说明）；
   - 命名格式：“班级-学号-姓名”（如“计算机2101-2021001-张三”），打包为ZIP压缩包；
   - 提交路径：个人提交给学委，学委汇总后于2025年1月28日前发送至对应老师QQ邮箱。
2. 纸质版：
   - 打印报告核心部分（精简代码、截图、分析内容），页数不超过10页；
   - 提交时间：2025年2月17日（开学第一周周一），提交至学院410办公室。

## 五、附录：串口读写参考代码
### （一）C++版（多线程实现COM4/COM5收发）
```cpp
#include <windows.h>
#include <iostream>
#include <string>
#include <thread>
#include <atomic>
#include <mutex>

class SerialPort {
public:
    // 构造函数：初始化串口名称、波特率
    SerialPort(const std::string& portName, int baudRate)
        : portName(portName), baudRate(baudRate), hSerial(INVALID_HANDLE_VALUE), stopThreads(false) {}

    // 析构函数：停止线程、关闭串口
    ~SerialPort() {
        stopThreads = true;
        if (hSerial != INVALID_HANDLE_VALUE) {
            CloseHandle(hSerial);
        }
        if (receiveThread.joinable()) {
            receiveThread.join();
        }
    }

    // 打开串口并配置参数
    bool open() {
        // 打开串口设备
        hSerial = CreateFileA(
            portName.c_str(),
            GENERIC_READ | GENERIC_WRITE,
            0,
            nullptr,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            nullptr
        );

        if (hSerial == INVALID_HANDLE_VALUE) {
            std::cerr << "串口打开失败 " << portName << "，错误码：" << GetLastError() << std::endl;
            return false;
        }

        // 配置串口参数（波特率9600，数据位8，停止位1，无校验）
        DCB dcbSerialParams = { 0 };
        dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
        if (!GetCommConfig(hSerial, &dcbSerialParams, nullptr)) {
            std::cerr << "获取串口配置失败 " << portName << std::endl;
            CloseHandle(hSerial);
            hSerial = INVALID_HANDLE_VALUE;
            return false;
        }
        dcbSerialParams.BaudRate = baudRate;
        dcbSerialParams.ByteSize = 8;
        dcbSerialParams.StopBits = ONESTOPBIT;
        dcbSerialParams.Parity = NOPARITY;
        if (!SetCommConfig(hSerial, &dcbSerialParams, sizeof(dcbSerialParams))) {
            std::cerr << "设置串口配置失败 " << portName << std::endl;
            CloseHandle(hSerial);
            hSerial = INVALID_HANDLE_VALUE;
            return false;
        }

        // 配置超时时间（读取超时1秒）
        COMMTIMEOUTS timeouts = { 0 };
        timeouts.ReadIntervalTimeout = 50;
        timeouts.ReadTotalTimeoutConstant = 1000;
        timeouts.ReadTotalTimeoutMultiplier = 10;
        if (!SetCommTimeouts(hSerial, &timeouts)) {
            std::cerr << "设置串口超时失败 " << portName << std::endl;
            CloseHandle(hSerial);
            hSerial = INVALID_HANDLE_VALUE;
            return false;
        }

        // 启动接收线程
        receiveThread = std::thread(&SerialPort::receiveData, this);
        return true;
    }

    // 发送数据
    bool sendData(const std::string& data) {
        if (hSerial == INVALID_HANDLE_VALUE) {
            std::cerr << "串口未打开 " << portName << std::endl;
            return false;
        }

        DWORD bytesWritten;
        bool success = WriteFile(
            hSerial,
            data.c_str(),
            data.length(),
            &bytesWritten,
            nullptr
        );

        if (success && bytesWritten == data.length()) {
            std::cout << "串口 " << portName << " 发送成功：" << data << std::endl;
            return true;
        } else {
            std::cerr << "串口 " << portName << " 发送失败，错误码：" << GetLastError() << std::endl;
            return false;
        }
    }

private:
    // 接收数据线程函数
    void receiveData() {
        char buf[256];
        DWORD bytesRead;
        std::mutex coutMutex; // 确保打印不冲突

        while (!stopThreads) {
            memset(buf, 0, sizeof(buf));
            if (ReadFile(hSerial, buf, sizeof(buf) - 1, &bytesRead, nullptr)) {
                if (bytesRead > 0) {
                    std::lock_guard<std::mutex> lock(coutMutex);
                    std::cout << "串口 " << portName << " 接收成功：" << std::string(buf, bytesRead) << std::endl;
                }
            } else {
                DWORD error = GetLastError();
                if (error != ERROR_TIMEOUT) { // 忽略超时错误
                    std::lock_guard<std::mutex> lock(coutMutex);
                    std::cerr << "串口 " << portName << " 读取失败，错误码：" << error << std::endl;
                }
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(100)); // 降低CPU占用
        }
    }

    std::string portName;       // 串口名称（如COM4）
    int baudRate;               // 波特率
    HANDLE hSerial;             // 串口句柄
    std::atomic<bool> stopThreads; // 线程停止标志
    std::thread receiveThread;  // 接收线程
};

int main() {
    // 初始化两个串口（COM4和COM5，波特率9600）
    SerialPort serial4("COM4", 9600);
    SerialPort serial5("COM5", 9600);

    if (!serial4.open()) {
        return 1;
    }
    if (!serial5.open()) {
        return 1;
    }

    // 主线程发送测试数据（每2秒发送一次）
    try {
        int count = 0;
        while (count < 5) { // 发送5次后退出
            serial4.sendData("Hello from COM4 (" + std::to_string(count + 1) + ")");
            serial5.sendData("Hello from COM5 (" + std::to_string(count + 1) + ")");
            std::this_thread::sleep_for(std::chrono::seconds(2));
            count++;
        }
    } catch (const std::exception& e) {
        std::cerr << "主线程异常：" << e.what() << std::endl;
    }

    std::cout << "实验结束，关闭串口..." << std::endl;
    return 0;
}
```

### （二）Python版（多线程实现COM4/COM5收发）
```python
import serial
import threading
import time

# 串口接收线程类
class SerialReader(threading.Thread):
    def __init__(self, port, baudrate=9600):
        super().__init__()
        self.port = port          # 串口名称
        self.baudrate = baudrate  # 波特率
        self.ser = None           # 串口对象
        self.running = True       # 线程运行标志

    def run(self):
        """线程运行函数：持续读取串口数据"""
        try:
            # 打开串口，配置超时时间1秒
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=1
            )
            print(f"串口 {self.port} 已打开，开始接收数据...")

            while self.running:
                # 检测串口缓冲区是否有数据
                if self.ser.in_waiting > 0:
                    # 读取数据并解码（UTF-8，忽略无法解码的字符）
                    data = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                    print(f"串口 {self.port} 接收：{data}")
                time.sleep(0.1)  # 降低CPU占用率
        except Exception as e:
            print(f"串口 {self.port} 接收线程异常：{str(e)}")
        finally:
            # 关闭串口
            if self.ser and self.ser.is_open:
                self.ser.close()
                print(f"串口 {self.port} 已关闭")

    def stop(self):
        """停止线程"""
        self.running = False

# 串口发送函数
def send_data(port, baudrate=9600, data=""):
    """向指定串口发送数据"""
    if not data:
        print("发送数据不能为空")
        return

    try:
        # 打开串口，发送数据后立即关闭
        with serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=1
        ) as ser:
            ser.write(data.encode('utf-8'))
            print(f"串口 {port} 发送：{data}")
    except Exception as e:
        print(f"串口 {port} 发送失败：{str(e)}")

def main():
    # 创建并启动两个串口接收线程（COM4和COM5）
    reader4 = SerialReader(port='COM4', baudrate=9600)
    reader5 = SerialReader(port='COM5', baudrate=9600)
    reader4.start()
    reader5.start()

    # 主线程发送测试数据（每2秒发送一次，共发送5次）
    try:
        for i in range(1, 6):
            send_data('COM4', data=f"Hello from COM4 ({i})")
            send_data('COM5', data=f"Hello from COM5 ({i})")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n接收到中断信号，停止程序...")
    finally:
        # 停止接收线程并等待线程结束
        reader4.stop()
        reader5.stop()
        reader4.join()
        reader5.join()
        print("所有线程已停止")

if __name__ == '__main__':
    main()
```

### （三）代码使用说明
1. 环境依赖：
   - C++版：需Windows系统，支持C++11及以上标准（推荐Visual Studio 2019+），无需额外第三方库（依赖Windows API）；
   - Python版：需安装Python 3.x及pyserial库（安装命令：`pip install pyserial`）。
2. 参数修改：
   - 需根据实际硬件配置修改串口名称（如COM4、COM5）和波特率（默认9600，需与串口调试助手一致）；
   - 数据位、停止位、校验位默认配置为8、1、无，如需修改可调整代码中对应参数。
3. 注意事项：
   - 运行前需确保串口未被其他程序占用（如串口调试助手）；
   - 若出现“访问被拒绝”错误，需检查串口是否已连接、驱动是否安装正常；
   - 多线程通信中需注意线程安全（如C++版的cout互斥锁、Python版的串口对象独占访问）。