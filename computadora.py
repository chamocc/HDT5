# -*- coding: cp1252 -*-
#Daniel Gerendas 13158
#Edgar Chamo 13083
import simpy
import random
import math

RANDOM_SEED = 42
NUEVOS_PROCESOS = 25
INTERVALO_PROCESOS = 3.0
global TIEMPO_PROCESO #tiempo que dedica el CPU a cada proceso
TIEMPO_PROCESO = 2
global TIEMPO_IO 
TIEMPO_IO = 3
global INSTRUCCIONES_MAX 
INSTRUCCIONES_MAX = 10
global MEMORIA_MAX
MEMORIA_MAX=10
global tiempoTot
tiempoTot=0


def proceso(env, nombre, CPU, memoriaRAM, inputOutput, memoria, instrucciones):
    global TIEMPO_PROCESO
    global TIEMPO_IO
    global tiempoTot
    #Se crea un nuevo proceso
    creacion = env.now #se marca el momento en el que se crea el proceso
    print('%s se creo a las %s unidades de tiempo' % (nombre, creacion))
    with memoriaRAM.get(memoria) as req:
        yield req
        ready=env.now
        print('%s paso a ready en %s' % (nombre,ready))
        
        while(instrucciones>0):
            with CPU.request() as req1:
                yield req1
                procesando=env.now
                print ('empezando a procesar %s en %s' % (nombre, procesando))
                yield env.timeout(TIEMPO_PROCESO)
                procesando=env.now
                print ('termino de procesar %s en %s' % (nombre, procesando))

                if (instrucciones-3)<0:
                    terminated=env.now
                    tiempoProceso=terminated-creacion
                    tiempoTot=tiempoTot +tiempoProceso
                    print('%s termino en %s' % (nombre, terminated))
                    memoriaRAM.put(memoria)
                    instrucciones=0
                else:
                    instrucciones=instrucciones-3
                    if random.randint(0,1)== 0:
                        with inputOutput.request() as req2:
                            yield req2
                            print(' %s empezo proceso I/O en %s' % (nombre, env.now))
                            tib = random.randint(1, TIEMPO_IO)
                            yield env.timeout(tib)
                            print(' %s termino proceso I/O en %s' % (nombre, env.now))
                    
def source(env, numero, intervalo, CPU, inputOutput, memoriaRAM):
    global INSTRUCCIONES_MAX 
    global MEMORIA_MAX
    for i in range(numero):
        p= proceso(env, 'proceso %s' % i, CPU, memoriaRAM, inputOutput, random.randint(1,MEMORIA_MAX), random.randint(1,INSTRUCCIONES_MAX)) 
        env.process(p)
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)

random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
CPU = simpy.Resource(env, capacity=1)
inputOutput = simpy.Resource(env, capacity=1)
memoriaRAM =simpy.Container(env, 10000, init=10000)
env.process(source(env, NUEVOS_PROCESOS, INTERVALO_PROCESOS, CPU, inputOutput, memoriaRAM))
env.run()

promedio=tiempoTot/NUEVOS_PROCESOS


print('=====================================================')
print('La computadora se tardó %s unidades de tiempo en terminar la cola de procesos' % (tiempoTot))
print ('El promedio de tiempo por operacion es de: %s unidades de tiempo' % (promedio))
print('=====================================================')
