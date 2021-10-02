from gurobipy import *

import pandas as pd
import math
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Mydata\Discrete optimization course\assignment_4\tsp\data\tsp_85900_1", header = None)

num_node = int(df[0][0])
df = df.iloc[1:]

df= df[0].str.split(" ", expand=True)

df[0] = df[0].astype('float')
df[1] = df[1].astype('float')

co_ord = {}

for i in range(len(df)):
    co_ord.update({i:[df.iloc[i][0], df.iloc[i][1]]})

def dist(node1, node2):
    x_diff = co_ord[node1][0] - co_ord[node2][0]
    y_diff = co_ord[node1][1] - co_ord[node2][1]

    d = math.sqrt(((x_diff)**2)+((y_diff)**2))

    return d


def subtourelim(model, where):
    if where == GRB.callback.MIPSOL:

        selected = []
        # for i in range(n):
        sol = model.cbGetSolution(model._x)
        selected = tuplelist((i, j) for i, j in model._x.keys() if sol[i, j] > 0.5)
        adjList = [[] for i in range(num_node)]
        for i, j in selected:
            adjList[i].append(j)
        # find the shortest cycle in the selected edge list
        components = subtour(adjList)
        print(components)
        count = 0
        if len(components) > 1:
            # add a subtour elimination constraint
            for component in components:

                if len(component) >= 2:
                    count += 1
            if count > 1:
                for component in components:
                    if (len(component) >= 2):
                        print('Add constraint for component: {}'.format(component))
                        m.cbLazy(
                            quicksum(x[i, j] for i in component for j in component if i != j) <= len(component) - 1)


def subtour(adjList):
    discover = [0 for i in range(num_node)]
    components = []
    for i in range(num_node):
        component = []
        queue = []
        if discover[i] == 0:
            discover[i] = 1
            component.append(i)
            queue.append(i)
            while queue:
                v = queue.pop(0)
                for u in adjList[v]:
                    if discover[u] == 0:
                        discover[u] = 1
                        component.append(u)
                        queue.append(u)
            components.append(component)
    return components

m=Model()

x={}
for i in range(num_node):
    for j in range( num_node):
        x[i,j] = m.addVar(vtype=GRB.BINARY, name='x'+"_"+str(i)+"_"+str(j))

z={}
z=m.addVar(vtype=GRB.CONTINUOUS, name='z', obj=1)

m.update()

m.addConstr(quicksum(x[i,j]*dist(i,j) for i in range(num_node) for j in range(num_node))<=z)

for i in range(num_node):
    m.addConstr(quicksum(x[i,j] for j in range(num_node) if i!=j)==1)

for j in range(0, num_node):
    m.addConstr(quicksum(x[i,j] for i in range(num_node) if i!=j)==1)

for i in range(num_node):
    for j in range(num_node):
        if i==j:
            m.addConstr(x[i, j]==0)

for i in range(num_node):
    for j in range(num_node):
        m.addConstr(x[i,j]+x[j,i]<=1)

# for i in range(num_node):
#     for j in range(num_node):
#         m.addConstr(x[i,j]==x[j,i])


m._x=x
m.params.LazyConstraints = 1
m.modelsense = GRB.MINIMIZE
#m.optimize()
m.optimize(subtourelim)



edges = []
for i in range(num_node):
    for j in range(num_node):
        if x[i,j].x>0.5:
            edges.append([i,j])

for edge in edges:
    plt.plot([co_ord[edge[0]][0], co_ord[edge[1]][0]], [co_ord[edge[0]][1], co_ord[edge[1]][1]], 'ro-')
    #plt.arrow(co_ord[edge[0]][0], co_ord[edge[0]][1] ,co_ord[edge[1]][0], co_ord[edge[1]][1])

for node in range(num_node):
    plt.plot(co_ord[node][0], co_ord[node][1], 'ro', label=str(i))

plt.show()





