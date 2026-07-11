import csv
import os
from typing import TypedDict, List, Dict

import Smart_Inventory_Engine_module as sim

# Language selection: 'zh' (default) or 'en'. Can be overridden with env var SIE_LANG
LANG = os.environ.get('SIE_LANG', 'zh')


class LangStrings(TypedDict):
    menu_title: str
    menu: List[str]
    enter_choice: str
    enter_name: str
    enter_price: str
    enter_stock: str
    enter_threshold: str
    invalid_number: str
    please_name: str
    not_found: str
    removed: str
    exit_save: str
    no_items: str
    found_results: str
    low_stock_title: str
    total_value: str


STRINGS: Dict[str, LangStrings] = {
    'zh': {
        'menu_title': '=== 智慧庫存系統 ===',
        'menu': [
            '1. 新增商品',
            '2. 刪除商品',
            '3. 尋找商品',
            '4. 更新商品庫存',
            '5. 查詢總資產',
            '6. 顯示缺貨商品',
            '7. 依價格排序商品',
            '0. 離開系統並儲存',
        ],
        'enter_choice': '請輸入選項：',
        'enter_name': '輸入名稱: ',
        'enter_price': '輸入價格: ',
        'enter_stock': '輸入庫存: ',
        'enter_threshold': '輸入警戒數值: ',
        'invalid_number': '\n請輸入數字!',
        'please_name': '\n請輸入商品名稱。',
        'not_found': '\n找不到該商品',
        'removed': '已刪除商品: {}',
        'exit_save': '系統已關閉',
        'no_items': '\n沒有商品',
        'found_results': '\n找到 {} 筆結果：',
        'low_stock_title': '\n缺貨商品: ',
        'total_value': '\n總資產: {}',
    },
    'en': {
        'menu_title': '=== Smart Inventory System ===',
        'menu': [
            '1. Add product',
            '2. Remove product',
            '3. Search products',
            '4. Update product stock',
            '5. Show total value',
            '6. Show low-stock items',
            '7. Sort items by price',
            '0. Exit and save',
        ],
        'enter_choice': 'Enter choice: ',
        'enter_name': 'Enter name: ',
        'enter_price': 'Enter price: ',
        'enter_stock': 'Enter stock: ',
        'enter_threshold': 'Enter threshold: ',
        'invalid_number': '\nPlease enter numeric values for price/stock/threshold',
        'please_name': '\nPlease provide a product name.',
        'not_found': '\nProduct not found',
        'removed': 'Removed product: {}',
        'exit_save': 'Exiting. Saving inventory to CSV...',
        'no_items': '\nNo items',
        'found_results': '\nFound {} result(s):',
        'low_stock_title': '\nLow-stock items:',
        'total_value': '\nTotal value: {}',
    }
}

CSV_HEADERS: Dict[str, List[str]] = {
    'zh': ['商品名稱', '價格', '庫存', '警戒數值', '總價值'],
    'en': ['Name', 'Price', 'Stock', 'Threshold', 'TotalValue'],
}

# normalize LANG
if LANG not in STRINGS:
    LANG = 'zh'
T: LangStrings = STRINGS[LANG]


def export_inventory_to_csv(inventory, filename='inventory.csv'):
    # choose headers by LANG; default behavior remains Chinese for backward compatibility
    headers = CSV_HEADERS.get(LANG, CSV_HEADERS['zh'])
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for product in inventory.items:
            # create a row that works for either header set
            row = {}
            if LANG == 'en':
                row = {
                    'Name': product.name,
                    'Price': product.price,
                    'Stock': product.stock,
                    'Threshold': product.threshold,
                    'TotalValue': product.price * product.stock,
                }
            else:
                row = {
                    '商品名稱': product.name,
                    '價格': product.price,
                    '庫存': product.stock,
                    '警戒數值': product.threshold,
                    '總價值': product.price * product.stock,
                }

            writer.writerow(row)

def import_inventory_from_csv(inventory, filename='inventory.csv'):
    if not os.path.exists(filename):
        return

    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        row_no = 0
        for row in reader:
            row_no += 1
            try:
                # support both English and Chinese headers
                name = (row.get('Name') or row.get('商品名稱') or '').strip()
                price_raw = row.get('Price') or row.get('價格') or '0'
                stock_raw = row.get('Stock') or row.get('庫存') or '0'
                threshold_raw = row.get('Threshold') or row.get('警戒數值') or '0'

                price = int(float(str(price_raw).replace(',', '').strip()))
                stock = int(float(str(stock_raw).replace(',', '').strip()))
                threshold = int(float(str(threshold_raw).replace(',', '').strip()))
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
        print("\n" + T['menu_title'])
        for line in T['menu']:
            print(line)

        choice = input(T['enter_choice'])

        if choice == '0':
            print(T['exit_save'])
            export_inventory_to_csv(my_inv)
            break

        if choice == '1':
            try:
                product = sim.Product()
                product_name = str(input(T['enter_name']))
                product_price = int(input(T['enter_price']))
                product_stock = int(input(T['enter_stock']))
                product_threshold = int(input(T['enter_threshold']))

                product.name = product_name
                product.price = product_price
                product.stock = product_stock
                product.threshold = product_threshold

                my_inv.add_product(product)
            except ValueError:
                print(T['invalid_number'])
                continue
        elif choice == '2':
            product_name = input(T['enter_name']).strip()
            if not product_name:
                print(T['please_name'])
                continue
            ok = my_inv.remove_product(product_name)
            if ok:
                print(T['removed'].format(product_name))
            else:
                print(T['not_found'])
        elif choice == '3':
            product_name = input(T['enter_name']).strip()
            if not product_name:
                print(T['please_name'])
                continue
            found_product = my_inv.find_products_by_name_contains(product_name)
            if found_product:
                print(T['found_results'].format(len(found_product)))
                for products in found_product:
                    print(f"\n商品名稱: {products.name} 價格: {products.price} 庫存: {products.stock} 警戒數值: {products.threshold}")
            else:
                print(T['not_found'])
        elif choice == '4':
            try:
                product_name = input(T['enter_name']).strip()
                if not product_name:
                    print(T['please_name'])
                    continue
                new_stock = int(input(T['enter_stock']).strip())
            except ValueError:
                print(T['invalid_number'])
                continue

            success = my_inv.update_stock(product_name, new_stock)
            if success:
                found_product = my_inv.find_product_by_name(product_name)
                print(f"\n商品名稱: {found_product.name} 價格: {found_product.price} 庫存: {found_product.stock} 警戒數值: {found_product.threshold}")
            else:
                print(T['not_found'])
        elif choice == '5':
            print(T['total_value'].format(my_inv.calculate_total_value()))
        elif choice == '6':
            low_stock_products = my_inv.get_low_stock_items()
            if low_stock_products:
                print(T['low_stock_title'])
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
                print(T['no_items'])
        else:
            # keep Chinese message here for compatibility in original file, but also show generic
            print("無效的選項，請重新輸入！")
            continue


if __name__ == '__main__':
    main()
