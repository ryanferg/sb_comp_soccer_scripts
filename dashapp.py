import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html,ctx,State
import pandas as pd
import plotly.graph_objects as go
import os


cur_dir=os.path.dirname(__file__)
passDF=pd.read_csv(os.path.join(cur_dir,'passDF.csv'))
player_options=passDF[['player_id','player_name']].drop_duplicates().rename(columns={'player_id':'value','player_name':'label'}).to_dict(orient='records')
gameDF=pd.read_csv(os.path.join(cur_dir,'gameDF.csv'))


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Player Explorer", className="display-4"),
        html.Hr(),
        dcc.Dropdown(id="player_search_drop", options=player_options,placeholder='select player'),
        dcc.Dropdown(id="match_drop",placeholder='select match',disabled=False),
    ],
    style=SIDEBAR_STYLE,
)

center=c_x,c_y=60,40
field_shapes=[dict(type="rect",x0=0,y0=0,x1=120,y1=80,layer="below"),
dict(type="rect",x0=0,y0=18,x1=18,y1=62,layer="below"),
dict(type="rect",x0=102,y0=18,x1=120,y1=62,layer="below"),
dict(type="rect",x0=0,y0=30,x1=6,y1=50,layer="below"),
dict(type="rect",x0=114,y0=30,x1=120,y1=50,layer="below"),
dict(type="rect",x0=-2,y0=35,x1=0,y1=44,layer="below"),
dict(type="rect",x0=120,y0=35,x1=122,y1=44,layer="below"),
dict(type="circle",x0=50,y0=30,x1=70,y1=50,layer="below"),
dict(type="line",x0=60,y0=0,x1=60,y1=80,layer="below"),
dict(type="path",path="M 18,32 C 25,35 25,45 18,48",layer="below"),
dict(type="path",path="M 102,32 C 95,35 95,45 102,48",layer="below")]

xaxis=go.layout.XAxis(range=[-5,125],showgrid=False,zeroline=False)
yaxis=go.layout.YAxis(range=[85,-5],showgrid=False,zeroline=False,scaleanchor='x',scaleratio=1)
margin=go.layout.Margin(l=0, r=0, b=3, t=50, pad=10)
layout=go.Layout(shapes=field_shapes,xaxis=xaxis,yaxis=yaxis,margin=margin,width=900,height=600)

fig=go.Figure(layout=layout)

content =html.Div([dcc.Graph(id='figure',figure=fig,config=dict(fillFrame=True))],                    style={
                        "position": "relative",
                        "display": "flex",
                        "justify-content": "center"})
app.layout = dbc.Container(dbc.Row([dbc.Col(sidebar),content]))


@app.callback(Output("match_drop", "options"),Output("match_drop", "value"), [Input("player_search_drop", "value")],prevent_initial_call=True)
def get_player_matches(player_id):
    player_matches=passDF.loc[passDF.player_id==player_id,'match_id'].unique()
    return gameDF.loc[gameDF.match_id.isin(player_matches),['match_id','match_name']].rename(columns={'match_id':'value','match_name':'label'}).to_dict(orient='records'),None


@app.callback(Output("figure", "figure"), [Input('match_drop','value'),Input('player_search_drop','value')],prevent_initial_call=True)
def output_plot(match_id,player_id):
    fig=go.Figure(layout=layout)
    if((ctx.triggered_id=='match_drop') & (match_id is not None)):
        selDF=passDF.loc[(passDF.player_id==player_id)&(passDF.match_id==match_id)].dropna(subset=['end_location_x'])
        arrow_list=[dict(x= x_end,
                    y= y_end,   
                    xref="x", yref="y",
                    text="",
                    showarrow=True,
                    axref = "x", ayref='y',
                    ax= x_start,
                    ay= y_start,
                    arrowhead = 3,
                    arrowwidth=1.5) for x_start,y_start,x_end,y_end in selDF[['location_x','location_y','end_location_x','end_location_y']].values]
        fig.add_trace(go.Scatter(x=selDF.location_x,y=selDF.location_y,text=selDF.xT_str,customdata=selDF.id,hovertemplate="xT = %{text}<extra></extra>",mode='markers',marker_size=10))
        fig.update_layout(annotations=arrow_list)
    return fig

if __name__ == "__main__":
    app.run(port=8118,debug=True,dev_tools_hot_reload=False)