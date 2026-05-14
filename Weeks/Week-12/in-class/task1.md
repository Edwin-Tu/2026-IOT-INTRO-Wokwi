# Task 1: Wokwi MicroPython Hello World (ESP32)

## 目標
依 `wokwi-vscode-micropython` 專案流程，在 Wokwi 中執行 ESP32 MicroPython，並於序列埠輸出 `Hello, World!`。

## 先在 solutions 建立你的作業資料夾（先做這步）
請先在本 repo 建立以下路徑，再開始寫程式：

`Weeks/Week-12/solutions/<你的學號>/task1/`

例如你的學號是 `112360001`，路徑應為：

`Weeks/Week-12/solutions/112360001/task1/`

接著在該資料夾內建立：
- `main.py`：放你的 Wokwi Python 程式（Hello, World!）
- `README.md`（可選）：簡短寫執行結果

重點：請不要先在其他地方寫完再搬檔，請直接在 `solutions/.../task1/` 內開始。

## Wokwi 專案位置（本題）

請使用本題提供的 Wokwi 專案資料夾：

`Weeks/Week-12/in-class/task1/`

此資料夾內已提供（官方結構）：
- `main.py`
- `esp32/diagram.json`
- `esp32/wokwi.toml`
- `esp32/ESP32_GENERIC-20251209-v1.27.0.bin`

請在此資料夾啟動與測試 Wokwi（ESP32），完成後再把你的解答程式整理到 `solutions/<你的學號>/task1/`。

## 任務要求
1. 在 VS Code 開啟 `Weeks/Week-12/in-class/task1/`。
2. 在命令面板執行 `Wokwi: Start Simulator`，並選擇 `esp32` 目錄。
3. 保持模擬器視窗在前景，於另一個 Terminal 執行：
   - `python -m mpremote connect port:rfc2217://localhost:4000 run main.py`
4. 確認序列埠（REPL/Serial）有輸出 `Hello, World!`。

## 程式範例
```python
print("Hello, World!")
```

## 繳交內容
請將本題程式放在：

`Weeks/Week-12/solutions/<你的學號>/task1/`

建議包含：
- `main.py`
- `README.md`（可簡短描述執行結果）

## 驗收標準
- 程式可在 Wokwi（`esp32`）正常執行。
- 序列埠可看到 `Hello, World!`。
- 檔案路徑正確。
