# **DH-TelegramBot**
使用前先给予DH-Bot管理员权限  
使用机器人之前请先在**群组内**进行初始化操作  
```/init``` 初始化  
不进行初始化操作将无法使用群组内签到等功能  
部署前请先配置```config.py```文件  

## **指令**
```/init``` 初始化  
```/update``` 更新群组数据库  
```/auto_hick``` 根据输入指令自动踢出  
```/status``` 展示群内成员状态  
```/group_status``` 获取群组状态  
```/kick_deleted``` 删除群组中所有已删除账户  
```/unban``` 解除封禁  
```kick_people``` 永久踢除  
```/banme``` 获得随机封禁时长  
```/dc``` 查询Datacenter位置  
```/queryid``` 查询用户ID  
```/ping``` 存活测试  
```/check_in``` 签到(根据群组)  
```/auto_kick``` 自动踢除(arguments)  
```/ip``` 查询IP信息(arguments)  

## **参数**

### auto_kick
“online” - 删除在线用户  
“offline” - 踢出所有在线用户  
“recently” - 踢出最近3天内未上线用户(慎重)  
“within_week” - 踢出2-3天或者一星期内未上线用户   
“within_month” - 踢出6-7天或者一个月内未上线用户  
“long_time_ago” - 踢出超过一个月未上线用户  

### ip
后面接IP地址即可

## **例子**
```/ip 8.8.8.8``` - 查询8.8.8.8的信息  
```/auto_kick long_time_ago``` - 删除超过一个月未登录用户  
```/kick_deleted``` - 踢出已删除账户  
```/status``` - 查看群内用户状态  

## TODO list
- [ ] 增加前端控制面板
- [ ] 查询whois信息
- [ ] 实现ping功能
- [ ] 实现自定义DNS查询功能
- [ ] 实现自定义查询DOH，DOT等
