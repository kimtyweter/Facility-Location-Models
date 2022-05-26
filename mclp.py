import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from itertools import product

# Demand
df_demand = pd.read_excel('10node.xlsx', 'Customer')
df_demand = df_demand['Demand'].tolist()

# Parameters
p = 4 # covers number
c = 2.5 # covers distance

# Transportation cost
df_dis = pd.read_excel('10node.xlsx', 'Distance')
df_dis = df_dis.iloc[:,1:]

# Number of viable pairings
aij = {(customer, facility): 1 if df_dis.iloc[customer, facility] <= c else 0
            for customer in range(0, 10)
            for facility in range(0, 10)}

m = gp.Model("MCLP")

# Decision variables: facilities open or close
fact = m.addVars(10, vtype = GRB.BINARY, name='fact')
z = m.addVars(10, vtype = GRB.BINARY, name='demand')

# Objection
obj = gp.quicksum(z[customer] * df_demand[customer] for customer in range(0, 10))
m.setObjective(obj, GRB.MAXIMIZE)

# Constraints
m.addConstrs((gp.quicksum(aij[(customer, facility)] * fact[facility] for facility in range(0, 10)) >= z[customer] 
              for customer in range(0, 10)), name='coverage distance')
m.addConstr((gp.quicksum(fact[facility] for facility in range(0, 10)) == p) , name='coverage number')

m.optimize()

# Display optimal values of decision variables

for facility in fact.keys():
    if (abs(fact[facility].x) > 1e-6):
        print(f"\n Build a warehouse at location {facility + 1}.")