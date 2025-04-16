'''
Protocole Réseau Pour Micro:bit OC Robotique 2025
Auteur·ice : Vincent Namy
Version : 1.4
Date : 03.03.25
'''

encryption = False

#### Libraries ####
from microbit import *
import radio

if encryption:
    import random
    import aes

#### Variables globales ####
seqNum = 0
tryTime = 100
Timeout = 300
ackMsgId = 255

#### Start radio module ####
radio.config(channel=7, address=50)
radio.on()

#### Init AES ####
if encryption:
    key    = bytes([156, 110, 239, 52, 206, 138, 164, 35, 3, 76, 3, 60, 84, 199, 63, 253]) # Generate yours with bytes([ random.getrandbits(8) for _ in range(16)])
    iv     = bytes([ 0 for _ in range(16)])
    cipher = aes.AES(key)



#### Classe Message ####
class Message:
  def __init__(self, dest:int, exped:int, seqNum:int, msgId:int, payload:List[int], crc:int):
    '''
    Constructeur de l'objet Message à partir des paramètres
            Parameters:
                    dest:int, exped:int, seqNum:int, msgId:int, payload:List[int], crc:int
            Returns:
                    self(Message): objet Message contenant les paramètres
    '''
    self.exped = exped
    self.dest = dest
    self.seqNum = seqNum
    self.msgId = msgId
    self.payload = payload
    self.crc = crc
  def msgStr(self):
    '''
    Crée une string contenant les détails du message
            Parameters:
                    self(Message): objet message
            Returns:
                    msgStr(str): string contenant les détails du message
    '''
    return str(self.exped)+ " -> "+ str(self.dest)+ "n[" + str(self.seqNum)+ "] "+ " : type "+ str(self.msgId)+" : " +str(self.payload)+ " (crc="+ str(self.crc)+")"

#### Toolbox ####
def bytes_to_int(bytesPayload:bytes):
    '''
    Convert bytes object to List[int]
            Parameters:
                    bytesPayload(bytes): payload in bytes format
            Returns:
                    intPayload(List[int]): payload in int format
    '''
    intPayload = []
    for i in bytesPayload:
        intPayload.append(ord(bytes([i])))        
    return intPayload


def int_to_bytes(intPayload:List[int]):    
    '''
    Convert  List[int] to bytes object 
            Parameters:
                    intPayload(List[int]): payload in int format
            Returns:
                    bytesPayload(bytes): payload in bytes format
    '''
    return bytes(intPayload)


#### Fonctions réseaux ####
def msg_to_trame(rawMsg : Message):
    '''
    Crée une trame à partir des paramètres d'un objet Message afin de préparer un envoi.
    1) Création d'une liste de int dans l'ordre du protocole
    2) Encryption si nécessaire
    3) Conversion en bytes
            Parameters:
                    rawMsg(Message): Objet Message contenant tous les paramètres du message à envoyer
            Returns:
                    trame(bytes): payload convertie au format bytes
    '''
    l = [rawMsg.dest, rawMsg.exped, rawMsg.seqNum, rawMsg.msgId] + rawMsg.payload
    rawMsg.crc = sum(l)%256
    trame = l + [rawMsg.crc]
    
    if encryption:
        trame = cipher.encrypt_cfb(trame, iv)
        
    return int_to_bytes(trame)


def trame_to_msg(trame : bytes, userId :int):
    '''
    Crée un objet Message à partir d'une trame brute recue.
    1) Conversion de bytes en liste de int
    2) Decryption si nécessaire
    3) Découpage de la liste de int dans l'ordre du protocole pour remplir l'objet Message
    4) Check du CRC et du destinataire
            Parameters:
                    trame(bytes): payload au format bytes
            Returns:
                    msgObj(Message): Objet Message contenant tous les paramètres du message recu si crc et destinataire ok, sinon None
    '''
    trame = bytes_to_int(trame)
    
    if encryption:
        trame = bytes_to_int(cipher.decrypt_cfb(trame, iv))
        
    msgObj = Message(trame[0], trame[1], trame[2], trame[3], trame[4:-1], trame[-1])
    if msgObj.crc == sum(trame[:-1])%256:
        if msgObj.dest == userId : 
            return msgObj
    
    
def ack_msg(msg : Message):
    '''
    Envoie un ack du message recu.
    1) Création d'une liste de int correspondant au ack dans l'ordre du protocole
    2) Conversion en bytes
    3) Envoi
            Parameters:
                    msg(Message): Objet Message contenant tous les paramètres du message à acker
    '''
    
    msgAck = Message(msg.exped, msg.dest, msg.seqNum, ackMsgId, [],0)
    trame = msg_to_trame(msgAck)
    radio.send_bytes(trame)


def receive_ack(msg: Msg):
    '''
    Attend un ack correspondant au message recu.
    1) Récupère les messages recus
    2) Conversion trame en objet Message
    3) Check si le ack correspond
            Parameters:
                    msg(Message): Objet Message duquel on attend un ack
            Returns:
                    acked(bool): True si message acké, sinon False
    '''
    new_trame = radio.receive_bytes()
    if new_trame:
        msgRecu = trame_to_msg(new_trame, msg.exped)
        return msgRecu and msgRecu.exped == msg.dest and msgRecu.dest == msg.exped and msgRecu.seqNum == msg.seqNum and msgRecu.msgId == ackMsgId
    else:
        return False
    

def send_msg(msgId:int, payload:List[int], userId:int, dest:int):
    '''
    Envoie un message.
    1) Crée un objet Message à partir des paramètres
    En boucle jusqu'à un timeout ou ack: 
        2) Conversion objet Message en trame et envoi 
        3) Attend et check le ack
    4) Incrémentation du numéro de séquence
            Parameters:
                    msgId(int): Id du type de message
                    payload(List[int]): liste contenant le corps du message
                    userId(int): Id de Utilisateur·ice envoyant message
                    dest(int): Id de Utilisateur·ice auquel le message est destiné
            Returns:
                    acked(bool): True si message acké, sinon False
    '''

    global seqNum
    
    msg = Message(dest, userId, seqNum, msgId, payload,0)
    
    acked = False
    t0 = running_time()
    while not acked and running_time()-t0 < Timeout:
        trame = msg_to_trame(msg)
        radio.send_bytes(trame)
        sleep(tryTime//2)
        display.clear()
        sleep(tryTime//2)
        acked = receive_ack(msg)
#         print(running_time()-t0)
        
    seqNum = (seqNum+1)%256
    return acked

def receive_msg(userId:int):
    '''
    Attend un message.
    1) Récupère les messages recus
    2) Conversion trame en objet Message
    3) Check si ce n'est pas un ack
            Parameters:
                    userId(int): Id de Utilisateur·ice attendant un message
            Returns:
                    msgRecu(Message): Objet Message contenant tous les paramètres du message
    '''
    new_trame = radio.receive_bytes()
    if new_trame:
        msgRecu = trame_to_msg(new_trame, userId)
        if msgRecu and msgRecu.msgId != ackMsgId:
            ack_msg(msgRecu)
            return msgRecu


if __name__ == '__main__':
    import music
    
    userId = 1

    while True:
        # Messages à envoyer
        destId = 0
        if button_a.was_pressed():
            print(send_msg(1,[60],userId, destId))
        elif button_b.was_pressed():
            send_msg(1,[120],userId, destId)
            

                
        # Reception des messages
        m = receive_msg(userId)
        if m:
            print(m.msgStr())
        if m and m.msgId==1:
            music.pitch(m.payload[0]*10, duration=100, pin=pin0)
        elif m and m.msgId==2:
            display.show(Image.SQUARE)
    
