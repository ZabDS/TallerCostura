import logging
import threading
import time

def costuraMangas(cond,cesta,condCLL):
    
    while True:
        with cond:
            Mangas = len(cesta)
            if (Mangas > 1):
                cond.notifyAll()
                logging.debug("Poniendo los Mangas disponibles")
            if Mangas == 10:
                logging.debug("Cesta de Mangas llena")
                with condCLL:
                    condCLL.wait()
                    #bloquear hasta que haya un espacio en cesta
            else:
                cesta.insert(Mangas,"Mangas")
                time.sleep(.5)
                #print("Poniendo los Mangas disponibles")
        

def costuraCuerpo(cond,cesta,condCLL):
    while True:
        with cond:
            Cuerpos = len(cesta)
            if (Cuerpos > 0):
                cond.notifyAll()
                logging.debug("Poniendo los cuerpos disponibles")
            if Cuerpos == 10:
                with condCLL:
                    condCLL.wait()
                logging.debug("Cesta de cuerpos llena")
                
            else:
                cesta.insert(Cuerpos,"cuerpo")
                time.sleep(.5)    
        
def Ensamblado(condM,condC,cestaMangas,cestaCuerpo,condCLLM,condCLLC):       
    while True:
        Mangas = len(cestaMangas)
        Cuerpos = len(cestaCuerpo)
        
        if(Mangas < 2):
            with condM:
                logging.debug("Esperando a que haya mangas")
                condM.wait()               
        if(Cuerpos < 1):
            with condC:
                logging.debug("Esperando a que haya Cuerpos")
                condC.wait()
                
        cestaMangas.pop()
        cestaMangas.pop()
        if Mangas == 10:
            with condCLLM:
                condCLLM.notifyAll()
        cestaCuerpo.pop()
        if Cuerpos == 10:
            with condCLLC:
                condCLLC.notifyAll()
        logging.debug("Se ha terminado una prenda")
    logging.debug("Terminado")
    
logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)
    
cestaMangas=[]
cestaCuerpo=[]

conditionC = threading.Condition()
conditionCCLL = threading.Condition()
conditionM = threading.Condition()
conditionMCLL = threading.Condition()

Persona3 = threading.Thread(target=Ensamblado,args=(conditionM,conditionC,cestaMangas,cestaCuerpo,conditionMCLL,conditionCCLL), name='Persona3E')
Persona3.start()
Persona1 = threading.Thread(target=costuraMangas,args=(conditionM,cestaMangas,conditionMCLL), name='Persona1M')
Persona1.start()
Persona2 = threading.Thread(target=costuraCuerpo,args=(conditionC,cestaCuerpo,conditionCCLL), name='Persona2C')
Persona2.start()
    