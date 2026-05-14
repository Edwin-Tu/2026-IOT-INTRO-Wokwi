# Task 3: 雙 LED 非阻塞計時

## 目標

讓兩顆 LED 同時以**不同頻率**閃爍，學習用 `ticks_ms()` 取代 `time.sleep()` 做非阻塞計時。

## 先在 solutions 建立你的作業資料夾（先做這步）

`Weeks/Week-12/solutions/<你的學號>/task3/`

## Wokwi 專案位置

`Weeks/Week-12/in-class/task3/`

## 電路說明

| LED | 顏色 | GPIO | 電阻 |
|-----|------|------|------|
| led1 | 紅 | GPIO5 | 220Ω |
| led2 | 綠 | GPIO2 | 220Ω |

## 核心概念：非阻塞計時

`time.sleep()` 會讓整個程式停下來等待，無法同時控制多個裝置。
改用 `ticks_ms()` 記錄上次觸發的時間，每次迴圈只「確認時間到了沒」：

```python
now = time.ticks_ms()
if time.ticks_diff(now, last) >= INTERVAL:
    # 時間到，執行動作
    last = now
```

## 程式說明

```python
from machine import Pin
import time

led1 = Pin(5, Pin.OUT)  # 紅 LED，2 秒切換
led2 = Pin(2, Pin.OUT)  # 綠 LED，3 秒切換

INTERVAL1 = 2000
INTERVAL2 = 3000

t1 = t2 = time.ticks_ms()
s1 = s2 = False

while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, t1) >= INTERVAL1:
        s1 = not s1
        led1.value(s1)
        t1 = now
    if time.ticks_diff(now, t2) >= INTERVAL2:
        s2 = not s2
        led2.value(s2)
        t2 = now
```

兩顆 LED 完全獨立，互不影響。

## 繳交內容

`Weeks/Week-12/solutions/<你的學號>/task3/main.py`

## 驗收標準

- 紅 LED 每 2 秒、綠 LED 每 3 秒各自切換
- 兩顆 LED 運作不互相影響
