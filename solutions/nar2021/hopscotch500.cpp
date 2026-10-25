// Hopscotch 500 (Kattis hopscotch500, difficulty 7.0)
// Distance is min(|dr|,|dc|)^2, so a hop costs EITHER dr^2 OR dc^2. Hence
//   best(i,j) = min( min over prev tiles of d + (i-a)^2,  min over prev tiles of d + (j-b)^2 )
// The first term depends only on the target ROW i, the second only on the target COLUMN j.
// Per layer: rowBest[a] = min d of previous tiles in row a (same for columns), then
// R[i] = min_a rowBest[a] + (i-a)^2 only for rows that hold next-layer tiles.
// Worst case about n^3 simple operations: fine in C++, too slow in Python.
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main() {
    int n, k;
    scanf("%d %d", &n, &k);
    vector<vector<pair<int,int>>> layer(k + 1);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) { int v; scanf("%d", &v); layer[v].push_back({i, j}); }
    for (int v = 1; v <= k; v++) if (layer[v].empty()) { printf("-1\n"); return 0; }
    const ll INF = LLONG_MAX / 4;
    vector<ll> d(layer[1].size(), 0);
    vector<ll> rowBest(n), colBest(n), R(n), C(n);
    for (int v = 2; v <= k; v++) {
        fill(rowBest.begin(), rowBest.end(), INF);
        fill(colBest.begin(), colBest.end(), INF);
        for (size_t t = 0; t < layer[v-1].size(); t++) {
            auto [a, b] = layer[v-1][t];
            rowBest[a] = min(rowBest[a], d[t]);
            colBest[b] = min(colBest[b], d[t]);
        }
        vector<int> prows, pcols;
        for (int a = 0; a < n; a++) { if (rowBest[a] < INF) prows.push_back(a); if (colBest[a] < INF) pcols.push_back(a); }
        vector<char> needR(n, 0), needC(n, 0);
        for (auto [i, j] : layer[v]) { needR[i] = 1; needC[j] = 1; }
        for (int i = 0; i < n; i++) {
            if (needR[i]) { ll best = INF; for (int a : prows) best = min(best, rowBest[a] + (ll)(i - a) * (i - a)); R[i] = best; }
            if (needC[i]) { ll best = INF; for (int b : pcols) best = min(best, colBest[b] + (ll)(i - b) * (i - b)); C[i] = best; }
        }
        vector<ll> nd(layer[v].size());
        for (size_t t = 0; t < layer[v].size(); t++) { auto [i, j] = layer[v][t]; nd[t] = min(R[i], C[j]); }
        d.swap(nd);
    }
    printf("%lld\n", *min_element(d.begin(), d.end()));
}
