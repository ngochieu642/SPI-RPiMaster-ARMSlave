import spidev
import struct
import time
'''
In this script, RPi receives 8 bytes from SPI-Slave, decode it into 2 float and
write to a text file in the same folder
'''

'''SPI'''
spi = spidev.SpiDev() #tao doi tuong cho SPI
spi.open(0,0)          #Mo port 0, device 0 (cs0)
spi.max_speed_hz = 16000000
print('Done config')

try:
    print('begin to send SPI slave');
    while True:

        #Send any 8 Bytes to get 8 bytes back
        to_send = [0X09,0x01,0x01,0x01,0x01,0x01,0x0D,0x0A]
        resp = spi.xfer2(to_send)

        #resp=[LSB1...MSB1 LSB2 MSB2], exactly what we want
        firstFloat_ByteList=resp[0:4]
        secondFloat_ByteList=resp[4:8]

        #Get Bytes from list
        firstFloat_Bytes=bytes(firstFloat_ByteList)
        secondFloat_Bytes=bytes(secondFloat_ByteList)

        #Unpack those value, return tuple type
        returnFirstValue = struct.unpack('f',firstFloat_Bytes)
        returnSecondValue = struct.unpack('f',secondFloat_Bytes)

        #Print information
        print('\n\nWriting to file...')
        print('1st: ',returnFirstValue[0],' 2nd: ',returnSecondValue[0])

        #Write file
        with open('2FloatResult.txt','a') as myFile:
            #We just took 2 number after comma for the shale of simplicity
            firstString = '%.2f'%(returnFirstValue[0])
            secondString ='%.2f'%(returnSecondValue[0])
            myFile.write(firstString+","+secondString+"\n")

        '''This rate = 10Hz, MUST BE EQUAL to the sending rate of SPI-Slave'''
        time.sleep(0.1)

except KeyboardInterrupt:
    spi.close()
    print('Interrupt detected')
finally:
    print('Done clean up port')
