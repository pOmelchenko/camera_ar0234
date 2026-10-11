# AR0234 на NVIDIA Jetson

**Статус: кандидат по исходникам; DECXIN не проверен.**
Kurokesu закреплён для JetPack 6.2.1 / L4T 36.4.4 и 6.2.2 / 36.5.0,
двух линий RAW10 и 1920 × 1200 при 60 кадр/с. Carrier и конкретный Jetson
для этого модуля не выбраны.

## Подготовка

1. Зафиксировать модуль Jetson, carrier, порт и L4T. Проверить
   [распиновку DECXIN](../../../docs/reference/pinout.md) против схемы carrier,
   питание, управляющие уровни, reset, clock и ориентацию кабеля.
2. Получить закреплённого кандидата:

   ```sh
   git clone https://github.com/Kurokesu/ar0234-jetson-driver.git
   cd ar0234-jetson-driver
   git checkout 9b71e90d2dbc8ad41332f8ffad0bae973583ddd3
   ```

3. Сопоставить module integration и DT с выбранным carrier. Для совпадающего
   оборудования [Setup](https://github.com/Kurokesu/ar0234-jetson-driver/blob/9b71e90d2dbc8ad41332f8ffad0bae973583ddd3/README.md#setup)
   устанавливает DKMS, DT overlay и ISP tuning, затем выбирает порт через
   Jetson-IO. Его сценарий рассчитан на оборудование автора.
4. Проверить chip ID и один непрерывный поток, согласовать RAW и ISP.
   Настройки другого объектива не квалифицируют цвет и shading для 200°.
5. Измерить поток, затем отдельно проверить intermittent trigger,
   таймауты, принимаемые импульсы и связь кадров с экспозицией.

Четырёхлинейный режим 120 кадр/с этой реализацией не установлен.
Версии внешних файлов, фактические команды и результат сохраняются
[по критериям пакета](../../../docs/development/README.md).
