# ED-HMI3020-070C

**基于Raspberry Pi 5的7寸工业平板电脑**

![ED-HMI3010-070C-Datasheetdiagram-2024.05.21](./images/ED-HMI3010-070C-Datasheetdiagram-2024.05.21.png)

### 产品亮点

- 7.0" TFT，分辨率1024x600，多点式电容触摸屏

- Broadcom BCM2712 4核Arm Cortex-A76 64位2.4GHz CPU

- 高达8GB LPDDR4X RAM，支持Micro SD Card和M.2 NVMe SSD扩展

- 2 x USB 3.0、2 x USB 2.0、1 x RS232、1 x RS485和1 x Buzzer

- 1 x Gigabit 网口，支持选配PoE功能

- 支持选配800万像素前置摄像头

- 双HDMI显示，支持同时输出2路4Kp60视频

- 立体声输入和输出(支持独立的3.5mm音频接口)，内置speaker

- USB Type-C接口的5V电源输入，具备ON/OFF电源开关

- 集成RTC，支持超级电容和CR1220R电池作为RTC备份电源

- CNC切割工艺的铝合金边框+钣金外壳，无风扇设计，提供良好的散热性能





### 产品规格

<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">系统</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">CPU</td>
      <td style="width: 80%; text-align: left;">Broadcom BCM2712 4核Cortex-A76 64位2.4GHz</td>
    </tr>
    <tr>
      <td>VPU</td>
      <td>H.265(HEVC)，最高支持4Kp60解码</td>
    </tr>
    <tr>
      <td>GPU</td>
      <td>OpenGL ES 3.1 & Vulkan 1.2</td>
    </tr>
    <tr>
      <td>内存</td>
      <td>4GB/8GB LPDDR4X-4267 SDRAM可选</td>
    </tr>
    <tr>
      <td>存储</td>
      <td>Micro SD卡槽(支持选配00GB/32GB/64GB的SD卡)M.2 NVMe SSD(支持选配00GB/128GB/256GB)</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">软件参数</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">操作系统</td>
      <td style="width: 80%; text-align: left;">Raspberry Pi OS(Desktop) 32-bitRaspberry Pi OS(Lite) 32-bitRaspberry Pi OS(Desktop) 64-bitRaspberry Pi OS(Lite) 64-bit</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">前面板I/O</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">摄像头</td>
      <td style="width: 80%; text-align: left;">支持选配800万像素前置摄像头</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">侧面板I/O</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">音频输出接口</td>
      <td style="width: 80%; text-align: left;">1 x 音频输出接口(HPO)，绿色3.5mm音频接口，立体声输出</td>
    </tr>
    <tr>
      <td>音频输入接口</td>
      <td>1 x 音频输入接口(LINE IN)，红色3.5mm音频接口，支持立体声输入</td>
    </tr>
    <tr>
      <td>Speaker</td>
      <td>1 x 功放输出，内置1个4Ω 3W的喇叭</td>
    </tr>
    <tr>
      <td>RS485接口</td>
      <td>1 x RS485接口，3-Pin 3.5mm间距凤凰端子，带120Ω端电阻信号定义为GND/A/B</td>
    </tr>
    <tr>
      <td>RS232接口</td>
      <td>1 x RS232接口，3-Pin 3.5mm间距凤凰端子，信号定义为GND/TX/RX</td>
    </tr>
    <tr>
      <td>USB 2.0接口</td>
      <td>2 x USB 2.0，双层type A接口，每一路最高支持480Mbps传输速率</td>
    </tr>
    <tr>
      <td>USB 3.0接口</td>
      <td>2 x USB 3.0，双层type A接口，每一路最高支持5Gbps传输速率</td>
    </tr>
    <tr>
      <td>1000M以太网接口</td>
      <td>1 x 以太网接口(10/100/1000M自适应)，RJ45端子，用于接入以太网可通过扩展模块支持PoE供电</td>
    </tr>
    <tr>
      <td>SD卡槽</td>
      <td>1 x Micro SD卡槽，用于安装SD卡，支持从SD卡启动系统</td>
    </tr>
    <tr>
      <td>HDMI接口</td>
      <td>2 x HDMI，Micro HDMI接口，分辨率支持4K 60Hz</td>
    </tr>
    <tr>
      <td>电源接口</td>
      <td>1 x USB Type-C接口，支持5V 5A的电源输入</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">按键和指示灯</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">ON/OFF按键</td>
      <td style="width: 80%; text-align: left;">1 x 开/关按键，用于对设备进行开机和关机</td>
    </tr>
    <tr>
      <td>PWR</td>
      <td>1 x 电源指示灯，红色，用于查看设备上电和断电的状态</td>
    </tr>
    <tr>
      <td>ACT</td>
      <td>1 x 系统状态指示灯，绿色，用于查看设备的工作状态</td>
    </tr>
    <tr>
      <td>COM1~COM2</td>
      <td>2 x 串口指示灯，绿色，用于查看串口的通信状态</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">内部I/O</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">M.2 M</td>
      <td style="width: 80%; text-align: left;">1 x M.2 M，M.2 M Key连接器，用于外接SSD和其他高速设备兼容M.2 2230、M.2 2242和M.2 2260，支持从SSD启动系统</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">LCD屏</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">屏幕类型</td>
      <td style="width: 80%; text-align: left;">7.0" TFT</td>
    </tr>
    <tr>
      <td>分辨率</td>
      <td>1024 x 600</td>
    </tr>
    <tr>
      <td>最大色彩</td>
      <td>16.7MB</td>
    </tr>
    <tr>
      <td>显示区域</td>
      <td>154.21mm(H) x 85.92mm(V)</td>
    </tr>
    <tr>
      <td>背光</td>
      <td>LED</td>
    </tr>
    <tr>
      <td>背光MTBF</td>
      <td>>30000h</td>
    </tr>
    <tr>
      <td>亮度</td>
      <td>400cd/m^2</td>
    </tr>
    <tr>
      <td>对比度</td>
      <td>800:1</td>
    </tr>
    <tr>
      <td>响应时间</td>
      <td>30ms</td>
    </tr>
    <tr>
      <td>视角(CR≥10)</td>
      <td>85°(L)/85°(R)/85°(U)/85°(D)</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">触摸屏</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">类型</td>
      <td style="width: 80%; text-align: left;">多点电容式触摸屏</td>
    </tr>
    <tr>
      <td>透光率</td>
      <td>≥85％</td>
    </tr>
    <tr>
      <td>连接方式</td>
      <td>COF</td>
    </tr>
    <tr>
      <td>通信方式</td>
      <td>I2C</td>
    </tr>
    <tr>
      <td>驱动支持</td>
      <td>Linux</td>
    </tr>
    <tr>
      <td>多点触摸</td>
      <td>可达到10点</td>
    </tr>
    <tr>
      <td>表面硬度</td>
      <td>6H</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">扩展功能</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">RTC</td>
      <td style="width: 80%; text-align: left;">集成1F超级电容作为RTC备份电源，保障系统时钟不受设备下电的影响同时提供RTC电池底座，用户也可以自行购买CR1220电池作为RTC备份电源</td>
    </tr>
    <tr>
      <td>Buzzer</td>
      <td>根据实际应用可配置提示或异常，实现报警功能</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">电气参数</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">输入电压</td>
      <td style="width: 80%; text-align: left;">5V DC</td>
    </tr>
    <tr>
      <td>最大功耗</td>
      <td>25W</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">机械参数</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">尺寸</td>
      <td style="width: 80%; text-align: left;">188mm x 123mm x 40.6mm(长x宽x高)</td>
    </tr>
    <tr>
      <td>重量</td>
      <td>约900g</td>
    </tr>
    <tr>
      <td>安装方式</td>
      <td>嵌入式前安装</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">无线</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">Wi-Fi</td>
      <td style="width: 80%; text-align: left;">双频802.11ac Wi-Fi</td>
    </tr>
    <tr>
      <td>蓝牙</td>
      <td>蓝牙5.0/BLE</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
      <th colspan="2" style="text-align: left;">环境参数&法规</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 20%; text-align: left;">工作温度</td>
      <td style="width: 80%; text-align: left;">-20°C ~ 60°C</td>
    </tr>
    <tr>
      <td>存储温度</td>
      <td>-25°C ~ 60°C</td>
    </tr>
    <tr>
      <td>工作环境湿度</td>
      <td>5% ~ 95%（非冷凝）</td>
    </tr>
    <tr>
      <td>认证</td>
      <td>FCCFCC 47 CFR Part 15 Subpart BCEEN IEC 62368-1/EN IEC 62311/EN IEC 61000-3-2/EN IEC 61000-3-3EN 55032/EN 55035EN 301 489-1/EN 301 489-3/EN 301 489-17/EN 301 489-52EN 301 328/EN 301 440/EN 301 511/EN 301 908-1/EN 301 908-2</td>
    </tr>
  </tbody>
</table>








### 系统框图

![ED-HMI3020-070C-Datasheet-2024.05.21](./images/ED-HMI3020-070C-Datasheet-2024.05.21.png)



### 产品尺寸

单位：mm

![ED-HMI3020-070C-Datasheetdimensions-2024.05.21](./images/ED-HMI3020-070C-Datasheetdimensions-2024.05.21.png)



### 订购编码

![ED-HMI3020-070C-Datasheetorderingcode-2024.05.21](./images/ED-HMI3020-070C-Datasheetorderingcode-2024.05.21.png)




### 可选配件


可根据实际需要选择Raspberry Pi 官方电源适配器。

<table>
  <thead>
    <tr>
      <th style="text-align: left;">订购编码</th>
      <th style="text-align: left;">描述</th>
      <th style="text-align: left;">图片</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 35%; text-align: left;">SC1149</td>
      <td style="width: 30%; text-align: left;">Raspberry Pi 27W USB-C Power Supply White UK</td>
      <td style="width: 35%; text-align: center;" rowspan="10"><img src="./images/ED-HMI3010-070C-Datasheet2-2024.05.21.png"></td>
    </tr>
    <tr>
      <td>SC1150</td>
      <td>Raspberry Pi 27W USB-C Power Supply White AU</td>
    </tr>
    <tr>
      <td>SC1151</td>
      <td>Raspberry Pi 27W USB-C Power Supply White IN</td>
    </tr>
    <tr>
      <td>SC1152</td>
      <td>Raspberry Pi 27W USB-C Power Supply White EU</td>
    </tr>
    <tr>
      <td>SC1153</td>
      <td>Raspberry Pi 27W USB-C Power Supply White US</td>
    </tr>
    <tr>
      <td>SC1154</td>
      <td>Raspberry Pi 27W USB-C Power Supply Black UK</td>
    </tr>
    <tr>
      <td>SC1155</td>
      <td>Raspberry Pi 27W USB-C Power Supply Black AU</td>
    </tr>
    <tr>
      <td>SC1156</td>
      <td>Raspberry Pi 27W USB-C Power Supply Black IN</td>
    </tr>
    <tr>
      <td>SC1157</td>
      <td>Raspberry Pi 27W USB-C Power Supply Black EU</td>
    </tr>
    <tr>
      <td>SC1158</td>
      <td>Raspberry Pi 27W USB-C Power Supply Black US</td>
    </tr>
  </tbody>
</table>



### 包装清单

- 1 x ED-HMI3020-070C主机

- 4 x 卡扣(包含4xM4*8螺钉和4xM4*16螺钉)





### 常见问答

