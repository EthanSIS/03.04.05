'''
OC Robotique 2025
Template pour librairie Protocole Réseau pour Micro:bit

Auteur·ice : Ethan, Chloé et Marcos
Version : 1.2
Date : 12.02.25
'''

#### Libraries ####
from microbit import *
import radio

#### Variables globales ####
seqNum = 0
tryTime = 100
Timeout = 300
ackMsgId = 255

#### Start radio module ####
radio.config(channel=7, address=77)
radio.on()


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
    
      return str(self.exped)+ " -> "+ str(self.dest)+ "n[" + str(self.seqNum)+ "] "+ " : type "+ str(self.msgId)+" : " +str(self.payload)+ " (crc="+ str(self.crc)+")"
     '''
#### Toolbox ####
def bytes_to_int(bytesPayload:bytes):
    '''
    Convert bytes object to List[int]
            Parameters:
                    bytesPayload(bytes): payload in bytes format
            Returns:
                    intPayload(List[int]): payload in int format
    ''''''
    intPayload = []
    for i in bytesPayload:
        intPayload.append(ord(bytes([i])))        
    return intPayload
     ''''''
'''
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
    2) Conversion en bytes
            Parameters:
                    rawMsg(Message): Objet Message contenant tous les paramètres du message à envoyer
            Returns:
                    trame(bytes): payload convertie au format bytes
    '''
    pass # à compléter


def trame_to_msg(trame : bytes, userId :int):
    '''
    Crée un objet Message à partir d'une trame brute recue.
    1) Conversion de bytes en liste de int
    2) Découpage de la liste de int dans l'ordre du protocole pour remplir l'objet Message
    3) Check du CRC et du destinataire
            Parameters:
                    trame(bytes): payload au format bytes
            Returns:
                    msgObj(Message): Objet Message contenant tous les paramètres du message recu si crc et destinataire ok, sinon None
    '''
    pass # à compléter
    
    
def ack_msg(msg : Message):
    '''
    Envoie un ack du message recu.
    1) Création d'une liste de int correspondant au ack dans l'ordre du protocole
    2) Conversion en bytes
    3) Envoi
            Parameters:
                    msg(Message): Objet Message contenant tous les paramètres du message à acker
    '''
    pass # à compléter


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
    pass # à compléter
    

def send_msg(msgId:int, payload:List[int], userId:int, dest:int):
    global seqNum
    
    msg = [msgId] + payload
    radio.send_bytes(int_to_bytes(msg))
    
    
    
    
    
    
    
    
    '''
    Envoie un message.
    
    1) Crée un objet Message à partir des paramètres
    message = Message(dest ,userId, payload#il manque des trucs ici, voir la classe message)
    #time = time.time()
    En boucle jusqu'à un timeout ou ack: 
    #while 
        2) Conversion objet Message en trame et envoi  
        radio.send_bytes(msg_to_trame(message))#la fonction msg to trame a pas encore été complétée

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
   

def receive_msg(userId:int):
    
    new_trame = radio.receive_bytes()
    if new_trame:
        trame = bytes_to_int(new_trame)
        msgObj = Message(None,None,None, trame[0], trame[1], None)
        
        return msgObj
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
    pass # à compléter


if __name__ == '__main__':
    
    userId = 0

    while True:
        # Messages à envoyer
        destId = 1
        if button_a.was_pressed():
            send_msg(1,[60],userId, destId)
            

                
        # Reception des messages
        m = receive_msg(userId)        
        if m and m.msgId==1:
            display.show(Image.SQUARE)

            

                
        # Reception des messages
        m = receive_msg(userId)        
        if m and m.msgId==1:
            display.show(Image.SQUARE)
            
            
