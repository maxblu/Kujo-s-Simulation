from generadores import *
import logging
import math
import matplotlib.pyplot as plt
import statistics

logging.basicConfig(format='Kojo\'s %(levelname)s system: %(message)s', level=logging.INFO)



intervals = [
				{
					'start':600, 
					'end':690,
					'arrival_interval':1/16
				},
				{
					'start':690, 
					'end':810,
                    'arrival_interval':1/2
				},
				{
					'start':810, 
					'end':1020,
                    'arrival_interval':1/13
				},
				{
					'start':1020, 
					'end':1140,
                    'arrival_interval':1/3
				},
				{
					'start':1140, 
					'end':1260,
                    'arrival_interval':1/10
				},
			]	
				
current_interval = 0    




def simula_kujos(dias=30):
    """Metodo que simula dias en la cocina del kojo para dos cocineros """
    means=[]
    eficiencias=[]
    i=1

    while i <= dias:
        
    ####################################################Inicializacion##########################################
        #Variables del sistema
        nA=0
        t0=600
        t=600 
        T=1260
        SS=[0]


        #variables de salida 
        A=[0] # A[i]  es tiempo de llegada del cliente i
        D={} # D[i] es tiempo de salida del cliente i

        #lista de eventos
                # donde ta es tiempo de arrivo del proximo cliente 
        ta=0            # ti es tiempo de partida del cliente que esta siendo atendido por chef 1 o 2
        t1=1              #nota pudiera en ves de llevar bools de los chef poner en uno a ti si no esta ocupado  
        t2=1
        t=0
        n=0
        SS=[0]
        t1=t2=float('Infinity')
        ta=t0
        timeInWait={}
        cantDuranteTiempo=[]
    #################################################Fin de la Inicializacion####################################
    #################################################Cuerpo de la Simulacion#####################################

        while n!=0   or  t<T:
            # log("Inicio while")
            # log(n)
            # log(["Actual time ",t])
            # log([t0,T])
            # log(['CAntidad de clientes en el sistema ',n])
            # log(['VAriable SS del sistema ',SS])
            # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])

            # input()



            #Caso 1
            if ta == min((ta,t1,t2)):
                # log('Entro en caso 1')
                
                if ta != float('Infinity'):
                    t=ta
                    log("New client #"+ str(nA+1)  + " at time: "+ str(t))
                    

                # log(["Actual time ",t])
                nA=nA+1
                n+=1
                cantDuranteTiempo.append((n,t))
                ##corregir esto preguntar en dependecia de que tiempo t estoy generar el proximo con el lambda que toca
                
                #si genero la proxima
                if t >=intervals[0]['start'] and t < intervals[0]['end']: 
                    ta=t+exponencial(intervals[0]['arrival_interval'])
                elif t >=intervals[1]['start'] and t < intervals[1]['end']: 
                    ta=t+exponencial(intervals[1]['arrival_interval'])
                elif t >=intervals[2]['start'] and t < intervals[2]['end']: 
                    ta=t+exponencial(intervals[2]['arrival_interval'])
                elif t >=intervals[3]['start'] and t < intervals[3]['end']: 
                    ta=t+exponencial(intervals[3]['arrival_interval'])    
                else: 
                    ta=t+exponencial(intervals[4]['arrival_interval'])        
                
                
                
                A.append(t)

                if ta >=T:
                    ta=float('Infinity')


                #Elegir que es lo que quiere el cliente que puede ser atendido 0:sandwish 1:sushi 
                tipo = bernoulli(0.5)
                

                if SS==[0]:
                    SS=[1,nA,0]
                    
                    if tipo ==0:
                        t1=t+uniforme(3,5)
                        timeInWait[nA]=t        
                    else:        
                        t1=t+uniforme(5,8)    
                        timeInWait[nA]=t
                elif SS[0]==1 and SS[1]!=0 and SS[2]==0:
                    SS[0]=2
                    SS[2]=nA

                    if tipo ==0:
                        t2=t+uniforme(3,5)
                        timeInWait[nA]=t        
                    else:        
                        t2=t+uniforme(5,8)
                        timeInWait[nA]=t    

                elif SS[0]==1 and SS[1]==0 and SS[2]!=0:

                    SS[0]=2
                    SS[1]=nA

                    if tipo ==0:
                        t1=t+uniforme(3,5)
                        timeInWait[nA]=t        
                    else:        
                        t1=t+uniforme(5,8)
                        timeInWait[nA]=t          
                else:
                    SS[0]+=1
                    SS.append(nA)

                # log("Caso uno final")
                # log([t0,T])
                # log(['CAntidad de clientes en el sistema ',n])
                # log(['VAriable SS del sistema ',SS])
                # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])
                # # input()    
                
            #Caso 2
            if t1<ta and t1 <=t2:
                # log('Entro en caso 2')
                t=t1
                # log(["Actual time ",t])
                D[SS[1]]=t
                log("Client #"+ str(SS[1])  + " gone at time: "+ str(t))
                n-=1
                cantDuranteTiempo.append((n,t))

                if SS[0]==1:
                    SS=[0]
                    t1=float('Infinity')
                
                elif SS[0]==2:
                    SS=[1,0,SS[2]]
                    t1=float('Infinity')
                else:
                    SS[0]-=1
                    temp=SS[3]
                    SS=[SS[0]]+[temp]+[SS[2]]+SS[4:len(SS)]

                    tipo = bernoulli(0.5)

                    if tipo ==0:
                        t1=t+uniforme(3,5)
                        timeInWait[SS[1]]=t        
                    else:        
                        t1=t+uniforme(5,8)
                        timeInWait[SS[1]]=t   

                # log("Caso 2 final")
                # log([t0,T])
                # log(['CAntidad de clientes en el sistema ',n])
                # log(['VAriable SS del sistema ',SS])
                # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])
                # input()

            #Caso 3
            if t2 < ta and t2 < t1:
                # log('Entro en caso 3')
                t=t2
                # log(["Actual time ",t])
                D[SS[2]]=t
                log("Client #"+ str(SS[2])  + " gone at time: "+ str(t))
                n-=1
                cantDuranteTiempo.append((n,t))

                # log("Caso 3 final")
                # log([t0,T])
                # log(['CAntidad de clientes en el sistema ',n])
                # log(['VAriable SS del sistema ',SS])
                # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])
                # log(D)
                # input()

                if SS[0]==1:
                    SS=[0]
                    t2=float('Infinity')
                
                elif SS[0]==2:
                    SS=[1,SS[1],0]
                    t2=float('Infinity')
                else:
                    SS[0]-=1
                    temp=SS[3]
                    SS=SS[0:2]+[temp]+SS[4:len(SS)]

                    tipo = bernoulli(0.5)

                    if tipo ==0:
                        t2=t+uniforme(3,5)
                        timeInWait[SS[2]]=t        
                    else:        
                        t2=t+uniforme(5,8)
                        timeInWait[SS[2]]=t         
                
    ###############################################Fin del cuerpo de la simulacion#####################################
    #################################################Calculos de salida para un dia#########################################
        # log(len(A))
        # log(len(D))

        # log(A)
        # log(D)
        
        #tiempo que pasa en la cola cada cliente
        diferences=[]

        for p in range(1,nA+1):
            diferences.append(timeInWait[p]-A[p])

        eficiencia=0
        moreThan5=[]
        for x in diferences: 
            if x<=5:
                moreThan5.append(x) 

        eficiencia = len(moreThan5)*100/nA


        mean_one_day=statistics.mean(diferences)
        means.append(mean_one_day)

        log("Mean: "+str(mean_one_day))
        log("Eficiencia: "+str(eficiencia))
        eficiencias.append(eficiencia)
        # print(i)
        if i>=30 and keep_going(eficiencias,k=i):
            dias+=1
        elif i>=30:
            log('Days simulated: '+str(dias))
            break         
        
        i+=1    
        # plt.plot(diferences,[x for x in range(len(diferences))])
        # plt.show()
        # plt.hist(diferences)
        # plt.plot([y for x,y in cantDuranteTiempo],[x for x,y in cantDuranteTiempo])
        # plt.plot([x for x in diferences])
        
        # plt.subplot(2,1,1)
        # plt.show()
    #################################################Fin de la simulacion total para un dia#####################################
    
    log('Mean of waiting time: '+ str(statistics.mean(means)))
    log('Mean of percent of efficienci: '+ str(statistics.mean(eficiencias)))

    print(dias)
    plt.plot(range(1,dias+1),eficiencias)
    plt.show()

def simula_kujos_twoCooks(dias=30):
    """Metodo que simula dias en la cocina del kojo para dos cocineros """
    means=[]
    eficiencias=[]
    i=1

    while i <= dias:
        
    ####################################################Inicializacion##########################################
        #Variables del sistema
        nA=0
        t0=600
        t=600 
        T=1260
        SS=[0]


        #variables de salida 
        A=[0] # A[i]  es tiempo de llegada del cliente i
        D={} # D[i] es tiempo de salida del cliente i

        #lista de eventos
                # donde ta es tiempo de arrivo del proximo cliente 
        ta=0            # ti es tiempo de partida del cliente que esta siendo atendido por chef 1 o 2
        t1=1              #nota pudiera en ves de llevar bools de los chef poner en uno a ti si no esta ocupado  
        t2=1
        t3=1
        t=0
        n=0
        SS=[0]
        t1=t2=t3=float('Infinity')
        ta=t0
        timeInWait={}
        cantDuranteTiempo=[]
    #################################################Fin de la Inicializacion####################################
    #################################################Cuerpo de la Simulacion#####################################

        while n!=0   or  t<T:
            # log("Inicio while")
            # log(n)
            # log(["Actual time ",t])
            # log([t0,T])
            # log(['CAntidad de clientes en el sistema ',n])
            # log(['VAriable SS del sistema ',SS])
            # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])

            # input()



            #Caso 1
            if ta == min((ta,t1,t2,t3)):
                # log('Entro en caso 1')
                
                if ta != float('Infinity'):
                    t=ta
                    log("New client #"+ str(nA+1)  + " at time: "+ str(t))
                    

                # log(["Actual time ",t])
                nA=nA+1
                n+=1
                cantDuranteTiempo.append((n,t))
                ##corregir esto preguntar en dependecia de que tiempo t estoy generar el proximo con el lambda que toca
                
                #si genero la proxima
                if t >=intervals[0]['start'] and t < intervals[0]['end']: 
                    ta=t+exponencial(intervals[0]['arrival_interval'])
                elif t >=intervals[1]['start'] and t < intervals[1]['end']: 
                    ta=t+exponencial(intervals[1]['arrival_interval'])
                elif t >=intervals[2]['start'] and t < intervals[2]['end']: 
                    ta=t+exponencial(intervals[2]['arrival_interval'])
                elif t >=intervals[3]['start'] and t < intervals[3]['end']: 
                    ta=t+exponencial(intervals[3]['arrival_interval'])    
                else: 
                    ta=t+exponencial(intervals[4]['arrival_interval'])        
                
                
                
                A.append(t)

                if ta >=T:
                    ta=float('Infinity')


                #Elegir que es lo que quiere el cliente que puede ser atendido 0:sandwish 1:sushi 
                tipo = bernoulli(0.5)
                

                if SS==[0]:
                    SS=[1,nA,0]
                    
                    if tipo ==0:
                        t1=t+uniforme(3,5)
                        timeInWait[nA]=t        
                    else:        
                        t1=t+uniforme(5,8)    
                        timeInWait[nA]=t
                elif SS[0]==1 and SS[1]!=0 and SS[2]==0:
                    SS[0]=2
                    SS[2]=nA

                    if tipo ==0:
                        t2=t+uniforme(3,5)
                        timeInWait[nA]=t        
                    else:        
                        t2=t+uniforme(5,8)
                        timeInWait[nA]=t    

                elif SS[0]==1 and SS[1]==0 and SS[2]!=0:

                    SS[0]=2
                    SS[1]=nA

                    if tipo ==0:
                        t1=t+uniforme(3,5)
                        timeInWait[nA]=t        
                    else:        
                        t1=t+uniforme(5,8)
                        timeInWait[nA]=t          
                else:
                    SS[0]+=1
                    SS.append(nA)

                # log("Caso uno final")
                # log([t0,T])
                # log(['CAntidad de clientes en el sistema ',n])
                # log(['VAriable SS del sistema ',SS])
                # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])
                # # input()    
                
            #Caso 2
            if t1<ta and t1 <=t2:
                # log('Entro en caso 2')
                t=t1
                # log(["Actual time ",t])
                D[SS[1]]=t
                log("Client #"+ str(SS[1])  + " gone at time: "+ str(t))
                n-=1
                cantDuranteTiempo.append((n,t))

                if SS[0]==1:
                    SS=[0]
                    t1=float('Infinity')
                
                elif SS[0]==2:
                    SS=[1,0,SS[2]]
                    t1=float('Infinity')
                else:
                    SS[0]-=1
                    temp=SS[3]
                    SS=[SS[0]]+[temp]+[SS[2]]+SS[4:len(SS)]

                    tipo = bernoulli(0.5)

                    if tipo ==0:
                        t1=t+uniforme(3,5)
                        timeInWait[SS[1]]=t        
                    else:        
                        t1=t+uniforme(5,8)
                        timeInWait[SS[1]]=t   

                # log("Caso 2 final")
                # log([t0,T])
                # log(['CAntidad de clientes en el sistema ',n])
                # log(['VAriable SS del sistema ',SS])
                # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])
                # input()

            #Caso 3
            if t2 < ta and t2 < t1:
                # log('Entro en caso 3')
                t=t2
                # log(["Actual time ",t])
                D[SS[2]]=t
                log("Client #"+ str(SS[2])  + " gone at time: "+ str(t))
                n-=1
                cantDuranteTiempo.append((n,t))

                # log("Caso 3 final")
                # log([t0,T])
                # log(['CAntidad de clientes en el sistema ',n])
                # log(['VAriable SS del sistema ',SS])
                # log([["ta ",ta],["t1 " ,t1],["t2  ",t2]])
                # log(D)
                # input()

                if SS[0]==1:
                    SS=[0]
                    t2=float('Infinity')
                
                elif SS[0]==2:
                    SS=[1,SS[1],0]
                    t2=float('Infinity')
                else:
                    SS[0]-=1
                    temp=SS[3]
                    SS=SS[0:2]+[temp]+SS[4:len(SS)]

                    tipo = bernoulli(0.5)

                    if tipo ==0:
                        t2=t+uniforme(3,5)
                        timeInWait[SS[2]]=t        
                    else:        
                        t2=t+uniforme(5,8)
                        timeInWait[SS[2]]=t         
                
    ###############################################Fin del cuerpo de la simulacion#####################################
    #################################################Calculos de salida para un dia#########################################
        # log(len(A))
        # log(len(D))

        # log(A)
        # log(D)
        
        #tiempo que pasa en la cola cada cliente
        diferences=[]

        for p in range(1,nA+1):
            diferences.append(timeInWait[p]-A[p])

        eficiencia=0
        moreThan5=[]
        for x in diferences: 
            if x<=5:
                moreThan5.append(x) 

        eficiencia = len(moreThan5)*100/nA


        mean_one_day=statistics.mean(diferences)
        means.append(mean_one_day)

        log("Mean: "+str(mean_one_day))
        log("Eficiencia: "+str(eficiencia))
        eficiencias.append(eficiencia)
        # print(i)
        if i>=30 and keep_going(eficiencias,k=i):
            dias+=1
        elif i>=30:
            log('Days simulated: '+str(dias))
            break         
        
        i+=1    
        # plt.plot(diferences,[x for x in range(len(diferences))])
        # plt.show()
        # plt.hist(diferences)
        # plt.plot([y for x,y in cantDuranteTiempo],[x for x,y in cantDuranteTiempo])
        # plt.plot([x for x in diferences])
        
        # plt.subplot(2,1,1)
        # plt.show()
    #################################################Fin de la simulacion total para un dia#####################################
    
    log('Mean of waiting time: '+ str(statistics.mean(means)))
    log('Mean of percent of efficienci: '+ str(statistics.mean(eficiencias)))

    print(dias)
    plt.plot(range(1,dias+1),eficiencias)
    plt.show()    







def keep_going(sample,d=1,k=31):
    """Metodo para saber cuantas simulaciones tengo que hacer para estimar el 
    parametro con el error que quiero """
    log(sample)
    if (statistics.stdev(sample)/math.sqrt(k))>= d:
        return True
    return False    


def log(string):
	logging.debug(str(string))
def log_i(string):
	logging.info(str(string))

if __name__ == "__main__":
    simula_kujos()
    print ("TErmine")