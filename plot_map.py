#!/usr/bin/env python

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_json("./zillscrape/out.json")
header = list(df)

print(header)

print(df.latLong)
print(df.description)
lat = [d[0]["latitude"] for d in df.latLong]
long = [d[0]["longitude"] for d in df.latLong]

new_df = df[['zpid', 'address', 'price']]
new_df['zpid'] = new_df['zpid'].apply(lambda x: x[0])
new_df['address'] = new_df['address'].apply(lambda x: x[0])
new_df['price'] = new_df['price'].apply(lambda x: x[0])
new_df['latitude'] = lat
new_df['longitude'] = long

fig = px.scatter_mapbox(new_df, 
                        lat="latitude", 
                        lon="longitude", 
                        hover_name="address", 
                        hover_data=["zpid", "address", "price"],
                        zoom=8, 
                        height=800,
                        width=1200)
fig.update_traces(
    marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(100, 100, 255)',
            opacity=0.75
        )
    )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
