import matplotlib.pyplot as plt


def gray_imshow(image, title=None, ax=None, border=True):
    if ax is None:
        ax = plt.gca()

    ax.imshow(image, cmap="gray")
    ax = _set_border(ax, border)
    ax = _set_title(ax, title)
    return ax


def rgb_imshow(image, title=None, ax=None, border=True):
    if ax is None:
        ax = plt.gca()

    ax.imshow(image)
    ax = _set_border(ax, border)
    ax = _set_title(ax, title)
    return ax


def bgr_imshow(image, title=None, ax=None, border=True):
    return rgb_imshow(image[..., ::-1], title, ax, border)


def _set_border(ax, border):
    if border:
        ax.set(xticks=[], yticks=[])
    else:
        ax.axis("off")
    return ax


def _set_title(ax, title):
    if title is not None:
        ax.set_title(title)
    return ax


