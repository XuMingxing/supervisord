#  eventlistener
该脚本可以放在supervisord的eventlistener中，用于监测程序的异常状态，
并进行报警。部署过程中有三个文件：listener.py 这就是我们event的监测脚本；
sendmsg.py 这是短信接口脚本，在监听程序中需要调用的;phonenumber.cfg号码
的配置文件，在配置文件中需要写你要监听的每个进程及你所配置的号码，若有多
个号码，用','隔开。

以树莓派217为例：
在家目录下新建文件夹event-listener，将三个文件拷到该目录下。
----第一步-----
配置文件的修改：
1.打开配置文件phonenumber.cfg;(nano phonenumber.cfg)
2.[process]下的"command="后即是你要监控的进程名（是supervisord配置下的进程名，
可利用'sudo supervisorctl status'查看),每个进程名间用','隔开。
3.[phonenumber]下是每个进程所配置的号码（格式为：'processname=15000000000,
15000000001' 多个号码间用','隔开。）

----第二步-----
对supervisord配置文件的修改
1.打开配置文件/etc/supervisord.conf;
2.修改[eventlistener:theeventlistenername]下的参数配置：
  中括号内':'后为监听脚本名；
 ' command='后为脚本打开的路径；
 ' events= '后为监听的异常状态；
 ' stdout_logfile='后为标准输出日志路径；
 ' stderr_logfile='后为标准错误日志路径；

----第三步------
重启supervisord服务

注：若系统没有安装过阿里云短信的SDK则无法发送短信，需要安装。
