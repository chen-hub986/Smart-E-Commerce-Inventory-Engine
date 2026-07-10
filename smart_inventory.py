import csv
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

def main():
    my_inv = sim.Inventory()

    while True:
        print("\n=== 智慧庫存系統 ===")
        print("1. 新增商品")
        print("2. 查詢總資產")
        print("0. 離開系統")

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
                product_stock = int(input("輸入存貨: "))
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
            print(f"\n總資產: {my_inv.calculate_total_value()}")
        else:
            print("無效的選項，請重新輸入！")
            continue


if __name__ == '__main__':
    main()
