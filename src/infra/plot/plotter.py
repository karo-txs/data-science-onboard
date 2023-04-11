from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import pandas as pd


@dataclass
class Plotter:
    df: pd.DataFrame
    save_path: str = field(default="results/graphs")

    def hist(self, attr: str):
        plt.hist(self.df[attr], bins=10)
        plt.xlabel(attr)
        plt.ylabel("count")
        plt.title(f"Distribution of Movie {attr}")
        plt.savefig(f"{self.save_path}/hist_{attr}")
    
    def scatter(self, attr_a: str, attr_b: str):
        plt.scatter(self.df[attr_a], self.df[attr_b])
        plt.xlabel(attr_a)
        plt.ylabel(attr_b)
        plt.title(f"Relationship between {attr_a} and {attr_b}")
        plt.savefig(f"{self.save_path}/scatter_{attr_a}_{attr_b}")
