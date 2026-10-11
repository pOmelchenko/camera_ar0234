# Драйверы AR0234

Открытые реализации AR0234 доступны для Raspberry Pi и Jetson.
Поддержка модуля DECXIN-3478V1 с объективом 200° не подтверждена ни одной
проверенной конфигурацией. Закреплённые исходники дают основу для портирования;
сборка, установка и физический захват не выполнены.

## Реализации

| Источник | Закреплённая версия | Область применения |
| --- | --- | --- |
| [Kurokesu Raspberry Pi](https://github.com/Kurokesu/ar0234-rpi-driver/tree/eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f) | `eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f` | Bookworm/Trixie, ядро 6.12+, две/четыре линии, RAW8/RAW10; полный кадр 60/120 кадр/с continuous |
| [Kurokesu Jetson](https://github.com/Kurokesu/ar0234-jetson-driver/tree/9b71e90d2dbc8ad41332f8ffad0bae973583ddd3) | `9b71e90d2dbc8ad41332f8ffad0bae973583ddd3` | JetPack 6.2.1 / L4T 36.4.4 и 6.2.2 / 36.5.0; две линии, RAW10, 1920 × 1200 при 60 кадр/с |

Оба драйвера имеют лицензию GPL-2.0. Заявленные платформы и частоты относятся
к реализациям авторов. Хеши просмотренных файлов и границы проверки:
[driver-sources.json](../vendor/driver-sources.json).
Версии libcamera/rpicam и скачиваемых пакетов нужно закрепить отдельно.

## Контракт кандидата Raspberry Pi

[Исходник](https://github.com/Kurokesu/ar0234-rpi-driver/blob/eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f/ar0234.c)
и [overlay](https://github.com/Kurokesu/ar0234-rpi-driver/blob/eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f/ar0234-overlay.dts)
задают следующие значения:

| Настройка | Значение в реализации |
| --- | --- |
| Compatible / I2C | `onnn,ar0234cs`, 7-битный адрес `0x10` |
| Идентификация | Регистр `0x3000`: цветной `0x0a56`, монохромный `0x1a56`; это ожидаемые значения, не чтение нашего модуля |
| Тактирование | PLL рассчитан на EXTCLK 24 МГц |
| CSI | По умолчанию две линии, опция `4lane` включает четыре |
| Link frequency | 450 МГц RAW10, 360 МГц RAW8 |
| Цвет | GRBG Bayer RAW8/RAW10; для монохромного Y8/Y10 |
| Интеграция | Pi endpoints, регуляторы, reset и power sequencing |

Наличие генератора с маркировкой 24.000 на DECXIN не доказывает правильность
всей последовательности питания и тактирования. Привязки Pi нужно адаптировать
к схемам модуля и выбранной платы. Настройка Q6A находится
[на отдельной странице](../../target/sbc/radxa_dragon_q6a/README.md).

## Внешний запуск

[README Raspberry Pi](https://github.com/Kurokesu/ar0234-rpi-driver/blob/eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f/README.md)
описывает pulsed/held-high trigger, continuous sync-sink и flash.
Интеграцию задают регистры; длительность импульса не равна экспозиции.
Для полного кадра пределы pulsed — 30 Гц на двух линиях и 60 Гц на четырёх,
в отличие от continuous 60/120 кадр/с. Указанные там 1,8 В относятся
к описанному оборудованию Kurokesu. Электрический контракт J2 DECXIN отсутствует.

[README Jetson](https://github.com/Kurokesu/ar0234-jetson-driver/blob/9b71e90d2dbc8ad41332f8ffad0bae973583ddd3/README.md)
дополнительно описывает таймауты при редком запуске и установку ISP tuning.
Нужно проверить пропущенные импульсы, момент экспозиции и связь кадра
с временной меткой для своего модуля и объектива.

## Область проверки

Манифест хранит датированные инвентаризации Linux, Raspberry Pi Linux
и esp-video-components без AR0234 в просмотренных каталогах на указанных
коммитах. Они характеризуют эти версии; текущую комплектацию конкретного
BSP нужно проверять на целевом устройстве.

onsemi [DevSuite](manufacturer.md#devsuite) предоставляет инструменты
работы с регистрами и цветом для оценочного оборудования. Наличие руководства
DevSuite не устанавливает Linux-путь захвата для DECXIN.

Подготовка и критерии результата: [Raspberry Pi](../../target/sbc/raspberry_pi/README.md),
[Jetson](../../target/sbc/nvidia_jetson/README.md), [Q6A](../../target/sbc/radxa_dragon_q6a/README.md).
