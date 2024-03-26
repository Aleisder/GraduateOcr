# from dash import Dash, callback, Output, Input
# from dash.exceptions import PreventUpdate
# from dash import html
# from dash.development.base_component import Component
#
#
# class TestComponent(html.Plaintext):
#
#     def __init__(self, component_id: str, test_property: str):
#         super().__init__([
#             html.Plaintext(
#                 id=component_id,
#                 children='example'
#             )
#         ])
#
#
# app = Dash(__name__)
#
# app.layout = html.Div([
#     TestComponent(
#         component_id='plain_text',
#         test_property='test-test'
#     ),
#     html.Button(id='test-button', children='Click')
# ])
#
#
# @callback(
#     Output('plain_text', 'test_property'),
#     Input('test-button', 'n_clicks')
# )
# def test_custom_property(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     return 'done'
#
#
# if __name__ == '__main__':
#     app.run(
#         debug=True
#     )


from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd

app = Dash(__name__)
app.layout = html.Div([
    html.Button("Download Excel", id="btn_xlsx"),
    dcc.Download(id="download-dataframe-xlsx"),
])


df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})


@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_string(df.to_json, "mydf.json")


# if __name__ == "__main__":
#     app.run(debug=True)

arr = [77.8, 75.8, 75.9, 98.2, 98.6, 93.5, 102, 94.1, 95.2, 93.8, 94.3, 93.8]
print(max(arr))
print(min(arr))
print(sum(arr) / len(arr))