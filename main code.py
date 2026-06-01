import csv

graph = {}

with open("friends.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)

    for user1, user2 in reader:
        if user1 not in graph:
            graph[user1] = []
        if user2 not in graph:
            graph[user2] = []

        graph[user1].append(user2)
        graph[user2].append(user1)

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

print("\n-DAFTAR USER-")

for user in sorted(graph.keys()):
    print(user)

print("_____________\n")    

start = input("Masukkan user awal: ").title()
target = input("Cari relasi dengan: ").title()

visited = set()
path = []

if start in graph and target in graph:
    found = dfs_path(start, target, visited, path)

    if found:
        print("\nRelasi ditemukan!\n")
        print("Jalur Relasi:")
        print(" → ".join(path))
    else:
        print("\nTidak ditemukan relasi.")
else:
    print("User tidak ada dalam data.")