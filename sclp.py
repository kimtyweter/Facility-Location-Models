import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from itertools import product

# Parameter
# Fixed cost
f = 1
# distance
c = 2.5
# Transportation cost
df_dis = pd.read_excel('10node.xlsx', 'Distance')
df_dis = df_dis.iloc[:,1:]

# aij
aij = {(customer, facility): 1 if df_dis.iloc[customer, facility] <= c else 0
            for customer in range(0, 10)
            for facility in range(0, 10)}

m = gp.Model("SCLP")

# Decision variables: facilities open or close
fact = m.addVars(10, vtype = GRB.BINARY, name='fact')

# Constraints
m.addConstrs((gp.quicksum(aij[(customer, facility)] * fact[facility] for facility in range(0, 10)) >= 1 
              for customer in range(0, 10)), name='coverage')

# Objective
obj = gp.quicksum(f * fact[facility] for facility in range(0, 10))
m.setObjective(obj, GRB.MINIMIZE)

m.optimize()

# display optimal values of decision variables
for facility in fact.keys():
    if (abs(fact[facility].x) > 1e-6):
        print(f"\n Build a factory at location {facility + 1}.")