# Hosts_scanV2优化版
这是一个用于IP和域名碰撞匹配访问的小工具优化版， 能大大减少碰撞中出来的假误报，旨意用来匹配出渗透过程中需要绑定hosts才能访问的弱主机或内部系统

# Hosts_scan原版规则如下
https://github.com/fofapro/Hosts_scan
假如 12.12.12.12  直接访问时 假如页面为 aaaaaaa页面
碰撞host域名之后，再访问时页面也为aaaaaaa页面， 按照之前的host碰撞脚本规则，会一并提取出来，算有效，保存到hosts_ok.txt中

但其实这样的碰撞出来的页面其实并不是真实有效，因为就算不加域名访问都一样，失去了host碰撞意义，也是一种误报，当资产过多时，人工排查起来也麻烦


# Hosts_scanV2版本优化后的规则如下
假如 12.12.12.12  直接访问时 页面为 aaaaaaa页面
绑定host域名之后，再访问时 页面也为aaaaaaa页面，V2直接忽略~

那什么才算有效？ 只有当 
12.12.12.12  直接访问时 页面为 aaaaaaa页面，或其他页面
碰撞host域名之后，再访问时 页面也为bbbbbb页面，算作有效碰撞
简单说，ip与域名 访问之间要有差别才算有效碰撞
![image](https://user-images.githubusercontent.com/50769953/139517788-0a8f6b81-b3df-4e09-ac07-0a35ef81fc31.png)



# 使用
使用还是原版本一样，默认开启多线程模式，20线程，python3直接运行即可
读取 ip.txt 和 hosts.txt 遍历匹配访问
![image](https://user-images.githubusercontent.com/50769953/139517797-6dc3cac0-bbc4-4d15-b85e-47acddbb2ab3.png)
