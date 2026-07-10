#include <algorithm>
#include <vector>
#include <string>
#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;


struct Product
{
    std::string name;
    int price = 0;
    int stock = 0;
    int threshold = 0;
};

struct Inventory
{
    std::vector<Product> items;

    void add_product(const Product& new_product)
    {
        items.push_back(new_product);
    }

    [[nodiscard]] int calculate_total_value() const
    {
        int total = 0;

        for (const Product& product : items)
        {
            total += product.price * product.stock;
        }

        return total;
    }

    [[nodiscard]] std::vector<Product> get_low_stock_items() const
    {
        std::vector<Product> low_stock_items;

        for (const Product& product : items)
        {
            if (product.stock <= product.threshold)
            {
                low_stock_items.push_back(product);
            }
        }
        return low_stock_items;
    }

    void sort_items_by_price()
    {
        std::sort(items.begin(), items.end(), [](const Product& a, const Product& b)
        {
            return a.price < b.price;
        });
    }
};


PYBIND11_MODULE(Smart_Inventory_Engine_module, m)
{
    py::class_<Product>(m, "Product")
        .def(py::init<>())
        .def_readwrite("name", &Product::name)
        .def_readwrite("price", &Product::price)
        .def_readwrite("stock", &Product::stock)
        .def_readwrite("threshold", &Product::threshold);

    py::class_<Inventory>(m, "Inventory")
        .def(py::init<>())
        .def("add_product", &Inventory::add_product, py::arg("product"))
        .def("calculate_total_value", &Inventory::calculate_total_value)
        .def("get_low_stock_items", &Inventory::get_low_stock_items)
        .def("sort_items_by_price", &Inventory::sort_items_by_price);
}