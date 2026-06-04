# -*- coding: utf-8 -*-
# Week 13 Homework: SH1107 + DHT22 中文動畫溫度看板
# Hardware: ESP32 + board-grove-oled-sh1107 + DHT22
#
# 修正重點：
# 1. 依 HOMEWORK.md 保留主視覺、英文資訊、中文字動畫、即時溫度與學號。
# 2. 依 task3 的 SH1107 觀察結果：driver 使用 rotate=0，避免 rotate=90 造成 wrap / 切割。
# 3. 保留 center_x、center_y、offset，並將 center_y 預設為 90，作為 Wokwi 實測視覺中心。
# 4. DHT22 每 2 秒讀一次，OLED 每 250ms 更新動畫。
# 5. 讀值失敗時不當機，Serial 顯示錯誤，OLED 顯示 Sensor Error 或 OLD 前次值。

from machine import Pin, I2C
import sh1107
import dht
import time

# =========================
# Adjustable constants
# =========================
OLED_WIDTH = 128
OLED_HEIGHT = 128
OLED_ADDR = 0x3C

# task3 實測建議：SH1107 driver 先使用 rotate=0。
# 不在 driver 層強制 rotate=90，避免 Page/Column 映射造成畫面 wrap 或切割。
OLED_ROTATE = 0

# 若畫面整體仍有偏移，先調整 center_y，不建議同時調 rotate / start line / center_y。
center_x = 64
center_y = 90
offset = 0

# 若要做 SH1107 可視區定位測試，可改成 True。
# 作業正式錄 GIF 建議維持 False，避免 grid 干擾版型。
DEBUG_GRID = False

# diagram.json 對應：
# OLED: SCL=GPIO21, SDA=GPIO22
# DHT22: DATA=GPIO23
I2C_SCL_PIN = 21
I2C_SDA_PIN = 22
DHT_PIN = 23

ANIMATION_MS = 250      # OLED 動畫更新：每 250ms 一幀
SENSOR_MS = 2000        # DHT22 建議至少 2 秒讀一次
STUDENT_ID = "1114405014"  # 請改成自己的學號


# =========================
# Device setup
# =========================
i2c = I2C(
    0,
    scl=Pin(I2C_SCL_PIN),
    sda=Pin(I2C_SDA_PIN),
    freq=400000
)

print("[DEBUG] I2C scan:", i2c.scan())

oled = sh1107.SH1107_I2C(
    OLED_WIDTH,
    OLED_HEIGHT,
    i2c,
    address=OLED_ADDR,
    rotate=OLED_ROTATE
)

# DHT22 DATA 腳使用 Pull-up 較穩定；Wokwi 也可正常使用
dht_sensor = dht.DHT22(Pin(DHT_PIN, Pin.IN, Pin.PULL_UP))


# =========================
# 16x16 Chinese bitmap font: 「花火節」
# =========================
GLYPHS = {
    "hua": [
        "0000000000000000",
        "0010010010010000",
        "0010010010010000",
        "1111111111111110",
        "0010010010010000",
        "0000100001000000",
        "0000100001000000",
        "0111111111110000",
        "0001000010000000",
        "0011000011000000",
        "0101000101000000",
        "1001001001000000",
        "0001010001000000",
        "0001100001000010",
        "0001000001111110",
        "0000000000000000",
    ],
    "huo": [
        "0000000000000000",
        "0000001000000000",
        "0000001000000000",
        "0010001000100000",
        "0001001001000000",
        "0000101010000000",
        "0000011100000000",
        "0000011100000000",
        "0000110110000000",
        "0001001001000000",
        "0010001000100000",
        "0100001000010000",
        "1000010000001000",
        "0000100000000100",
        "0011000000000010",
        "0000000000000000",
    ],
    "jie": [
        "0000000000000000",
        "0100010001000100",
        "1110111011101110",
        "0100010001000100",
        "0001111111100000",
        "0001000000100000",
        "0001111111100000",
        "0001000000100000",
        "0001111111100000",
        "0000010010000000",
        "0001111111110000",
        "0001010010010000",
        "0001010011110000",
        "0001110010000000",
        "0000010011111000",
        "0000000000000000",
    ],
}


# =========================
# Basic drawing helpers
# =========================
def safe_pixel(display, x, y, color=1):
    if 0 <= x < OLED_WIDTH and 0 <= y < OLED_HEIGHT:
        display.pixel(x, y, color)


def draw_rect(display, x, y, w, h, color=1):
    display.hline(x, y, w, color)
    display.hline(x, y + h - 1, w, color)
    display.vline(x, y, h, color)
    display.vline(x + w - 1, y, h, color)


def draw_grid(display, cx, cy, width, height, step=16, color=1):
    # task3 用：觀察 128x128 可視區是否 wrap，以及中心線是否對齊。
    for x in range(0, width, step):
        for y in range(0, height, 4):
            display.pixel(x, y, color)
    for y in range(0, height, step):
        for x in range(0, width, 4):
            display.pixel(x, y, color)

    display.hline(0, cy, width, color)
    display.vline(cx, 0, height, color)


def draw_circle(display, cx, cy, r, color=1):
    x = r
    y = 0
    err = 0

    while x >= y:
        safe_pixel(display, cx + x, cy + y, color)
        safe_pixel(display, cx + y, cy + x, color)
        safe_pixel(display, cx - y, cy + x, color)
        safe_pixel(display, cx - x, cy + y, color)
        safe_pixel(display, cx - x, cy - y, color)
        safe_pixel(display, cx - y, cy - x, color)
        safe_pixel(display, cx + y, cy - x, color)
        safe_pixel(display, cx + x, cy - y, color)

        y += 1
        if err <= 0:
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1


def draw_star(display, cx, cy, size, color=1):
    pts = [
        (cx, cy - size),
        (cx + int(size * 0.35), cy - int(size * 0.25)),
        (cx + size, cy - int(size * 0.2)),
        (cx + int(size * 0.5), cy + int(size * 0.25)),
        (cx + int(size * 0.6), cy + size),
        (cx, cy + int(size * 0.45)),
        (cx - int(size * 0.6), cy + size),
        (cx - int(size * 0.5), cy + int(size * 0.25)),
        (cx - size, cy - int(size * 0.2)),
        (cx - int(size * 0.35), cy - int(size * 0.25)),
    ]

    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        display.line(x1, y1, x2, y2, color)


def draw_glyph(display, glyph_name, x, y, scale=1, color=1):
    bitmap = GLYPHS[glyph_name]

    for row, line in enumerate(bitmap):
        for col, bit in enumerate(line):
            if bit == "1":
                px = x + col * scale
                py = y + row * scale

                if scale == 1:
                    safe_pixel(display, px, py, color)
                else:
                    for dx in range(scale):
                        for dy in range(scale):
                            safe_pixel(display, px + dx, py + dy, color)


# =========================
# Scene drawing
# =========================
def draw_static_scene(display):
    # 128x128 SH1107 是單色螢幕，版面分成：
    # 上方標題 / 左側資訊 / 右側龍珠 / 中下方中文字 / 底部溫濕度框。
    draw_rect(display, 0, 0, 128, 128, 1)

    display.text("DRAGON TEMP", 18, 4)
    display.hline(6, 15, 116, 1)

    display.text("ID:" + STUDENT_ID[-5:], 5, 20)
    display.text("DHT22 LIVE", 5, 32)
    display.text("HANABI", 5, 44)

    # 底部溫濕度資訊框。使用 center_y + 11，讓 SH1107 視覺中心修正集中在 center_y。
    draw_rect(display, 3, center_y + 11, 122, 23, 1)


def draw_dragon_ball(display, cx, cy, frame, temp_c=None):
    # 溫度視覺化加分：高溫時龍珠外圈略微變大；平時也會微微跳動。
    extra = 0
    if temp_c is not None and temp_c >= 30:
        extra = 2
    elif frame % 4 == 0:
        extra = 1

    radius = 19 + extra
    draw_circle(display, cx, cy, radius, 1)
    draw_circle(display, cx, cy, radius - 1, 1)

    # 四星龍珠
    star_size = 4
    draw_star(display, cx - 7, cy - 5, star_size, 1)
    draw_star(display, cx + 7, cy - 5, star_size, 1)
    draw_star(display, cx - 7, cy + 8, star_size, 1)
    draw_star(display, cx + 7, cy + 8, star_size, 1)

    # 外圍閃爍星星動畫
    sparkle_points = [
        (cx - 27, cy),
        (cx, cy - 27),
        (cx + 27, cy),
        (cx, cy + 27),
    ]
    sx, sy = sparkle_points[frame % len(sparkle_points)]
    draw_star(display, sx, sy, 3, 1)


def draw_chinese_animation(display, frame):
    # 「花火節」三字：上下波浪動畫 + 底線閃爍。
    # base_y 使用 center_y - 17，讓視覺中心可統一用 center_y 微調。
    base_x = 8 + offset
    base_y = center_y - 17

    wave = [0, 2, 4, 2, 0, -2, -4, -2]

    y_hua = base_y + wave[frame % len(wave)]
    y_huo = base_y + wave[(frame + 2) % len(wave)]
    y_jie = base_y + wave[(frame + 4) % len(wave)]

    draw_glyph(display, "hua", base_x, y_hua, 1, 1)
    draw_glyph(display, "huo", base_x + 19, y_huo, 1, 1)
    draw_glyph(display, "jie", base_x + 38, y_jie, 1, 1)

    if frame % 2 == 0:
        display.hline(base_x, base_y + 20, 54, 1)
    else:
        display.hline(base_x + 6, base_y + 20, 42, 1)


def draw_temperature(display, temp_c, humidity, sensor_ok):
    temp_y = center_y + 18

    if temp_c is None:
        display.text("Sensor Error", 14, temp_y)
        return

    # HOMEWORK.md 指定格式：xx.x C
    temp_text = "{:.1f} C".format(temp_c)
    display.text(temp_text, 12, temp_y)

    if humidity is not None:
        humidity_text = "H:{:.0f}%".format(humidity)
        display.text(humidity_text, 76, temp_y)

    # 本次讀值失敗，但保留前次有效值
    if not sensor_ok:
        display.text("OLD", 100, 20)


# =========================
# Sensor reading
# =========================
def read_sensor_safe(last_temp, last_humidity):
    try:
        dht_sensor.measure()
        temp_c = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # MicroPython DHT 有時可能回傳 None，保守處理。
        if temp_c is None or humidity is None:
            raise RuntimeError("DHT22 returned None")

        print("[DEBUG] temperature = {:.1f} C, humidity = {:.1f} %".format(temp_c, humidity))
        return temp_c, humidity, True

    except Exception as e:
        print("[ERROR] temperature/humidity read failed:", e)
        return last_temp, last_humidity, False


# =========================
# Main loop
# =========================
def main():
    frame = 0
    temp_c = None
    humidity = None
    sensor_ok = False

    # 開機後立即讀一次，之後每 2 秒讀一次
    last_sensor_ms = time.ticks_ms() - SENSOR_MS

    while True:
        now = time.ticks_ms()

        # DHT22 特性：不可每幀讀值，至少間隔約 2 秒
        if time.ticks_diff(now, last_sensor_ms) >= SENSOR_MS:
            temp_c, humidity, sensor_ok = read_sensor_safe(temp_c, humidity)
            last_sensor_ms = now

        oled.fill(0)

        if DEBUG_GRID:
            draw_grid(oled, center_x, center_y, OLED_WIDTH, OLED_HEIGHT)

        draw_static_scene(oled)

        # 龍珠主視覺：沿用原版型的右上位置，但改成由 center_x / center_y 推導。
        # center_x + 30 = 94；center_y - 37 = 53。
        draw_dragon_ball(oled, center_x + 30 + offset, center_y - 37, frame, temp_c)

        draw_chinese_animation(oled, frame)
        draw_temperature(oled, temp_c, humidity, sensor_ok)

        oled.show()

        frame = (frame + 1) % 1000
        time.sleep_ms(ANIMATION_MS)


main()
