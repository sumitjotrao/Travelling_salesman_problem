from gurobipy import *

from data_processing import dist

class integer_program:

    def __init__(self, num_node, co_ord):

        self.num_node = num_node
        self.x = {}
        self.z = {}
        self.co_ord = co_ord


    def subtour(self, adjList):
        discover = [0 for i in range(self.num_node)]
        components = []
        for i in range(self.num_node):
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

    def build_model(self):

        def subtourelim(model, where):

            if where == GRB.callback.MIPSOL:
                selected = []
                sol = model.cbGetSolution(model._x)
                selected = tuplelist((i, j) for i, j in model._x.keys() if sol[i, j] > 0.5)
                adjList = [[] for i in range(self.num_node)]

                for i, j in selected:
                    adjList[i].append(j)

                components = self.subtour(adjList)
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
                                model.cbLazy(
                                    quicksum(self.x[i, j] for i in component for j in component if i != j) <= len(
                                        component) - 1)
        m = Model()

        for i in range(self.num_node):
            for j in range(self.num_node):
                self.x[i, j] = m.addVar(vtype=GRB.BINARY, name='x' + "_" + str(i) + "_" + str(j))

        self.z = m.addVar(vtype=GRB.CONTINUOUS, name='z', obj=1)

        m.update()

        m.addConstr(quicksum(self.x[i, j] * dist(i, j, self.co_ord) for i in range(self.num_node) for j in range(self.num_node)) <= self.z)

        for i in range(self.num_node):
            m.addConstr(quicksum(self.x[i, j] for j in range(self.num_node) if i != j) == 1)

        for j in range(0, self.num_node):
            m.addConstr(quicksum(self.x[i, j] for i in range(self.num_node) if i != j) == 1)

        for i in range(self.num_node):
            for j in range(self.num_node):
                if i == j:
                    m.addConstr(self.x[i, j] == 0)

        for i in range(self.num_node):
            for j in range(self.num_node):
                m.addConstr(self.x[i, j] + self.x[j, i] <= 1)

        m._x = self.x
        m.params.LazyConstraints = 1
        m.modelsense = GRB.MINIMIZE
        # m.optimize()
        m.optimize(subtourelim)
        edges = []
        for i in range(self.num_node):
            for j in range(self.num_node):
                if self.x[i, j].x > 0.5:
                    edges.append([i, j])
        obj = m.getObjective()

        return edges, obj.getValue()
