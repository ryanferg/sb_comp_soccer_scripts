import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
import itertools
from matplotlib.pyplot import cm
import math
import pandas as pd

zline = 8000

zfield = -5000

zheatmap = 7000

zaction = 9000

ztext = 9500

sbomb_config = {
    "length": 120,
    "width": 80,
    "penalty_box_length": 18,
    "penalty_box_width": 62-18,
    "six_yard_box_length": 6,
    "six_yard_box_width": 20,
    "penalty_spot_distance": 12,
    "goal_width": 8,
    "goal_length": 2,
    "origin_x": 0,
    "origin_y": 0,
    "circle_radius": 10,
}

def _plot_rectangle(x1, y1, x2, y2, ax, color):
    ax.plot([x1, x1], [y1, y2], color=color, zorder=zline)
    ax.plot([x2, x2], [y1, y2], color=color, zorder=zline)
    ax.plot([x1, x2], [y1, y1], color=color, zorder=zline)
    ax.plot([x1, x2], [y2, y2], color=color, zorder=zline)


def field(color="white", figsize=None, ax=None, show=True):
    if color == "white":
        return _field(
            ax=ax,
            linecolor="black",
            fieldcolor="white",
            alpha=1,
            figsize=figsize,
            field_config=sbomb_config,
            show=show,
        )
    elif color == "green":
        return _field(
            ax=ax,
            linecolor="white",
            fieldcolor="green",
            alpha=0.4,
            figsize=figsize,
            field_config=sbomb_config,
            show=show,
        )
    else:
        raise Exception("Invalid field color")


def _field(
    ax=None,
    linecolor="black",
    fieldcolor="white",
    alpha=1,
    figsize=None,
    field_config=sbomb_config,
    show=True,
):
    cfg = field_config

    # Create figure
    if ax is None:
        fig = plt.figure()
        ax = fig.gca()

    # Pitch Outline & Centre Line
    x1, y1, x2, y2 = (
        cfg["origin_x"],
        cfg["origin_y"],
        cfg["origin_x"] + cfg["length"],
        cfg["origin_y"] + cfg["width"],
    )

    d = cfg["goal_length"]
    rectangle = plt.Rectangle(
        (x1 - 2 * d, y1 - 2 * d),
        cfg["length"] + 4 * d,
        cfg["width"] + 4 * d,
        fc=fieldcolor,
        alpha=alpha,
        zorder=zfield,
    )
    ax.add_patch(rectangle)
    _plot_rectangle(x1, y1, x2, y2, ax=ax, color=linecolor)
    ax.plot([(x1 + x2) / 2, (x1 + x2) / 2], [y1, y2], color=linecolor, zorder=zline)

    # Left Penalty Area
    x1 = cfg["origin_x"]
    x2 = cfg["origin_x"] + cfg["penalty_box_length"]
    m = (cfg["origin_y"] + cfg["width"]) / 2
    y1 = m - cfg["penalty_box_width"] / 2
    y2 = m + cfg["penalty_box_width"] / 2
    _plot_rectangle(x1, y1, x2, y2, ax=ax, color=linecolor)

    # Right Penalty Area
    x1 = cfg["origin_x"] + cfg["length"] - cfg["penalty_box_length"]
    x2 = cfg["origin_x"] + cfg["length"]
    m = (cfg["origin_y"] + cfg["width"]) / 2
    y1 = m - cfg["penalty_box_width"] / 2
    y2 = m + cfg["penalty_box_width"] / 2
    _plot_rectangle(x1, y1, x2, y2, ax=ax, color=linecolor)

    # Left 6-yard Box
    x1 = cfg["origin_x"]
    x2 = cfg["origin_x"] + cfg["six_yard_box_length"]
    m = (cfg["origin_y"] + cfg["width"]) / 2
    y1 = m - cfg["six_yard_box_width"] / 2
    y2 = m + cfg["six_yard_box_width"] / 2
    _plot_rectangle(x1, y1, x2, y2, ax=ax, color=linecolor)

    # Right 6-yard Box
    x1 = cfg["origin_x"] + cfg["length"] - cfg["six_yard_box_length"]
    x2 = cfg["origin_x"] + cfg["length"]
    m = (cfg["origin_y"] + cfg["width"]) / 2
    y1 = m - cfg["six_yard_box_width"] / 2
    y2 = m + cfg["six_yard_box_width"] / 2
    _plot_rectangle(x1, y1, x2, y2, ax=ax, color=linecolor)

    # Left Goal
    x1 = cfg["origin_x"] - cfg["goal_length"]
    x2 = cfg["origin_x"]
    m = (cfg["origin_y"] + cfg["width"]) / 2
    y1 = m - cfg["goal_width"] / 2
    y2 = m + cfg["goal_width"] / 2
    _plot_rectangle(x1, y1, x2, y2, ax=ax, color=linecolor)

    # Right Goal
    x1 = cfg["origin_x"] + cfg["length"]
    x2 = cfg["origin_x"] + cfg["length"] + cfg["goal_length"]
    m = (cfg["origin_y"] + cfg["width"]) / 2
    y1 = m - cfg["goal_width"] / 2
    y2 = m + cfg["goal_width"] / 2
    _plot_rectangle(x1, y1, x2, y2, ax=ax, color=linecolor)

    # Prepare Circles
    mx, my = (cfg["origin_x"] + cfg["length"]) / 2, (cfg["origin_y"] + cfg["width"]) / 2
    centreCircle = plt.Circle(
        (mx, my), cfg["circle_radius"], color=linecolor, fill=False, zorder=zline
    )
    centreSpot = plt.Circle((mx, my), 0.4, color=linecolor, zorder=zline)

    lx = cfg["origin_x"] + cfg["penalty_spot_distance"]
    leftPenSpot = plt.Circle((lx, my), 0.4, color=linecolor, zorder=zline)
    rx = cfg["origin_x"] + cfg["length"] - cfg["penalty_spot_distance"]
    rightPenSpot = plt.Circle((rx, my), 0.4, color=linecolor, zorder=zline)

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    r = cfg["circle_radius"] * 2
    leftArc = Arc(
        (lx, my),
        height=r,
        width=r,
        angle=0,
        theta1=307,
        theta2=53,
        color=linecolor,
        zorder=zline,
    )
    rightArc = Arc(
        (rx, my),
        height=r,
        width=r,
        angle=0,
        theta1=127,
        theta2=233,
        color=linecolor,
        zorder=zline,
    )

    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    if figsize:
        h, w = fig.get_size_inches()
        newh, neww = figsize, w / h * figsize
        fig.set_size_inches(newh, neww, forward=True)
    plt.ylim(max(plt.ylim()), min(plt.ylim()))


    return ax