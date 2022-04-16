import numpy as np

item_id_dict= dict() #dictionary for item id 和 列数 （id为1的item 在第一列）

def load_data():
    '''测试数据'''
    #to do: 将sql数据写入
    data_mat = np.mat([[1, 1, 1, 0, 0], [2, 2, 2, 0, 0], [1, 1, 1, 0, 0], [5, 5, 5, 0, 0],
                     [1, 1, 0, 2, 2], [0, 0, 0, 3, 3], [0, 0, 0, 1, 1]])
    return data_mat

# 相似度计算...
def eu_dis(inv1, inv2):
    '''欧氏距离相似度'''
    return 1.0/(1.0+np.linalg.norm(inv1-inv2))

def pear_dis(inv1, inv2):
    '''皮尔逊相关系数'''
    if len(inv1) < 3:
        return 1.0
    return 0.5 + 0.5 * np.corrcoef(inv1, inv2, rowvar=False)[0][1]

def cos_dis(inv1, inv2):
    '''余弦相似度'''
    num = float(inv1.T*inv2)
    den = np.linalg.norm(inv1) * np.linalg.norm(inv2)
    return num/den

def stand_est(data_mat, user, sim_means, item):
    '''计算在给定相似度计算方法的条件下，用户对物品的估计评分值'''
    n = data_mat.shape[1]  # 取数据集的列数
    sim_total = 0.0; rat_sim_total = 0.0
    for j in range(n):
        user_rating = data_mat[user, j]  # 通过循环得到地user行的每列元素
        if user_rating == 0:
            continue
        over_lap = np.nonzero(np.logical_and(data_mat[:, item].A>0, data_mat[:, j].A>0))[0]

        if len(over_lap) == 0:
            sim_laity = 0.0
        else:
            sim_laity = sim_means(data_mat[over_lap, item], data_mat[over_lap, j])
            
        sim_total += sim_laity
        rat_sim_total += sim_laity * user_rating
    if sim_total == 0:
        return 0
    else:
        return rat_sim_total/sim_total

def recommend(data_mat, user, N, sim_means=cos_dis, est_method=stand_est):
    # Main Recommendation
    print(np.nonzero(data_mat[user, :].A==0))
    un_rated_item = np.nonzero(data_mat[user, :].A==0)[1]
    if len(un_rated_item) == 0:
        return 'you rated everything'
    item_score = []
    for item in un_rated_item:
        est_mated_score = est_method(data_mat, user, sim_means, item)
        item_score.append((item, est_mated_score))
    return sorted(item_score, key=lambda jj: jj[1], reverse=True)[:N]

def svd_est(data_mat, user, sim_means, item):
    #using SVD
    n = data_mat.shape[1]
    sim_total = 0.0; rate_sim_total = 0.0
    u, sigma, v = np.linalg.svd(data_mat)
    sig4 = np.mat(np.eye(4)*sigma[:4])
    x_formed_items = data_mat.T * u[:, :4] * sig4.I
    for j in range(n):
        user_rating = data_mat[user, j]
        if user_rating == 0 or j == item:
           continue
        sim_laity = sim_means(x_formed_items[item, :].T, x_formed_items[j, :].T)
        print('the %d and %d similarity is %f' % (item, j, sim_laity))
        sim_total += sim_laity
        rate_sim_total += sim_laity * user_rating
    if sim_total == 0:
        return 0
    else:
        return rate_sim_total/sim_total

def loadExData2():
    # To do: 将data导入 最好有评分

    # data= [[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
    #        [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
    #        [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
    #        [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
    #        [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
    #        [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
    #        [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
    #        [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
    #        [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
    #        [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
    #        [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

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

data = loadExData2()
data = np.mat(data)
user = 3
N = 3
ans = recommend(data, user, N, sim_means=cos_dis, est_method=stand_est)
print(ans)#结果