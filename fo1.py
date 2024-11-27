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
cantidades = {1:4, 2:1, 3:1, 4:1, 5:4, 6:2, 7:2}


#print(precios_unitarios)

#Creación de variables
variables = []
for i in range(len(precios_unitarios)):
    distribuidor = precios_unitarios[i]
    #print(len(distribuidor))
    holder_distribuidor = []
    for j in range(len(distribuidor)):
        #print(distribuidor[j])
        Yij = LpVariable(f'{nombres[j+1]} del proveedor {i+1}', lowBound=0)
        holder_distribuidor.append(Yij)
    variables.append(holder_distribuidor)
print("##################### \nCREACIÓN DE VARIABLES \n#####################")
for i in range(len(variables)):
    distribuidor = variables[i]
    print(f"Distribuidor {i+1}:")
    print(*distribuidor)
    print("\n")

#CREACIÓN DE FO:
print("##################### \nFUNCIÓN OBJETIVO \n#####################")
Z = []
for i in range(len(precios_unitarios)):
    distribuidor = precios_unitarios[i]
    cantidad = variables[i]
    #print(f'Cantidad {i}: {cantidad}')
    #print(len(cantidad),len(distribuidor))
    holder = list(zip(distribuidor,cantidad))
    #print(f'Con Coeficientes: \n {list(holder)}')
    operation = lpSum([float(sigma) * y for sigma, y in holder])
    Z.append(operation)
    
fo = lpSum(Z)
costo += fo
print(f'Min: \n {fo}')
#CREACIÓN DE RESTRICCIONES
print("##################### \nRESTRICCIONES \n#####################")
#Restricción cantidades de producto
print("-> Restricciones por cantidad de producto: \n")
productos = [[] for _ in range(len(cantidades))]
for i in range(len(variables)):
    distribuidor = variables[i]
    for j in range(len(distribuidor)):
        productos[j].append(distribuidor[j])

restricciones = []
for i in range(len(productos)):
    producto = productos[i]
    r = (lpSum(producto) == cantidades[i+1])
    restricciones.append(r)
    print(r)

#print(*restricciones)
"""print(*productos)
print(len(variables[0]))
print(len(restricciones))"""

#Restricción de presupuesto
print("\n-> Restricción de presupuesto: \n")
budget = []
for i in range(len(precios_unitarios)):
    distribuidor = precios_unitarios[i]
    cantidad = variables[i]
    #print(f'Cantidad {i}: {cantidad}')
    #print(len(cantidad),len(distribuidor))
    holder = list(zip(distribuidor,cantidad))
    recepy = []
    for i in range(len(holder)):
        if i == 0 or i in range(4,7):
            recepy.append(holder[i])
    operation = [float(sigma) * Y for sigma,Y in recepy]
    budget.append(operation)
    
#print(*budget)
presupuesto = (lpSum(budget) <= 2500)
print(presupuesto)  
restricciones.append(presupuesto)

#Añadir restricciones
for resitriccion in restricciones:
    costo += resitriccion

costo.solve(PULP_CBC_CMD(msg=False))

for distribuidor in variables:
    for var in distribuidor:
        print(var.name, var.varValue)
print(costo.objective.value())


