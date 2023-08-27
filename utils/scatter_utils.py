import numpy as np
from adjustText import adjust_text
from utils.regional_utils import get_best_fit_line, get_r_squared
import matplotlib.pyplot as plt


class ScatterPlotBase:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.annotate_props = {
            "fontsize": 12,
            "color": "red",
            "xycoords": "axes fraction",
        }

    def _plot_best_fit_line(self):
        fit_line, fit_line_text = get_best_fit_line(self.x, self.y)
        plt.plot(self.x, fit_line, color="red", label="Best Fit Line")
        plt.annotate(fit_line_text, xy=(0.5, 0.45), **self.annotate_props)

    def _plot_r_squared_annotation(self):
        _, r_squared_text = get_r_squared(self.x, self.y)
        plt.annotate(r_squared_text, xy=(0.5, 0.4), **self.annotate_props)

    def _plot_main_scatter(self):
        plt.scatter(self.x, self.y, s=100, c="blue", alpha=0.7)
        plt.tick_params(axis="both", which="major", labelsize=16)
        plt.xlabel("Total Household Income", size=16)

    def plot(self):
        plt.figure(figsize=(10, 5))
        self._plot_main_scatter()
        self._plot_best_fit_line()
        self._plot_r_squared_annotation()
        plt.show()


class ScatterPlotRegional(ScatterPlotBase):
    def __init__(self, data, key):
        self.x = data.groupby("Region")["Total Household Income"].mean()
        self.y = data.groupby("Region")[key].mean()
        super().__init__(self.x, self.y)
        
    def _plot_main_scatter(self):
        plt.scatter(self.x, self.y, s=100, c="blue", alpha=0.7)
        plt.tick_params(axis="both", which="major", labelsize=16)
        plt.xlabel("Average Total Household Income", size=16)

        # Add region labels to the data points
        texts = [
            plt.annotate(
                region.split()[0],
                (income, expenditure),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=12,
            )
            for region, income, expenditure in zip(self.y.index, self.x, self.y)
        ]
        adjust_text(texts, only_move={"points": "y", "texts": "y"})
        
        
def regional_scatter_plot(data, key):
    return ScatterPlotRegional(data, key).plot()

def basic_scatter_plot(x, y):
    return ScatterPlotBase(x, y).plot()