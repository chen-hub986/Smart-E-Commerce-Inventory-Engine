import csv
import os
import Smart_Inventory_Engine_module as sim


def export_inventory_to_csv(inventory, filename='inventory.csv'):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['商品名稱', '價格', '庫存', '警戒數值', '總價值']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product in inventory.items:
            writer.writerow({
                '商品名稱': product.name,
                '價格': product.price,
                '庫存': product.stock,
                '警戒數值': product.threshold,
                '總價值': product.price * product.stock
            })

def import_inventory_from_csv(inventory, filename='inventory.csv'):
    if not os.path.exists(filename):
        return

    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        row_no = 0
        for row in reader:
            row_no += 1
            try:
                name = row.get('商品名稱', '').strip()
                price = int(row.get('價格', 0))
                stock = int(row.get('庫存', 0))
                threshold = int(row.get('警戒數值', 0))
            except (ValueError, TypeError) as e:
                print(f"Warning: skip invalid row {row_no} in CSV: {e}")
                continue

            product = sim.Product()
            product.name = name
            product.price = price
            product.stock = stock
            product.threshold = threshold

            inventory.add_product(product)

def main():
    my_inv = sim.Inventory()
    import_inventory_from_csv(my_inv)

    while True:
        print("\n=== 智慧庫存系統 ===")
        print("1. 新增商品")
        print("2. 刪除商品")
        print("3. 尋找商品")
        print("4. 更新商品庫存")
        print("5. 查詢總資產")
        print("6. 顯示缺貨商品")
        print("7. 依價格排序商品")
        print("0. 離開系統並儲存")

        choice = input("請輸入選項：")

        if choice == '0':
            print("系統已關閉")
            export_inventory_to_csv(my_inv)
            break

        if choice == '1':
            try:
                product = sim.Product()
                product_name = str(input("輸入名稱: "))
                product_price = int(input("輸入價格: "))
                product_stock = int(input("輸入庫存: "))
                product_threshold = int(input("輸入警戒數值: "))

                product.name = product_name
                product.price = product_price
                product.stock = product_stock
                product.threshold = product_threshold

                my_inv.add_product(product)
            except ValueError:
                print("\n請輸入數字!")
                continue
        elif choice == '2':
            product_name = input("輸入名稱: ").strip()
            if not product_name:
                print("\n請輸入商品名稱。")
                continue
            ok = my_inv.remove_product(product_name)
            if ok:
                print(f"已刪除商品: {product_name}")
            else:
                print(f"找不到商品: {product_name}")
        elif choice == '3':
            product_name = input("輸入名稱: ").strip()
            if not product_name:
                print("\n請輸入搜尋關鍵字。")
                continue
            found_product = my_inv.find_products_by_name_contains(product_name)
            if found_product:
                print(f"\n找到 {len(found_product)} 筆結果：")
                for products in found_product:
                    print(f"\n商品名稱: {products.name} 價格: {products.price} 庫存: {products.stock} 警戒數值: {products.threshold}" )
            else:
                print("\n找不到該商品")
        elif choice == '4':
            try:
                product_name = input("輸入名稱: ").strip()
                if not product_name:
                    print("\n請輸入商品名稱。")
                    continue
                new_stock = int(input("輸入新的庫存: ").strip())
            except ValueError:
                print("\n請輸入整數數字")
                continue

            success = my_inv.update_stock(product_name, new_stock)
            if success:
                found_product = my_inv.find_product_by_name(product_name)
                print(f"\n商品名稱: {found_product.name} 價格: {found_product.price} 庫存: {found_product.stock} 警戒數值: {found_product.threshold}")
            else:
                print("\n找不到該商品")
        elif choice == '5':
            print(f"\n總資產: {my_inv.calculate_total_value()}")
        elif choice == '6':
            low_stock_products = my_inv.get_low_stock_items()
            if low_stock_products:
                print(f"\n缺貨商品: ")
                for p in low_stock_products:
                    print(f"{p.name}: 目前庫存{p.stock} 警戒值: {p.threshold}")
            else:
                print("\n目前沒有缺貨商品")
        elif choice == '7':
            my_inv.sort_items_by_price()
            if my_inv.items:
                for item in my_inv.items:
                    print(f"\n商品名稱: {item.name} 價格: {item.price} 庫存: {item.stock}")
            else:
                print("\n沒有商品")
        else:
            print("無效的選項，請重新輸入！")
            continue


if __name__ == '__main__':
    main()
