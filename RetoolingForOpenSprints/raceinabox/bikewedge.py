"""------------------------------------------------------------------------bikewedge.py
    
    DESCRIPTION: This code intercepts both sides of opensprints/goldsprintsfx 
    "conversation" to control a visual indication of progress using something 
    like a phsical clock or a race tree.
    This makes it possible to not have a projector that costs more than your rollers.
    It also makes it possible to do outdoor or mobile events.
    
    COPYRIGHT: (c) 2013 Donald Delmar Davis, Suspect Devices, All Rights Reserved.
    This is free software released under modified BSD (details included in source).
    
    TECHNICAL: This is a basic combination of the client and server software from the 
    python in a nutshell book. It makes a lot of assumtions and should do a better 
    job of recovering when the pile of flash or the serial proxy crashes (which 
    happens). 
    It creates a server on 5331 (the only port gold sprints checks) and expects 
    to listen to serproxy on 5330 it talks to the clock on 5332
    it should eventually check and start serproxy and the goldsprints programs.
    it should also do a better job of recovering from issues created by externals.
    
    It has a lot of number foo (hard coding) in it that should be cleaned up
    
"""
import socket
import re
isocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
osocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
csocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
isocket.connect(('localhost',5330))
#isocket.setblocking(0)
isocket.settimeout(0.2)
print "Connected to serproxy"
csocket.connect(('localhost',5332))
csocket.settimeout(0.2)
print "Connected to clock"
osocket.bind(('',5331))
osocket.listen(1)

try:
    while True:
        connection,address=osocket.accept()
        if not connection: break
        print "Connected From", address
        #connection.setblocking(0)
        connection.settimeout(0.2)
        while True:
            try:
                receivedData = connection.recv(8192)
            except socket.error:
                receivedData=None
            if receivedData is not None:
                #print ">"+re.escape(str(receivedData))+">"+str(len(receivedData))
                isocket.sendall(receivedData)
                for chunk in receivedData.split('\x00'):
                    if len(chunk)>0 and chunk[0] == 's':
                        print "(RE)SET RACE !!!"
                        csocket.sendall("s\n");
                if len(receivedData)==0:
                    print "ISSUE WITH CLIENT"
                
            try:
                sentData = isocket.recv(8192)
            except socket.error:
                sentData=None
            if sentData is not None:
                #print "<"+re.escape(str(sentData))+"<"+str(len(sentData))
                connection.sendall(sentData)
                for chunk in sentData.split('\x00'):
                    #if len(chunk.rstrip('\r')):
                    #    print "<",re.escape(chunk),len(chunk)
                    if len(chunk) > 4 and chunk[0]=='0' :
                        done1=(float(chunk[3:])/1566.0) * 100.00
                        if done1>100.00 :
                            done1=100.00
                        print "Bike # 1 is ", str(int(done1)), "percent done"
                        csocket.sendall("d1:"+str(int(21.32*(done1)))+"\n")
                    if len(chunk) > 4 and chunk[0]=='1' :
                        done2=(float(chunk[3:])/1566.0) * 100.00
                        if done2>100.00 :
                            done2=100.00
                        print "Bike # 2 is ", str(int(done2)), "percent done"
                        csocket.sendall("d2:"+str(int(21.32*(done2)))+"\n")
                    
                if len(sentData)==0:
                    print "ISSUE WITH SERPROXY"
                    try:
                        isocket.sendall("\rv\r\x00")
                    except socket.error:
                        isocket.close()
                        isocket.connect(('localhost',5330))                        
                    break
finally:
    #need to see if connections is defined....
    connection.close()
    csocket.close()
    osocket.close()
    isocket.close()
