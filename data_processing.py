
import math
import pandas as pd
import matplotlib.pyplot as plt

def read_coordinates(file_path):
    df = pd.read_csv(file_path, header=None)

    num_node = int(df[0][0])
    df = df.iloc[1:]

    df = df[0].str.split(" ", expand=True)

    df[0] = df[0].astype('float')
    df[1] = df[1].astype('float')

    co_ord = {}

    for i in range(len(df)):
        co_ord.update({i: [df.iloc[i][0], df.iloc[i][1]]})

    return num_node, co_ord

def dist(node1, node2, co_ord):
    x_diff = co_ord[node1][0] - co_ord[node2][0]
    y_diff = co_ord[node1][1] - co_ord[node2][1]

    d = math.sqrt(((x_diff)**2)+((y_diff)**2))

    return d

def path_plotting(edges, co_ord, num_node):
    for edge in edges:
        plt.plot([co_ord[edge[0]][0], co_ord[edge[1]][0]], [co_ord[edge[0]][1], co_ord[edge[1]][1]], 'ro-')
        # plt.arrow(co_ord[edge[0]][0], co_ord[edge[0]][1] ,co_ord[edge[1]][0], co_ord[edge[1]][1])

    for node in range(num_node):
        plt.plot(co_ord[node][0], co_ord[node][1], 'ro', label=str(node))

    plt.show()
