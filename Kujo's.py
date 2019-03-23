from generadores import *
import logging
import math
import matplotlib.pyplot as plt
import statistics

logging.basicConfig(format='Kojo\'s Cocina %(levelname)s system: %(message)s', level=logging.INFO)



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



# eficiencia_=[]


def simula_kujos(eficiencia_=[],dias=30,cooks=3):
    """Metodo que simula dias en la cocina del kojo para dos cocineros """
    log_info("Simulating Kojo's Kitchen with "+ str(cooks)+" cooks")
    means=[]
    means_of_number_of_customers=[]
    n1=0
    sandwisheros=[]
    eficiencias=[]
    i=1
    
    while i <= dias:
        
    ####################################################Inicializacion##########################################
        #Variables del sistema
        nA=0
        t0=intervals[0]['start']
        T=intervals[4]['end']
        SS=[0]


        #variables de salida 
        A=[0] # A[i]  es tiempo de llegada del cliente i
        D={} # D[i] es tiempo de salida del cliente i
            
        #lista de eventos
        t=0
        n=0
        SS=[0]
        ti=[float('Infinity')]*cooks
        ta=t0
        timeInWait={}
        cantDuranteTiempo=[]
    #################################################Fin de la Inicializacion####################################
    #################################################Cuerpo de la Simulacion#####################################

        
        while n!=0   or  t<T:
            
            #Caso Llegada
            if ta == min([ta]+ti):
                                
                if ta != float('Infinity'):
                    t=ta
                    log("New client #"+ str(nA+1)  + " at time: "+ str(t))
                    
                nA=nA+1
                n+=1
                cantDuranteTiempo.append((n,t))
               
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

                cook_ready=cook_ocupied(ti)

                if SS==[0]:
                    tem=[0]*(cooks-1)
                    SS=[1,nA]+tem
                    
                    if tipo ==0:
                        ti[0]=t+uniforme(3,5)
                        timeInWait[nA]=t        
                        
                    else:        
                        ti[0]=t+uniforme(5,8)    
                        timeInWait[nA]=t
                elif cook_ready!=-1 :
                    
                    SS[0]+=1
                    SS[cook_ready+1]=nA

                    if tipo ==0:
                        ti[cook_ready]=t+uniforme(3,5)
                        timeInWait[nA]=t   
                        n1+=1     
                    else:        
                        ti[cook_ready]=t+uniforme(5,8)
                        timeInWait[nA]=t    

                else:
                    SS[0]+=1
                    SS.append(nA)

                                
            #Caso 1

            if ti[0]==min([ta]+ti) and (ti[0]<=T or (ti[0]>T and n>0)):
                # log('Entro en caso 2')
                t=ti[0]
                # log(["Actual time ",t])
                #SS[1] porque esa posicion pernetence al cook ti[0] asi para cada posicion de SS .. example SS[i] pertenece al cook ti[i-1]
                D[SS[1]]=t
                log("Client #"+ str(SS[1])  + " gone at time: "+ str(t))
                n-=1
                cantDuranteTiempo.append((n,t))

                if SS[0]==1:
                    SS=[0]
                    ti[0]=float('Infinity')
                
                elif SS[0]<=len(ti):
                    SS[0]-=1
                    SS[1]=0
                    ti[0]=float('Infinity')
                else:
                    SS[0]-=1
                    temp=SS[len(ti)+1]

                    SS=[SS[0]]+[temp]+SS[2:len(ti)+1]+SS[len(ti)+2:len(SS)]

                    tipo = bernoulli(0.5)

                    if tipo ==0:
                        ti[0]=t+uniforme(3,5)
                        timeInWait[SS[1]]=t        
                        n1+=1
                    else:        
                        ti[0]=t+uniforme(5,8)
                        timeInWait[SS[1]]=t   
            
            #Caso 2
            if ti[1]==min([ta]+ti) and (ti[1]<=T or (ti[1]>T and n>0)):
                t=ti[1]
                
                D[SS[2]]=t
                log("Client #"+ str(SS[2])  + " gone at time: "+ str(t))
                n-=1
                cantDuranteTiempo.append((n,t))

                if SS[0]==1:
                    SS=[0]
                    ti[1]=float('Infinity')
                
                elif SS[0]<=len(ti):
                    SS[0]-=1
                    SS[2]=0
                    ti[1]=float('Infinity')
                else:
                    SS[0]-=1
                    temp=SS[len(ti)+1]
                    SS=SS[0:2]+[temp]+SS[3:len(ti)+1]+SS[len(ti)+2:len(SS)]

                    tipo = bernoulli(0.5)

                    if tipo ==0:
                        ti[1]=t+uniforme(3,5)
                        timeInWait[SS[2]]=t        
                        n1+=1
                    else:        
                        ti[1]=t+uniforme(5,8)
                        timeInWait[SS[2]]=t   

            if cooks==3:
                #Caso 3
                if ti[2]==min([ta]+ti) and (ti[2]<=T or (ti[2]>T and n>0)):
                    t=ti[2]
                    
                    #SS[1] porque esa posicion pernetence al cook ti[0] asi para cada posicion de SS .. example SS[i] pertenece al cook ti[i-1]
                    D[SS[3]]=t
                    log("Client #"+ str(SS[2])  + " gone at time: "+ str(t))
                    n-=1
                    cantDuranteTiempo.append((n,t))

                    if SS[0]==1:
                        SS=[0]
                        ti[2]=float('Infinity')
                    
                    elif SS[0]<=len(ti):
                        SS[0]-=1
                        SS[3]=0
                        ti[2]=float('Infinity')
                    else:
                        SS[0]-=1
                        temp=SS[len(ti)+1]
                        SS=SS[0:3]+[temp]+SS[4:len(ti)+1]+SS[len(ti)+2:len(SS)]

                        tipo = bernoulli(0.5)

                        if tipo ==0:
                            ti[2]=t+uniforme(3,5)
                            timeInWait[SS[3]]=t       
                            n1+=1 
                        else:        
                            ti[2]=t+uniforme(5,8)
                            timeInWait[SS[3]]=t   
                                 
    ###############################################Fin del cuerpo de la simulacion#####################################
    #################################################Calculos de salida para un dia#########################################
        
        #tiempo que pasa en la cola cada cliente
        diferences=[]
        sandwisheros.append(n1)
        n1=0

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
       
        means_of_number_of_customers.append(nA)

        if i>=30 and keep_going(eficiencias,k=i):
            dias+=1
        elif i>=30:
            log('Days simulated: '+str(dias))
            break         
        

        i+=1    
        
    #################################################Fin de la simulacion total para un dia#####################################
    
    log_info("Simulation finish with the following stats: ")
    log_info('-Mean of waiting time: '+ str(statistics.mean(means)))
    log_info('-Mean of percent of efficienci: '+ str(statistics.mean(eficiencias)))
    log_info('-Number of days simulated: '+str(dias))
    log_info('-Mean of the number of clients per day: '+str(statistics.mean(means_of_number_of_customers)))
    log_info('Have a nice day!!!\n')

    plt.plot(range(1,dias+1),eficiencias)
        
    





def cook_ocupied(cookss):
    """Saber si hay al menos un cocinero disponible y cual"""
    for cook in cookss:
        
        if cook == float('Infinity'):
            log(cook)
            return cookss.index(cook)
   
    return -1    
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
def log_info(string):
    logging.info(string)

if __name__ == "__main__":
    # simula_kujos()
    simula_kujos(cooks=2)
    simula_kujos()

    # plt.plot(range(efi[0][0]),efi[0][1])
    # plt.show()