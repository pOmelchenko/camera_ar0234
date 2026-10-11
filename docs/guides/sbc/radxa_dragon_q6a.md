# AR0234 на CAM2 Radxa Dragon Q6A

Физический захват проверен 2026-10-11: цветной сенсор `0x0a56`, две линии
RAW10, 1920×1200 при 60,226 кадров/с. Рабочая конфигурация и ограничения
записаны в [результате проверки](../../../target/sbc/radxa_dragon_q6a/validation/2026-10-11.json).
Код и команды находятся в [каталоге Q6A](../../../target/sbc/radxa_dragon_q6a/README.md).

## Проверенное подключение и стек

| Узел | Проверенная конфигурация |
| --- | --- |
| Хост | Radxa Dragon Q6A; ревизия физической PCB не зафиксирована |
| Камера | Заказанный цветной MIPI-модуль AR0234, выбранный объектив 200°; маркировка DECXIN-3478V1 взята из материалов продавца |
| Подключение | CAM2 / J16; точная модель кабеля/переходника и поконтактная схема не зафиксированы |
| Linux | Ubuntu 24.04.5 LTS, ядро `7.0.11-7-qcom`, загрузка с NVMe |
| Загрузка DT | Radxa embloader `0.7.r1.f3a03df`, Type #1 entry на `/boot/efi` |
| Драйвер | Kurokesu `ar0234-rpi-driver`, коммит `eefdf9c42cb8f06f7cf00a18b08c7c23d9363a9f`; `ar0234.c` без изменений |
| Sensor endpoint | `cci1_i2c0`, I2C адрес `0x10`, на этой загрузке `18-0010` |
| CSI endpoint | CAMSS CSIPHY2, две линии, link frequency 450 МГц |
| Обработка | libcamera simple pipeline + software ISP, пакет `0.7.1-1-radxa-3` |
| Рабочий стол | GNOME/Wayland, SDL2 2.30.0, Mesa 25.2.8, OpenGL ES 3.2 / FD643 |

Работа имеющегося подключения не устанавливает распиновку произвольного
DECXIN-переходника. CAM2 имеет 15 контактов, а модуль из документов — 22;
ориентацию и соединения нужно установить для своего экземпляра по
[распиновке камеры](../../reference/pinout.md) и
[разъёмам Q6A](https://github.com/pOmelchenko/radxa_dragon_q6a/blob/main/docs/reference/hardware.md#камерные-разъёмы).
J2 TRG/STRB в этой проверке не использовался.

Overlay моделирует локальный генератор модуля как fixed-clock 24 МГц;
SoC MCLK не выводится. GPIO77 включает питание CAM2, CAMSS получает
`vreg_l10c_0p88` и `vreg_l6b_1p2`; добавлен CMA 128 МиБ. Это параметры
работающего примера. Частота генератора и схема локальных стабилизаторов
не были отдельно измерены. Номера I2C/video/media устройств могут измениться.

## Сборка на Q6A

Подготовка ОС, BIOS и NVMe описана в
[репозитории платы](https://github.com/pOmelchenko/radxa_dragon_q6a).
На Linux Q6A:

```sh
sudo apt-get install --no-install-recommends build-essential pkg-config python3 \
    device-tree-compiler v4l-utils libcamera-tools libcamera-ipa libcamera-dev \
    libsdl2-dev libgles2-mesa-dev libdecor-0-plugin-1-cairo \
    linux-headers-7.0.11-7-qcom
git clone https://github.com/pOmelchenko/camera_ar0234.git
cd camera_ar0234/target/sbc/radxa_dragon_q6a
make driver overlay demo
sudo cat "/boot/efi/RadxaOS/$(uname -r)/qcs6490-radxa-dragon-q6a.dtb" > build/base-q6a.dtb
make overlay-check
```

Команды установки пакетов используют настроенный репозиторий Radxa;
проверенные версии перечислены в записи результата. Заголовки должны
соответствовать `uname -r`. `make driver` скачивает закреплённые исходник
и GPL-лицензию в исключённый из Git `vendor/`, проверяет SHA-256 и собирает
`build/driver/ar0234.ko`. EFI-раздел на проверенной установке доступен только
root; `sudo cat` создаёт доступную пользователю копию DTB. `make overlay`
собирает CAM1/CAM2/CAM3. `overlay-check` применяет их к `build/base-q6a.dtb`
отдельно, парами и втроём во всех 15 порядках; проверяет адреса, линии,
GPIO, уникальность phandles и взаимные ссылки sensor/CSIPHY. Итог сохраняется
в `build/overlay-validation.json`. Другой DTB можно задать через `BASE_DTB=путь`.
Эти цели не меняют установленный драйвер и загрузочные файлы.

## Установка для проверенного ядра

Ниже тот же способ установки, который дал рабочую загрузку на
`7.0.11-7-qcom`, с путями сборки этого репозитория. Выполнять из каталога
Q6A. Для другой версии ядра или загрузчика сначала сверить базовый DT,
символы и формат entry. После обновления ядра модуль нужно пересобрать.

Проверить, что установленные файлы не будут перезаписаны, и сохранить
исходные настройки:

```sh
kernel=$(uname -r)
test "$kernel" = 7.0.11-7-qcom || exit 1
boot_entry="/boot/efi/loader/entries/RadxaOS-$kernel.conf"
loader_conf=/boot/efi/loader/loader.conf
overlay_file="/boot/efi/RadxaOS/$kernel/dtbo/ar0234-cam2.dtbo"
module_file="/lib/modules/$kernel/updates/ar0234.ko"
modules_conf=/etc/modules-load.d/ar0234-cam2.conf
recovery_entry=/boot/efi/loader/entries/Q6A-camera-recovery.conf
test -f "$boot_entry" || exit 1
grep -Eq '^[[:space:]]*devicetree-overlay[[:space:]]*$' "$boot_entry" || exit 1
for destination in "$overlay_file" "$module_file" "$modules_conf" "$recovery_entry"; do
    test ! -e "$destination" || exit 1
done
backup_dir=$(mktemp -d "$HOME/ar0234-boot-backup.XXXXXX")
sudo cp "$boot_entry" "$backup_dir/boot-entry.conf"
sudo cp "$loader_conf" "$backup_dir/loader.conf"
printf 'Backup: %s\n' "$backup_dir"
```

Сохранить напечатанный путь: он нужен для восстановления. Если камера уже
настроена, использовать раздел просмотра; этот блок завершится без замены
её файлов. Проверка пустой строки `devicetree-overlay` исключает случайное
совмещение с другой камерой на CAM2.

```sh
sudo install -D -m 0644 build/driver/ar0234.ko "$module_file"
sudo depmod -a "$kernel"
sudo modprobe ar0234
sudo install -m 0644 build/ar0234-cam2.dtbo "$overlay_file"
sudo cp "$boot_entry" "$recovery_entry"
sudo sed -i 's/^title[[:space:]].*/title      Q6A recovery - cameras disabled/' "$recovery_entry"
sudo sed -i "s|^[[:space:]]*devicetree-overlay[[:space:]]*$|devicetree-overlay /RadxaOS/$kernel/dtbo/ar0234-cam2.dtbo|" "$boot_entry"
printf '\ndefault RadxaOS-%s.conf\n' "$kernel" | sudo tee -a "$loader_conf" >/dev/null
printf 'i2c_qcom_cci\nqcom_camss\nar0234\n' | sudo tee "$modules_conf" >/dev/null
sync
sudo reboot
```

Основной DTB остаётся исходным. Меню получает отдельную запись без камеры.
После перезагрузки вернуться в каталог Q6A репозитория.

## Подготовка CAM1 и CAM3

Оверлеи имеют названия `Enable AR0234 camera on CAM1`,
`Enable AR0234 camera on CAM2` и `Enable AR0234 camera on CAM3`.
CAM1 использует `cci0_i2c0` / CSIPHY0 / GPIO36, CAM2 —
`cci1_i2c0` / CSIPHY2 / GPIO77, CAM3 — `cci1_i2c1` / CSIPHY3 / GPIO78.
Отдельные узлы питания и clocks позволяют совместное применение оверлеев.
Адрес `0x10` не конфликтует, поскольку камеры находятся на разных CCI-шинах.

Чтобы файлы были доступны для последующего выбора в меню, после сборки
установить CAM1/CAM3, сохранив существующую boot entry:

```sh
kernel=$(uname -r)
test "$kernel" = 7.0.11-7-qcom || exit 1
for camera in 1 3; do
    destination="/boot/efi/RadxaOS/$kernel/dtbo/ar0234-cam$camera.dtbo"
    test ! -e "$destination" || exit 1
done
for camera in 1 3; do
    sudo install -m 0644 "build/ar0234-cam$camera.dtbo" \
        "/boot/efi/RadxaOS/$kernel/dtbo/ar0234-cam$camera.dtbo"
done
```

Активировать только подключённые камеры, с одним сенсорным overlay на порт.
Для трёх подключённых AR0234 строка Type #1 entry будет такой:

```text
devicetree-overlay /RadxaOS/7.0.11-7-qcom/dtbo/ar0234-cam1.dtbo /RadxaOS/7.0.11-7-qcom/dtbo/ar0234-cam2.dtbo /RadxaOS/7.0.11-7-qcom/dtbo/ar0234-cam3.dtbo
```

Маршруты взяты из закреплённых оверлеев Radxa; проверены сборка и применение
к базовому DTB. Физическая проверка AR0234 была только на CAM2. Для CAM1
требуется переходник к 31-контактному разъёму, работа с управляющими сигналами
1,8 В и проверка первых двух CSI-линий. Overlay оставляет CAM1 в режиме
двух линий, несмотря на четыре линии разъёма. SoC MCLK/reset не включаются:
используется контракт имеющегося модуля с локальным генератором.

CMA 128 МиБ общий; достаточность памяти и суммарная пропускная способность
трёх потоков не проверены. После подключения нужны `cam -l` и отдельный
захват каждой камеры, затем одновременный прогон с измерением ошибок и FPS.
Демка пока выбирает первую AR0234, поэтому не является просмотром трёх камер.

## Найти камеру и получить кадры

```sh
uname -r
sudo dmesg | grep -Ei 'ar0234|camss|cci'
v4l2-ctl --list-devices
media-ctl -d /dev/media0 -p
cam -l
```

На проверенной системе CAMSS был `/dev/media0`, сенсор —
`/base/soc@0/cci@ac4b000/i2c-bus@0/ar0234@10`. Появление entity ещё не
проверяет поток; нужен конечный захват. Освободить камеру от предыдущей
демки перед запуском `cam`.

```sh
capture_dir=$(mktemp -d "$HOME/ar0234-frames.XXXXXX")
cam -c 1 -s width=1920,height=1200 --capture=120 \
    --file="$capture_dir/frame-#.ppm"
```

`-c 1` соответствует одной камере в проверенной установке; при нескольких
камерах выбрать нужную из `cam -l`. В логах ожидается вход
`1920x1200-GRBG-10-CSI2P stride 2400`, выход `1912x1200-ABGR8888`.
RGB-буфер имеет stride 7680 байт; `bytesused=9216000` включает padding.
Объектив 200° даёт круг изображения: его край не означает ошибку разрешения.

Из терминала рабочего стола:

```sh
sh tools/preview.sh
```

Клавиши, сравнение и параметры — в [описании демки](../../../target/sbc/radxa_dragon_q6a/demo/README.md).
Обычный просмотр без её фильтра: `sh tools/preview-original.sh`.
GPU-тест `make check` требует доступной графической сессии.

Для запуска через пользовательскую службу из того же терминала:

```sh
systemctl --user import-environment WAYLAND_DISPLAY DISPLAY XDG_RUNTIME_DIR
systemd-run --user --collect --unit=ar0234-preview \
    --setenv=SDL_VIDEODRIVER=wayland "$PWD/build/ar0234-demo"
journalctl --user -u ar0234-preview.service -n 30 --no-pager
```

Остановка: `systemctl --user stop ar0234-preview.service`.
Если HDMI показывает «Нет сигнала» после простоя, проверить Automatic
Suspend и Screen Blank в GNOME: в этой сессии причиной оказался сон системы.

## Ограничения и восстановление

В simple pipeline используется `uncalibrated.yaml`: AR0234 sensor helper,
статические свойства, задержки управления и профиль цвета не настроены.
libcamera предупреждает о недостающих рекомендованных controls и rotation.
Наличие изображения не подтверждает корректность gain, экспозиции или
цветовой калибровки. При слабом свете видны шум и яркие зелёные точки;
демка уменьшает их, но исходный RAW и карта дефектов отдельно не исследованы.

120 кадров/с, четыре линии, внешний trigger/STRB, cold power-on и долгий
непрерывный прогон не проверены. Выход software ISP на восемь пикселей уже
сенсора. Полосы и круги около ярких ламп описаны как наблюдения в
[диагностике](../../../target/sbc/radxa_dragon_q6a/validation/observations.md);
конкретный дефект оптики или сенсора не установлен.

Для восстановления выбрать `Q6A recovery - cameras disabled` в меню или
вернуть сохранённые настройки. Установить `backup_dir` в напечатанный выше
путь и проверить наличие обоих файлов; `kernel` ниже — установленное ядро:

```sh
kernel=7.0.11-7-qcom
test -f "$backup_dir/boot-entry.conf" && test -f "$backup_dir/loader.conf" || exit 1
systemctl --user stop ar0234-preview.service
sudo cp "$backup_dir/boot-entry.conf" "/boot/efi/loader/entries/RadxaOS-$kernel.conf"
sudo cp "$backup_dir/loader.conf" /boot/efi/loader/loader.conf
sudo rm -f /etc/modules-load.d/ar0234-cam2.conf
sync
sudo reboot
```

На первоначальной установке копии находятся в
`/home/radxa/camera-ar0234-20261011/boot-backup`, а готовое восстановление —
`sudo sh /home/radxa/camera-ar0234-20261011/restore-boot.sh`.
