#include <algorithm>
#include <vector>
#include <string>


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