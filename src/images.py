import matplotlib.pyplot as plt
from matplotlib.image import AxesImage

squares = {
    "⬛": plt.imread("resources/squares/black.png"),
    "🟦": plt.imread("resources/squares/blue.png"),
    "🟫": plt.imread("resources/squares/brown.png"),
    "🟩": plt.imread("resources/squares/green.png"),
    "🟥": plt.imread("resources/squares/red.png"),
    "⬜": plt.imread("resources/squares/white.png"),
    "🟪": plt.imread("resources/squares/purple.png"),
    "🟨": plt.imread("resources/squares/yellow.png"),
    "🟧": plt.imread("resources/squares/orange.png"),
    "🔳": plt.imread("resources/squares/waiting_zone.png"),
}

faces = {
    "😀": plt.imread("resources/faces/smiling.png"),
    "😁": plt.imread("resources/faces/smiling2.png"),
    "🤔": plt.imread("resources/faces/thinking.png"),
    "😶": plt.imread("resources/faces/without_mouth.png"),
    "🙄": plt.imread("resources/faces/white_eyes.png"),
    "😎": plt.imread("resources/faces/sunglasses.png"),
    "😐": plt.imread("resources/faces/neutral.png"),
    "😰": plt.imread("resources/faces/anxiety.png"),
}

def place_image(ax: plt.Axes, img, x, y) -> AxesImage:
    return ax.imshow(img, extent=[x, x + 1, y, y + 1])