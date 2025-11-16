#include <iostream>
#include <random>
#include <cmath>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

struct Circle {
    double x, y, r;
};

bool is_inside(double x, double y, const Circle& c) {
    double dx = x - c.x;
    double dy = y - c.y;
    return dx*dx + dy*dy <= c.r*c.r;
}

double monte_carlo(int n, double x_min, double x_max, double y_min, double y_max, const vector<Circle>& circles) {
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> x_dist(x_min, x_max);
    uniform_real_distribution<double> y_dist(y_min, y_max);

    int inside_count = 0;
    for (int i = 0; i < n; i++) {
        double x = x_dist(gen);
        double y = y_dist(gen);
        bool in_all = true;
        for (const Circle& c : circles) {
            if (!is_inside(x, y, c)) {
                in_all = false;
                break;
            }
        }
        if (in_all) inside_count++;
    }

    double area_ratio = static_cast<double>(inside_count) / n;
    return area_ratio * (x_max - x_min) * (y_max - y_min);
}

int main() {
    // Заданные круги для эксперимента A1
    vector<Circle> circles = {
        {1.0, 1.0, 1.0},
        {1.5, 2.0, sqrt(5.0)/2},
        {2.0, 1.5, sqrt(5.0)/2}
    };

    // Точное значение площади
    double S_exact = 0.25 * M_PI + 1.25 * asin(0.8) - 1;

    // Области генерации точек
    double wide_x_min = 0.0, wide_x_max = 3.0, wide_y_min = 0.0, wide_y_max = 3.0;
    double narrow_x_min = 1.0, narrow_x_max = 2.0, narrow_y_min = 1.0, narrow_y_max = 2.0;

    ofstream out("experiment_results.csv");
    out << "N,wide_area,wide_error,narrow_area,narrow_error" << endl;

    const int repeats = 10; // Количество повторений для усреднения

    cout << "Starting experiment..." << endl;
    cout << "Exact area: " << S_exact << endl;

    for (int n = 100; n <= 100000; n += 500) {
        double wide_sum = 0.0;
        double narrow_sum = 0.0;

        // Многократный запуск для усреднения
        for (int r = 0; r < repeats; r++) {
            wide_sum += monte_carlo(n, wide_x_min, wide_x_max, wide_y_min, wide_y_max, circles);
            narrow_sum += monte_carlo(n, narrow_x_min, narrow_x_max, narrow_y_min, narrow_y_max, circles);
        }

        double wide_avg = wide_sum / repeats;
        double narrow_avg = narrow_sum / repeats;

        double wide_error = fabs(wide_avg - S_exact) / S_exact;
        double narrow_error = fabs(narrow_avg - S_exact) / S_exact;

        out << n << "," << wide_avg << "," << wide_error << "," << narrow_avg << "," << narrow_error << endl;

        // Прогресс
        if (n % 10000 == 0) {
            cout << "Progress: " << n << "/100000" << endl;
        }
    }

    out.close();
    cout << "Эксперимент удался. Результат сохранён в experiment_results.csv" << endl;

    return 0;
}