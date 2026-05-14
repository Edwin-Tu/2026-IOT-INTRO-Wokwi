# Task 4: 四 LED 多裝置管理

## 目標

擴展 Task 3 的概念，用 **list** 管理 4 顆 LED，每顆以不同頻率閃爍。

## 先在 solutions 建立你的作業資料夾（先做這步）

`Weeks/Week-12/solutions/<你的學號>/task4/`

## Wokwi 專案位置

`Weeks/Week-12/in-class/task4/`

## 電路說明

| LED | 顏色 | GPIO | 間隔 |
|-----|------|------|------|
| led1 | 紅 | GPIO5 | 1 秒 |
| led2 | 綠 | GPIO2 | 2 秒 |
| led3 | 藍 | GPIO15 | 3 秒 |
| led4 | 黃 | GPIO4 | 5 秒 |

## 程式說明

```python
from machine import Pin
import time

PINS      = [5, 2, 15, 4]
INTERVALS = [1000, 2000, 3000, 5000]
leds      = [Pin(p, Pin.OUT) for p in PINS]
states    = [False] * 4
last      = [time.ticks_ms()] * 4

while True:
    now = time.ticks_ms()
    for i in range(4):
        if time.ticks_diff(now, last[i]) >= INTERVALS[i]:
            states[i] = not states[i]
            leds[i].value(states[i])
            last[i] = now
```

用 list comprehension 初始化 `leds`，再用 for loop 統一處理所有 LED。
增加新 LED 只需在 `PINS` 和 `INTERVALS` 加一個數字。

## 繳交內容

`Weeks/Week-12/solutions/<你的學號>/task4/main.py`

## 驗收標準

- 4 顆 LED 各自依指定間隔閃爍
- 程式使用 list 管理裝置（不得使用 4 段獨立的 if）
