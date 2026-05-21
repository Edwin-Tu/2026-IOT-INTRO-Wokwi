# Week-12 Homework — Knight Rider

## 解題說明

本專案為 `homework/knight-rider/task.md` 所述的 Knight Rider 跑馬燈題目。

目標是完成 `main.py` 中的 `TODO`，使 4 顆 LED 從左到右掃描，抵達最右端後反向回到最左端，持續往返。

## 實作內容

- 使用 `PINS = [5, 2, 15, 4]` 定義 4 顆 LED 的腳位。
- `all_off()` 會熄滅所有 LED。
- 以 `pos` 紀錄目前亮著的 LED 索引，範圍為 `0` 到 `3`。
- 以 `direction` 紀錄移動方向，`+1` 表示向右，`-1` 表示向左。
- 每次迴圈先關閉所有 LED，再亮起 `leds[pos]`。
- 每 0.15 秒更新一次位置。
- 當 `pos` 到達邊界時，反轉 `direction`，並繼續移動。

## 執行方式

將 `main.py` 上傳到支援 MicroPython 的開發板，或在 Wokwi 上執行。

如果本機環境有 `tools/wokwi_run.py`，可於 `Weeks/Week-12/solutions/1114405014` 執行：

```bash
python3 ../../../../tools/wokwi_run.py --port 4000 main.py
```

## 預期行為

- 4 顆 LED 依序點亮，從左到右掃描：
  `[*][ ][ ][ ] -> [ ][*][ ][ ] -> [ ][ ][*][ ] -> [ ][ ][ ][*]`
- 到達最右端後反向，回到最左端：
  `[*][ ][ ][ ] <- [ ][*][ ][ ] <- [ ][ ][*][ ] <- [ ][ ][ ][*]`
- 每步間隔 0.15 秒，且同一時間只有一顆 LED 亮。

## 檔案

- `main.py`：Knight Rider 行為的實作程式。

## 備註

此資料夾目前僅含 `main.py`，如要提交至 `solutions/<學號>/knight-rider`，請一併確認目錄結構是否符合作業規定。