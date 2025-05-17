#!/usr/bin/python3
"""
General utility functions.
"""

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, LinearSegmentedColormap

# from labellines import labelLines

# Initialize default palette
C_1 = "xkcd:cobalt"
C_2 = "xkcd:leaf green"
C_3 = "black"
C_4 = "white"
C_SUBDUED = "grey"

# Initialize default color map
CMAP_DIVERGENT = LinearSegmentedColormap.from_list(
    "default-divergent", colors=[C_2, C_4, C_1]
)
CMAP = LinearSegmentedColormap.from_list("default", [C_4, C_1])

# Initialize default truncated color map
# this can be done easier by modifying alpha channel but if there is overlap
# like the 1px edge overlap of bar chart, the shade is darkened
cobalt_rgb = np.array(to_rgb(C_1))
truncated_cobalt_rgb = cobalt_rgb + (1 - cobalt_rgb) * 0.3
colors = [
    (0, truncated_cobalt_rgb),
    (1, C_1),
]
CMAP_TRUNCATED = LinearSegmentedColormap.from_list("default-truncated", colors)

# Initialize subdued truncated color map
grey_rgb = np.array(to_rgb(C_SUBDUED))
truncated_grey_rgb = grey_rgb + (1 - grey_rgb) * 0.3
colors = [
    (0, truncated_grey_rgb),
    (1, C_SUBDUED),
]
CMAP_TRUNCATED_SUBDUED = LinearSegmentedColormap.from_list("subdued-truncated", colors)


def get_numeric_histogram(series, labelsize=10, bins=20):
    """
    Plot a numeric series as a histogram.
    """
    series = series[~series.isna()]
    fig, (ax_box, ax_hist) = plt.subplots(
        nrows=2, gridspec_kw={"height_ratios": [1, 5]}
    )
    ax_box.boxplot(
        series[series >= 0],
        showmeans=True,
        showfliers=True,
        orientation="horizontal",
        widths=0.97,
    )
    ax_box.set_axis_off()
    ax_box.sharex(ax_hist)
    *_, patches = ax_hist.hist(series, bins=bins, color=C_1, alpha=0.8, density=True)
    add_gradient(patches)
    ax_hist.set_ylabel("Proportion")
    ax_hist.tick_params(axis="both", labelsize=labelsize)
    ax_hist.set_xticks([-1, 1, 2, 3, 4, 5, 6], ["unsolved", 1, 2, 3, 4, 5, 6])
    title = series.name.replace("_", " ").title()
    fig.suptitle(title, color=C_1, fontsize=32)
    fig.set_size_inches(12, 8)
    return fig, ax_box, ax_hist


def add_gradient(patches, cmap=CMAP_TRUNCATED):
    """
    Add a colormap gradient to patches from a bar chart or histogram.
    Based on:
    https://stackoverflow.com/questions/60220089/how-to-add-color-gradients-according-to-y-value-to-a-bar-plot
    """
    axes = patches[0].axes
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()
    for patch in patches:
        patch.set_zorder(1)
        patch.set_facecolor("none")
        x_coord, y_coord = patch.get_xy()
        width, height = patch.get_width(), patch.get_height()
        grad = np.linspace(y_coord, y_coord + height, 256).reshape(256, 1)
        if width > 0 and height > 0:
            axes.imshow(
                grad,
                extent=[x_coord, x_coord + width, y_coord, y_coord + height],
                aspect="auto",
                zorder=0,
                origin="lower",
                vmin=ymin,
                vmax=ymax,
                cmap=cmap,
            )
    axes.axis([xmin, xmax, ymin, ymax])
