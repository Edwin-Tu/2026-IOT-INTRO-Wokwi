# Task 2: LED 閃燈（外接電阻）

## 目標

用 MicroPython 控制外接 LED，透過 `time.sleep()` 讓 LED 每 0.5 秒切換一次。

## 先在 solutions 建立你的作業資料夾（先做這步）

`Weeks/Week-12/solutions/<你的學號>/task2/`

## Wokwi 專案位置

`Weeks/Week-12/in-class/task2/`

## 電路說明

```
GPIO5 ──[220Ω]──▶|── GND
                LED（紅）
```

| 元件 | 接腳 | 連接到 |
|------|------|--------|
| 電阻 220Ω | 腳 1 | ESP32 GPIO5 |
| 電阻 220Ω | 腳 2 | LED 陽極（A） |
| LED（紅） | 陰極（C） | ESP32 GND |

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

`time.sleep()` 會讓程式**暫停**，這段時間內什麼事都做不了。

## 繳交內容

`Weeks/Week-12/solutions/<你的學號>/task2/main.py`

## 驗收標準

- LED 每 0.5 秒規律閃爍
