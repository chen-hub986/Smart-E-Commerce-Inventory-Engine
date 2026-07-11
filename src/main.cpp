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

    void print_items() const
    {
        if (items.empty())
        {
            std::cout << "No products\n";
            return;
        }

        for (const Product& product : items)
        {
            std::cout << "Name: " << product.name
                      << " Price: " << product.price
                      << " Stock: " << product.stock
                      << " Threshold: " << product.threshold << '\n';
        }
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

int main()
{
    Inventory inv;
    inv.add_product("keyboard", 2500, 2, 3); // threshold = 3
    inv.add_product("mouse", 800, 10, 2);    // threshold = 2
    inv.add_product("cable", 100, 4, 5);     // threshold = 5

    std::cout << "=== Initial inventory ===\n";
    inv.print_items();

    // Show total value
    std::cout << "\nTotal inventory value: " << inv.calculate_total_value() << '\n';

    // Sort by price and show before/after
    std::cout << "\n=== Sort by price ===\n";
    std::cout << "Before sort:\n";
    inv.print_items();

    inv.sort_items_by_price();
    std::cout << "After sort:\n";
    inv.print_items();

    // Update stock for an existing product
    std::cout << "\n=== Update stock ===\n";
    if (inv.update_stock("mouse", 5)) {
        std::cout << "Updated 'mouse' stock to 5\n";
    } else {
        std::cout << "Failed to update 'mouse' (not found)\n";
    }
    inv.print_items();

    // Try to update a non-existent product
    if (!inv.update_stock("nonexistent", 1)) {
        std::cout << "Could not update 'nonexistent' (as expected)\n";
    }

    // Remove one product by name
    std::cout << "\n=== Remove product ===\n";
    if (inv.remove_product("cable")) {
        std::cout << "Removed 'cable' (first match)\n";
    } else {
        std::cout << "'cable' not found\n";
    }
    inv.print_items();

    // Remove all products by name
    size_t removed = inv.remove_all_products("mouse");
    std::cout << "Removed " << removed << " item(s) named 'mouse'\n";
    inv.print_items();

    // Find a product by name
    std::cout << "\n=== Find product ===\n";
    Product* p = inv.find_product_by_name("keyboard");
    if (p) {
        std::cout << "Found keyboard: price=" << p->price << " stock=" << p->stock << '\n';
    }

    // Show low stock items
    std::cout << "\n=== Low stock items ===\n";
    auto low = inv.get_low_stock_items();
    if (low.empty()) {
        std::cout << "No low stock items\n";
    } else {
        for (const auto& item : low) {
            std::cout << "  " << item.name << " stock=" << item.stock
                      << " threshold=" << item.threshold << '\n';
        }
    }

    return 0;
}