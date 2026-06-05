import csv
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

# bacacsv

graph = {}

with open("friends.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        parent = row[0].strip()

        if parent not in graph:
            graph[parent] = []

        for child in row[1:]:
            child = child.strip()

            if child != "":
                if child not in graph:
                    graph[child] = []

                # graph dua arah
                graph[parent].append(child)
                graph[child].append(parent)

last_path = []


#fungsi DFS

def dfs_path(node, target, visited, path):
    visited.add(node)
    path.append(node)

    if node == target:
        return True

    for neighbor in graph[node]:
        if neighbor not in visited:
            if dfs_path(neighbor, target, visited, path):
                return True

    path.pop()
    return False


# edge


def build_tree(node, visited, prefix=""):
    text = prefix + node + "\n"

    visited.add(node)

    children = [n for n in graph[node] if n not in visited]

    for i, child in enumerate(children):

        if i == len(children) - 1:
            text += build_tree(child, visited, prefix + "└── ")
        else:
            text += build_tree(child, visited, prefix + "├── ")

    return text

#Relasi
def cari_relasi():

    global last_path

    start = combo_awal.get()
    target = combo_tujuan.get()

    visited = set()
    path = []

    dfs_path(start, target, visited, path)

    last_path = path.copy()

    hasil_text.delete("1.0", tk.END)

    hasil_text.insert(tk.END, "TREE RELASI\n")
    hasil_text.insert(tk.END, "=" * 40 + "\n\n")

    tree = build_tree(start, set())
    hasil_text.insert(tk.END, tree)

    hasil_text.insert(tk.END, "\n" + "=" * 40 + "\n\n")

    hasil_text.insert(tk.END, "RELASI DITEMUKAN!\n\n")
    hasil_text.insert(tk.END, " → ".join(path))

#graf

def hierarchy_pos(graph, root, width=1., vert_gap=0.2,
                  vert_loc=0, xcenter=0.5, pos=None,
                  parent=None):

    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)

    children = [n for n in graph[root] if n != parent]

    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2

        for child in children:
            nextx += dx
            pos = hierarchy_pos(
                graph,
                child,
                width=dx,
                vert_gap=vert_gap,
                vert_loc=vert_loc-vert_gap,
                xcenter=nextx,
                pos=pos,
                parent=root
            )

    return pos


def tampilkan_graf():

    G = nx.Graph()

    for node in graph:
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)

    plt.figure(figsize=(12, 8))

    # root graph
    root_node = "Andi"

    pos = hierarchy_pos(G, root_node)

    # edge biasa
    nx.draw_networkx_edges(
        G,
        pos,
        width=1.5
    )

    # highlight jalur DFS
    if len(last_path) > 1:

        path_edges = []

        for i in range(len(last_path)-1):
            path_edges.append(
                (last_path[i], last_path[i+1])
            )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=path_edges,
            width=4,
            edge_color="red"
        )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=2200
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=9,
        font_weight="bold"
    )

    plt.title("Graf Relasi User (DFS)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


#GUI

root = tk.Tk()
root.title("Pencarian Relasi User Dengan DFS")
root.geometry("850x650")

judul = tk.Label(
    root,
    text="PENCARIAN RELASI USER MENGGUNAKAN DFS",
    font=("Arial", 14, "bold")
)
judul.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

#user awal
tk.Label(
    frame,
    text="User Awal :",
    font=("Arial", 11)
).grid(row=0, column=0, padx=10, pady=10)

combo_awal = ttk.Combobox(
    frame,
    values=sorted(graph.keys()),
    state="readonly",
    width=25
)
combo_awal.grid(row=0, column=1)

# User Tujuan
tk.Label(
    frame,
    text="Cari Relasi Dengan :",
    font=("Arial", 11)
).grid(row=1, column=0, padx=10, pady=10)

combo_tujuan = ttk.Combobox(
    frame,
    values=sorted(graph.keys()),
    state="readonly",
    width=25
)
combo_tujuan.grid(row=1, column=1)

# tombol cari
btn_cari = tk.Button(
    root,
    text="Cari Relasi",
    font=("Arial", 11, "bold"),
    command=cari_relasi
)
btn_cari.pack(pady=5)

# tombol graf
btn_graf = tk.Button(
    root,
    text="Tampilkan Graf",
    font=("Arial", 11, "bold"),
    command=tampilkan_graf
)
btn_graf.pack(pady=5)

# hasil
hasil_text = tk.Text(
    root,
    width=100,
    height=25,
    font=("Consolas", 10)
)
hasil_text.pack(pady=10)

root.mainloop()