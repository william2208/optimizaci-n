from pulp import LpMinimize, LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD
import csv


costo = LpProblem("Minimizar_Costo", LpMinimize)
lista_precios = 'optimizaci-n\lista_precios.csv'
with open(lista_precios, mode = 'r', encoding = 'utf-8') as file:
    csv_reader = csv.reader(file, delimiter=';', quotechar='"')
    precios_unitarios = [row for row in csv_reader if row[1] == 'U']
    """for row in csv_reader:
        print(row)"""
    
#filtro de columnas necesarias
for i in range(len(precios_unitarios)):
    distribuidor = precios_unitarios[i][2:]
    precios_unitarios[i] = distribuidor



#Cantidad de producto
nombres = {
    1:'Gusanos', #usado en cantidades
    2:'Empaque',
    3:'Chamoy',
    4:'Tajín',
    5:'Aritos', #usado en cantidades
    6:'Tiburón', #usado en cantidades
    7:'Banderitas' #usado en cantidades
}
cantidades = {1:4, 5:4, 6:2, 7:2}


#print(precios_unitarios)

#Creación de variables
variables = []
for i in range(len(precios_unitarios)):
    distribuidor = precios_unitarios[i]
    #print(len(distribuidor))
    holder_distribuidor = []
    for j in range(1,len(distribuidor)):
        #print(distribuidor[j])
        Yij = LpVariable(f'{nombres[j]} del proveedor {i+1}', lowBound=0)
        holder_distribuidor.append(Yij)
    variables.append(holder_distribuidor)

"""for distribuidor in variables:
    print(*distribuidor)"""

#CREACIÓN DE FO:

for i in range(len(precios_unitarios)):
    distribuidor = precios_unitarios[i]
    cantidad = variables[i]
    operation = lpSum([float(sigma) * y for sigma, y in zip(distribuidor,cantidad)])
    print(operation)
    costo += operation

#CREACIÓN DE RESTRICCIONES



