import json

import pandas as pd

pd.set_option('display.max_columns', None)
import plotly.graph_objects as go

mapbox = 'pk.eyJ1IjoiYXNoZ2F6ZXIiLCJhIjoiY2s0NjI5OTU0MGVsazNlcW05eXp1bjJzYSJ9.nCP8uShNjm2bbqy_QHM2bA'
file_name = "data/birmingham.json"


def load_establishments():
    with open(file_name, 'r') as f:
        bdata = json.load(f)

    return bdata["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"]


def map_to_columns(df, columns_name: str):
    df[columns_name] = df[columns_name].map(lambda x: {} if len(x) == 0 else x)
    df = df.join(pd.json_normalize(df[columns_name]))

    return df


df = pd.DataFrame(load_establishments())
df = map_to_columns(df, "Scores")
df = map_to_columns(df, "Geocode")

ratings = list(map(str, range(0, 4)))
rated_df = df.loc[df['RatingValue'].isin(ratings)]
# rated_df = rated_df[rated_df['RatingValue'].notna()]


def colorcode(v):
    chart = {"0": "darkred", "1": "red", "2": "lightpink", "3": "orange", "4": "lightgreen"}
    return chart.get(v, "black")


rated_df = rated_df[rated_df['Latitude'].notna()]
rated_df['test_col'] = rated_df['BusinessName'].astype(str) + '<br>' + rated_df['RatingValue'] + "<br>" + rated_df['RatingDate'] + "<br>" + rated_df['BusinessType']
rated_df['colorcode'] = rated_df['RatingValue'].apply(colorcode)
rated_df[['Latitude', "Longitude", "test_col", "colorcode"]].to_csv("dummy_data.csv", index=False)


# def return_map_data(df):
#     longitude = list(map(float, df['Longitude']))
#     latitude = list(map(float, df['Latitude']))
#     map_text = list(df['BusinessName'].astype(str) + '<br>' + df['RatingValue'] + "<br>" + df['RatingDate'] + "<br>" + df['BusinessType'])
#     # map_text = list('\n' +df['RatingValue'])
#
#     return longitude, latitude, map_text
#
#
# mapbox_access_token = mapbox
# fig = go.Figure()
# alerts = ["darkred", "red", "lightpink", "orange", "lightgreen", "green"]
# for x in range(4):
#     temp_df = rated_df.loc[rated_df['RatingValue'] == str(x)]
#     long, lat, maptext = return_map_data(temp_df)
#
#     fig.add_scattermapbox(lat=lat,
#                           lon=long,
#                           mode='markers',
#                           marker=go.scattermapbox.Marker(
#                               size=9, color=alerts[x]
#
#                           ),
#                           hovertext=maptext)
#
# fig.update_layout(
#     width=1400,
#     height=1000,
#     autosize=True,
#     hovermode='closest',
#     mapbox=go.layout.Mapbox(
#
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=go.layout.mapbox.Center(
#             lat=52.472139
#             ,
#             lon=-1.930735
#
#         ),
#         pitch=0,
#         zoom=17
#     ),
# )
#
# # fig.show()
# fig.write_html("map2.html", include_plotlyjs="cdn")
#
# #
