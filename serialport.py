import serial
from time import sleep

def openSerial():
    serial = serial.Serial('COM5', 9600, timeout=0.5)  #/dev/ttyUSB0
    if serial.isOpen() :
        print("open success")
    else :
        print("open failed")
    return serial


def wrserial(serial):
    serial.write([0x42, 0x4D, 0xAB, 0x00, 0x00, 0x01, 0x3A])
    data = serial.read_all()
    print(data)
    return dealReplyAB(data)

def dealReplyAB(data):
    # 查找到数据.
    print(len(data),':',data)
    datalen = len(data)
    cmdpos = -1
    for i in range(datalen):
        if (i+1) < datalen: 
            if data[i] == 0x42 and data[i+1] == 0x4D:
                cmdpos = i
    if(cmdpos >= 0):
        print('find cmd ' + str(cmdpos))
    # 获取命令长度
    cmdlen = (data[cmdpos+2] << 8) + data[cmdpos+3] + 4
    if cmdpos + cmdlen > datalen:
        print('错误!命令起始%d+命令长度%d>数据长度%d'%(cmdpos, cmdlen, datalen))
        return
    print('cmdpos:%d, cmdlen:%d'%(cmdpos, cmdlen))
    # 校验
    checksum = 0
    for i in range(cmdlen-2):
        checksum += data[cmdpos+i]
    checksum = checksum & 0xffff
    checksum2 = (data[cmdpos+cmdlen-2]<<8) + data[cmdpos+cmdlen-1]
    print('checksum:%04x, cal:%04x'%(checksum2, checksum))
    print(data)
    if (checksum != checksum2):
        print('错误!校验和不一致!')
        return
    # 读取数据.
    dict = {}
    dict['Pm25'] = (data[cmdpos+4]<<8) + data[cmdpos+5]
    dict['Tvoc'] = (data[cmdpos+6]<<8) + data[cmdpos+7]
    dict['Hcho'] = (data[cmdpos+9]<<8) + data[cmdpos+10]
    dict['Co2'] = (data[cmdpos+12]<<8) + data[cmdpos+13]
    dict['Temp'] = (data[cmdpos+14]<<8) + data[cmdpos+15]
    dict['Hum'] = (data[cmdpos+16]<<8) + data[cmdpos+17]
    return dict


def test():
    # barr = [0x42, 0x4D, 0xAB, 0x00, 0x00, 0x01, 0x3A]
    barr = [0x42, 0x4D, 0x00, 0x14, 0x01, 0x02, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 
    0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA9]
    result = dealReplyAB(barr)
    print(result)

if __name__ == '__main__':
    test()