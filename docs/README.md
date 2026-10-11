# Документация AR0234

## Справочник

- [Модуль DECXIN-3478V1 и объектив 200°](reference/module.md).
- [Распиновка FPC 22 контакта и J2](reference/pinout.md).
- [Драйверы, тактирование и режимы запуска](reference/drivers.md).
- [Документы сенсора onsemi AR0234CS](reference/manufacturer.md).

## Запуск на SBC

| SBC | Материал | Статус |
| --- | --- | --- |
| Radxa Dragon Q6A | [Запуск на CAM2](guides/sbc/radxa_dragon_q6a.md), [код и результаты](../target/sbc/radxa_dragon_q6a/README.md) | Физический захват 1920×1200 ≈60 кадров/с; схема переходника не зафиксирована |
| Raspberry Pi | [Кандидат Kurokesu](../target/sbc/raspberry_pi/README.md) | Разбор закреплённого исходного кода; DECXIN не проверен |
| NVIDIA Jetson | [Кандидат Kurokesu](../target/sbc/nvidia_jetson/README.md) | Разбор закреплённого исходного кода; DECXIN не проверен |

## Микроконтроллеры

[Waveshare ESP32-P4](../target/mcu/waveshare_esp32_p4_wifi6_dev_kit/README.md):
драйвер, сборка и физический захват не проверены.

В `docs/guides` опубликован проверенный маршрут Q6A CAM2.
[Правила оформления результата](development/README.md) отделяют разбор
источников, сборку и физическую проверку.

## Оригиналы

[Каталог источников](vendor/README.md): материалы продавца, семь PDF onsemi,
справочник разъёмов Raspberry Pi и манифесты происхождения/драйверов.
