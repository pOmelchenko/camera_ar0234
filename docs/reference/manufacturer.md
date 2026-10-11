# Документы onsemi AR0234CS

В пакете сохранены документы сенсора, оценочной платы и общие application
notes onsemi. Они помогают исследовать модуль, но не определяют электрическую
схему DECXIN-3478V1 или полный код установленного сенсора.

## Сохранённые PDF

| Документ | Версия и полезные страницы |
| --- | --- |
| [Product overview](../vendor/onsemi-product-overview.pdf), 2 страницы | Обзор семейства; стр. 1 — режимы, стр. 2 — варианты заказа и параметры; полный register datasheet отсутствует |
| [AR0234-CSP83-Demo3Head schematic](../vendor/onsemi-color-evaluation-schematic.pdf), 6 страниц | Rev. 1.0, титул 2020-04-16; стр. 2 — блоки, 3 — сенсор, 4 — питание, 5 — clock/reset, 6 — интерфейсы |
| [BOM оценочной платы](../vendor/onsemi-color-evaluation-bom.pdf), 1 страница | Rev. 1.0, 2018-09-03; компоненты Demo3, не DECXIN |
| [AN52561/D: Handling and Best Practices](../vendor/onsemi-image-sensor-handling.pdf), 8 страниц | Rev. 11, June 2019; ESD, хранение, загрязнение и cover glass; PDF стр. 2 соответствует печатной стр. 1 |
| [TND6115/D: ISO Measurement](../vendor/onsemi-iso-measurement.pdf), 3 страницы | Rev. 2, July 2014; стр. 2 — saturation/noise и зависимость от оптики, gain и преобразования |
| [Корпус 570CK](../vendor/onsemi-package-570ck.pdf), 1 страница | Issue A, 2019-08-16, `98AON87372G`; ODCSP83, оптическая плоскость, ориентация шаров и footprint сенсора |
| [DevSuite Quick-Start](../vendor/devsuite-quick-start-guide.pdf), 13 страниц | Rev. 72, copyright 2024; стр. 1–4 — установка и оценочное оборудование, стр. 9 — register/tuning/SDK |

Даты BOM и схемы различаются; согласованный производственный комплект
не подтверждён. Схема Demo3 не задаёт распиновку FPC и уровни TRG DECXIN.
Рекомендации для cover glass сенсора нельзя автоматически применять
к покрытию объектива 200°. TND6115 описывает измерение, не ISO этой сборки.

[official-sources.json](../vendor/official-sources.json) содержит URL `.com`
и фактические официальные адреса `.cn`, версии, даты получения, размеры
и хеши. Два color schematic URL (C00/C28) дали одинаковые PDF, поэтому
сохранён один файл и alias в манифесте. Это не доказывает тождественность
комплектации оценочных плат. Оригиналы проверяются по
[SHA256SUMS](../vendor/SHA256SUMS).

## DevSuite

[Статья onsemi](https://www.onsemi.com/company/newsroom/blog/company/how-high-speed-global-shutter-image-sensors-ease-the-burden-on-ai-based-vision-systems)
ссылается на DevSuite. В сохранённом guide:

- Register Wizard формирует настройки регистров по режиму и выходу.
- SensorTune помогает получить color-correction matrix.
- ApBase SDK предоставляет API DevWare.
- LensTools формирует lens-shading correction.

Рабочий процесс относится к оценочным комплектам Demo3/USB3 и адаптерам.
Возможны дополнительные пакеты для отдельных сенсоров; наличие AR0234 mode
data и поддержка DECXIN не установлены. Рассмотренные Linux-кандидаты описаны
[отдельно](drivers.md).

## Недостающие данные

[Страница AR0234CS](https://www.onsemi.com/products/sensors/image-sensors/ar0234cs)
предлагает Request Datasheet. Полного register/timing datasheet в пакете нет.
Для завершения подключения нужны:

- схема и ревизия DECXIN, ток питания, reset/clock и полный код сенсора;
- напряжения, направление, полярность и тайминги TRG/STRB;
- регистры режимов, лицензированный драйвер, DT и tuning;
- модель объектива 200°, соглашение об угле и оптические данные.

[Распиновка FPC/J2](pinout.md) уже содержит назначения из материалов продавца.
Она не восполняет электрические и временные ограничения.
Дополнительные позиции каталога onsemi (TND6370, nomenclature TND310,
solution guides SSG8210/SSG8213) не являются готовым описанием подключения
модуля. Их датированный перечень и область просмотра сохранены
[в происхождении источников](../vendor/official-sources.json).
