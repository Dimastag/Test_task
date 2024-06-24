import numpy as np
import yaml
import cv2


class Processing:

    def __init__(self):
        self.std = self.standart_deviation()
        self.dispersion = self.dispersion()
        self.x = self.position_x()
        self.y = self.position_y()

    def coordinates(self):
        self.data = self.data_parser()
        spisok = self.data.get("position")
        return spisok

    def position_x(self):
        self.coordinates()
        if self.coordinates() and len(self.coordinates()) >= 2:
            x = self.coordinates()[0]
            return x

    def position_y(self):
        self.coordinates()
        if self.coordinates() and len(self.coordinates()) >= 2:
            y = self.coordinates()[1]
            return y

    def standart_deviation(self):
        self.data = self.data_parser()
        return self.data.get("std")

    def dispersion(self):
        self.data = self.data_parser()
        return self.data.get("dispersion")

    def define_centre_position(self):
        image = cv2.imread('spot.png')

        # Нахождение контуров зеленого пятна
        green_lower = np.array([0, 0, 0])
        green_upper = np.array([255, 255, 255])
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, green_lower, green_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Находим координаты центра контура (центр пятна)
        m = cv2.moments(contours[0])
        center_x = int(m["m10"] / m["m00"])
        center_y = int(m["m01"] / m["m00"])

        # Вычисляем сдвиг
        shift_x = image.shape[1] // 2 - center_x
        shift_y = image.shape[0] // 2 - center_y

        # Применяем сдвиг ко всем точкам изображения
        translated_image = np.roll(image, shift_x, axis=1)
        translated_image = np.roll(translated_image, shift_y, axis=0)
        # print(translated_image)

        # Отображаем результат
        # cv2.imshow('Translated Image', translated_image)
        cv2.imwrite('test_image.png', translated_image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    @staticmethod
    def data_parser():
        with open("data.yaml") as r:
            templates = yaml.safe_load(r)
        return templates


if __name__ == "__main__":
    process = Processing()
    process.define_centre_position()
    # process.coordinates()
    # process.standart_deviation()
    # process.dispersion()
    # process.position_x()
    # process.position_y()
