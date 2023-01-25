#include <cstdio>
#include <algorithm>
#include <queue>
#include <cstring>
#define MC(a, v) memset(a,v,sizeof(a))

const int N = 15000, M = 60000;
int head[N],nxt[M],to[M],tot = 0;
inline void addedge(int u,int v){
    nxt[++tot] = head[u];to[tot] = v;head[u] = tot;
    nxt[++tot] = head[v];to[tot] = u;head[v] = tot;
}
// graph in "linking forward star" style

int dis[N];                         // Distance
int n2c[N],connsz[N],conncnt = 0;   // Info of Connected Component
                                    // n2c[u] -> Conn index of node u
int dia[N];                         // Diameter of Conn

std::queue<int> Q;                  // For BFS
int main(){
    while(!Q.empty()) Q.pop();
    MC(head, -1);
    MC(connsz, 0);
    MC(dia, 0);
    freopen("graph0.in","r",stdin);
    freopen("conn.out","w",stdout);
    
    int n, k, m;scanf("%d%d%d", &n, &k, &m);
    for(int i = 0;i < m;i++){
        int u, v;scanf("%d%d", &u, &v);
        addedge(u + k, v + k);
    }
    
    MC(dis, 0);
    
    for(int U = 0;U < n;U++){   // Conn size and index
        if(dis[U + k]) continue;
        Q.push(U + k);dis[U + k] = 1;
        while(!Q.empty()){
            int u = Q.front();Q.pop();
            if(u >= k){
                n2c[u] = conncnt;++connsz[conncnt];
            }
            for(int i = head[u];~i;i = nxt[i]){
                int v = to[i];
                if(!dis[v]){dis[v] = 1;Q.push(v);}
            }
        }
        ++conncnt;
    }

    for(int U = 0;U < n;U++){   // BFS for each node
        MC(dis, -1);
        Q.push(U + k);dis[U + k] = 0;
        int mxd = 0;
        while(!Q.empty()){
            int u = Q.front();Q.pop();
            if(u >= k && dis[u] > mxd) mxd = dis[u];
            for(int i = head[u];~i;i = nxt[i]){
                int v = to[i];
                if(!~dis[v]){dis[v] = dis[u] + 1;Q.push(v);}
            }
        }
        dia[n2c[U + k]] = std::max(dia[n2c[U + k]], mxd);
    }

    printf("conncnt = %d\n", conncnt);
    for(int i = 0;i < conncnt;i++){
        printf("size = %d, diameter = %d\n", connsz[i], dia[i] / 2);
    }
    return 0;
}