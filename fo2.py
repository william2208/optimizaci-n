from pulp import LpMinimize, LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD
max_ganancias = LpProblem('Maximizar_Ganancias',LpMaximize)

precios_venta = [2000,3000,4000,5000,6000,7000,8000]
"""
preferencias = [
    [0.65,0.26,0.09], #gusanos
    [0.65, 0.21,0.14], #aros
    [0.44,0.28,0.28], #tiburones
    [0.42,0.18,0.40]  #banderitas
]
"""
demanda = [
    [0.18, 0.26, 0.39, 0.17,0,0,0], #Tipo 1
    [0.34,0.39,0.21,0.06,0,0,0], #Tipo 2
    [0.1,0.23,0.39,0.22,0.03,0.03,0] #Tipo 3
]


#CREACIÓN DE VARIABLES
variables = []
#count = 0
for tau in range(len(demanda)):
    tipo = []
    for p in range(len(demanda[tau])):
        Xtk = LpVariable(f'Cantidad_Tipo{tau+1}_Precio{p+1}',lowBound=0)
        tipo.append(Xtk)
    #print(*tipo)
    #count += len(tipo)
    variables.append(tipo)

#CREACION DE LA FO
Z = []
for tau in range(len(demanda)):
    holder = []
    for p in range(len(demanda[tau])):
        Ctp = demanda[tau][p]
        Rp = precios_venta[p]
        Xtp = variables[tau][p]
        termino = (Ctp,Rp,Xtp)
        holder.append(termino)
    #print(*holder)
    Z.append(holder)

operations = []
for tau in range(len(Z)):
    operation = [Ctp * Rp * Xtp for Ctp,Rp,Xtp in Z[tau]]
    operations.append(operation)
    #for p in range(len(Z[tau])):
fo = lpSum(operations)
#print(fo)
#Añadimos fo
max_ganancias += fo

#CREACIÓN DE RESTRICCIONES

#GEQ
restricciones = []
for tau in range(len(variables)):
    tipo = lpSum(variables[tau])
    r = (tipo >= 5)
    print(r)
    restricciones.append(r)

for tau in range(len(variables)):
    tipo = lpSum(variables[tau])
    r = (tipo <= 25)
    print(r)
    restricciones.append(r)

for restriccion in restricciones:
    max_ganancias += restriccion

max_ganancias.solve()

print(f'Solucion: {max_ganancias.objective.value()}')
for tipo in variables:
    for precio in tipo:
        print(precio.name, precio.varValue)