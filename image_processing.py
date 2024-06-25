import numpy as np
import yaml
import cv2
import PIL as plt
from PIL import Image, ImageDraw


class Processing:

    def __init__(self, img):
        self.image = img
        self.std = self.standart_deviation()
        self.disp = self.dispersion()
        self.x = self.position_x()
        self.y = self.position_y()
        self.real_x = self.define_real_centre_x()
        self.real_y = self.define_real_centre_y()

    def coordinates(self):

        """ Метод для определения координат по оси x и y из файла yaml """

        self.data = self.data_parser()
        spisok = self.data.get("position")
        return spisok

    def position_x(self):

        """ Метод для определения координат по оси x из файла yaml """

        self.coordinates()
        if self.coordinates() and len(self.coordinates()) >= 2:
            x = self.coordinates()[0]
            return x

    def position_y(self):

        """ Метод для определения координат по оси y из файла yaml """

        self.coordinates()
        if self.coordinates() and len(self.coordinates()) >= 2:
            y = self.coordinates()[1]
            return y

    def standart_deviation(self):

        """ Метод для определения стандартного отклонения из файла yaml """

        self.data = self.data_parser()
        return self.data.get("std")

    def dispersion(self):

        """ Метод для определения дисперсии из файла yaml """

        self.data = self.data_parser()
        return self.data.get("dispersion")

    def define_real_centre_x(self):

        """ Метод определяет реальные координаты центра пятна по оси x """

        image = cv2.imread(self.image)

        green_lower = np.array([0, 0, 0])  # Определение оттенков зелёного пятна нижняя и верхние границы
        green_upper = np.array([255, 255, 255])
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, green_lower, green_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Определение координаты x
        m = cv2.moments(contours[0])
        center_x = int(m["m10"] / m["m00"])

        return center_x

    def define_real_centre_y(self):

        """ Метод определяет реальные координаты центра пятна по оси y  """

        image = cv2.imread(self.image)

        green_lower = np.array([0, 0, 0])  # Определение оттенков зелёного пятна нижняя и верхние границы
        green_upper = np.array([255, 255, 255])
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, green_lower, green_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #  Определение координаты y
        m = cv2.moments(contours[0])

        center_y = int(m["m01"] / m["m00"])

        return center_y

    @staticmethod
    def data_parser():
        with open("data.yaml") as r:
            sample_json = yaml.safe_load(r)
        return sample_json


class Handler:

    def __init__(self):
        pass

    def find_coordinates(self):
        pass

    def find_dispersion(self):
        pass

    def find_std(self):
        pass

    def statistics(self, data_input):
        st_dev = data_input
        st_dev_out = np.std(st_dev)
        disp = np.var(data_input)
        disp_out = np.average(disp)
        return [round(st_dev_out), round(disp_out)]

    # def define_centre_position(self):
    #     image = cv2.imread('spot.png')
    #     green_lower = np.array([0, 0, 0])  # Нахождение контуров зеленого пятна
    #     green_upper = np.array([255, 255, 255])
    #     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #     mask = cv2.inRange(hsv, green_lower, green_upper)
    #     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    #     # Находим координаты центра контура (центр пятна)
    #     m = cv2.moments(contours[0])
    #     center_x = int(m["m10"] / m["m00"])
    #     center_y = int(m["m01"] / m["m00"])
    #
    #     # Вычисляем сдвиг
    #     shift_x = image.shape[1] // 2 - center_x
    #     shift_y = image.shape[0] // 2 - center_y
    #
    #     # Применяем сдвиг ко всем точкам изображения
    #     translated_image = np.roll(image, shift_x, axis=1)
    #     translated_image = np.roll(translated_image, shift_y, axis=0)
    #     # print(translated_image)
    #
    #     # Отображаем результат
    #     # cv2.imshow('Translated Image', translated_image)
    #     cv2.imwrite('test_image.png', translated_image)
    #     # plt.imshow('test_image.png')
    #     # plt.show()
    #     img = Image.open("test_image.png")
    #     draw = ImageDraw.Draw(img)
    #     draw.point((center_x, center_y), fill='red')  # Рисуем красную точку по координатам 100x100
    #     img.show()
    #     cv2.waitKey()
    #     cv2.destroyAllWindows()


if __name__ == "__main__":
    process = Processing('spot.png')

    # process.define_centre_position()
    # process.coordinates()
    # process.standart_deviation()
    # process.dispersion()
    # process.position_x()
    # process.position_y()
    # process.define_real_centre_x()
    # process.define_real_centre_y()

    # handler = Handler()
