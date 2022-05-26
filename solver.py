#!/usr/bin/env python
# coding: utf-8

#        Yu-Heng Chien 132005200

# # 8.2

#     (a) Optimal locations: 1, 2, 3, 4, 5, 7, 8 and 9

#     (b) Optimal cost: 1940

# # 8.8

#     Optimal locations: 1, 2, 5, 6, 7 and 9

# # 8.9

#     (a) Optimal locations: 1, 3, 5 and 6

#     (b) Total number of demands covered: 367

# # 8.19

#     (a) Bethlehem and Springfield

#     (b) 
#     Akron is from Bethlehem
#     Albany is from Springfield
#     Nasuha is from Springfield
#     Scranton is from Bethlehem
#     Utica is from Springfield

#     (c) 16265000

# # Calculation

# In[958]:


import pandas as pd



# ### 8.2

# In[1217]:


import gurobipy as gp
from gurobipy import GRB



# In[1218]:


# Demand
df_demand = pd.read_excel('10node.xlsx', 'Customer')
df_demand = df_demand['Demand'].tolist()
df_demand


# In[1219]:


# Fixed cost
f = 200


# In[1220]:


# Transportation cost
df_dis = pd.read_excel('10node.xlsx', 'Distance')
df_dis = df_dis.iloc[:,1:]
df_dis


# In[1221]:


# transportation cost

shipping_cost = {(customer, facility): df_dis.iloc[customer, facility] * 10
            for customer in range(0, 10)
            for facility in range(0, 10)}

print("Number of viable pairings: {0}".format(len(shipping_cost.keys())))


# In[1222]:


m = gp.Model("Facility location")


# In[1223]:


# Decision variables: facilities open or close
fact = m.addVars(10, vtype=GRB.BINARY, name='fact')


# In[1224]:


# Decision variables: assign customer clusters to a facility location
cartesian_prod = list(product(range(0, 10), range(0, 10)))
cust = m.addVars(cartesian_prod, lb = 0 ,vtype = GRB.CONTINUOUS, name='cust')


# In[1225]:


# Deploy Objective Function
# Minimize total cost
# obj = gp.quicksum(f * fact[facility] + df_demand[customer] * cust[customer, facility] * shipping_cost[customer, facility] for customer, facility in shipping_cost.keys())
m.setObjective(gp.quicksum(df_demand[customer] * shipping_cost[customer, facility] * cust[customer, facility] for customer in range(0, 10) for facility in range(0, len(fact))) + gp.quicksum(fact[facility] for facility in range(0, len(fact))) * 200 , GRB.MINIMIZE)

# 1. 
m.addConstrs((gp.quicksum(cust[(customer, facility)] for facility in range(0, 10)) == 1 for customer in range(0, 10)), name='Demand')

# 2.
m.addConstrs((cust[customer, facility] <= fact[facility] for customer, facility in cartesian_prod), name='Setup2ship')

m.optimize()


# In[1226]:


# display optimal values of decision variables

for facility in fact.keys():
    if (abs(fact[facility].x) > 1e-6):
        print(f"\n Build a factory at location {facility + 1}.")


# ### 8.8

# In[1235]:


# Parameter
# Fixed cost
f = 1
# distance
c = 2.5


# In[1236]:


# aij
aij = {(customer, facility): 1 if df_dis.iloc[customer, facility] <= c else 0
            for customer in range(0, 10)
            for facility in range(0, 10)}

print("Number of viable pairings: {0}".format(len(pairings.keys())))


# In[1237]:


m = gp.Model("8.8 SCLP")


# In[1238]:


# Decision variables: facilities open or close
fact = m.addVars(10, vtype = GRB.BINARY, name='fact')
fact


# In[1239]:


# 1. 
m.addConstrs((gp.quicksum(aij[(customer, facility)] * fact[facility] for facility in range(0, 10)) >= 1 
              for customer in range(0, 10)), name='coverage')


# In[1240]:


obj = gp.quicksum(f * fact[facility] for facility in range(0, 10))
m.setObjective(obj, GRB.MINIMIZE)


# In[1241]:


m.optimize()


# In[1242]:


# display optimal values of decision variables

for facility in fact.keys():
    if (abs(fact[facility].x) > 1e-6):
        print(f"\n Build a factory at location {facility + 1}.")


# ### 8.9

# In[1206]:


p = 4
c = 2.5


# In[1207]:


# demand
df_demand


# In[1208]:


# aij
aij = {(customer, facility): 1 if df_dis.iloc[customer, facility] <= c else 0
            for customer in range(0, 10)
            for facility in range(0, 10)}

print("Number of viable pairings: {0}".format(len(pairings.keys())))


# In[1209]:


# Decision variables: facilities open or close
fact = m.addVars(10, vtype = GRB.BINARY, name='fact')
fact


# In[1210]:


z = m.addVars(10, vtype = GRB.BINARY, name='demand')
z


# In[1211]:


# constraint
m.addConstrs((gp.quicksum(aij[(customer, facility)] * fact[facility] for facility in range(0, 10)) >= z[customer] 
              for customer in range(0, 10)), name='coverage')


# In[1212]:


# constraint
m.addConstr((gp.quicksum(fact[facility] for facility in range(0, 10)) == p) , name='coverage')


# In[1213]:


obj = gp.quicksum(z[customer] * df_demand[customer] for customer in range(0, 10))
m.setObjective(obj, GRB.MAXIMIZE)


# In[1214]:


m.optimize()


# In[1215]:


# display optimal values of decision variables

for facility in fact.keys():
    if (abs(fact[facility].x) > 1e-6):
        print(f"\n Build a warehouse at location {facility + 1}.")


# ### 8.19

# In[1244]:


place = ['Akron', 'Albany',  'Nasuha', 'Scranton', 'Utica']
h = [1200000, 1150000, 1350000, 1800000, 900000]
fact = ['Bethlehem', 'Pittsburgh', 'Rochester', 'Springfield']


# In[1245]:


f = [4000000, 7500000, 4500000, 5200000]
cap = [3300000, 4800000, 4200000, 3750000]


# In[1246]:


# Decision variables: facilities open or close
x = m.addVars(len(fact), vtype = GRB.BINARY, name='factility')


# In[1247]:


cartesian_prod = list(product(range(0, len(place)), range(0, len(fact))))
y = m.addVars(cartesian_prod, lb = 0 ,vtype = GRB.CONTINUOUS, name='custnomer friction')


# In[1248]:


transp_cost = [[2.2, 1.6, 3.2, 0.8, 1.6], [1.8, 3.2, 4, 2.1, 2.4], [2.7, 1.2, 2.5, 1.4, 0.7], 
               [3.8, 0.6, 0.7, 1.3, 1.5]]


# In[1249]:


df_transp_cost = pd.DataFrame(transp_cost, columns = place)
df_transp_cost


# In[1250]:


c = {(customer, facility): df_transp_cost.iloc[facility, customer]
            for customer in range(0, len(place))
            for facility in range(0, len(fact))}


# In[1251]:


# constraint
m.addConstrs((gp.quicksum(y[(customer, facility)] for facility in range(0, len(fact))) == 1 
              for customer in range(0, len(place))), name='1')


# In[1252]:


m.addConstrs((y[customer, facility] <= x[facility] for customer in range(0, len(place)) 
              for facility in range(0, len(fact))), name='2')


# In[1253]:


m.addConstrs((gp.quicksum(y[(customer, facility)] * h[customer] for customer in range(0, len(place))) <= cap[facility] 
              for facility in range(0, len(fact))), name='3')


# In[1254]:


# Objection
# obj = gp.quicksum(f[facility] * x[facility] + h[customer] * c[customer, facility] * y[customer, facility] for facility in range(0, len(fact)) for customer in range(0, len(place)))
m.setObjective(gp.quicksum(h[customer] * c[customer, facility] * y[customer, facility] 
                           for customer in range(0, len(place)) for facility in range(0, len(fact))) 
               + gp.quicksum(f[facility] * x[facility] for facility in range(0, len(fact))) , GRB.MINIMIZE)


# In[1255]:


m.optimize()


# In[1259]:


for facility in x.keys():
    if (abs(x[facility].x) > 1e-6):
        print(fact[facility])


# In[1261]:


for customer, facility in cartesian_prod:
    if (abs(y[customer, facility].x) > 1e-6):
        print(place[customer], 'is from', fact[facility])

