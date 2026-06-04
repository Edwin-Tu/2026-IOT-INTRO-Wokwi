# Week 13 Homework：SH1107 + DHT22 中文動畫溫度看板

## 作業說明

本作業以 ESP32、Grove SH1107 OLED 與 DHT22 感測器完成一個可持續運作的中文動畫溫度看板。OLED 使用 `board-grove-oled-sh1107`，解析度為 128x128，並以 `sh1107` driver 控制，不使用 SSD1306。程式透過 I2C 連接 OLED，並由 GPIO23 讀取 DHT22 的溫度與濕度資料。

## 版面配置

畫面採用分層式設計，對齊作業參考圖的版型邏輯。上方顯示標題 `DRAGON TEMP`，左側放置學號識別、DHT22 狀態與 `HANABI` 文字，右上方放置龍珠主視覺，底部則以框線區塊顯示即時溫度與濕度。畫面中可看到學號尾碼，確保學號不是只出現在文件中，而是實際呈現在 OLED 畫面上。

## 動畫設計

動畫每 250ms 更新一幀。龍珠外圈會依幀數產生輕微跳動，當溫度達到較高區間時，外圈會稍微放大，形成溫度視覺化效果。中文字「花火節」使用 16x16 點陣字形繪製，不依賴外部中文字型，並透過上下波浪位移與底線閃爍呈現連續動畫效果。

## DHT22 整合

DHT22 每 2 秒讀取一次，避免過度讀取造成感測失敗。每次成功讀值後，Serial Monitor 會輸出包含 `temperature` 與 `humidity` 的 debug 訊息。OLED 底部以 `xx.x C` 格式顯示即時溫度，並同步顯示濕度 `H:xx%`。若讀值失敗，程式會使用 `try/except` 捕捉錯誤，不會直接當掉，並保留前一次有效資料或顯示 `Sensor Error`。

## 遇到的問題與解法

實作時遇到 SH1107 顯示座標與 Wokwi 可視區不完全一致的問題，若直接使用旋轉或理論中心 `(64, 64)`，畫面可能出現偏移、wrap 或切割。解法是依照定位測試結果，讓 driver 維持 `rotate=0`，並保留 `center_x`、`center_y`、`offset` 作為可調校常數。目前使用 `center_x = 64`、`center_y = 90` 作為 Wokwi 實測後較穩定的視覺中心，正式展示時關閉 grid，讓畫面符合繳交版型。

## 執行方式

```bash
make run
```

若使用 Windows，也可以執行：

```bash
make.bat
```

## 繳交檔案

- `main.py`
- `README.md`
- `pr.md`
- `diagram.json`
- `homework.gif`
- OLED 畫面截圖
- Serial debug 截圖

## 驗收重點

- 畫面有龍珠主視覺
- 畫面有英文資訊區塊
- 畫面有可辨識中文字「花火節」
- 畫面有即時溫度 `xx.x C`
- OLED 畫面可看到學號識別
- Serial Monitor 有 temperature / humidity debug
- 程式可持續執行，不會因 DHT22 暫時性錯誤而崩潰
