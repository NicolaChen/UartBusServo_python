class MyCheckSum:
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data
        self.sum_data = 0x00
        self.result = 0x00
        # get data all summed up
        self.sumCheckSum()

        # reverse by bit
        self.complementData()

    def get(self):
        return self.result

    # 求和
    def sumCheckSum(self):
        data_len = len(self.data)
        for i in range(data_len):
            self.sum_data += self.data[i]

    # 取反
    def complementData(self):
        two_result = bin(self.sum_data)
        cal_len = len(hex(self.sum_data)[2:])
        two_result_len = len(two_result[2:])
        if cal_len * 4 > two_result_len:
            sub_len = cal_len * 4 - two_result_len
            two_result = '0b' + '0' * sub_len + two_result[2:]
        if len(two_result[2:]) < 8:
            sub_l = 8 - len(two_result[2:])
            two_result = '0b' + '0' * sub_l + two_result[2:]
        reverse_result = '0b'
        for i in two_result[2:]:
            if i == '1':
                reverse_result += '0'
            else:
                reverse_result += '1'
        pre_res = hex(eval(reverse_result))
        if len(pre_res) < 4:
            pre_res = '0x0' + pre_res[2:]
        self.result = '0x' + str.upper(pre_res[-2:])
