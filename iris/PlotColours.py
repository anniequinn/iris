import numpy as np
import plotly.graph_objects as go


class PlotColours:
    @staticmethod
    def plot(colours, vertical=True):
        n = len(colours)
        z = [list(range(n))]
        text = [[colour for colour in colours] for _ in range(n)]
        
        if vertical:
            z = np.transpose(z)
            text = np.transpose(text)

        trace = {
            "z": z,
            "colorscale": colours,
            "showscale": False,
            "text": text, 
            "texttemplate": "%{text}",
            "textfont_size": 14,
            "hovertemplate": "%{text} <extra></extra>"
        }

        layout = {
            "xaxis": {"showticklabels": False},
            "yaxis": {"showticklabels": False},
            "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
        }

        fig = go.Figure(data=go.Heatmap(**trace), layout=layout)
        fig.show()