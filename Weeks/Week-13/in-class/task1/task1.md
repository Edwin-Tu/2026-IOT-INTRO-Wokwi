# Task 1: ESP32 C Hello World

## 目標
在 Wokwi 中使用 ESP32 C 專案輸出 `Hello, World!`。

## 先在 solutions 建立你的作業資料夾（先做這步）
請先在本 repo 建立以下路徑，再開始寫程式：

`Weeks/Week-13/solutions/<你的學號>/task1/`

例如你的學號是 `112360001`，路徑應為：

`Weeks/Week-13/solutions/112360001/task1/`

## Wokwi 專案位置（本題）
請使用本題提供的 Wokwi 專案資料夾：

`Weeks/Week-13/in-class/task1/`

此資料夾內已提供：
- `diagram.json`
- `wokwi.toml`
- `src/main.c`

## 任務要求
1. 使用 Wokwi 開啟本題 ESP32 C 專案。
2. 在 `src/main.c` 完成程式，輸出：`Hello, World!`
3. 執行後，確認序列埠（Serial Monitor）有正確顯示輸出。

## 程式範例
```c
#include <stdio.h>

void app_main(void) {
  printf("Hello, World!\\n");
}
```

## 繳交內容
請將本題程式放在：

`Weeks/Week-13/solutions/<你的學號>/task1/`

建議包含：
- `src/main.c`
- `README.md`（可簡短描述執行結果）

## 驗收標準
- 程式可在 Wokwi 正常執行。
- 序列埠可看到 `Hello, World!`。
- 檔案路徑正確。
