import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from itertools import product

# Demand
df_demand = pd.read_excel('10node.xlsx', 'Customer')
df_demand = df_demand['Demand'].tolist()
df_demand


# Fixed cost
f = 200

# Transportation cost
df_dis = pd.read_excel('10node.xlsx', 'Distance')
df_dis = df_dis.iloc[:,1:]

# transportation cost

shipping_cost = {(customer, facility): df_dis.iloc[customer, facility] * 10
            for customer in range(0, 10)
            for facility in range(0, 10)}

print("Number of viable pairings: {0}".format(len(shipping_cost.keys())))


m = gp.Model("Facility location")

# Decision variables: facilities open or close
fact = m.addVars(10, vtype=GRB.BINARY, name='fact')

# Decision variables: assign customer clusters to a facility location
cartesian_prod = list(product(range(0, 10), range(0, 10)))
cust = m.addVars(cartesian_prod, lb = 0 ,vtype = GRB.CONTINUOUS, name='cust')

print(shipping_cost[0,1])

# Objective Function
# Minimize total cost
m.setObjective(gp.quicksum(df_demand[customer] * shipping_cost[customer, facility] * cust[customer, facility] for customer in range(0, 10) for facility in range(0, len(fact))) + gp.quicksum(fact[facility] for facility in range(0, len(fact))) * 200 , GRB.MINIMIZE)

# Constration
# 1. 
m.addConstrs((gp.quicksum(cust[(customer, facility)] for facility in range(0, 10)) == 1 for customer in range(0, 10)), name='Demand')

# 2.
m.addConstrs((cust[customer, facility] <= fact[facility] for customer, facility in cartesian_prod), name='Setup2ship')

##### Solver ##### 
m.optimize()
##### ##### ##### 

# display optimal values of decision variables

for facility in fact.keys():
    if (abs(fact[facility].x) > 1e-6):
        print(f"\n Build a factory at location {facility + 1}.")