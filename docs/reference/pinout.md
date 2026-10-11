# DECXIN-3478V1 Connector Pinout

Reference for the module pictured in the retained seller
[drawing](../vendor/dimensions-and-pinout.png) and
[rear photograph](../vendor/module-back.png). This is a transcription of the
pictured **DECXIN-3478V1** module, not a pinout of the bare AR0234CS sensor or
onsemi evaluation board. No physical continuity, supply or capture test is
recorded.

## 22-Pin FPC

The drawing specifies **22 contacts, 0.5 mm pitch, contacts under the flip
cover**. In the retained rear photograph, with the FPC connector at the bottom,
the PCB marks **22 on the left and 1 on the right**. Preserve this viewing
direction when identifying contacts; the lens-side view is mirrored.

The first two columns below follow the seller's `NO. / CAM-SYMBOL` table.
`MDP`/`MDN` mean the positive/negative CSI data signals; `MCP`/`MCN` are the
clock pair. The last column compares signal positions with the official
[Raspberry Pi 22-pin reference](https://www.raspberrypi.com/documentation/accessories/camera.html#camera-connector-pinout-22-pin),
whose [original source is retained](../vendor/raspberry-pi-camera-advanced-2026-10-11.adoc).
It is a signal comparison, not a qualified cable wiring diagram.

| DECXIN pin | Seller label | Function | Corresponding standard RPi 22-pin contact |
| --- | --- | --- | --- |
| 1 | `3.3V` | Module supply | 22 |
| 2 | `SDA` | I2C data | 21 |
| 3 | `SCL` | I2C clock | 20 |
| 4 | `GND` | Ground | 19 |
| 5 | `NC` | No connection specified | No signal equivalent; RPi 18 is `CAM_IO1` |
| 6 | `NC` | No connection specified | No signal equivalent; RPi 17 is `CAM_IO0` |
| 7 | `GND` | Ground | 16 |
| 8 | `MDP3` | CSI data lane 3, positive | 15 |
| 9 | `MDN3` | CSI data lane 3, negative | 14 |
| 10 | `GND` | Ground | 13 |
| 11 | `MDP2` | CSI data lane 2, positive | 12 |
| 12 | `MDN2` | CSI data lane 2, negative | 11 |
| 13 | `GND` | Ground | 10 |
| 14 | `MCP` | CSI clock, positive | 9 |
| 15 | `MCN` | CSI clock, negative | 8 |
| 16 | `GND` | Ground | 7 |
| 17 | `MDP1` | CSI data lane 1, positive | 6 |
| 18 | `MDN1` | CSI data lane 1, negative | 5 |
| 19 | `GND` | Ground | 4 |
| 20 | `MDP0` | CSI data lane 0, positive | 3 |
| 21 | `MDN0` | CSI data lane 0, negative | 2 |
| 22 | `GND` | Ground | 1 |

**DECXIN pin 1 is 3.3 V; standard RPi 22-pin pin 1 is ground.** For the
documented power, ground, I2C and CSI signals, the numbering corresponds to
`RPi pin = 23 - DECXIN pin`. This does not mean that a crossover cable is
required: connector contact side, cable end orientation and the manufacturer's
numbering convention determine the physical routing. Establish that routing
before applying power. Pins 5/6 remain `NC`; do not turn them into reset,
power-enable or XCLK inputs by analogy with another module.

The table supplies no I2C voltage tolerance, pull-up circuit or supply-current
limit. The drawing's separate `2.8 / 1.8 / 1.2 V` entries describe sensor
rails; they are not additional FPC supply inputs. The rear photo also shows
a `24.000` oscillator marking, but does not establish its circuit or clock
configuration.

## J2 Trigger/Strobe Pads

With the same rear-photo orientation, J2 is to the right of the FPC connector:

| Position in the rear photograph | PCB label |
| --- | --- |
| Upper, square pad | `STRB` |
| Middle, round pad | `TRG` |
| Lower, round pad | `GND` |

The drawing describes a three-position **1.25 mm** connector footprint. It
does not explicitly number these pads, so this page uses their photographed
positions. The labels alone do not specify voltage, direction/drive type,
polarity, pulse width or required sensor-register settings. Obtain that
electrical/timing specification before connecting a trigger or strobe circuit.

## Sources

- [Original seller drawing](../vendor/dimensions-and-pinout.png), supplied on
  2026-09-23; SHA-256
  `409dfdb11f7039873f07c3cfb0ae41ca04f4eca330de5eb9d86b4d6a23e55ca8`.
- [Original rear photograph](../vendor/module-back.png), supplied on 2026-09-23;
  SHA-256 `3df4491f13d23fd797ab7970f4bd6b58f8f660820681b81a2ee4dc96b3ce1236`.
  [Seller provenance](../vendor/sources.json) and [checksums](../vendor/SHA256SUMS).
- Raspberry Pi Ltd, [camera connector reference](https://www.raspberrypi.com/documentation/accessories/camera.html#pinout-information),
  checked on 2026-10-11; retained source and commit/license provenance in the
  [local pinout source manifest](../vendor/pinout-sources.json).

Return to the [AR0234 camera reference](../../README.md).
