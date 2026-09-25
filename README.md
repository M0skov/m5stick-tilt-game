# M5Stick Tilt Game

Lab 4 (ELEE 2045): two Pygame projects driven by the M5Stick (ESP32).

## Part 1 - RC circuit charging simulator

Pygame visualization of a capacitor charging through a resistor (Vs = 5 V, R = 2 kΩ, C = 1 mF), with a block rising as charge builds. Hold C to charge.

- `Lab_4_part_1.py`

Demo: https://youtube.com/shorts/0Ls5Hv6GwFU

## Part 2 - Tilt-controlled ball-balancing game

The M5Stick streams accelerometer data over Bluetooth LE; tilting the stick moves the platform (a seal) to keep the ball balanced, with angry bird sprites falling as obstacles.

- `Lab_4_part_2.py` - Pygame game (connects over BLE with `bleak`)
- `Lab4_Part2_connection/Lab4_Part2_connection.ino` - M5Stick BLE server streaming accelerometer data
- `*.png` - game sprites (background, ball, birds, seal platform)

Demos: [corrected version](https://youtube.com/shorts/eG8xdvAxmqg) · [before corrections](https://youtube.com/shorts/H0SE2TWTHB0)

## Setup

```bash
pip install pygame bleak
```

Flash the `.ino` to the M5Stick with the Arduino IDE (M5StickC board support), then run the game (it scans for and connects to the M5Stick over Bluetooth LE):

```bash
python Lab_4_part_2.py
```
