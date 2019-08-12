import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from flask import Flask,jsonify,request

anime = pd.read_csv("anime.csv")
anime.head()

anime.loc[(anime["genre"]=="Hentai") & (anime["episodes"]=="Unknown"),"episodes"] = "1"
anime.loc[(anime["type"]=="OVA") & (anime["episodes"]=="Unknown"),"episodes"] = "1"

anime.loc[(anime["type"] == "Movie") & (anime["episodes"] == "Unknown")] = "1"

known_animes = {"Naruto Shippuuden":500, "One Piece":784,"Detective Conan":854, "Dragon Ball Super":86,
                "Crayon Shin chan":942, "Yu Gi Oh Arc V":148,"Shingeki no Kyojin Season 2":25,
                "Boku no Hero Academia 2nd Season":25,"Little Witch Academia TV":25}

for k,v in known_animes.items():    
    anime.loc[anime["name"]==k,"episodes"] = v

anime["episodes"] = anime["episodes"].map(lambda x:np.nan if x=="Unknown" else x)    

anime["episodes"].fillna(anime["episodes"].median(),inplace = True)

anime["rating"] = anime["rating"].astype(float)
anime["rating"].fillna(anime["rating"].median(),inplace = True)

pd.get_dummies(anime[["type"]]).head()

anime["members"] = anime["members"].astype(float)

anime_features = pd.concat([anime["genre"].str.get_dummies(sep=","),
                            pd.get_dummies(anime[["type"]]),anime[["rating"]],anime[["members"]],anime["episodes"]],axis=1)

anime["name"] = anime["name"].map(lambda name:re.sub('[^A-Za-z0-9]+', " ", name))   
anime["name2"] = anime["name"].str.lower() 
anime["name2"] = anime["name2"].str.strip() 
anime["name2"] = anime["name2"].str.replace(" ","") 

anime["name2"] = anime["name2"].replace('\\n','', regex=True)



from sklearn.preprocessing import MaxAbsScaler
max_abs_scaler = MaxAbsScaler()
anime_features = max_abs_scaler.fit_transform(anime_features)


from sklearn.neighbors import NearestNeighbors
nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(anime_features)
distances, indices = nbrs.kneighbors(anime_features)

all_anime_names = list(anime.name.values)
all_anime_names2 = list(anime.name2.values)

def get_index_from_name(name):
    return anime[anime["name"]==name].index.tolist()[0]
    
def get_index_from_name2(name):
    name2 = name.lower()
    name2 = name2.replace(' ', '')
    #print(name2)
    animes = anime[anime["name2"]==name2].index.tolist()
    if(animes):
        #print(animes[0])
        return anime[anime["name2"]==name2].index.tolist()[0] 
    else:
        #print("Null")
        return 0
    #return anime[anime["name2"]==name2].index.tolist()[0]    




def print_similar_animes2(query=None):
    animelist = []
    animelist2 = []
    if query:
        found_id = get_index_from_name2(query)
        #print(found_id)
        if(found_id):
            for id in indices[found_id][1:]:
                #print(id)
                #print(anime.iloc[id]["name"])
                t = anime.iloc[id]["name"]
                animelist.append(t)
                #print(t)
                #print(animelist)
            return animelist    
        else:
            return animelist2
            

















 