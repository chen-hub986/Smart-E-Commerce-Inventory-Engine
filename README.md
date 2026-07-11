# Smart E-Commerce Inventory Engine / 智能電商庫存管理系統

This repository contains a high-performance Smart Inventory Engine implemented
with a C++ core and a Python CLI wrapper. The C++ core is written with
modern C++ (C++20) and exposed to Python via pybind11 so you can have both
performance and ease of use.

本專案使用 C++20 開發高效能的庫存引擎，並透過 pybind11 封裝成 Python 模組，提供簡潔的 CLI 操作介面，兼顧效能與易用性。

---

## Features / 系統特色

- High-performance C++ core for fast searching and sorting on large datasets.
- Python integration via pybind11 for an easy-to-use CLI.
- i18n support (Traditional Chinese `zh` and English `en`) for menu and CSV headers.
- Persistent storage: load/save `inventory.csv` with support for both Chinese and English headers.
- Full inventory features: add/remove/search products, update stock, show total value, low-stock warnings, sort by price.

高效能 C++ 核心、pybind11 整合、雙語支援（中文/英文）、CSV 資料持久化，以及完整的庫存管理功能（新增、刪除、搜尋、更新庫存、總資產、低庫存警示、價格排序）。

---

## Prerequisites / 環境要求

- C++ compiler with C++20 support (GCC, Clang, MSVC)
- CMake
- Python 3.x and development headers
- pybind11 (install via `pip install pybind11`)

建置需具備支援 C++20 的編譯器、CMake、Python 3.x（含開發 headers）及 pybind11（可透過 `pip install pybind11` 安裝）。

---

## Build / 建置（簡易說明）

Build the C++ extension module with CMake. After building, ensure the produced
shared module (e.g. `Smart_Inventory_Engine_module.cp311-win_amd64.pyd` or
`.so`) is available in the same directory as `smart_inventory.py` or is on
Python's import path.

使用 CMake 建置 C++ 擴充模組，編譯後請確認產生的模組（例如 Windows 的 `.pyd` 或 Linux/macOS 的 `.so`）位於 `smart_inventory.py` 相同目錄或已被安裝到 Python 模組搜尋路徑中。

Windows (PowerShell):

```powershell
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

---

## Usage / 使用方式

Run the Python CLI:

```bash
python smart_inventory.py
```


Windows (PowerShell):

```powershell
$env:SIE_LANG="en"; python smart_inventory.py
```

---

## Project structure / 專案架構

- `smart_inventory.py` — Python multi-language CLI entry (supports `SIE_LANG`).
- `src/` — C++ core source files and pybind11 bindings.
- `Smart_Inventory_Engine_module.cpp` — pybind11 binding / engine implementation (usually under `src/`).
- `main.cpp` — optional native C++ entry point.
- `CMakeLists.txt` — CMake build script.
- `inventory.csv` — persistent CSV data store for inventory.
- `test/` — pytest tests (if present).

---
