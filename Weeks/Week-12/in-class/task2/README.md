# Week 12 Task2：LED 閃燈（MicroPython on Wokwi ESP32）

## 目標電路

```
GPIO5 ──[220Ω]──▶|── GND
```

## 在 Wokwi 中自己加元件

1. 用 VS Code 開啟 `diagram.json`，Wokwi 電路編輯器會自動開啟
2. 點左下角 **「+」** 搜尋並加入元件：
   - 搜尋 `resistor` → 加入電阻 → 右鍵 Edit → `value` 設為 `220`
   - 搜尋 `led` → 加入 LED → 右鍵 Edit → `color` 設為 `red`
3. 點擊 ESP32 的接腳拉線，完成以下接線：

| 元件 | 接腳 | 連接到 |
|------|------|--------|
| 電阻 220Ω | 腳 1 | ESP32 GPIO5 |
| 電阻 220Ω | 腳 2 | LED 陽極（A） |
| LED（紅） | 陰極（K） | ESP32 GND |

## 執行步驟

1. Command Palette（`Cmd+Shift+P`）→ `Wokwi: Start Simulator`
2. 確認模擬器視窗保持開啟，在 Terminal 執行：

```bash
make
```

## 程式說明

```python
from machine import Pin
import time

led = Pin(5, Pin.OUT)   # GPIO5 設為輸出

while True:
    led.on()            # 點亮
    time.sleep(0.5)     # 等 0.5 秒
    led.off()           # 熄滅
    time.sleep(0.5)     # 等 0.5 秒
```
