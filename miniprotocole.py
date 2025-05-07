from microbit import *
import radio
encryption=False
seqNum=0
tryTime=100
Timeout=300
ackMsgId=255
radio.config(channel=7,address=50)
radio.on()
if encryption:
 import random
 import aes
 key=bytes([156,110,239,52,206,138,164,35,3,76,3,60,84,199,63,253])
 iv=bytes([0]*16)
 cipher=aes.AES(key)
class Message:
 def __init__(s,d,e,n,i,p,c):s.exped=e;s.dest=d;s.seqNum=n;s.msgId=i;s.payload=p;s.crc=c
 def msgStr(s):return str(s.exped)+" -> "+str(s.dest)+"n["+str(s.seqNum)+"] : type "+str(s.msgId)+" : "+str(s.payload)+" (crc="+str(s.crc)+")"
def bytes_to_int(b):return [ord(bytes([i])) for i in b]
def int_to_bytes(l):return bytes(l)
def msg_to_trame(m):
 l=[m.dest,m.exped,m.seqNum,m.msgId]+m.payload
 m.crc=sum(l)%256
 t=l+[m.crc]
 if encryption:t=cipher.encrypt_cfb(t,iv)
 return int_to_bytes(t)
def trame_to_msg(t,u):
 t=bytes_to_int(t)
 if encryption:t=bytes_to_int(cipher.decrypt_cfb(t,iv))
 m=Message(t[0],t[1],t[2],t[3],t[4:-1],t[-1])
 if m.crc==sum(t[:-1])%256 and m.dest==u:return m
def ack_msg(m):
 a=Message(m.exped,m.dest,m.seqNum,ackMsgId,[],0)
 radio.send_bytes(msg_to_trame(a))
def receive_ack(m):
 t=radio.receive_bytes()
 if t:
  r=trame_to_msg(t,m.exped)
  return r and r.exped==m.dest and r.dest==m.exped and r.seqNum==m.seqNum and r.msgId==ackMsgId
 return False
def send_msg(i,p,u,d):
 global seqNum
 m=Message(d,u,seqNum,i,p,0)
 a=False
 t0=running_time()
 while not a and running_time()-t0<Timeout:
  radio.send_bytes(msg_to_trame(m))
  sleep(tryTime//2)
  display.clear()
  sleep(tryTime//2)
  a=receive_ack(m)
 seqNum=(seqNum+1)%256
 return a
def receive_msg(u):
 t=radio.receive_bytes()
 if t:
  m=trame_to_msg(t,u)
  if m and m.msgId!=ackMsgId:
   ack_msg(m)
   return m
if __name__=="__main__":
 import music
 userId=1
 while True:
  destId=0
  if button_a.was_pressed():print(send_msg(1,[60],userId,destId))
  elif button_b.was_pressed():send_msg(1,[120],userId,destId)
  m=receive_msg(userId)
  if m:
   print(m.msgStr())
   if m.msgId==1:music.pitch(m.payload[0]*10,duration=100,pin=pin0)
   elif m.msgId==2:display.show(Image.SQUARE)
