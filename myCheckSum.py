class myCheckSum():
    def __init__(self, data=[]):
        self.data = data
        self.sumdata = 0x00
        self.result = 0x00
        #get data all summed up
        self.sumCheckSum()
        
        #reverse by bit
        self.complementData()
    
    def get(self):
        return self.result
    
    # 求和    
    def sumCheckSum(self):
        dataLen = len(self.data)
        for i in range(dataLen): 
            self.sumdata += self.data[i]
    
    # 取反
    def complementData(self):                   
        twoResult = bin(self.sumdata)
        calLen = len(hex(self.sumdata)[2:])
        twoResultLen = len( twoResult[2:])     
        if calLen*4 > twoResultLen:
            subLen = calLen*4 - twoResultLen
            twoResult = '0b' + '0'*subLen + twoResult[2:]
        if len(twoResult[2:]) < 8:
            subL = 8 - len(twoResult[2:])
            twoResult = '0b' + '0'*subL + twoResult[2:]
        reverseResult = '0b'
        for i in twoResult[2:]:
            if i == '1':
                reverseResult += '0'
            else:
                reverseResult += '1'
        preRes = hex(eval(reverseResult))
        if len(preRes) < 4:
            preRes = '0x0' + preRes[2:]
        self.result = '0x' + str.upper(preRes[-2:])

# Test Cases
# data1 = [0x03, 0x09, 0x03, 0x2a, 0x40, 0x1f, 0x00, 0x00, 0x00, 0x00]    #0x67
# data2 = [0x01, 0x02]    #0xFC
# data3 = [0xfe, 0x04, 0x03, 0x05, 0x01]  #0xF4
# data4 = [0x01, 0x09, 0x03, 0x2a, 0x2c, 0x01, 0x00, 0x00, 0x00, 0x00]    #0x9B
# data5 = [0x01, 0x09, 0x03, 0x2a, 0xc8, 0x00, 0x00, 0x00, 0x00, 0x00]    #0x00

# print(myCheckSum(data1).get(), myCheckSum(data2).get(), myCheckSum(data3).get(), myCheckSum(data4).get(), myCheckSum(data5).get())
