import socket
import re
import struct


class FinsPLCMemoryAreas:
    def __init__(self):
        """Hex code for memory areas

        Each memory area has a corresponding hex code for word access, bit access
        forced word access and forced bit access. This class provides name-based
        access to them.
        """
        self.CIO_BIT=b'\x30'
        self.WORK_BIT=b'\x31'
        self.HOLDING_BIT=b'\x32'
        self.AUXILIARY_BIT=b'\x33'
        self.CIO_BIT_FORCED=b'\70'
        self.WORK_BIT_FORCED=b'\x71'
        self.HOLDING_BIT_FORCED=b'\x72'
        self.CIO_WORD=b'\xB0'
        self.WORK_WORD=b'\xB1'
        self.HOLDING_WORD=b'\xB2'
        self.AUXILIARY_WORD=b'\xB3'
        self.CIO_WORD_FORCED=b'\xF0'
        self.WORK_WORD_FORCED=b'\xF1'
        self.HOLDING_WORD_FORCED=b'\xF2'
        self.TIMER_FLAG=b'\x09'
        self.COUNTER_FLAG=b'\x09'
        self.TIMER_FLAG_FORCED=b'\x49'
        self.COUNTER_FLAG_FORCED=b'\x49'
        self.TIMER_WORD=b'\x89'
        self.COUNTER_WORD=b'\x89'
        self.DATA_MEMORY_BIT=b'\x02'
        self.DATA_MEMORY_WORD=b'\x82'
        self.EM0_BIT=b'\x20'
        self.EM1_BIT=b'\x21'
        self.EM2_BIT=b'\x22'
        self.EM3_BIT=b'\x23'
        self.EM4_BIT=b'\x24'
        self.EM5_BIT=b'\x25'
        self.EM6_BIT=b'\x26'
        self.EM7_BIT=b'\x27'
        self.EM8_BIT=b'\x28'
        self.EM9_BIT=b'\x29'
        self.EMA_BIT=b'\x2A'
        self.EMB_BIT=b'\x2B'
        self.EMC_BIT=b'\x2C'
        self.EMD_BIT=b'\x2D'
        self.EME_BIT=b'\x2E'
        self.EMF_BIT=b'\x2F'
        self.EM10_BIT=b'\xE0'
        self.EM11_BIT=b'\xE1'
        self.EM12_BIT=b'\xE2'
        self.EM13_BIT=b'\xE3'
        self.EM14_BIT=b'\xE4'
        self.EM15_BIT=b'\xE5'
        self.EM16_BIT=b'\xE6'
        self.EM17_BIT=b'\xE7'
        self.EM18_BIT=b'\xE8'
        self.EM0_WORD=b'\xA0'
        self.EM1_WORD=b'\xA1'
        self.EM2_WORD=b'\xA2'
        self.EM3_WORD=b'\xA3'
        self.EM4_WORD=b'\xA4'
        self.EM5_WORD=b'\xA5'
        self.EM6_WORD=b'\xA6'
        self.EM7_WORD=b'\xA7'
        self.EM8_WORD=b'\xA8'
        self.EM9_WORD=b'\xA9'
        self.EMA_WORD=b'\xAA'
        self.EMB_WORD=b'\xAB'
        self.EMC_WORD=b'\xAC'
        self.EMD_WORD=b'\xAD'
        self.EME_WORD=b'\xAE'
        self.EMF_WORD=b'\xAF'
        self.EM10_WORD=b'\x60'
        self.EM11_WORD=b'\x61'
        self.EM12_WORD=b'\x62'
        self.EM13_WORD=b'\x63'
        self.EM14_WORD=b'\x64'
        self.EM15_WORD=b'\x65'
        self.EM16_WORD=b'\x66'
        self.EM17_WORD=b'\x67'
        self.EM18_WORD=b'\x68'
        self.EM_CURR_BANK_BIT=b'\x0A'
        self.EM_CURR_BANK_WORD=b'\x98'
        self.EM_CURR_BANK_NUMBER=b'\xBC'
        self.TASK_FLAG_BIT=b'\x06'
        self.TASK_FLAG_STATUS=b'\x46'
        self.INDEX_REGISTER=b'\xDC'
        self.DATA_REGISTER=b'\xBC'
        self.CLOCK_PULSES=b'\x07'
        self.CONDITION_FLAGS=b'\x07'


class FinsCommandCode:
    def __init__(self):
        """Hex code for fins command code

        Each fins command has a corresponding hex code. This class provides name-based
        access to them.
        """
        self.MEMORY_AREA_READ = b'\x01\x01'
        self.MEMORY_AREA_WRITE = b'\x01\x02'
        self.MEMORY_AREA_FILL = b'\x01\x03'
        self.MULTIPLE_MEMORY_AREA_READ=b'\x01\x04'
        self.MEMORY_AREA_TRANSFER=b'\x01\x05'
        self.PARAMETER_AREA_READ=b'\x02\x01'
        self.PARAMETER_AREA_WRITE=b'\x02\x02'
        self.PARAMETER_AREA_FILL=b'\x02\x03'
        self.PROGRAM_AREA_READ=b'\x03\x06'
        self.PROGRAM_AREA_WRITE=b'\x03\x07'
        self.PROGRAM_AREA_CLEAR=b'\x03\x08'
        self.RUN=b'\x04\x01'
        self.STOP=b'\x04\x02'
        self.CPU_UNIT_DATA_READ=b'\x05\x01'
        self.CONNECTION_DATA_READ=b'\x05\x02'
        self.CPU_UNIT_STATUS_READ=b'\x06\x01'
        self.CYCLE_TIME_READ=b'\x06\x20'
        self.CLOCK_READ=b'\x07\x01'
        self.CLOCK_WRITE=b'\x07\x02'
        self.MESSAGE_READ=b'\x09\x20'
        self.ACCESS_RIGHT_ACQUIRE=b'\x0C\x01'
        self.ACCESS_RIGHT_FORCED_ACQUIRE=b'\x0C\x02'
        self.ACCESS_RIGHT_RELEASE=b'\x0C\x03'
        self.ERROR_CLEAR=b'\x21\x01'
        self.ERROR_LOG_READ=b'\x21\x02'
        self.ERROR_LOG_CLEAR=b'\x21\x03'
        self.FINS_WRITE_ACCESS_LOG_READ=b'\x21\x40'
        self.FINS_WRITE_ACCESS_LOG_CLEAR=b'\x21\x41'
        self.FILE_NAME_READ=b'\x22\x01'
        self.SINGLE_FILE_READ=b'\x22\x02'
        self.SINGLE_FILE_WRITE=b'\x22\x03'
        self.FILE_MEMORY_FORMAT=b'\x22\x04'
        self.FILE_DELETE=b'\x22\x05'
        self.FILE_COPY=b'\x22\x07'
        self.FILE_NAME_CHANGE=b'\x22\x08'
        self.MEMORY_AREA_FILE_TRANSFER=b'\x22\x0A'
        self.PARAMETER_AREA_FILE_TRANSFER=b'\x22\x0B'
        self.PROGRAM_AREA_FILE_TRANSFER=b'\x22\x0C'
        self.DIRECTORY_CREATE_DELETE=b'\x22\x15'
        self.MEMORY_CASSETTE_TRANSFER=b'\x22\x20'
        self.FORCED_SET_RESET=b'\x23\x01'
        self.FORCED_SET_RESET_CANCEL=b'\x23\x02'
        self.CONVERT_TO_COMPOWAY_F_COMMAND=b'\x28\x03'
        self.CONVERT_TO_MODBUS_RTU_COMMAND=b'\x28\x04'
        self.CONVERT_TO_MODBUS_ASCII_COMMAND=b'\x28\x05'


def int2bytes(value,length):
    return value.to_bytes(length,'big')


class MakeFrame:
    magic_bytes = b'\x46\x49\x4e\x53'  # FINS
    def __init__(self,ICF=b'\x80', RSV=b'\x00', GCT=b'\x02', DNA=b'\x00',DA1=b'\x00',DA2=b'\x00', SNA=b'\x00',
                 SA1=b'\x00', SA2=b'\x00', SID=b'\x00', cmd=b''):
        self.cmd_frame=b''
        self.fin_frame=b''
        self.ICF=ICF    # 1 byte
        self.RSV=RSV    # 1 byte
        self.GCT=GCT    # 1 byte
        self.DNA=DNA    # 1 byte
        self.DA1=DA1    # 1 byte
        self.DA2=DA2    # 1 byte
        self.SNA=SNA    # 1 byte
        self.SA1=SA1    # 1 byte
        self.SA2=SA2    # 1 byte
        self.SID=SID    # 1 byte
        self.cmd=cmd    # 2 byte
    def cmdFINS(self,cmd=b''):
        self.cmd=cmd
        self.cmd_frame = self.cmd_frame+self.ICF+self.RSV+self.GCT+self.DNA+self.DA1+self.DA2+self.SNA+self.SA1+self.SA2+self.SID+self.cmd
        return self.cmd_frame
    def FINScmdHeader(self,length_cmd,cmd,error_code=0,client_node_address=None):
        self.fin_frame += self.magic_bytes                  # FINS
        self.fin_frame += int2bytes(8+length_cmd,4)         # frame length=len(FINS_header)+len(cmd)=8+len(cmd)
        self.fin_frame += int2bytes(cmd,4)                  # cmd=0:client to server/ cmd=1:server to client
        self.fin_frame += int2bytes(error_code,4)           # Error code
        if client_node_address is not None:
            self.fin_frame += int2bytes(client_node_address,4)  # first time client_node_address = 0
        return self.fin_frame


class TCPconnect():
    def __init__(self,host = '', port = 9600):
        self.sock=None
        self.DA1=None
        self.SA1=None
        self.isOpen = False
        self.host = host
        self.port = port
        self.responseCMDS = b''
        self.response = None
    def connectt(self):
        # Check if connect open: if: open=>close else: open
        if self.isOpen:
            self.sock.close()
            self.isOpen=False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        self.sock.settimeout(2.0)
        self.isOpen = True
        # Send first time with empty Client Node Address field 0x00000000 to get DA1 and SA1/send NADS
        self.send_data(MakeFrame().FINScmdHeader(length_cmd=4, cmd=0,client_node_address=0))
        self.responseCMDS = self.receive_data(4096)    # Get client node address and server node address/ DA1 and SA1
        self.DA1= int2bytes(self.responseCMDS[23],1)
        #print('DA1 ',self.DA1)
        self.SA1= int2bytes(self.responseCMDS[19],1)
        return self.sock
    def send_data(self,request):
        self.sock.send(request)
    def receive_data(self,size):
        data = self.sock.recv(size)
        return data

    def ReadMemory(self, mem_area_code, type, des_address, number_of_item=1):
        cmdFS = MakeFrame().FINScmdHeader(length_cmd=18,cmd = 2)
        Cmd = mem_area_code+ type + int2bytes(des_address,2)+int2bytes(number_of_item,3)
        cmdFINS = MakeFrame(DA1=self.DA1, SA1=self.SA1,SID=b'\x01').cmdFINS(cmd= Cmd)
        self.send_data(cmdFS)
        self.send_data(cmdFINS)
        b = self.receive_data(4096)
        return list(b)

    def WriteMemory(self, mem_area_code, type, des_address, message=0, number_of_item=1):
        cmdFS = MakeFrame().FINScmdHeader(length_cmd=20,cmd = 2)
        Cmd = mem_area_code + type + int2bytes(des_address,2)+int2bytes(number_of_item,3)
        cmdFINS = MakeFrame(DA1=self.DA1, SA1=self.SA1,SID=b'\x01').cmdFINS(cmd= Cmd)
        self.send_data(cmdFS)
        self.send_data(cmdFINS)
        self.send_data(int2bytes(message,2))
        resFINS = self.receive_data(4096)
    def __del__(self):
        self.sock.close()
        self.isOpen = False
        print('Connection is closed')


# __________________________TEST_AREA______________________________ #
def main():
    cmd_NADS = MakeFrame().FINScmdHeader(length_cmd=4, cmd=0)
    dung = TCPconnect(host='192.168.250.1', port=9600)
    dung.connectt()
    i = 0
    while i < 100:
        dung.WriteMemory(FinsCommandCode().MEMORY_AREA_WRITE, FinsPLCMemoryAreas().DATA_MEMORY_WORD,200,i)
        dataax = dung.ReadMemory(FinsCommandCode().MEMORY_AREA_READ, FinsPLCMemoryAreas().DATA_MEMORY_WORD, 200)
        i += 1
        print('D200_after', dataax)
    print(dung.isOpen)


if __name__=='main':
    main()