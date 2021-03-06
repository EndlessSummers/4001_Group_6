import numpy as np
from Funbox.models import Activities, UserHash, UserInfo, UserPreference, Notes

item_id_dict= dict() #dictionary for item id 和 列数 （id为1的item 在第一列）

def load_data():
    # test data format  1
    data_mat = np.mat([[1, 1, 1, 0, 0], [2, 2, 2, 0, 0], [1, 1, 1, 0, 0], [5, 5, 5, 0, 0],
                     [1, 1, 0, 2, 2], [0, 0, 0, 3, 3], [0, 0, 0, 1, 1]])
    return data_mat

def loadExData2():
    # test data format2
    data= [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
           [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
           [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
           [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
           [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
           [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
           [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
           [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
           [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]]       
    return np.mat(data)

# Similarity Calculation

def eu_dis(inv1, inv2):
    # Euclidean Correlation
    return 1.0/(1.0+np.linalg.norm(inv1-inv2))

def pear_dis(inv1, inv2):
    #Pearson Correlation
    if len(inv1) < 3:
        return 1.0
    return 0.5 + 0.5 * np.corrcoef(inv1, inv2, rowvar=False)[0][1]

def cos_dis(inv1, inv2):
    # Cosine Similarity
    num = float(inv1.T*inv2)
    den = np.linalg.norm(inv1) * np.linalg.norm(inv2)
    return num/den

# It is a heuristic method to generate a scored matrix for specific user
# After selecting one user, the algo will predict what is the score of 
# unrated items. Then the final recommendation will return a list with item id
# and corresponding ratings

def stand_est(data_mat, user, sim_means, item):
    # given any similarity calculation method, rate each item
    n = data_mat.shape[1]  # num of cols
    sim_total = 0.0; rat_sim_total = 0.0
    for j in range(n):
        user_rating = data_mat[user, j]  # retrieve every elements from each cols iterately
        if user_rating == 0:
            continue
        over_lap = np.nonzero(np.logical_and(data_mat[:, item].A>0, data_mat[:, j].A>0))[0] #for calculation of similarity

        if len(over_lap) == 0:
            sim_laity = 0.0
        else:
            sim_laity = sim_means(data_mat[over_lap, item], data_mat[over_lap, j])
            
        sim_total += sim_laity
        rat_sim_total += sim_laity * user_rating #update similarity
    if sim_total == 0:
        return 0
    else:
        return rat_sim_total/sim_total

# Another method for generating scores. The algo first use SVD for the whole rating matrix. 
# Then, we derive the new matrix for calculation using the multiply of the original matrix, u and sigma
# Repeat the same procedure in the standard one.
def svd_est(data_mat, user, sim_means, item):
    #using SVD
    n = data_mat.shape[1]
    sim_total = 0.0; rate_sim_total = 0.0
    u, sigma, v = np.linalg.svd(data_mat) #SVD decomposition
    sig4 = np.mat(np.eye(4)*sigma[:4])
    x_formed_items = data_mat.T * u[:, :4] * sig4.I # for similarity calculation
    for j in range(n):
        user_rating = data_mat[user, j]
        if user_rating == 0 or j == item:
           continue
        sim_laity = sim_means(x_formed_items[item, :].T, x_formed_items[j, :].T)
        print('the %d and %d similarity is %f' % (item, j, sim_laity))
        sim_total += sim_laity
        rate_sim_total += sim_laity * user_rating #update
    if sim_total == 0:
        return 0
    else:
        return rate_sim_total/sim_total

# Recommendation of item. It will append the scores into a list for certain users.
def recommend(data_mat, user, N, sim_means=cos_dis, est_method=stand_est):
    # Main Recommendation
    un_rated_item = np.nonzero(data_mat[user, :].A==0)[1]
    if len(un_rated_item) == 0:
        return 'you rated everything'
    item_score = []
    for item in un_rated_item:
        est_mated_score = est_method(data_mat, user, sim_means, item)
        item_score.append((item, est_mated_score))
    return sorted(item_score, key=lambda jj: jj[1], reverse=True)[:N]