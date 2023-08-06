import time


class StopWatch:
    def __init__(self) -> None:
        self.timeHistory = []
        self.__timeElapsed = 0
        self.__isRunning = False

    def Start(self):
        if(self.__isRunning):
            return
        self.__isRunning = True
        self.timeHistory.append({
            "timestamp": time.time(),
            "isStartEvent": True
        })
        self.__UpdateTimeElapsed()
        return
    
    def Stop(self):
        if not(self.__isRunning):
            return
        self.__isRunning = False
        self.timeHistory.append({
            "timestamp": time.time(),
            "isStartEvent": False
        })
        return
    def Reset(self):
        self.__isRunning = False
        self.timeHistory = []

    def __UpdateTimeElapsed(self):
        endTime = time.time() #take end time directly to avoid spending time while calculating
        self.__timeElapsed = 0
        startTime = None
        for timeEvent in self.timeHistory:
            if(timeEvent["isStartEvent"]):
                startTime = timeEvent["timestamp"]
                continue
            self.__timeElapsed += timeEvent["timestamp"] - startTime
            startTime = None
        if(startTime is not None):
            self.__timeElapsed += endTime - startTime

    def GetElapsedSeconds(self) -> float: 
        '''gets elapsed time in seconds with high precision'''
        self.__UpdateTimeElapsed()
        return  self.__timeElapsed

    def GetElapsedMilliseconds(self) -> float:
        '''get elapsed time in milliseconds with high precision'''
        return self.GetElapsedSeconds() * 1000
    def ToString(self, decimalPrecision:int = 11) -> str:
        '''Prints time in seconds with specified precision example "1.00202312323" in Seconds'''
        return str(round(self.GetElapsedSeconds(), decimalPrecision))


