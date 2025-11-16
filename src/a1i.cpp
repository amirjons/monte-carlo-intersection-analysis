// ID: 349291527
#include <iostream>
#include <random>
#include <algorithm>
#include <cmath>

struct Circle {
    double x, y, r;
};

bool is_inside(double x, double y, const Circle& c) {
    double dx = x - c.x;
    double dy = y - c.y;
    return dx*dx + dy*dy <= c.r*c.r;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    Circle circles[3];
    for (int i = 0; i < 3; ++i) {
        std::cin >> circles[i].x >> circles[i].y >> circles[i].r;
    }

    // Находим ограничивающий прямоугольник, который покрывает все три круга
    double x_min = circles[0].x - circles[0].r;
    double x_max = circles[0].x + circles[0].r;
    double y_min = circles[0].y - circles[0].r;
    double y_max = circles[0].y + circles[0].r;

    for (int i = 1; i < 3; ++i) {
        x_min = std::min(x_min, circles[i].x - circles[i].r);
        x_max = std::max(x_max, circles[i].x + circles[i].r);
        y_min = std::min(y_min, circles[i].y - circles[i].r);
        y_max = std::max(y_max, circles[i].y + circles[i].r);
    }

    // Инициализация генератора случайных чисел
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> x_dist(x_min, x_max);
    std::uniform_real_distribution<double> y_dist(y_min, y_max);

    // Количество точек - выбрано для обеспечения точности 0.01
    const int total_points = 1000000;
    int inside_count = 0;

    // Генерация точек и проверка принадлежности пересечению кругов
    for (int i = 0; i < total_points; ++i) {
        double x = x_dist(gen);
        double y = y_dist(gen);
        if (is_inside(x, y, circles[0]) &&
            is_inside(x, y, circles[1]) &&
            is_inside(x, y, circles[2])) {
            inside_count++;
        }
    }

    // Вычисление площади пересечения
    double area_ratio = static_cast<double>(inside_count) / total_points;
    double bounding_area = (x_max - x_min) * (y_max - y_min);
    double intersection_area = area_ratio * bounding_area;

    // Вывод с высокой точностью как в примерах
    std::cout.precision(20);
    std::cout << intersection_area << std::endl;

    return 0;
}
