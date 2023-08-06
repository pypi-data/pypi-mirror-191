

# includes self as the first neighbor
# data is either X or distance matric d_e
def nearest_neighbors(data, k_nn=7, radius=0.5, metric='euclidean', method='k_nn', n_jobs=-1):
    if method == 'k_nn':
        neigh = NearestNeighbors(n_neighbors=k_nn-1, metric=metric, n_jobs=n_jobs)
    else:
        neigh = NearestNeighbors(radius=radius, metric=metric, n_jobs=n_jobs)
    neigh.fit(data)
    
    if method == 'k_nn':
        neigh_dist, neigh_ind = neigh.kneighbors()
        n = neigh_dist.shape[0]
        neigh_dist = np.insert(neigh_dist, 0, np.zeros(n), axis=1)
        neigh_ind = np.insert(neigh_ind, 0, np.arange(n), axis=1)
    else:
        neigh_dist, neigh_ind = neigh.radius_neighbors()
        n = neigh_dist.shape[0]
        for k in range(n):
            neigh_dist[k] = np.insert(neigh_dist[k], 0, 0)
            neigh_ind[k] = np.insert(neigh_ind[k], 0, k)
            
    return neigh_dist, neigh_ind
            
def sparse_matrix(neigh_ind, neigh_dist):
    if neigh_ind.dtype == 'object':
        row_inds = []
        col_inds = []
        data = []
        for k in range(neigh_ind.shape[0]):
            row_inds.append(np.repeat(k, neigh_ind[k].shape[0]).tolist())
            col_inds.append(neigh_ind[k].tolist())
            data.append(neigh_dist[k].tolist())
        row_inds = list(itertools.chain.from_iterable(row_inds))
        col_inds = list(itertools.chain.from_iterable(col_inds))
        data = list(itertools.chain.from_iterable(data))
    else:
        row_inds = np.repeat(np.arange(neigh_dist.shape[0]), neigh_dist.shape[1])
        col_inds = neigh_ind.flatten()
        data = neigh_dist.flatten()
    return csr_matrix((data, (row_inds, col_inds)))