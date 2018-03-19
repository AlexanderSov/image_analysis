from PIL import Image, ImageDraw
from skimage import img_as_float, exposure
from skimage.io import imread, imsave

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class ImageTransform:
    def __init__(self, path):
        self.path = path
        self.path_new = None
        self.letter = None
        self.image = Image.open(self.path)
        self.draw = ImageDraw.Draw(self.image)
        # для рисования.
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

        self.image2 = imread(self.path)
        self.path3 = ''

    def do_new_path(self):
        self.path_new = self.path.split('.')[0] + self.letter + \
                        '.' + self.path.split('.')[-1]

    def transform_picture(self, mode):
        mode_list = ["f", 'h', 'd', 'min', 'max', "g"]
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.pix[i, j]
                if mode == 0:
                    s = (r + g + b) // 3
                elif mode == 1:
                    s = round(0.3 * r + 0.59 * g + 0.11 * b)
                elif mode == 2:
                    s = (min(r, g, b) + max(r, g, b)) // 2
                elif mode == 3:
                    s = min(r, g, b)
                elif mode == 4:
                    s = max(r, g, b)
                self.draw.point((i, j), (s, s, s))
        self.letter = mode_list[mode]
        self.do_new_path()
        self.image.save(self.path_new)

    def make_bar_chart(self, changed, ackv):
        img = self.image2
        if ackv == 0:
            img_1 = img
        elif ackv == 1:
            img_1 = exposure.equalize_hist(img)
        matplotlib.rcParams['font.size'] = 8

        def plot_img_and_hist(image, axes, bins=256):
            image = img_as_float(image)
            ax_img, ax_hist = axes
            # ax_cdf = ax_hist.twinx()

            # Display histogram
            ax_hist.hist(image.ravel(), bins=bins, histtype='step',
                         color='black')
            ax_hist.ticklabel_format(axis='y', style='scientific',
                                     scilimits=(0, 0))
            ax_hist.set_xlabel('Pixel intensity')
            ax_hist.set_xlim(0, 1)
            ax_hist.set_yticks([])

            # Display cumulative distribution
            # img_cdf, bins = exposure.cumulative_distribution(image, bins)
            # ax_cdf.plot(bins, img_cdf, 'r')
            # ax_cdf.set_yticks([])
            return ax_img, ax_hist
        fig = plt.figure(figsize=(8, 5))
        axes = np.zeros((2, 4), dtype=np.object)
        axes[1, 0] = fig.add_subplot(1, 1, 1)
        ax_img, ax_hist = plot_img_and_hist(img_1, axes[:, 0])
        fig.tight_layout()

        self.letter = 'g'
        self.do_new_path()
        fig.savefig(self.path_new)
        imsave(self.path3, img_1)

    def make_bar_chart_2(self, changed, ackv):
        bar_chart_list = [0 for x in range(256)]
        if changed:
            for i in range(self.width):
                for j in range(self.height):
                    s = self.pix[i, j][0]
                    bar_chart_list[s] += 1
            image = Image.new('L', size=(256, 500), color=255)
            draw = ImageDraw.Draw(image)
            tot = sum(bar_chart_list)
            tot_10 = round(tot / 10)
            if ackv == 1:
                bar_chart_list_1 = []
                for number in bar_chart_list:
                    if number != 0:
                        bar_chart_list_1.append(number)
                cdf_min = min(bar_chart_list_1)
                bar_chart_list_new = []
                for t in range(len(bar_chart_list)):
                    cdf = sum(bar_chart_list[:t])
                    new_value = round(((cdf - cdf_min) * 255) / tot)  # new
                    if new_value >= 0:
                        bar_chart_list_new.append(new_value)
                    else:
                        bar_chart_list_new.append(0)
                bar_chart_list = bar_chart_list_new
            else:
                pass
            for k in range(256):
                y = 500 - 500 * bar_chart_list[k] / tot_10
                draw.line([(k, 500),
                           (k, y)],
                          fill=0, width=3)
            self.letter = 'g'
            self.do_new_path()
            image.save(self.path_new)

    def get_color(self, mode):
        img_f = img_as_float(self.image2)
        link = img_f[:, :, mode]
        self.letter = str(mode)
        self.do_new_path()
        imsave(self.path_new, link)

    def apply_matrix(self, matrix_size, matrix):
        indent = (matrix_size - 1) // 2
        div, div1 = 0, 0
        for i in range(indent, self.width-indent):
            for j in range(indent, self.height-indent):
                s = 0
                for k in range(matrix_size):
                    for l in range(matrix_size):
                        s += self.pix[i-indent+k, j-indent+l][0] * matrix[k][l]
                        if div == 0 and i == indent and j == indent:
                            div1 += matrix[k][l]
                div = div1
                s1 = s // div
                self.draw.point((i, j), (s1, s1, s1))
        self.letter = 'matrix'
        self.do_new_path()
        self.image.save(self.path_new)
