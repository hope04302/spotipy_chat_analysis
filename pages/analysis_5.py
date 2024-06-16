import streamlit as st
from common_container import menu
from data_analysis import song_df

menu()

st.code("""def set_doc_topics(model, corpus): 

    d = []
    
    for doc_num, doc in enumerate(corpus):
        topic_probs = model[doc]
        nn = np.zeros(NUM_TOPICS)

        for topic_id, prob in topic_probs:
            nn[topic_id] = prob
        
        d.append(nn)
    return np.stack(d)
    
text_vector = set_doc_topics(lda_model, corpus)
text_vector.shape""")

st.code("""(8054, 15)""")

st.code("""from tqdm import tqdm
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

dbs = DBSCAN(eps=0.001, min_samples=2, metric="cosine")
dbs_cluster_labels = dbs.fit_predict(text_vector)

text_df["dbs_cluster"] = dbs_cluster_labels
duplicated = (text_df["dbs_cluster"] == -1) | ~(text_df["dbs_cluster"].duplicated())
text_df_dupli_removed = text_df[duplicated]
text_df_dupli_removed.info()""")

st.code("""Index: 7832 entries, 38541 to 36705594
Data columns (total 14 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   name          7832 non-null   object
 1   album         7832 non-null   object
 2   year          7829 non-null   Int64 
 3   month         7819 non-null   Int64 
 4   day           7771 non-null   Int64 
 5   artist        7832 non-null   object
 6   genre         7832 non-null   object
 7   lyric_writer  7832 non-null   object
 8   composer      7832 non-null   object
 9   arranger      7832 non-null   object
 10  lyrics_row    7832 non-null   int64 
 11  lyrics        7832 non-null   object
 12  tk_lyrics     7832 non-null   object
 13  dbs_cluster   7832 non-null   int64 """)

st.code("""text_vector_dupli_removed = text_vector[duplicated]
text_vector_dupli_removed.shape""")
st.code("""(7832, 15)""")

st.code("""# =====================================
# 초기 변수
# =====================================

param_init = 'random'
param_n_init = 10
param_max_iter = 300
param_max_step = 60

# =====================================
# K-Means Clustering을 반복
# =====================================

clusters_range = range(2, param_max_step + 1)
elbow_res = []
sil_res = []

for i in tqdm(clusters_range, desc='K-Means Clustering'):
    km = KMeans(n_clusters=i, init=param_init, n_init=param_n_init, max_iter=param_max_iter, random_state=0)
    cluster_labels = km.fit_predict(text_vector_dupli_removed)
    silhouette_avg = silhouette_score(text_vector_dupli_removed, cluster_labels)

    sil_res.append([i, silhouette_avg])
    elbow_res.append(km.inertia_)""")

st.code("""# =====================================
# elbow method
# =====================================

plt.figure(figsize=(20, 5))
plt.xticks(range(0, 100, 2))
plt.grid()

plt.plot(clusters_range, elbow_res)
plt.show()""")

st.code("""# =====================================
# shihouette method
# =====================================

result = pd.DataFrame(sil_res, columns=["n_clusters", "silhouette_score"])
pivot_km = pd.pivot_table(result, index="n_clusters", values="silhouette_score")

plt.figure(figsize=(5, 10))
sns.heatmap(pivot_km, annot=True, linewidths=0, fmt='.5f', cmap=sns.cm._rocket_lut)
plt.tight_layout()
plt.show()""")

st.code("""# 최종 선택 클러스터 개수
n_cluster = 10

km = KMeans(n_clusters=n_cluster, init=param_init, n_init=param_n_init, max_iter=param_max_iter, random_state=0)
km.fit_predict(text_vector_dupli_removed)

cluster_labels = km.labels_
cluster_centers = km.cluster_centers_
text_df_dupli_removed['cluster'] = cluster_labels

def mapping_cluster(song_id):
    dbs_cluster = text_df.loc[song_id, "dbs_cluster"]
    if dbs_cluster == -1:
        return text_df_dupli_removed.loc[song_id, "cluster"]
    else:
        leader_id = text_df_dupli_removed[text_df_dupli_removed["dbs_cluster"] == dbs_cluster].index[0]
        return text_df_dupli_removed.loc[leader_id, "cluster"]

text_df["cluster"] = text_df.index.map(mapping_cluster)
text_df""")
st.dataframe(song_df[song_df.columns[:-3]])

st.code("""from sklearn.decomposition import PCA

pca = PCA(n_components = 2)
pca_transformed = pca.fit_transform(text_vector)
pca_transformed

text_df['pca_x'] = pca_transformed[:, 0]  #x좌표
text_df['pca_y'] = pca_transformed[:, 1]  #y좌표
text_df""")
st.dataframe(song_df[song_df.columns[:-1]])

st.code("""plt.figure(figsize=(10, 10))

text_df["cluster_str"] = text_df["cluster"].map(str)
sns.scatterplot(data=text_df, x="pca_x", y="pca_y",
                hue="cluster_str", hue_order={str(i): i for i in range(n_cluster)},
                alpha=0.5)

plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.legend()

plt.title('3 Clusters Visualization by 2 PCA Components')
plt.show()""")

st.code("""temp = {}

for topic_id in range(NUM_TOPICS):
    n = lda_model_c.show_topic(topic_id)
    for i, j in n:
        temp[i] = temp.get(i, 0) + cluster_centers[:, topic_id] * j

def keyword_find(topic_id):
    return sorted(temp.keys(), key=lambda x: -temp[x][topic_id])[:10]

keyword_list = [keyword_find(i) for i in range(n_cluster)]

for i in range(n_cluster):
    print(f"{i:>3d} | {sum(cluster_labels == i):>5}개; keyword = {keyword_list[i]}")""")


st.code("""def check_cluster(num, count):

    for row in text_df_dupli_removed[cluster_labels == num]["lyrics"].head(20):
        print('-' * 20)
        print(row)
        print('-' * 20)

        if count == 0: return
        count -= 1
        
check_cluster(0, count=5)""")