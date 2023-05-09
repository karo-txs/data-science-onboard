from dataclasses import dataclass, field
import plotly.express as px
import pandas as pd


@dataclass
class Plotter:
    df: pd.DataFrame
    save_path: str = field(default="results/graphs")

    def line(self, x: str, y: str):
        fig = px.line(self.df, x=x, y=y)
        self.save(fig, f"line_{x}_{y}")
    
    def area(self, facet_col: str):
        fig = px.area(self.df, facet_col=facet_col, facet_col_wrap=2)
        self.save(fig, f"area_{facet_col}")

    def bar(self, x: str, y: str, color: str):
        fig = px.bar(self.df, x=x, y=y, color=color, barmode="group")
        self.save(fig, f"bar_{x}_{y}")
        
    def scatter(self, x: str, y: str, size:str, color: str, hover_name: str):
        fig = px.scatter(self.df, x=x, y=y,
                 size=size, color=color, hover_name=hover_name,
                 log_x=True, size_max=60)
        self.save(fig, f"scatter_{x}_{y}")
    
    def save(self, fig: any, name: str):
        fig.write_html(f"{self.save_path}/{name}.html")