#coding=utf-8

import os,time,_thread,base64,re,threading,logging
from socket import *

BUFSIZ = 2048

STATUS = True

testlist = ["test001","test002","test003","test004","test005"]

def do_recv(status,tcpCliSock,f):
    try:
        while status:
            data1 = tcpCliSock.recv(BUFSIZ)
            if data1==b'':
                time.sleep(1)
            else:
                f.write(data1)
    except:
        f.close()

def get_rtcm_diffAccount(diffAccount,diffPwd,ip,port,mounted,_time):
    logging.basicConfig(level=logging.DEBUG,filename=os.getcwd() + os.sep + "rtcm" + os.sep + "DiffAccount", format='%(asctime)s  - %(message)s')
    logging.info("start: account = {} pwd = {}".format(diffAccount,diffPwd))
    ADDR = (ip, port)
    if not os.path.isdir("rtcm"):
        os.mkdir("rtcm")
    f = open(os.getcwd() + os.sep + "rtcm" + os.sep + "diffAccount" + "_" + diffAccount + "_" +diffPwd+ "_" + mounted + "_rtcm" + ".log",'wb', buffering=1)
    # Time_start = time.time()
    lopnumber = 0
    error_ = 0
    error_login = 0
    error_flag = False

    STATUS = True
    while STATUS:
        try:
            try:
                tcpCliSock = socket(AF_INET,SOCK_STREAM)
                tcpCliSock.connect(ADDR)
            except Exception as e:
                error_ +=1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},download error NO{}，reason:creat connet fail{}".format(aa,error_,e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

            try:
                EncryptionStr = base64.b64encode(str.encode(":".join([diffAccount, diffPwd])))
                header = 'GET /' + mounted + ' HTTP/1.1\r\nUser-Agent: NTRIP RTKLIB/2.4.3\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(
                    EncryptionStr) + '\r\n\r\n'
                tcpCliSock.send(header.encode('utf-8'))
                line=tcpCliSock.recv(BUFSIZ)
                result=line.decode('utf-8').rstrip()

            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},download error NO{},reason:login error user={},passwd={} recv:{}".format(aa,error_,diffAccount,diffPwd,e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

            try:
                if 'ICY 200 OK' in result:
                    _thread.start_new_thread(do_recv,(STATUS,tcpCliSock,f))
                    logging.info("account {},downloading ....".format(diffAccount))

                    for i in range(_time-1):
                        a = time.strftime('%H%M%S.%S', time.localtime())
                        data_gga = '$GPGGA,' + a + ',3113.2180600,N,12148.8000000,E,4,24,0.6,43.580,M,-6.251,M,,*47'
                        lopnumber = lopnumber+1
                        if lopnumber <= _time:
                            tcpCliSock.send((data_gga+'\r\n').encode())
                            time.sleep(1)
                        if lopnumber == _time-1:
                            logging.info("account {},dowload conplete,path:{}\r\n".format(diffAccount,os.getcwd()+os.sep+"rtcm"+os.sep+"_"+diffAccount+"_"+mounted+"_rtcm"+".log"))
                            STATUS = False
                            error_flag = False
                else:
                    error_login += 1
                    logging.info("login fail user={},passwd={} recv:{}".format(diffAccount,diffPwd,line))
                    logging.info("error_login:{}".format(error_login))
                    time.sleep(5)

                    if error_login > 10:
                        error_flag = True
                        break
                    continue
            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{}, downloading error NO{} ,reason:send gga fail  user={},passwd={} recv:{}".format(aa,error_,diffAccount, diffPwd, e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

        except Exception as e:
            continue

    return bool(1-error_flag)

def get_rtcm_FixedTerminal(diffAccount,diffPwd,ip,port,mounted,_time):
    logging.basicConfig(level=logging.DEBUG,filename=os.getcwd() + os.sep + "rtcm" + os.sep + "FixedTerminal", format='%(asctime)s  - %(message)s')
    logging.info("start: account = {} pwd = {}".format(diffAccount,diffPwd))
    ADDR = (ip, port)
    if not os.path.isdir("rtcm"):
        os.mkdir("rtcm")
    f = open(os.getcwd() + os.sep + "rtcm" + os.sep + "FixdTerminal" + "_" + diffAccount + "_" +diffPwd+ "_" + mounted + "_rtcm" + ".log",'wb', buffering=1)
    # Time_start = time.time()
    lopnumber = 0
    error_ = 0
    error_flag = False
    error_login = 0
    STATUS = True
    while STATUS:
        try:
            try:
                tcpCliSock = socket(AF_INET,SOCK_STREAM)
                tcpCliSock.connect(ADDR)
            except Exception as e:
                error_ +=1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},download fail NO{},reasom:creat connet fail{}".format(aa,error_,e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)

                continue

            try:
                header = "GET /" + mounted + " HTTP/1.0\r\n"+"User-Agent:CMSRSDK\r\n"+"Accept:*/*\r\n"+"Connection: close\r\n"+"Auth-Type: 1002\r\n"+ "Encryption-Type: 1000\r\n" + "Authorization: Basic " + diffAccount + "\r\n" + "\r\n"
                tcpCliSock.send(header.encode('utf-8'))
                line = tcpCliSock.recv(BUFSIZ)
                result = line.decode('utf-8').rstrip()

            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},dowmload fail NO{}, reason:fail connect  user={},passwd={} recv:{}".format(aa,error_,diffAccount,diffPwd,e))

                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

            try:
                if 'ICY 200 OK' in result:
                    _thread.start_new_thread(do_recv,(STATUS,tcpCliSock,f))
                    logging.info("account :{},downloading ...".format(diffAccount))

                    for i in range(_time-1):
                        a = time.strftime('%H%M%S.%S', time.localtime())
                        data_gga = '$GPGGA,' + a + ',3113.2180600,N,12148.8000000,E,4,24,0.6,43.580,M,-6.251,M,,*47'
                        lopnumber = lopnumber+1
                        if lopnumber <= _time:
                            tcpCliSock.send((data_gga+'\r\n').encode())
                            time.sleep(1)
                        if lopnumber == _time-1:
                            logging.info("account:{},download complete,path:{}\r\n".format(diffAccount,os.getcwd()+os.sep+"rtcm"+os.sep+"_"+diffAccount+"_"+mounted+"_rtcm"+".log"))
                            STATUS = False
                            error_flag = False
                else:
                    error_login += 1
                    logging.info("error_login:".format(error_login))
                    logging.info("login error user={},passwd={} recv:{}".format(diffAccount,diffPwd,line))
                    time.sleep(5)
                    if error_login > 10:
                        error_flag = True
                        break
                    continue
            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{}，download fail  NO{},reason: send gga fail user={},passwd={} recv:{}".format(aa,error_,diffAccount, diffPwd, e))

                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

        except Exception as e:
            continue
    return bool(1-error_flag)

def get_rtcm_AccountPool_allUser2(diffAccount,diffPwd,ip,port,mounted,_time,testlist):
    logging.basicConfig(level=logging.DEBUG,filename= os.getcwd() + os.sep + "rtcm" + os.sep +"AccountPool", format='%(asctime)s  - %(message)s')
    result_flag = True
    t_list = []
    t_result = []

    testlist = testlist.split(",")
    # print(testlist)
    # print(type(testlist))

    try:
        for i in testlist :
            t = MyThread(get_rtcm_AccountPool2,(diffAccount,diffPwd,i,ip,port,mounted,_time))
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join()
            t_result.append(t.get_result())
        #多线程只要有一个线程返回的结果是异常的，都报错误
        for t in t_result:
            if t_result[t]== False:
                result_flag = False
                break
            else:
                result_flag = True
    except:
        logging.info("Error: Failed to enable thread")
        exit(1)
    return result_flag

def get_rtcm_AccountPool2(diffAccount,diffPwd,zhc,ip,port,mounted,_time):

    logging.info("start: account = {} pwd = {}".format(diffAccount,diffPwd))
    ADDR = (ip, port)
    if not os.path.isdir("rtcm"):
        os.mkdir("rtcm")
    f = open(os.getcwd() + os.sep + "rtcm" + os.sep + "AccountPool" + "_" + diffAccount + "_" +diffPwd+ "_" + zhc+"_"+mounted + "_rtcm" + ".log",'wb', buffering=1)
    # Time_start = time.time()
    lopnumber = 0
    error_ = 0
    error_flag = False
    error_login = 0
    STATUS = True
    while STATUS:
        try:
            try:
                tcpCliSock = socket(AF_INET,SOCK_STREAM)
                tcpCliSock.connect(ADDR)
            except Exception as e:
                error_ +=1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},download fail NO{},reason: creat connect fail{}".format(aa,error_,e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

            try:
                header = "GET /" + mounted + " HTTP/1.0\r\n" +"User-Agent:CMSRSDK\r\n"+"Accept:*/*\r\n" +"Connection: close\r\n" + "Auth-Type: 1004\r\n" +"Encryption-Type: 1000\r\n"+ "Authorization: Basic "+ diffAccount+":"+diffPwd+":"+zhc + "\r\n"+ "\r\n"
                tcpCliSock.send(header.encode('utf-8'))
                line = tcpCliSock.recv(BUFSIZ)
                result = line.decode('utf-8').rstrip()

            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{}，download fail  NO{},reason:login error user={},passwd={} recv:{}".format(aa,error_,diffAccount,diffPwd,e))

                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

            try:
                if 'ICY 200 OK' in result:
                    _thread.start_new_thread(do_recv,(STATUS,tcpCliSock,f))
                    logging.info("account {}:{}:{},downloading ....".format(diffAccount,diffPwd,zhc))

                    for i in range(_time-1):
                        a = time.strftime('%H%M%S.%S', time.localtime())
                        data_gga = '$GPGGA,' + a + ',3113.2180600,N,12148.8000000,E,4,24,0.6,43.580,M,-6.251,M,,*47'
                        lopnumber = lopnumber+1
                        if lopnumber <= _time:
                            tcpCliSock.send((data_gga+'\r\n').encode())
                            time.sleep(1)
                        if lopnumber == _time-1:
                            logging.info("account:{},download conplete,path:{}\r\n".format(diffAccount,os.getcwd()+os.sep+"rtcm"+os.sep+"_"+diffAccount+"_"+diffPwd+"_"+ zhc+ "_"+mounted+"_rtcm"+".log"))
                            STATUS = False
                else:
                    error_login += 1
                    logging.info("login fail user={},passwd={} recv:{}".format(diffAccount,diffPwd,line))
                    logging.info("error_login: {}".format(error_login))
                    time.sleep(5)
                    if error_login > 5:
                        error_flag = True
                        break
                    continue
            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{}, downloading fail NO{}，reason:send gga fail user={},passwd={} recv:{}".format(aa,error_,diffAccount, diffPwd, e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

        except Exception as e:
            continue
    return bool(1-error_flag)

def get_rtcm_TimePool(diffAccount,diffPwd,zhc,ip,port,mounted,_time):
    logging.info("start: account = {} pwd = {}".format(diffAccount,diffPwd))
    ADDR = (ip, port)
    if not os.path.isdir("rtcm"):
        os.mkdir("rtcm")
    f = open(os.getcwd() + os.sep + "rtcm" + os.sep + "sjc" + "_" + diffAccount + "_" +diffPwd+ "_" + zhc+"_"+mounted + "_rtcm" + ".log",'wb', buffering=1)
    # Time_start = time.time()
    lopnumber = 0
    error_ = 0
    error_flag = False
    error_login = 0
    STATUS = True
    while STATUS:
        try:
            try:
                tcpCliSock = socket(AF_INET,SOCK_STREAM)
                tcpCliSock.connect(ADDR)
            except Exception as e:
                error_ +=1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{}，donwloading NO{} fail,reason:creat connect fail{}".format(aa,error_,e))
                logging.info(error_)
                if error_ > 5:
                    error_flag = True
                    STATUS = False
                    tcpCliSock.shutdown(2)
                    break
                continue

            try:
                header = "GET /" + mounted + " HTTP/1.0\r\n" +"User-Agent:CMSRSDK\r\n"+"Accept:*/*\r\n" +"Connection: close\r\n" + "Auth-Type: 1005\r\n" +"Encryption-Type: 1000\r\n"+ "Authorization: Basic "+ diffAccount+":"+diffPwd+":"+zhc + "\r\n"+ "\r\n"
                tcpCliSock.send(header.encode('utf-8'))
                line = tcpCliSock.recv(BUFSIZ)
                result = line.decode('utf-8').rstrip()

            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},download error head NO {} error,reason: login fail user={},passwd={} recv:{}".format(aa,error_,diffAccount,diffPwd,e))
                if error_ > 5:
                    error_flag = True
                    STATUS = False
                    tcpCliSock.shutdown(2)
                    break

                continue

            try:
                if 'ICY 200 OK' in result:
                    _thread.start_new_thread(do_recv,(STATUS,tcpCliSock,f))
                    logging.info("accout:{}:{}:{},downloading ".format(diffAccount,diffPwd,zhc))

                    for i in range(_time-1):
                        a = time.strftime('%H%M%S.%S', time.localtime())
                        data_gga = '$GPGGA,' + a + ',3113.2180600,N,12148.8000000,E,4,24,0.6,43.580,M,-6.251,M,,*47'
                        lopnumber = lopnumber+1
                        logging.info(lopnumber)
                        if lopnumber <= _time:
                            tcpCliSock.send((data_gga+'\r\n').encode())
                            time.sleep(1)
                        if lopnumber == _time-1:
                            logging.info("account:{},download complete,path:{}\r\n".format(diffAccount,os.getcwd()+os.sep+"rtcm"+os.sep+"_"+diffAccount+"_"+diffPwd+"_"+ zhc+ "_"+mounted+"_rtcm"+".log"))
                            STATUS = False
                else:
                    error_login += 1
                    logging.info("fail login user={},passwd={} recv:{}".format(diffAccount,diffPwd,line))
                    logging.info("error_login:{}".format(error_login))
                    time.sleep(1)
                    if grep_exceed(str(line)):
                        error_flag = False
                        STATUS = False
                        tcpCliSock.shutdown(2)
                        break
                    if error_login > 5:
                        error_flag = True
                        STATUS = False
                        tcpCliSock.shutdown(2)
                        break
                    continue
            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},downloading fail send NO{}，reason: send gga fail user={},passwd={} recv:{}".format(aa,error_,diffAccount, diffPwd, e))
                if error_ > 5:
                    error_flag = True
                    STATUS = False
                    tcpCliSock.shutdown(2)
                    break
                continue

        except Exception as e:
            continue
    return bool(1-error_flag)


class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def grep_exceed(str):
    out = re.split(r'[ \\r\s]\s*',str)
    for i in out:
        if i == 'TimePool_TimeExceed':
            return True
    return False


def get_rtcm_TimePool_allUser(diffAccount,diffPwd,ip,port,mounted,_time):
    logging.basicConfig(level=logging.DEBUG,filename=os.getcwd() + os.sep + "rtcm" + os.sep + "TimePool", format='%(asctime)s  - %(message)s')
    result_flag = True
    t_list = []
    t_result = []
    try:
        for i in testlist :
            t = MyThread(get_rtcm_TimePool,(diffAccount,diffPwd,i,ip,port,mounted,_time))
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join()
            t_result.append(t.get_result())
        #多线程只要有一个线程返回的结果是异常的，都报错误
        for t in t_result:
            if t_result[t]== False:
                result_flag = False
                break
            else:
                result_flag = True
    except:
        logging.info("Error: Failed to enable thread")
        exit(1)
    return result_flag

def get_rtcm_AccountPool(diffAccount,diffPwd,zhc,ip,port,mounted,_time):
    logging.info("start: account = {} pwd = {}".format(diffAccount,diffPwd))
    ADDR = (ip, port)
    if not os.path.isdir("rtcm"):
        os.mkdir("rtcm")
    f = open(os.getcwd() + os.sep + "rtcm" + os.sep + "AccountPool" + "_" + diffAccount + "_" +diffPwd+ "_" + zhc+"_"+mounted + "_rtcm" + ".log",'wb', buffering=1)
    # Time_start = time.time()
    lopnumber = 0
    error_ = 0
    error_flag = False
    error_login = 0
    STATUS = True
    while STATUS:
        try:
            try:
                tcpCliSock = socket(AF_INET,SOCK_STREAM)
                tcpCliSock.connect(ADDR)
            except Exception as e:
                error_ +=1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{},download fail NO{},reason: creat connect fail{}".format(aa,error_,e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

            try:
                header = "GET /" + mounted + " HTTP/1.0\r\n" +"User-Agent:CMSRSDK\r\n"+"Accept:*/*\r\n" +"Connection: close\r\n" + "Auth-Type: 1004\r\n" +"Encryption-Type: 1000\r\n"+ "Authorization: Basic "+ diffAccount+":"+diffPwd+":"+zhc + "\r\n"+ "\r\n"
                tcpCliSock.send(header.encode('utf-8'))
                line = tcpCliSock.recv(BUFSIZ)
                result = line.decode('utf-8').rstrip()

            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{}，download fail  NO{},reason:login error user={},passwd={} recv:{}".format(aa,error_,diffAccount,diffPwd,e))

                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

            try:
                if 'ICY 200 OK' in result:
                    _thread.start_new_thread(do_recv,(STATUS,tcpCliSock,f))
                    logging.info("account {}:{}:{},downloading ....".format(diffAccount,diffPwd,zhc))

                    for i in range(_time-1):
                        a = time.strftime('%H%M%S.%S', time.localtime())
                        data_gga = '$GPGGA,' + a + ',3113.2180600,N,12148.8000000,E,4,24,0.6,43.580,M,-6.251,M,,*47'
                        lopnumber = lopnumber+1
                        if lopnumber <= _time:
                            tcpCliSock.send((data_gga+'\r\n').encode())
                            time.sleep(1)
                        if lopnumber == _time-1:
                            logging.info("account:{},download conplete,path:{}\r\n".format(diffAccount,os.getcwd()+os.sep+"rtcm"+os.sep+"_"+diffAccount+"_"+diffPwd+"_"+ zhc+ "_"+mounted+"_rtcm"+".log"))
                            STATUS = False
                else:
                    error_login += 1
                    logging.info("login fail user={},passwd={} recv:{}".format(diffAccount,diffPwd,line))
                    logging.info("error_login:{}".format(error_login))
                    time.sleep(5)
                    if error_login > 5:
                        error_flag = True
                        break
                    continue
            except Exception as e:
                error_ += 1
                aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                logging.info("{}, downloading fail NO{}，reason:send gga fail user={},passwd={} recv:{}".format(aa,error_,diffAccount, diffPwd, e))
                if error_ > 5:
                    error_flag = True
                    break
                tcpCliSock.shutdown(2)
                continue

        except Exception as e:
            continue
    return bool(1-error_flag)

def get_rtcm_AccountPool_allUser(diffAccount,diffPwd,ip,port,mounted,_time):
    logging.basicConfig(level=logging.DEBUG,filename=os.getcwd() + os.sep + "rtcm" + os.sep + "AccountPool", format='%(asctime)s  - %(message)s')
    result_flag = True
    t_list = []
    t_result = []
    try:
        for i in testlist :
            t = MyThread(get_rtcm_AccountPool,(diffAccount,diffPwd,i,ip,port,mounted,_time))
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join()
            t_result.append(t.get_result())
        #多线程只要有一个线程返回的结果是异常的，都报错误
        for t in t_result:
            if t_result[t]== False:
                result_flag = False
                break
            else:
                result_flag = True
    except:
        logging.info("Error: Failed to enable thread")
        exit(1)
    return result_flag

def sendData(tcpConn, ggaList, interval, max):
    try:
        for i in range (0, max-1):
            n_time = time.strftime ( '%H%M%S.%S', time.localtime () )
            time.sleep ( 1 )
            GGAo = '$GPGGA,' + n_time + ',' + ggaList[i * interval]

            GGA = str.encode ( GGAo )
            print ( GGA )
            tcpConn.send ( GGA )
    except:
        print("sendData Error")

def clientGL(ip, port, username, passwd, mounted):
    flag = False
    print (
        "aa\nip: {}\nport: {}\nusername: {}\npasswd: {}\nmounted: {}\n".format ( ip, port, username, passwd, mounted ) )
    try:
        # s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        s = socket(AF_INET,SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, True)

        s.connect ( (ip, port) )

        EncryptionStr = base64.b64encode ( str.encode ( ":".join ( (username, passwd) ) ) )
        header = 'GET /' + mounted + ' HTTP/1.1\r\nUser-Agent: NTRIP RTKLIB/2.4.3\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode (
            EncryptionStr ) + '\r\n\r\n'
        print ( header )
        s.send ( header.encode () )
        data = s.recv ( 1024 ).decode ()

        result = data.rstrip ()
        if 'ICY 200 OK' == result:
            print ( "Client connect status{}".format ( result ) )
            gga_data_file = ["$GPGGA,111906.089,3208.1920973,N,11212.0712111,E,5,28,1.7,70.629,M,0.000,M,1.1,0000*6B",     "$GPGGA,111909.089,3208.1879985,N,11212.0699306,E,5,26,2.5,71.212,M,0.000,M,1.1,0000*64","$GPGGA,111914.889,3208.1509266,N,11212.0566779,E,5,28,2.8,72.884,M,0.000,M,0.9,0000*6F","$GPGGA,111915.889,3208.1492193,N,11212.0560380,E,5,27,2.8,73.018,M,0.000,M,0.9,0000*63","$GPGGA,111916.889,3208.1491331,N,11212.0560111,E,5,25,2.8,73.079,M,0.000,M,0.9,0000*66"]
            gga_lst = []
            #gga_data_file = open ( gga_data_path, 'r' )
            for gga in gga_data_file:
                gga_lst.append ( ','.join ( gga.split ( ',' )[2:] ) )

            get_pot_interval = 1

            max = int ( len ( gga_lst ) / get_pot_interval ) + 1
            t = MyThread(sendData,(s, gga_lst, get_pot_interval, max))
            t.start()
            flag = True
    except:
        return flag
    return flag