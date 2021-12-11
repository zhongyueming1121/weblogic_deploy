# weblogic_deploy
一键部署具有admin server功能的weblogic服务

1.修改：info.properties 
2.执行：python create_weblogic_server.py 

注意点 
1.
run_mode= 1 #仅安装启动adminServer: 1, 仅安装启动mServer: 2, 安装启动前两者: 3 
2.
nm_port=5556 #本机mServer建议使用5556，其他主机依次递增，不能重复 
