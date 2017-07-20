#!/usr/bin/env python
#coding= utf-8
# Author zhyaof(mail@zhyaof.net)
'''
    Suprevisord Listener example.
'''

import sys
import os
import sample1

def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

#def baojing(msg=None, data=None):
  #  if msg == None and data == None:
   #     return
    # alert

def parseData(data):
    tmp = data.split('\n')
    pheaders = dict([ x.split(':') for x in tmp[0].split() ])
    pdata = None
    if len(tmp) > 1:
        pdata = tmp[1]
    return pheaders, pdata

def main():
    #Only supervisord can run this listener, otherwise exit.
    if not 'SUPERVISOR_SERVER_URL' in os.environ:
        print "%s must be run as a supervisor listener." % sys.argv[0]
        return

    while 1 :
        #echo 'READY' and wait for event for stdin.
        write_stdout('READY\n')
        line = sys.stdin.readline()  # read header line from stdin
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len'])) # read the event payload

        if headers['eventname'] == 'PROCESS_STATE_EXITED' or\
           headers['eventname'] == 'PROCESS_STATE_FATAL' or\
           headers['eventname'] == 'PROCESS_STATE_STOPPED':
            pheaders, pdata = parseData(data)
            from_state = pheaders['from_state']
            process_name = pheaders['processname']
            if headers['eventname'] == 'PROCESS_STATE_EXITED' and\
                not int(pheaders['expected']):
                msg = '进程%s(PID: %s)异常退出，请检查进程状态.'\
                    % (process_name, pheaders['pid'])
              #  print(msg)
                sample1.send_msg("pro:%s","state","exited") 
            if headers['eventname'] == 'PROCESS_STATE_FATAL':
                msg = '进程%s启动失败，请检查进程状态.'\
                    % (process_name)
               # print(msg)
                sample1.send_msg("pro:%s","state","fatal")
        elif headers['eventname'] == 'PROCESS_LOG_STDERR':
            pheaders, pdata = parseData(data)
            process_name = pheaders['processname']
            pid = pheaders['pid']
            msg = '进程%s(PID: %s)错误输出，请检查进程状态，错误输出信息: %s.' \
                % (process_name, pid, pdata)
           # print(msg)
            sample1.send_msg("pro:%s","log","stderr")
        #echo RESULT
        write_stdout('RESULT 2\nOK') # transition from READY to ACKNOWLEDGED

if __name__ == '__main__':
    main()
