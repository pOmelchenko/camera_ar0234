# AR0234 на Raspberry Pi

**Статус: кандидат по исходникам; DECXIN не проверен.**
За основу рассматривается Kurokesu для Raspberry Pi OS Bookworm/Trixie,
ядро 6.12+. Точная модель Pi, разъём, ОС и версии userspace не выбраны.

## Подготовка

1. Сверить [FPC DECXIN](../../../docs/reference/pinout.md) с разъёмом
   выбранной Pi и проверить кабель без питания. Pi 3/4 с 15 контактами
   и Zero с 22 контактами предоставляют две линии; четыре требуют
   соответствующего хоста/разъёма. Число контактов не определяет число линий.
2. Получить закреплённого кандидата:

   ```sh
   git clone https://github.com/Kurokesu/ar0234-rpi-driver.git
   cd ar0234-rpi-driver
   git checkout eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f
   ```

3. Сопоставить его EXTCLK 24 МГц, I2C/chip ID, питание и reset с DECXIN.
   [Ограничения драйвера](../../../docs/reference/drivers.md) не заменяют
   электрической схемы своего модуля.
4. Для совместимого оборудования следовать
   [Install закреплённого README](https://github.com/Kurokesu/ar0234-rpi-driver/blob/eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f/README.md#install):
   DKMS и Kurokesu libcamera/rpicam forks, настройка `config.txt`,
   отключение autodetect и overlay AR0234 с выбранным портом/числом линий.
   Версии полученных пакетов и скрипта установки нужно записать.
5. Сначала перечислить камеры и получить непрерывный кадр; проверить
   цвет, экспозицию/gain, формат и фактическую частоту. Затем тестировать
   внешний запуск по отдельному электрическому контракту DECXIN.

Continuous full-frame 60/120 кадр/с для двух/четырёх линий и pulsed
30/60 Гц — разные режимы кандидата. Это не проверка DECXIN 200°.
Результат: [критерии записи](../../../docs/development/README.md).

Источник хостовых ограничений:
[Raspberry Pi CSI/Unicam](https://www.raspberrypi.com/documentation/computers/camera_software.html#unicam).
