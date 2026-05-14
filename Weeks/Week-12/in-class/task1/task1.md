# Task 1: MicroPython Hello World

## 目標

在 Wokwi 模擬器中執行第一支 MicroPython 程式，確認開發環境正常運作。

## 先在 solutions 建立你的作業資料夾（先做這步）

請先在本 repo 建立以下路徑，再開始寫程式：

`Weeks/Week-12/solutions/<你的學號>/task1/`

## Wokwi 專案位置

`Weeks/Week-12/in-class/task1/`

## 任務要求

1. 開啟 VS Code，Command Palette（`Cmd+Shift+P`）→ `Wokwi: Start Simulator`
2. 在另一個 Terminal 執行 `make`
3. 確認 Serial Monitor 正確顯示輸出

## 程式說明

```python
def main(args=None):
    print("Hello, World!")

main()
```

`print()` 會透過 ESP32 的 UART 輸出到 Serial Monitor。

## 繳交內容

`Weeks/Week-12/solutions/<你的學號>/task1/main.py`

## 驗收標準

- 程式可在 Wokwi 正常執行
- Serial Monitor 顯示 `Hello, World!`
