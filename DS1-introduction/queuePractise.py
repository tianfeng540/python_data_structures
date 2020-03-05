# class Queue:
#     """双端队列"""
#     def __init__(self):
#         self.items = []
    
#     def isEmpty(self):
#        """判断队列是否为空"""
#         return self.items == []
    
#     def enqueue(self,item):
#       """在队头添加元素"""
#         self.items.insert(0,item)

#     def dequeue(self):    
#          """从队尾删除元素"""
#         return self.items.pop()

#     def size(self):
#        """返回队列大小"""
#         return len(self.items)


'''
平均每天10名学生在任何给定时间在实验室工作，每个学生通常在此期间打印2次
打印一次的范围1-20页   20  400     2 40     4 80
每分钟打印机可以处理10页，但打印的质量比较差
如果需要打印的质量比较好，那么打印机每分钟只能处理5页
'''
'''
    1. 创建打印任务的队列。每个任务都有个时间戳，队列启动的时候为空
    2. 是否创建新的打印任务？如果是，创建时间戳添加到队列 090101
    3. 打印机不忙并且有任务在等待：
       从打印机队列中删除一个任务并将其分配给打印机  090301
       当前时间减去创建任务的时间戳，计算该任务的等待时间  2
       将该任务的等待时间添加到列表中稍后处理
       根据打印任务的页数，确定需要多少时间
    4. 打印机需要1s打印，所以得从2分钟内-1s = 等待时间
    5. 任务完成，所需要的时间是0，打印机空闲
    6. 模拟完成后，从生成的等待时间列表中计算平均等待时间
    Printer 打印机对象 两种状态，默认是空闲状态
    PrinterQueue  打印队列对象  用来创建任务
    Task  任务对象 1-20随机，random
'''
class Printer:
    # 初始化参数：设置打印机的速率（每分钟5页还是10页）
    def __init__(self,ppm):
        self.pagerate = ppm  # 打印机的速率
        self.currentTask = None # 空闲状态
        self.timeRemaining = 0  # 打印任务需要的时间为0,为空闲状态

    def tick(self):
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        if self.currentTask != None:
            return True
        else:
            return False
    
    def startNext(self,newTask):
        self.currentTask = newTask
        self.timeRemaining = newTask.getPages()*60/self.pagerate  


import random
class Task:
    def __init__(self,time):
        self.timestamp = time
        self.pages = random.randrange(1,21)
    
    def getStamp(self):
        return self.timestamp
    
    def getPages(self):
        return self.pages
    
    def waitTime(self,currenttime):
        return currenttime - self.timestamp


from pythonds.basic.queue import Queue

# newPrintTask 决定是否创建一个新的打印任务。1个小时之内20任务打印完成，打印任务每180秒到达一次
def simulation(numSeconds,pagesPerMinute):
    labprinter = Printer(pagesPerMinute) # 初始化打印机
    printQueue = Queue()
    waitingtimes = []

    for currentSecond in range(numSeconds):
        if newPrintTask():
            task = Task(currentSecond)
            printQueue.enqueue(task)
        
        if (not labprinter.busy()) and (not printQueue.isEmpty()):
            nexttask = printQueue.dequeue()
            waitingtimes.append(nexttask.waitTime(currentSecond))
            labprinter.startNext(nexttask)

        labprinter.tick()

    averageWait = sum(waitingtimes)/len(waitingtimes)

    print("平均等待时间为：%6.2f"%averageWait)


def newPrintTask():
    num = random.randrange(1,181)
    if num == 180:
        return True
    else:
        return False


for i in range(10):
    simulation(3600,5) # 一个小时，速率5页