from src.generadores import *
import logging
import math
import matplotlib.pyplot as plt
import statistics

logging.basicConfig(format='Kojo\'s Cocina %(levelname)s system: %(message)s', level=logging.INFO)



intervals = [
				{
					'start':600, 
					'end':690,
					'arrival_interval':1/10
				},
				{
					'start':690, 
					'end':810,
                    'arrival_interval':1/1
				},
				{
					'start':810, 
					'end':1020,
                    'arrival_interval':1/9
				},
				{
					'start':1020, 
					'end':1140,
                    'arrival_interval':1/1
				},
				{
					'start':1140, 
					'end':1260,
                    'arrival_interval':1/8
				},
			]	
				


def simula_kujos(dias=30,cooks_fix=2, cooks_extras=3,lambd1=16,lambd2=2,lambd3=13,lambd4=3,lambd5=10):
    """Metodo que simula dias en la cocina del kojo para dos cocineros """
    log_info("Simulating Kojo's Kitchen with  cooks")
    means=[]
    means_of_number_of_customers=[]
    n1=0
    sandwisheros=[]
    eficiencias=[]
    i=1
    default=False
    if dias == 30:
        default=True

    intervals[0]['arrival_interval']=1/lambd1
    intervals[1]['arrival_interval']=1/lambd2
    intervals[2]['arrival_interval']=1/lambd3
    intervals[3]['arrival_interval']=1/lambd4
    intervals[4]['arrival_interval']=1/lambd5


    
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
        ti=[float('Infinity')]*cooks_extras
        ta=t0
        timeInWait={}
        cantDuranteTiempo=[]
        demand_interval=False
        # init=True
    #################################################Fin de la Inicializacion####################################
    #################################################Cuerpo de la Simulacion#####################################

        
        while n!=0   or  t<T:
            
            #Caso Llegada
            if ta == min([ta]+ti):
                                
                if ta != float('Infinity'):
                    t=ta
                    log("New client #"+ str(nA+1)  + " at time: "+ str(t))
                    # input()
                    
                nA=nA+1
                n+=1
                cantDuranteTiempo.append((n,t))
               
                if t >=intervals[0]['start'] and t < intervals[0]['end']: 
                    ta=t+exponencial(intervals[0]['arrival_interval'])
                    if(cooks_fix!=cooks_extras):
                        demand_interval=False
                elif t >=intervals[1]['start'] and t < intervals[1]['end']: 
                    ta=t+exponencial(intervals[1]['arrival_interval'])
                    if(cooks_fix!=cooks_extras):
                        demand_interval=True
                elif t >=intervals[2]['start'] and t < intervals[2]['end']: 
                    ta=t+exponencial(intervals[2]['arrival_interval'])
                    if(cooks_fix!=cooks_extras):
                        demand_interval=False
                elif t >=intervals[3]['start'] and t < intervals[3]['end']: 
                    ta=t+exponencial(intervals[3]['arrival_interval'])
                    if(cooks_fix!=cooks_extras):
                        demand_interval=True    
                else: 
                    ta=t+exponencial(intervals[4]['arrival_interval'])   
                    if(cooks_fix!=cooks_extras):
                        demand_interval=False     
                
                
                
                A.append(t)

                if ta >=T:
                    ta=float('Infinity')


                #Elegir que es lo que quiere el cliente que puede ser atendido 0:sandwish 1:sushi 
                tipo = bernoulli(0.5)

                cook_ready=cook_ocupied(ti ,cooks_fix,cooks_extras,inter=demand_interval)

                if SS==[0]:
                    tem=[0]*(cooks_extras-1)
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

            minimo=min([ta]+ti)
            if minimo!=ta:
                ind=ti.index(minimo)
                

                if (ti[ind]<=T or (ti[ind]>T and n>0)):
                    # log('Entro en caso 2')
                    t=ti[ind]
                    if(cooks_fix!=cooks_extras):
                        demand_interval=critic_time(t)
                    # log(["Actual time ",t])
                    #SS[1] porque esa posicion pernetence al cook ti[0] asi para cada posicion de SS .. example SS[i] pertenece al cook ti[i-1]
                    D[SS[ind+1]]=t
                    log("Client #"+ str(SS[ind+1])  + " gone at time: "+ str(t))
                    # input()
                    n-=1
                    cantDuranteTiempo.append((n,t))
                    

                    if SS[0]==1:
                        SS=[0]
                        ti[ind]=float('Infinity')
                    elif cooks_fix ==cooks_extras:
                        if SS[0]<=len(ti):
                            SS[0]-=1
                            SS[ind+1]=0
                            ti[ind]=float('Infinity')
                        else:
                            SS[0]-=1
                            temp=SS[len(ti)+1]

                            SS=SS[0:ind+1]+[temp]+SS[ind+2:len(ti)+1] + SS[len(ti)+2:len(SS)]
                            tipo = bernoulli(0.5)

                            if tipo ==0:
                                ti[ind]=t+uniforme(3,5)
                                timeInWait[SS[ind+1]]=t        
                                n1+=1
                            else:        
                                ti[ind]=t+uniforme(5,8)
                                timeInWait[SS[ind+1]]=t

                    elif demand_interval:
                        if SS[0]<=len(ti):
                            SS[0]-=1
                            SS[ind+1]=0
                            ti[ind]=float('Infinity')
                        else:
                            SS[0]-=1
                            temp=SS[len(ti)+1]

                            SS=SS[0:ind+1]+[temp]+SS[ind+2:len(ti)+1] + SS[len(ti)+2:len(SS)]

                            tipo = bernoulli(0.5)

                            if tipo ==0:
                                ti[ind]=t+uniforme(3,5)
                                timeInWait[SS[ind+1]]=t        
                                n1+=1
                            else:        
                                ti[ind]=t+uniforme(5,8)
                                timeInWait[SS[ind+1]]=t       

                    elif SS[0]<=len(ti)-1:
                            SS[0]-=1
                            SS[ind+1]=0
                            ti[ind]=float('Infinity')
                    elif SS[0]>=3 and two_off(ti,cooks_fix)  :
                        SS[0]-=1
                        SS[ind+1]=0
                        ti[ind]=float('Infinity')      
                    else:
                        SS[0]-=1

                        temp=SS[len(ti)+1]

                        SS=SS[0:ind+1]+[temp]+SS[ind+2:len(ti)+1] + SS[len(ti)+2:len(SS)]
                        tipo = bernoulli(0.5)

                        if tipo ==0:
                            ti[ind]=t+uniforme(3,5)
                            timeInWait[SS[ind+1]]=t        
                            n1+=1
                        else:        
                            ti[ind]=t+uniforme(5,8)
                            timeInWait[SS[ind+1]]=t   
                
            
                                 
    ###############################################Fin del cuerpo de la simulacion#####################################
    #################################################Calculos de salida para un dia#########################################
        
        #tiempo que pasa en la cola cada cliente
        diferences=[]
        sandwisheros.append(n1)
        n1=0

        for p in range(1,nA+1):
            diferences.append( timeInWait [p]-A[p])


        eficiencia=0
        moreThan5=[]
        for x in diferences: 
            if x>5:
                moreThan5.append(x) 

        eficiencia = len(moreThan5)*100/nA


        mean_one_day=statistics.mean(diferences)
        means.append(mean_one_day)

        log("Mean: "+str(mean_one_day))
        log("Eficiencia: "+str(eficiencia))
        eficiencias.append(eficiencia)
       
        means_of_number_of_customers.append(nA)

        if default:
            # log_info("Es el default")
            if i>=30 and keep_going(eficiencias,k=i):
                dias+=1
                # log_info("Aumente k")
            elif i>=30:
                log('Days simulated: '+str(dias))
                break         
        

        i+=1    
        
    #################################################Fin de la simulacion total para un dia#####################################
    
    log_info("Simulation finish with the following stats: ")
    log_info('-Mean of waiting time: '+ str(statistics.mean(means)))
    log_info('-Mean of percent of dissatisfied clients (more than 5 min): '+ str(statistics.mean(eficiencias)))
    log_info('-Number of days simulated: '+str(dias))
    log_info('-Mean of the number of clients per day: '+str(statistics.mean(means_of_number_of_customers)))
    log_info('Have a nice day!!!\n')

    plt.plot(range(1,dias+1),eficiencias)
        
    


def cook_ocupied(cookss,cooks_fix,cooks_extras,inter=False ):
    """Saber si hay al menos un cocinero disponible y cual"""
    c=0
    for cook in cookss:
        
        if cook == float('Infinity'):
            if not inter :
                return cookss.index(cook)
            log(cook)
            c+=1
            if  inter or c==cooks_fix: 
                return cookss.index(cook)
   
    return -1    
def keep_going(sample,d=1,k=31):
    """Metodo para saber cuantas simulaciones tengo que hacer para estimar el 
    parametro con el error que quiero """
    log(sample)
    if (statistics.stdev(sample)/math.sqrt(k))>= d:
        return True
    return False    
def critic_time(t):
    if t >=intervals[0]['start'] and t < intervals[0]['end']: 
        return False
    elif t >=intervals[1]['start'] and t < intervals[1]['end']: 
        return True
    elif t >=intervals[2]['start'] and t < intervals[2]['end']: 
        return False
    elif t >=intervals[3]['start'] and t < intervals[3]['end']: 
        return True    
    else: 
        return False  
def two_off(cookss,cook_fix):
    c=0
    for cook in cookss:
        
        if cook != float('Infinity'):
            log(cook)
            c+=1
    if c>=cook_fix+1:
        return True

    return  False   


def log(string):
	logging.debug(str(string))
def log_i(string):
	logging.info(str(string))
def log_info(string):
    logging.info(string)

# if __name__ == "__main__":
#     # simula_kujos()
#     cprint("Welcome to Kujo's Kitchen simulator",)
#     print("Please introduce the values of the times between clientes arrival for intervals, separated by white space:")
#     print("If you press enter the defaults will be loaded")
#     lamdas=input()
#     print("How many days do you want to simulate:")
#     print("If you press enter the defaults will be loaded")
#     days=30
#     try:
#         days =int(input())
#     except Exception as identifier:
#         days=30
        
    
#     params=[]
#     default=False
#     try:
#         for x in lamdas.split(' '):
#             params.append(int(x))
    
#     except Exception as identifier:
#         default=True
    
#     lenth=len(params)
#     if not default:
#         try:
#             lamdas1=params[0]
#             lamdas2=params[1]
#             lamdas3=params[2]
#             lamdas4=params[3]
#             lamdas5=params[4]
        
#         except Exception  as identifier:
#             print('Introduce the the five params')

        
        
#         simula_kujos(dias=days ,cooks=2,lambd1=lamdas1,lambd2=lamdas2,lambd3=lamdas3,lambd4=lamdas4,lambd5=lamdas5)
#         simula_kujos(dias=days, lambd1=lamdas1,lambd2=lamdas2,lambd3=lamdas3,lambd4=lamdas4,lambd5=lamdas5)
#     else:
#         simula_kujos(dias=days,cooks=2)
#         simula_kujos(dias=days,cooks=3)
#     # plt.plot(range(efi[0][0]),efi[0][1])
#     plt.show()