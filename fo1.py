from pulp import LpMinimize, LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

costo = LpProblem("Minimizar_Costo", LpMinimize)
beneficios = LpProblem("maximizar_Ganancias", LpMaximize)