import numpy as np
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram

def sim_func(a,b):
    if a == b:
        return 1
    else:
        return -1
    
def distance(val):
    if val > 0:
        return 0
    else:
        return -val
    
def pretty_print(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    print('\n')
    
    
# examples:
#citation networks

# To create data:
# 1. use make_sample
# 2. read in datafile
# 3. input networks, generate random walk data

# return: Dataframe with each row is an observation
# length > 3
def make_sample(length, category, size, var = 2, prob = None, distribution = np.random.rand, var_len=False):
    sample = []
    leng = length
    for k in range(size):
        if var_len == True:
            leng = np.random.randint(3, length)
        cate_lst = []
        lst = [cate_lst]
        for i in range(var):
            x = distribution(size = leng + 1)
            lst.append(x)

        for i in range(leng):
            if prob != None:
                cur = category[np.random.choice(np.arange(len(category)), p=prob)]
            else:
                cur = category[np.random.randint(0, len(category))]
            cate_lst.append(cur)
        sample.append(lst)
    return normalize(pd.DataFrame(sample, columns= ["category"] + [str(i+1) for i in range(var)]))

def read_data(filename, column_name, category_index = 0):
    if "parquet.gzip" in filename:
        df = pd.read_parquet(filename, columns = column_name)
    elif "csv" in filename:
        df = pd.read_csv(filename, names= column_name)
    elif "json" in filename:
        df = pd.read_json(filename, names= column_name)
    elif "excel" in filename:
        df = pd.read_excel(filename, names= column_name)
    else:
        df = pd.read_data(filename, names= column_name)
    dct = {}
    count = 1
    for i in range(len(column_name)):
        if  i == category_index:
            dct[column_name[i]] = "category"
        else:
            dct[column_name[i]] = count
            count += 1
    df.rename(columns = dct, inplace=True)
    df = df[['category'] + [ col for col in df.columns if col != 'category']]
    return df

#normalized 
def normalize(df):
    for i in df.columns:
        if i != "category":
            min_ = 100000000000000000
            max_ = 0
            for j, row in df.iterrows():
                for num in row[i]:
                    if num > max_:
                        max_ = num
                    if num < min_:
                        min_ = num
            lst = []
            for j, row in df.iterrows():
                tmp = []
                for num in row[i]:
                    tmp.append(round((num - min_) / (max_ - min_), 4))
                lst.append(tmp)
            
            df[i] = lst
    return df

#only work with random variable now

#weighted edge and node network
#logistic network
def random_walk(G, walk_len, count, var=2, distribution=None):
    walks = []
    for i in range(count):
        cur_node = random.choice(list(G.nodes))
        lst = [[cur_node]]
        for j in range(1, walk_len):
            neigh = list(G.neighbors(cur_node))
            if neigh:
                neighbor = random.choice(neigh)   # choose one random neighbor
                lst[0].append(neighbor)   # add it to walk
                cur_node = neighbor   # save it to cur_node to continue from it next iteration
            else:
                break
        for j in range(var):
            if distribution == "normal":
                x = np.random.normal(size = len(lst[0]) + 1)
                x = (x - x.min()) / (x.max() - x.min())
                x = np.delete(x, np.where(x == 0))
                x = np.delete(x, np.where(x == 1))
                lst.append(x)
            else:
                x = np.random.rand(len(lst[0]) - 1)
                lst.append(x)
        walks.append(lst)
    return pd.DataFrame(walks, columns= ["category"] + [str(i+1) for i in range(var)])

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

#TODO: edge length not thickness
def draw(df, sample, color = "hsv"):
    # only work for var = 2, best suitable to show data inteprated as time and dis
    # color example: {"A": "r", "B": "y", "C": "g", "D":"b"} or cmap
    
    G=nx.DiGraph()
    X = df.loc[sample][0]
    X1 = df.loc[sample][1]
    X2 = df.loc[sample][2]
    
    if isinstance(color, dict) == False:
        tmp = np.unique(np.array(X))
        cmap = get_cmap(len(tmp)+1, name = color)
        color = {}
        for i in range(len(tmp)):
            color[tmp[i]] = cmap(i)
        
    plt.figure(1,figsize=(2.5 * len(X),2)) 

    node_size = []
    for i in range(len(X) - 1):
        node_size.append(1000 + 10000 * float(X1[i]))
    node_size.append(1000)
    
    node_color = []
    width = []
    sum_dis = 0
    for i in range(len(X)):
        if i == 0:
            G.add_node(i, pos = (0,1))
        elif i != len(X) - 1:
            diss = (np.sqrt(node_size[i]/31400)-np.sqrt(2000/31400) + np.sqrt(node_size[i-1]/31400)-np.sqrt(2000/31400))**2
            sum_dis = sum_dis + diss + 1
            G.add_node(i, pos = (sum_dis,1))
        else:
            G.add_node(i, pos = (sum_dis+1,1))
        node_color.append(color[X[i]])
    
    edge_labels = {}
    for i in range(len(X) - 1):
        G.add_edge(i, i+1, len= 1)
        edge_labels[(i, i+1)] = round(float(X2[i]),2)
        width.append(0.2+float(X2[i]) * 10)
    pos=nx.get_node_attributes(G,'pos')
    
    labeldict = {}
    
    for i in range(len(X) - 1):
        labeldict[i] = X[i] + "\n" + str(round(float(X2[i]),2))
    labeldict[i+1] = X[i+1]
    
    nx.draw(G,pos, labels = labeldict, node_size = node_size, width = width, node_color = node_color, edge_color = 'b')
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.show()
    
def com_draw(df, lst, color = None):
    for x in lst:
        draw(df, x, color = color)
    
def propogate_matrix_global_two_vars(X, Y, X1, Y1, X2, Y2, ratio, gap_score, align_score, proportion):
    X1 = np.insert(X1, 0, 0)
    X2 = np.insert(X2, 0, 0)
    Y1 = np.insert(Y1, 0, 0)
    Y2 = np.insert(Y2, 0, 0)
    
    value_matrix = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_matrix = [[[0, 0] for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_gap_score = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    need_constant_gap = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    
    need_constant_gap[0][0] = 1
    
    for j in range(len(Y)+1):
        for i in range(len(X)+1):
            if j == 0 and i == 0:
                continue
            # For the global approach, the first row and column involves the time penalties
            # of adding in a gap of a given length to the beginning of either sequence.
            elif j == 0:
                above_score = update_gap_two_vars(i - 1, j, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "above")
                above_value = value_matrix[i-1][j] - gap_score * need_constant_gap[i-1][j] + source_gap_score[i-1][j] * proportion - above_score[0] * proportion
                    
                value_matrix[i][j] = above_value
                source_matrix[i][j] = [i - 1,j]
                source_gap_score[i][j] = above_score[0]
                need_constant_gap[i][j] = 0
            elif i == 0:
                left_score = update_gap_two_vars(i, j - 1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "left")
                left_value = value_matrix[i][j-1] - gap_score * need_constant_gap[i][j-1] + source_gap_score[i][j-1] * proportion - left_score[0] * proportion
                    
                value_matrix[i][j] = left_value
                source_matrix[i][j] = [i,j-1]
                source_gap_score[i][j] = left_score[0]
                need_constant_gap[i][j] = 0
            else:
                score = align_score(X[i-1], Y[j-1])
                
                diag_score = update_gap_two_vars(i-1, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "diag")
                diag_value = value_matrix[i-1][j-1] + score + source_gap_score[i-1][j-1] * proportion- diag_score[0] * proportion
                    
                left_score = update_gap_two_vars(i, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "left")
                left_value = value_matrix[i][j-1] - gap_score * need_constant_gap[i][j-1] + source_gap_score[i][j-1] * proportion - left_score[0] * proportion
                
                above_score = update_gap_two_vars(i-1, j, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "above")
                above_value = value_matrix[i-1][j] - gap_score * need_constant_gap[i-1][j] + source_gap_score[i-1][j] * proportion - above_score[0] * proportion
                
                max_score = max(diag_value, left_value, above_value)
                value_matrix[i][j] = max_score
                if diag_value == max_score:
                    source_matrix[i][j] = [i -1, j-1]
                    source_gap_score[i][j] = 0
                    need_constant_gap[i][j] = 1
                elif left_value == max_score:
                    source_matrix[i][j] = [i,j-1]
                    if left_score[1] or above_score[1]:
                        source_gap_score[i][j] = 0
                        need_constant_gap[i][j] = 1
                    else:
                        source_gap_score[i][j] = left_score[0]
                        need_constant_gap[i][j] = 0
                else:
                    source_matrix[i][j] = [i -1,j]
                    if left_score[1] or above_score[1]:
                        source_gap_score[i][j] = 0
                        need_constant_gap[i][j] = 1
                    else:
                        source_gap_score[i][j] = above_score[0]
                        need_constant_gap[i][j] = 0
    # pretty_print(value_matrix)
    return value_matrix[len(X)][len(Y)]

def propogate_matrix_local_two_vars(X, Y, X1, Y1, X2, Y2, ratio, gap_score, align_score, proportion):
    X1 = np.insert(X1, 0, 0)
    X2 = np.insert(X2, 0, 0)
    Y1 = np.insert(Y1, 0, 0)
    Y2 = np.insert(Y2, 0, 0)
    
    value_matrix = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_matrix = [[[0, 0] for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_gap_score = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    need_constant_gap = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    
    need_constant_gap[0][0] = 1
    
    for j in range(1, len(Y)+1):
        for i in range(1, len(X)+1):
            score = align_score(X[i-1], Y[j-1])

            diag_score = update_gap_two_vars(i-1, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "diag")
            diag_value = value_matrix[i-1][j-1] + score + source_gap_score[i-1][j-1] * proportion- diag_score[0] * proportion

            left_score = update_gap_two_vars(i, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "left")
            left_value = value_matrix[i][j-1] - gap_score * need_constant_gap[i][j-1] + source_gap_score[i][j-1] * proportion - left_score[0] * proportion

            above_score = update_gap_two_vars(i-1, j, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "above")
            above_value = value_matrix[i-1][j] - gap_score * need_constant_gap[i-1][j] + source_gap_score[i-1][j] * proportion - above_score[0] * proportion

            max_score = max(diag_value, left_value, above_value, 0)
            value_matrix[i][j] = max_score
            if diag_value == max_score or max_score == 0:
                source_matrix[i][j] = [i-1, j-1]
                source_gap_score[i][j] = 0
                need_constant_gap[i][j] = 1
            elif left_value == max_score:
                source_matrix[i][j] = [i,j-1]
                if left_score[1] or above_score[1]:
                    source_gap_score[i][j] = 0
                    need_constant_gap[i][j] = 1
                else:
                    source_gap_score[i][j] = left_score[0]
                    need_constant_gap[i][j] = 0
            else:
                source_matrix[i][j] = [i -1,j]
                if left_score[1] or above_score[1]:
                    source_gap_score[i][j] = 0
                    need_constant_gap[i][j] = 1
                else:
                    source_gap_score[i][j] = above_score[0]
                    need_constant_gap[i][j] = 0
    # pretty_print(value_matrix)
    return value_matrix[len(X)][len(Y)]

# ratio 0-1, X/Y1 * ratio + X/Y2 * (1-ratio)
def update_gap_two_vars(row_index, column_index, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, direction):
    # This means we are dealing with a value alongside the edge.
    if row_index == 0 or column_index == 0:
        return [abs(sum(X1[0:row_index+1]) - sum(Y1[0:column_index+1])) * ratio + abs(sum(X2[0:row_index+1]) - sum(Y2[0:column_index+1])) * (1-ratio), 0]
    # This means this value came from our diagonal direction.
    elif source_matrix[row_index][column_index][0] < row_index and source_matrix[row_index][column_index][1] < column_index:
        if direction == "left":
            return [Y1[column_index] * ratio + Y2[column_index] * (1-ratio), 0]
        elif direction == "above":
            return [X1[row_index] * ratio + X2[row_index] * (1-ratio), 0]
        else:
            return [abs(X1[row_index] - Y1[column_index]) * ratio + abs(X2[row_index] - Y2[column_index]) * (1-ratio), 0]
    # In this case, this value came from a downward movement, meaning an extended gap in the y-direction.
    elif source_matrix[row_index][column_index][0] < row_index:
        # This means that our best choice is a 'zigzag' movement.  So, we need to have the algorithm
        # reset the gap score, since we are now going to deal with a gap in the other sequence.
        if direction == "left":
            return [abs(source_gap_score[row_index][column_index] - Y1[column_index] * ratio - Y2[column_index] * (1-ratio)), 1]
        elif direction == "above":
            return [source_gap_score[row_index][column_index] + X1[row_index] * ratio + X2[row_index] * (1-ratio), 0]
        else:
            return [abs(source_gap_score[row_index][column_index] + (X1[row_index] - Y1[column_index]) * ratio + (X2[row_index] - Y2[column_index]) * (1-ratio)), 0]
    # In this case, this value came from a rightward movement, meaning an extended gap in the x-direction.
    elif source_matrix[row_index][column_index][1] < column_index:
        if direction == "left":
            return [source_gap_score[row_index][column_index] + Y1[column_index] * ratio + Y2[column_index] * (1-ratio), 0]
        # This means that our best choice is a 'zigzag' movement.  So, we need to have the algorithm
        # reset the gap score, since we are now going to deal with a gap in the other sequence.
        elif direction == "above":
            return [abs(source_gap_score[row_index][column_index] - X1[row_index] * ratio - X2[row_index] * (1-ratio)), 1]
        else:
            return [abs(source_gap_score[row_index][column_index] + (Y1[column_index ] - X1[row_index])*ratio + (Y2[column_index] - X2[row_index]) * (1-ratio)), 0]
        
#analysis
def distance_metric(df, treat_dis = True):
    dist = np.zeros((len(df),len(df)))
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            dis = propogate_matrix_global_two_vars(df.loc[i]["category"], df.loc[j]["category"], df.loc[i]["1"], df.loc[j]["1"], df.loc[i]["2"], df.loc[j]["2"], 0.5, 1, sim_func, 2)
            if treat_dis:
                dis = distance(dis)
            dist[i][j] = dis
            dist[j][i] = dis
    return dist

def neighbours(dis, target, thres):
    count = 0
    lst = []
    for x in dis[target]:
        if x < thres & count != target:
            lst.append(count)
        count += 1
    return lst

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
    
def cluster(dis, distance = None, n_clusters = None):
    model = AgglomerativeClustering(affinity="precomputed", distance_threshold=distance,n_clusters=n_clusters, linkage="average", compute_distances=True)
    model = model.fit(dis)
    return model

def count(model):
    labels = np.array(model.labels_)
    unique, counts = np.unique(labels, return_counts=True)
    return unique, counts