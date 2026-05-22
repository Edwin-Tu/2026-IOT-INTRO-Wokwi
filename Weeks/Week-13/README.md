# Week 13

> 本週主題：`ESP32 + MicroPython + SH1107 OLED + DHT22`。

## 本週重點
- 使用 ESP32（Wokwi）進行 MicroPython 實作
- 練習 SH1107 128x128 OLED 顯示與座標校正
- 加入 DHT22 感測器，完成即時溫度顯示
- 整合中文版面與動畫效果

## 目錄結構
- `in-class/`：課堂練習題（task1 ~ task4）
- `solutions/`：同學解答（請放在 `solutions/<你的學號>/`）
- `HOMEWORK.md`：本週作業說明（詳細評分與繳交規格）

## 課堂練習建議順序
1. `in-class/task3a`：
- SH1107 版面排版
- 中文字呈現
- 動畫效果（如花火節）

2. `in-class/task4`：
- DHT22 讀值
- Serial debug 訊息
- 溫度顯示整合到 OLED

## 本週作業
請完成：
- [HOMEWORK.md](HOMEWORK.md)

作業核心要求：
1. 版型需對齊 `task3a` 風格
2. 必須有動畫
3. 必須呈現中文字
4. 必須顯示 DHT22 即時溫度

## 開發與執行
在各 task 目錄（例如 `in-class/task4/`）執行：

```bash
make run
```

若遇到 `ModuleNotFoundError: No module named 'serial'`：

```bash
python3 -m pip install pyserial
```

## 基本規範
- 開發板：`ESP32`
- 語言：`MicroPython`
- 顯示器驅動：`sh1107`（不可改成 `ssd1306`）
- 感測器：`DHT22`

## 繳交規範
- 解答放置：`solutions/<你的學號>/`
- 至少包含：
  - `main.py`
  - `README.md`（說明設計與問題解法）
  - 作業要求的截圖/錄影證明

## PR 前檢查
1. 路徑是否正確
2. 程式是否可執行
3. 是否符合 `HOMEWORK.md` 評分項目
