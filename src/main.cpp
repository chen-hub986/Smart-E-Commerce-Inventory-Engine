#include <algorithm>
#include <vector>
#include <string>
#include <iostream>


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

    // convenience overload: construct Product in-place from parameters
    void add_product(const std::string& name, int price, int stock, int threshold = 0)
    {
        items.push_back(Product{ name, price, stock, threshold });
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

int main() {
    Inventory inv;
    inv.add_product("keyboard", 2500, 2, 3); // threshold = 3
    inv.add_product("mouse",    800, 10, 2); // threshold = 2
    inv.add_product("cable",    100, 4, 5);  // threshold = 5

    // Show total value
    std::cout << "Total inventory value: " << inv.calculate_total_value() << '\n';

    // Show items before sorting
    std::cout << "Items before sorting by price:\n";
    for (const auto& p : inv.items) {
        std::cout << "  " << p.name << " price=" << p.price << " stock=" << p.stock << '\n';
    }

    // Sort by price and show after
    inv.sort_items_by_price();
    std::cout << "Items after sorting by price:\n";
    for (const auto& p : inv.items) {
        std::cout << "  " << p.name << " price=" << p.price << " stock=" << p.stock << '\n';
    }

    // Show low stock items
    auto low = inv.get_low_stock_items();
    std::cout << "Low stock items:\n";
    for (const auto& p : low) {
        std::cout << "  " << p.name << " stock=" << p.stock
                  << " threshold=" << p.threshold << '\n';
    }
}