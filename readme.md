## Before We Start:

本教程将介绍如何用树莓派安装Home Assistant系统（HassOS）及其Wi-Fi和SSH设置。内容主要参照Home Asisstant[官方文档](https://www.home-assistant.io/getting-started/)。以及我的[blog](https://www.lynnislu.com/posts/home_assistant_1/)。

### Agenda

1. Prerequisites 

## 1. Prerequisites 

- 一个树莓派4（3也可以）和电源适配器，USB直接连接电脑或充电宝等设备可能会导致电压不够的问题。
- 一台电脑用于烧录Home Assistant系统。
- 一张micro sd卡，推荐至少使用32G的sd卡及其读卡器。
- 有线键盘、显示器和显示器与树莓派的连接线。
- 一个U盘用于配置Wi-Fi。

## 2. HassOS Installation

- 根据[您的设备](https://www.home-assistant.io/hassio/installation/)下载HassOS的镜像文件到您的计算机上。
  - Note: 虽然官网说推荐32bit的，但是我试过下载[Raspberry Pi 4 Model B 32bit](https://github.com/home-assistant/operating-system/releases/download/3.12/hassos_rpi4-3.12.img.gz)之后无法烧录，后来成功运行的是64bit的。
- 下载好的镜像文件用读卡器通过**[balenaEtcher](https://link.zhihu.com/?target=https%3A//www.balena.io/etcher/)**烧录到SD卡。
- 

## 3. [Wi-Fi Configuration](https://github.com/home-assistant/operating-system/blob/dev/Documentation/network.md)

以下内容均在您的计算机上操作：

- 首先先格式化您的U盘到FAT格式，并取名为`CONFIG`。

- 打开`CONFIG`，在U盘里新建一个**文件夹**：`network`，所以目前您所在的位置应该是`/CONFIG/network/`。

- 接下来，用一个不会随便加格式的记事本或者代码编辑器（比如[Atom](https://atom.io/)，我个人是直接vim了）新建一个**文件**：`my-network`，没有任何后缀。

- 于是你需要编辑这个`/CONFIG/network/my-network`，复制以下代码并填写您的Wi-Fi名字和密码。

  ```bash
  [connection]
  id=my-network
  uuid=72111c67-4a5d-4d5c-925e-f8ee26efb3c3
  type=802-11-wireless
  
  [802-11-wireless]
  mode=infrastructure
  ssid=MY_SSID #替换MY_SSID到您的Wi-Fi名字，字面意思
  # Uncomment below if your SSID is not broadcasted
  #hidden=true
  
  [802-11-wireless-security]
  auth-alg=open
  key-mgmt=wpa-psk
  psk=MY_WLAN_SECRET_KEY #替换MY_WLAN_SECRET_KEY为您的Wi-Fi密码，也是字面意思
  
  [ipv4]
  method=auto
  
  [ipv6]
  addr-gen-mode=stable-privacy
  method=auto
  ```

- 保存后，安全拔出U盘，准备运行树莓派。

  - HassOS账号root，没有密码直接回车就可以登陆

- 将U盘和sd卡都插在树莓派上，连接电源、显示器和键盘，树莓派会自动开机运行sd卡上的内容，也会自动配置好无线网络。如果您觉得您的网络配置有误，也不要参照文档里的这个重置网络，因为并不存在这个文件`/usr/share/system-connections/*`，也就是说执行完第一步删除之后，您就啥也不剩了。（当然您可以在HassOS的无图形界面用nano编辑器再把默认配置打进去）

  > If you want to reset the network configuration back to the default DHCP settings, use the following commands on the host:

  > ```bash
  > $ rm /etc/NetworkManager/system-connections/*
  > $ cp /usr/share/system-connections/* /etc/NetworkManager/system-connections/
  > $ nmcli con reload
  > ```

- 您可以试着`ping baidu.com`看看数据包是不是顺利发出+接收了。一旦成功连接了Wi-Fi后，您可以将设置Wi-Fi的U盘拔下，网络依然有效。

### 4. SSH Configuration

​	我写不动了，用您自己的计算机的浏览器打开http://homeassistant.local:8123/。SSH设置是被集成好的。左侧有一个**Supervisor**然后选择 **Add-on Store**。官方文档在这：[Home Assistant Add-on: SSH server](https://github.com/home-assistant/hassio-addons/blob/master/ssh/README.md)。但是这个**add on**不叫**ssh server**叫**terminal & ssh**。反正你搜索**ssh**总能搜到的。

- 生成自己计算机上的公钥和私钥，方便起见不要设置密码

> To use this add-on, you must have a private/public key to log in. To generate them, follow the [instructions for Windows](https://www.digitalocean.com/community/tutorials/how-to-create-ssh-keys-with-putty-to-connect-to-a-vps) and [these for other platforms](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/). 

- 填写到**add-on**的**ssh**界面（可以用`cat filename`，输出公钥复制）

```bash
authorized_keys:
  - ssh-rsa AKDJD3839...== my-key
password: ''
```

### Summary 

​	Hmmm 我一开始就装了这个HassOS在树莓派上，后来觉得延展性不够，我就重新再装了Raspbian lite，目前我的Home Assistant是在Raspbian上运行的，教程之后补上，有兴趣的朋友可以先看一眼我的[gitlab](https://gitlab.com/lynnislu/home-assistant/-/tree/master)。本项目成了我疫情在家的巨大乐趣。疫情来了买点啥囤家里，买个树莓派吧。
