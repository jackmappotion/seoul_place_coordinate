import numpy as np
import pandas as pd
import geopandas as gpd

FILE_PATH = "./data/서울시 주요 115장소 영역/서울시 주요 115장소 영역.shp"


def read_shp_file(file_path):
    gdf = gpd.read_file(file_path)
    return gdf


polygon2coords = lambda poligon: poligon.exterior.coords
coords2lng = lambda coords: list(map(lambda coord: coord[0], coords))
coords2lat = lambda coords: list(map(lambda coord: coord[1], coords))

def format_all_coord_df(gdf):
    gdf_all_coord_df = pd.concat(
        [
            gdf.drop(columns=["geometry"]),
            gdf["geometry"]
            .apply(lambda x: (list(polygon2coords(x))))
            .apply(pd.Series),
        ],
        axis=1,
    )
    return gdf_all_coord_df


def format_mean_coord_df(gdf):
    gdf_mean_coord_df = pd.concat(
        [
            gdf.drop(columns=["geometry"]),
            gdf["geometry"]
            .apply(
                lambda x: {
                    "lat": np.mean(coords2lat(polygon2coords(x))),
                    "lng": np.mean(coords2lng(polygon2coords(x))),
                }
            )
            .apply(pd.Series),
        ],
        axis=1,
    )
    return gdf_mean_coord_df


if __name__ == "__main__":
    gdf = read_shp_file(FILE_PATH)
    
    # all_coord
    all_coord_df = format_all_coord_df(gdf)
    all_coord_df.to_csv("./all_coord_df.csv")
    # mean_coord
    mean_coord_df = format_mean_coord_df(gdf)
    mean_coord_df.to_csv("./mean_coord_df.csv")
