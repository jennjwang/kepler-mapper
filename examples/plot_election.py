import kmapper as km
import numpy as np
import matplotlib.pyplot as plt
import sys, os
# from kmapper.plotlyviz import plotlyviz 
# import networkx as nx
import sklearn
# from numpy import genfromtxt
import pandas as pd
# import geopandas as gpd
# from statistics import mode

chicago_mayoral = pd.read_csv("data/chicago_mayoral.csv")

mapper = km.KeplerMapper(verbose=1)

salary_cols = [col for col in chicago_mayoral.columns if "K_pct" in col or col == "200K_MORE_pct"]

chicago_dem_df = chicago_mayoral[["BVAP_pct", "HVAP_pct", "WVAP_pct", "GARCIA_G15_pct"] + salary_cols]

chicago_dem_data = np.array(chicago_dem_df)

dem_col_num = chicago_dem_df.columns.get_loc("GARCIA_G15_pct")

lens = mapper.fit_transform(chicago_dem_data, projection = [dem_col_num], scaler=None)

cval1 = chicago_dem_data[:,chicago_dem_df.columns.get_loc("WVAP_pct")]
cval2 = chicago_dem_data[:,chicago_dem_df.columns.get_loc("BVAP_pct")]
cval3 = chicago_dem_data[:,chicago_dem_df.columns.get_loc("HVAP_pct")]
cval4 = chicago_dem_data[:, chicago_dem_df.columns.get_loc('200K_MORE_pct')]

n_cubes = 40
p_overlap = .2

graph = mapper.map(
    lens, 
    chicago_dem_data,
    # clusterer=sklearn.cluster.DBSCAN(eps=0.1, min_samples=5),
    cover = km.Cover(n_cubes=n_cubes, perc_overlap=p_overlap)
)

mapper.visualize(
    graph,
    path_html="output/election.html",
    title="Chicago Mayoral Election",
    color_values=np.c_[cval1, cval2, cval3, cval4], 
    color_function_name=['WVAP_pct', "BVAP_pct", "HVAP_pct", '200K_MORE_pct'],
    node_color_function=["mean", "std", "median", "max"]
)