import matplotlib.pyplot as plt
import queue
import subprocess
import os

# FILENAME = "imdb.top250.txt"     # Graph source file
FILENAME = "imdb.no-tv-v.txt"     

def Import_Graph():
    print("正在导入图, 请耐心等待...")

    global graph
    global actor_names, actor_ids
    global actor_cnt, edge_cnt, movie_cnt
    global movie_ids
    graph = {}
    actor_names, actor_ids = {}, {}
    movie_dic = {}
    movie_ids = {}
    actor_cnt, edge_cnt, movie_cnt = 0, 0, 0
    with open(FILENAME, 'r') as fp:
        while True:                 # These 3 lines can be replaced by
            line = fp.readline()    # while line := fp.readline() in Py3.8,
            if not line: break      # this form is for compatiblity.
            actor, movie = line.split('|')
            if not actor in actor_ids:
                actor_ids[actor] = actor_cnt
                actor_names[actor_cnt] = actor
                actor_cnt += 1
            if not movie in movie_ids:
                movie_cnt += 1
                movie_ids[movie] = -movie_cnt
                movie_dic[movie_ids[movie]] = []
            movie_dic[movie_ids[movie]].append(actor_ids[actor])

    # Calculate degrees and edge cnt
    deg = [0] * actor_cnt
    for v, actor_list in movie_dic.items():
        l = len(actor_list)
        edge_cnt += l * (l - 1) / 2
        def addedge(u, v): # connect u -> v
            if not u in graph: graph[u] = []
            graph[u].append(v)
        for u in actor_list:
            deg[u] += l - 1
            addedge(u, v)
            addedge(v, u)
    
    deg_map = {}
    for d in deg:
        if not d in deg_map: deg_map[d] = 0
        deg_map[d] += 1
    
    print("原图的节点数:", actor_cnt)
    print("电影个数:", movie_cnt)
    print("原图的边数:", int(edge_cnt))
    plt.hist(x=deg, bins=50)
    plt.savefig("deg.png")
    print("度数分布直方图已保存到 deg.png")
    plt.show()

def sp2():  # Shortest path between 2 actors
    print("输入两个演员，求出其最短路径。")
    Actor1 = input("第1位演员名字:")
    Actor2 = input("第2位演员名字:")
    if not Actor1 in actor_ids or not Actor2 in actor_ids:
        raise Exception("演员不存在")
    offset = movie_cnt      # to keep index >= 0
    U, V = actor_ids[Actor1], actor_ids[Actor2]
    U += offset
    V += offset
    dis = [None] * (actor_cnt + movie_cnt)
    pre = [None] * (actor_cnt + movie_cnt)
    Q = queue.Queue()
    Q.put(U)
    dis[U] = 0
    while(not Q.empty()):   # BFS
        u = Q.get()
        if(u == V):
            print("距离:", dis[V] // 2)
            path = ""
            while(u != None):   # restore path backward
                if(u - offset >= 0):
                    if(path != ""): path = " -> " + path
                    path = actor_names[u - offset] + path
                u = pre[u]
            print("路径为:")
            print(path)
            return
        for v_ in graph[u - offset]:
            v = v_ + offset
            if dis[v] == None:
                dis[v] = dis[u] + 1
                pre[v] = u
                Q.put(v)
    print("无法到达")

def bacon():
    print("正在计算Bacon Number...")
    offset = movie_cnt      # to keep index >= 0
    U = actor_ids["Kevin Bacon (I)"] + offset
    dis = [None] * (actor_cnt + movie_cnt)
    Q = queue.Queue()
    Q.put(U)
    dis[U] = 0
    while(not Q.empty()):   # BFS
        u = Q.get()
        for v_ in graph[u - offset]:
            v = v_ + offset
            if dis[v] == None:
                dis[v] = dis[u] + 1
                Q.put(v)
    def save_bacon(fname):
        with open(fname, "w") as fp:
            for aid in range(actor_cnt):
                if(dis[aid + offset] != None):
                    print(actor_names[aid], dis[aid + offset] // 2, file = fp)
    save_bacon("bacon.txt")
    print("Bacon Number被保存到 bacon.txt")
    bacon_map = [0] * 10
    for aid in range(actor_cnt):
        if(dis[aid + offset] != None):
            d = dis[aid + offset] // 2
            if(0 <= d <= 9): bacon_map[d] += 1
    plt.bar(range(10), bacon_map)
    plt.savefig("bacon.png")
    print("Bacon Number分布直方图已保存到 bacon.png")
    plt.show()

def conncomp():
    print("导出图结构到文件 graph0.in")
    with open("graph0.in", "w") as fp:  # export graph
        print(actor_cnt, file = fp)
        print(movie_cnt, file = fp)
        eg_cnt = 0
        for u in graph:
            for v in graph[u]: eg_cnt += 1
        print(eg_cnt, file = fp)
        for u in graph:
            for v in graph[u]:
                print(u, v, file = fp)
    print("调用 ./t2part 计算结果")
    if(os.name == 'posix'): subprocess.run("./t2part", shell=True)
    else: subprocess.run("./t2part.exe", shell=True)
    print("结果保存到 conn.out")

def fakeconncomp():
    print("两次bfs, 估计直径的下界, 请耐心等待...")
    offset = movie_cnt          # to keep index >= 0
    with open("conn2.out", "w") as fp:
        conncnt = 0
        isvisited = [False] * actor_cnt
        Q = queue.Queue()
        dis1 = [None] * (actor_cnt + movie_cnt)
        dis2 = [None] * (actor_cnt + movie_cnt)
        for aid in range(actor_cnt):
            if isvisited[aid]: continue
            isvisited[aid] = True
            connsz = 0
            U = aid + offset
            Q.put(U)
            dis1[U] = 0
            mxdis, mxid = 0, U
            while(not Q.empty()):   # 1st BFS
                u = Q.get()
                if(u >= offset):
                    isvisited[u - offset] = True
                    connsz += 1
                if(u >= offset and mxdis < dis1[u]): mxdis, mxid = dis1[u], u
                for v_ in graph[u - offset]:
                    v = v_ + offset
                    if dis1[v] == None:
                        dis1[v] = dis1[u] + 1
                        Q.put(v)
            U = mxid                # New start
            Q.put(U)
            dis2[U] = 0
            mxdis, mxid = 0, U
            while(not Q.empty()):   # 1st BFS
                u = Q.get()
                if(u >= offset and mxdis < dis2[u]): mxdis, mxid = dis2[u], u
                for v_ in graph[u - offset]:
                    v = v_ + offset
                    if dis2[v] == None:
                        dis2[v] = dis2[u] + 1
                        Q.put(v)
            print("连通分支大小", connsz, "直径", mxdis // 2, file = fp)
            conncnt += 1
        print("连通分支个数", conncnt, file = fp)
    print("结果保存到 conn2.out")

txtMenu = """
选项:
(1) 求两演员的最短距离
(2) 求连通分支及其直径(适用于250数据集)
(3) 求Bacon Number
(4) 两次bfs估计直径(适用于大数据集的近似估计)
(0) 退出程序
"""

if __name__ == '__main__':
    Import_Graph()
    while(1):
        print(txtMenu)
        op = input("输入选项: ")
        if op == "1" : sp2()
        elif op == "2" : conncomp()
        elif op == "3" : bacon()
        elif op == "4" : fakeconncomp()
        elif op == "0" : break
        else: print("非法选项")