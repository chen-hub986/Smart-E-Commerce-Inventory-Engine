import pytest
import os
import sys
import csv

# 加入上層目錄到 path，讓 pytest 能找到模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Smart_Inventory_Engine_module as sim
from smart_inventory import export_inventory_to_csv, import_inventory_from_csv


@pytest.fixture
def test_inventory():
    """建立測試用的庫存"""
    return sim.Inventory()


@pytest.fixture
def test_csv_file():
    """建立測試用的 CSV 檔案路徑"""
    csv_file = 'test_inventory.csv'
    yield csv_file
    # 清理：測試後刪除檔案
    if os.path.exists(csv_file):
        os.remove(csv_file)

# ============ 新增商品測試 ============
def test_add_single_product(test_inventory):
    """測試新增單一商品"""
    product = sim.Product()
    product.name = "手機"
    product.price = 5000
    product.stock = 10
    product.threshold = 2

    test_inventory.add_product(product)
    assert len(test_inventory.items) == 1
    assert test_inventory.items[0].name == "手機"


def test_add_multiple_products(test_inventory):
    """測試新增多個商品"""
    products_data = [
        ("手機", 5000, 10, 2),
        ("平板", 3000, 5, 1),
        ("筆電", 25000, 3, 1),
    ]

    for name, price, stock, threshold in products_data:
        product = sim.Product()
        product.name = name
        product.price = price
        product.stock = stock
        product.threshold = threshold
        test_inventory.add_product(product)

    assert len(test_inventory.items) == 3

# ============ 查詢功能測試 ============
def test_find_product_by_name(test_inventory):
    """測試透過名稱查找商品"""
    product = sim.Product()
    product.name = "手機"
    product.price = 5000
    product.stock = 10
    product.threshold = 2
    test_inventory.add_product(product)

    found = test_inventory.find_product_by_name("手機")
    assert found is not None
    assert found.name == "手機"
    assert found.price == 5000


def test_find_nonexistent_product(test_inventory):
    """測試查找不存在的商品"""
    found = test_inventory.find_product_by_name("不存在的商品")
    assert found is None

# ============ 刪除商品測試 ============
def test_remove_product(test_inventory):
    """測試刪除商品"""
    product = sim.Product()
    product.name = "手機"
    product.price = 5000
    product.stock = 10
    product.threshold = 2
    test_inventory.add_product(product)

    assert len(test_inventory.items) == 1
    test_inventory.remove_product("手機")
    assert len(test_inventory.items) == 0


def test_remove_nonexistent_product(test_inventory):
    """測試刪除不存在的商品"""
    initial_count = len(test_inventory.items)
    test_inventory.remove_product("不存在的商品")
    # 應該不拋錯，只是沒有刪除任何東西
    assert len(test_inventory.items) == initial_count

# ============ 更新庫存測試 ============
def test_update_stock(test_inventory):
    """測試更新商品庫存"""
    product = sim.Product()
    product.name = "手機"
    product.price = 5000
    product.stock = 10
    product.threshold = 2
    test_inventory.add_product(product)

    success = test_inventory.update_stock("手機", 20)
    assert success is True
    updated = test_inventory.find_product_by_name("手機")
    assert updated.stock == 20


def test_update_stock_nonexistent(test_inventory):
    """測試更新不存在商品的庫存"""
    success = test_inventory.update_stock("不存在的商品", 100)
    assert success is False

# ============ 計算資產測試 ============
def test_calculate_total_value(test_inventory):
    """測試計算總資產"""
    products_data = [
        ("手機", 5000, 10),
        ("平板", 3000, 5),
    ]

    for name, price, stock in products_data:
        product = sim.Product()
        product.name = name
        product.price = price
        product.stock = stock
        product.threshold = 1
        test_inventory.add_product(product)

    # 總資產 = 5000*10 + 3000*5 = 50000 + 15000 = 65000
    total = test_inventory.calculate_total_value()
    assert total == 65000


def test_calculate_total_value_empty(test_inventory):
    """測試空庫存的總資產"""
    total = test_inventory.calculate_total_value()
    assert total == 0

# ============ 缺貨商品測試 ============
def test_get_low_stock_items(test_inventory):
    """測試取得缺貨商品"""
    products_data = [
        ("手機", 5000, 10, 2),      # 正常
        ("平板", 3000, 1, 3),       # 缺貨 (1 <= 3)
        ("筆電", 25000, 2, 2),      # 缺貨 (2 <= 2)
    ]

    for name, price, stock, threshold in products_data:
        product = sim.Product()
        product.name = name
        product.price = price
        product.stock = stock
        product.threshold = threshold
        test_inventory.add_product(product)

    low_stock = test_inventory.get_low_stock_items()
    assert len(low_stock) == 2
    names = [p.name for p in low_stock]
    assert "平板" in names
    assert "筆電" in names


def test_get_low_stock_items_none(test_inventory):
    """測試沒有缺貨商品"""
    product = sim.Product()
    product.name = "手機"
    product.price = 5000
    product.stock = 100
    product.threshold = 10
    test_inventory.add_product(product)

    low_stock = test_inventory.get_low_stock_items()
    assert len(low_stock) == 0

# ============ 排序測試 ============
def test_sort_items_by_price(test_inventory):
    """測試按價格排序商品"""
    products_data = [
        ("筆電", 25000, 3, 1),
        ("手機", 5000, 10, 2),
        ("平板", 3000, 5, 1),
    ]

    for name, price, stock, threshold in products_data:
        product = sim.Product()
        product.name = name
        product.price = price
        product.stock = stock
        product.threshold = threshold
        test_inventory.add_product(product)

    test_inventory.sort_items_by_price()

    # 排序後應該是: 平板(3000) < 手機(5000) < 筆電(25000)
    prices = [p.price for p in test_inventory.items]
    assert prices == [3000, 5000, 25000]

# ============ CSV 匯入/匯出測試 ============
def test_export_to_csv(test_inventory, test_csv_file):
    """測試匯出到 CSV"""
    products_data = [
        ("手機", 5000, 10, 2),
        ("平板", 3000, 5, 1),
    ]

    for name, price, stock, threshold in products_data:
        product = sim.Product()
        product.name = name
        product.price = price
        product.stock = stock
        product.threshold = threshold
        test_inventory.add_product(product)

    export_inventory_to_csv(test_inventory, test_csv_file)

    # 驗證檔案存在
    assert os.path.exists(test_csv_file)

    # 驗證 CSV 內容
    with open(test_csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]['商品名稱'] == '手機'
        assert rows[1]['商品名稱'] == '平板'


def test_import_from_csv(test_csv_file):
    """測試從 CSV 匯入"""
    # 先建立一個測試 CSV
    test_data = [
        {'商品名稱': '手機', '價格': '5000', '庫存': '10', '警戒數值': '2', '總價值': '50000'},
        {'商品名稱': '平板', '價格': '3000', '庫存': '5', '警戒數值': '1', '總價值': '15000'},
    ]

    with open(test_csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['商品名稱', '價格', '庫存', '警戒數值', '總價值'])
        writer.writeheader()
        writer.writerows(test_data)

    # 匯入到新庫存
    new_inventory = sim.Inventory()
    import_inventory_from_csv(new_inventory, test_csv_file)

    # 驗證匯入的資料
    assert len(new_inventory.items) == 2
    assert new_inventory.items[0].name == '手機'
    assert new_inventory.items[0].price == 5000
    assert new_inventory.items[1].name == '平板'


def test_export_import_roundtrip(test_inventory, test_csv_file):
    """測試匯出再匯入（往返測試）"""
    # 建立原始資料
    products_data = [
        ("手機", 5000, 10, 2),
        ("平板", 3000, 5, 1),
        ("筆電", 25000, 3, 1),
    ]

    for name, price, stock, threshold in products_data:
        product = sim.Product()
        product.name = name
        product.price = price
        product.stock = stock
        product.threshold = threshold
        test_inventory.add_product(product)

    # 匯出
    export_inventory_to_csv(test_inventory, test_csv_file)

    # 匯入到新庫存
    new_inventory = sim.Inventory()
    import_inventory_from_csv(new_inventory, test_csv_file)

    # 驗證資料一致
    assert len(new_inventory.items) == len(test_inventory.items)
    for orig, imported in zip(test_inventory.items, new_inventory.items):
        assert orig.name == imported.name
        assert orig.price == imported.price
        assert orig.stock == imported.stock
        assert orig.threshold == imported.threshold
