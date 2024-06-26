import random
import json
import numpy as np
import yaml
import cv2
from PIL import Image, ImageDraw


class Processing:
    """
    Класс для работы с входными данными из файла yaml, а так же как база для последующего класса обработки изображения

    """

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


class Handler(Processing):
    """
        Класс для работы с сырыми данными, привёднными в центр изображения координатами для последующего
        расчета среднеквадратичного отклонения и дисперсии

    """

    def __init__(self, img):
        self.image = img

    def set_coordinates_x(self):

        image = cv2.imread(self.image)

        shift_x = image.shape[1] // 2 - self.define_real_centre_x()  # Сдвиг координат к нулю на рисунке

        return shift_x

    def set_coordinates_y(self):

        image = cv2.imread(self.image)

        shift_y = image.shape[0] // 2 - self.define_real_centre_y()

        return shift_y

    def translated_image(self):

        """ Метод обозначающий точку начала координат 0, 0 как середина картинки c визуализацией этой точки """

        image = cv2.imread(self.image)
        x = self.set_coordinates_x()
        y = self.set_coordinates_y()
        translated_image = np.roll(image, x, axis=1)
        translated_image = np.roll(translated_image, y, axis=0)

        cv2.imwrite('test_image.png', translated_image)
        img = Image.open("test_image.png")
        draw = ImageDraw.Draw(img)
        draw.point((self.define_real_centre_x(), self.define_real_centre_y()),
                   fill='red')  # Рисуем красную точку по координатам 10x10
        img.show()
        cv2.waitKey()
        cv2.destroyAllWindows()

    def count_statistics_x(self):

        """
            Метод подсчёта стандартного отклонения и дисперсии по случайно выбранным координатам оси X,
         в методе реализован рандомный набор случайных координат по оси X для имитации случайной выборки

        """

        x = []
        min_value = self.set_coordinates_x()
        step = 0
        while step < 25:
            temp = random.randint(min_value, step)
            x.append(temp)
            step += 1

        data = list(set(x))

        std = np.std(data)

        dispersion = np.var(data)
        return [round(std), round(dispersion), data]

    def count_statistics_y(self):

        """
            Метод подсчёта стандартного отклонения и дисперсии по случайно выбранным координатам оси Y,
         в методе реализован рандомный набор случайных координат по оси Y для имитации случайной выборки

        """

        y = []
        min_value = self.set_coordinates_x()
        step = 0
        while step < 25:
            temp = random.randint(min_value, step)
            y.append(temp)
            step += 1

        data = list(set(y))

        std = np.std(data)

        dispersion = np.var(data)
        return [round(std), round(dispersion), data]

    def publish_statistic_to_json(self):

        """Метод для отправки статистики по расчёту отклонения и дисперсии в json"""

        data_x = self.count_statistics_x()
        data_y = self.count_statistics_y()

        statistic_for_x_y = {
        "x" : {
            "std": data_x[0],
            "dispersion": data_x[1],
            "position": data_x[2]
        },

        "y" : {
             "std": data_y[0],
             "dispersion": data_y[1],
             "position": data_y[2]
        }
        }

        with open('statistics.json', 'w') as file:
            json.dump(statistic_for_x_y, file,  indent=4)


if __name__ == "__main__":
    # process = Processing('spot.png')

    # process.define_centre_position()
    # process.coordinates()
    # process.standart_deviation()
    # process.dispersion()
    # process.position_x()
    # process.position_y()
    # process.define_real_centre_x()
    # process.define_real_centre_y()

    handler = Handler('spot.png')
    # handler.translated_image()
    # handler.count_statistics_x()
    # handler.count_statistics_y()
    handler.publish_statistic_to_json()
