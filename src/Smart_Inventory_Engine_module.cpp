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

    Product* find_product_by_name(const std::string& name)
    {
        for (Product& product : items)
        {
            if (product.name == name)
            {
                return &product;
            }
        }
        return nullptr;
    }

    bool update_stock(const std::string& name, int new_stock)
    {
        Product* product = find_product_by_name(name);
        if (product == nullptr)
        {
            return false;
        }

        product->stock = new_stock;
        return true;
    }

    bool remove_product(const std::string& name)
    {
        auto it = std::find_if(items.begin(), items.end(),
            [&name](const Product& p){return p.name == name;});
        if (it == items.end())
            return false;
        items.erase(it);
        return true;
    }

    size_t remove_all_products(const std::string& name)
    {
        auto old_size = items.size();
        items.erase(std::remove_if(items.begin(), items.end(),
            [&name](const Product& p){return p.name == name;}), items.end());
        return old_size - items.size();
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
        .def("sort_items_by_price", &Inventory::sort_items_by_price)
        .def("find_product_by_name", &Inventory::find_product_by_name, py::return_value_policy::reference)
        .def("update_stock", &Inventory::update_stock, py::arg("name"), py::arg("new_stock"))
        .def("remove_product", &Inventory::remove_product, py::arg("name"))
        .def("remove_all_products", &Inventory::remove_all_products, py::arg("name"))
        .def_readwrite("items", &Inventory::items);
}