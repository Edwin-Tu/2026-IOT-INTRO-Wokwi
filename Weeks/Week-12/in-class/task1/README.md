# Week 12 Task1: MicroPython on Wokwi (ESP32)

## 環境需求

1. 安裝 VS Code 擴充套件：`Wokwi for VS Code`
2. 安裝 pyserial：

```bash
pip install pyserial
```

## 專案結構

```
task1/
├── main.py        ← 在這裡撰寫程式
├── Makefile
├── diagram.json
└── wokwi.toml
```

## 執行步驟

1. 用 VS Code 開啟 `Weeks/Week-12/in-class/task1/` 資料夾
2. Command Palette（`Cmd+Shift+P`）→ `Wokwi: Start Simulator`
3. 確認模擬器視窗保持開啟，在 Terminal 執行：

```bash
make
```

## 注意事項

- 請勿使用 Debug 模式。
- 重新啟動模擬器會重置虛擬檔案系統。
