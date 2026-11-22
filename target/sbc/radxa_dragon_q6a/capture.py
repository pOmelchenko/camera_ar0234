#!/usr/bin/env python3
"""Capture one free-running pgAA frame from the AR0234 on the selected Q6A connector."""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from tempfile import mkdtemp
from typing import NamedTuple

from ports import PORTS

WIDTH, HEIGHT = 1920, 1200


def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def find_camera(port, phy):
    # Match this physical receiver even when another AR0234 uses the same I2C address.
    detected = []
    for media in sorted(Path("/dev").glob("media[0-9]*")):
        graph = subprocess.check_output(["media-ctl", "-d", media, "-p"], text=True)
        for entity in graph.split("- entity ")[1:]:
            sensor = re.match(r"\d+: (ar0234 \d+-0010) \(", entity)
            if sensor:
                if re.search(rf'-> "{phy}":0 \[ENABLED\b', entity):
                    return media, sensor[1]
                detected.append(f"{media}: {entity.splitlines()[0]}")
    if detected:
        raise ValueError(f"Для {port.upper()} нет связи AR0234 → {phy}. Обнаруженные сенсоры:\n"
                         + "\n".join(detected)
                         + "\nПри 0 link посмотрите, какой сенсор ожидает qcom-camss в текущей загрузке:\n"
                           "sudo cat /sys/kernel/debug/v4l2-async/pending_async_subdevices")
    raise ValueError(f"В media graph нет связи ar0234 → {phy}. Проверьте probe и порт {port.upper()}.")


def format_value(description, field, pattern):
    match = re.search(rf"^\s*{field}\s*:\s*({pattern})", description, re.MULTILINE)
    if not match:
        raise ValueError(f"Не удалось прочитать {field} из v4l2-ctl.")
    return match[1]


class Link(NamedTuple):
    source: str
    pad: int
    sink: str
    sink_pad: int
    enabled: bool

    def setting(self, enable):
        return f'"{self.source}":{self.pad} -> "{self.sink}":{self.sink_pad} [{int(enable)}]'


def select_route(graph, sensor, phy):
    links = []
    for section in graph.split("- entity ")[1:]:
        name = section.split(": ", 1)[1].split(" (", 1)[0]
        pad = None
        for line in section.splitlines()[1:]:
            m = re.match(r"\s*pad(\d+):", line)
            if m:
                pad = int(m[1])
            m = re.match(r'\s*-> "([^"]+)":(\d+) \[([^\]]*)\]', line)
            if m and pad is not None:
                flags = {flag.strip() for flag in m[3].split(",")}
                links.append(Link(name, pad, m[1], int(m[2]), "ENABLED" in flags))
    if Link(sensor, 0, phy, 0, True) not in links:
        raise ValueError(f"Связь {sensor} → {phy} изменилась перед захватом.")
    active = [link for link in links if link.enabled]
    # On Q6A use VC0, RDI0 and the matching CSID/VFE pair. Keep foreign links intact.
    candidates = []
    for first in links:
        csid = re.fullmatch(r"msm_csid(\d+)", first.sink)
        if first.source != phy or first.pad != 1 or first.sink_pad != 0 or not csid:
            continue
        rdi = f"msm_vfe{csid[1]}_rdi0"
        for second in links:
            if (second.source, second.pad, second.sink, second.sink_pad) != (first.sink, 1, rdi, 0):
                continue
            related = [l for l in active if l.source in (phy, first.sink) or l.sink == first.sink
                       or (l.source.startswith("msm_csid") and l.sink.startswith(f"msm_vfe{csid[1]}_"))]
            if any(l not in (first, second) for l in related) or (second.enabled and not first.enabled):
                continue
            video = next((l.sink for l in active if l.source == rdi and l.pad == 1
                          and re.fullmatch(r"msm_vfe\d+_video\d+", l.sink)), None)
            if video:
                candidates.append((not first.enabled, int(csid[1]), first, second, video))
    if not candidates:
        raise ValueError("Нет свободного маршрута CSID/VFE RDI0. Активные связи камер сохранены.")
    _, _, first, second, video = min(candidates)
    return first, second, video


def capture(port):
    import fcntl
    os.environ["LC_ALL"] = "C"
    phy = f"msm_csiphy{PORTS[port][1]}"
    media, sensor = find_camera(port, phy)
    ctl = ["media-ctl", "-d", media]
    with media.open("rb", buffering=0) as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        graph = subprocess.check_output([*ctl, "-p"], text=True)
        first, second, video = select_route(graph, sensor, phy)
        print(f"{media}: {sensor} → {phy} → {first.sink} → {second.sink}", flush=True)
        created = []
        try:
            for link in (first, second):
                if not link.enabled:
                    run(*ctl, "-l", link.setting(True))
                    created.append(link)
            capture_frame(ctl, sensor, phy, first.sink, second.sink, video)
        finally:
            for link in reversed(created):
                result = subprocess.run([*ctl, "-l", link.setting(False)], check=False)
                if result.returncode:
                    print(f"Не удалось освободить связь {link.source} → {link.sink}.", file=sys.stderr)


def capture_frame(ctl, sensor, phy, csid, rdi, video_entity):
    for entity, pad in [(sensor, 0), (phy, 0), (csid, 0), (csid, 1), (rdi, 0)]:
        run(*ctl, "-V", f'"{entity}":{pad} [fmt:SGRBG10_1X10/{WIDTH}x{HEIGHT} field:none]')

    video = subprocess.check_output([*ctl, "-e", video_entity], text=True).strip()
    v4l2 = ["v4l2-ctl", "-d", video]
    run(*v4l2, f"--set-fmt-video=width={WIDTH},height={HEIGHT},pixelformat=pgAA")
    fmt = subprocess.check_output([*v4l2, "--get-fmt-video"], text=True)
    print(video, fmt, sep="\n", flush=True)
    if (format_value(fmt, "Pixel Format", r"'[^']+'") != "'pgAA'" or
            format_value(fmt, "Width/Height", r"\d+/\d+") != f"{WIDTH}/{HEIGHT}"):
        raise ValueError("CAMSS согласовал другой формат или размер кадра.")
    stride = int(format_value(fmt, "Bytes per Line", r"\d+"))
    size = int(format_value(fmt, "Size Image", r"\d+"))
    row_bytes = WIDTH * 5 // 4
    if stride < row_bytes or size < stride * HEIGHT:
        raise ValueError(f"Некорректные параметры буфера: stride={stride}, sizeimage={size}.")

    output = Path(mkdtemp(prefix="ar0234-", dir="."))
    raw = output / "frame.raw"
    print(f"Захват в {output.resolve()}", flush=True)
    run(*v4l2, "--stream-mmap=4", "--stream-count=1", f"--stream-to={raw}", timeout=15)
    frame = raw.read_bytes()
    if len(frame) != size:
        raise ValueError(f"Получено {len(frame)} байт, ожидалось {size}.")

    with (output / "preview.ppm").open("wb") as preview:
        write_preview(preview, frame, WIDTH, HEIGHT, stride)
    print(f"RAW10 и 8-битное превью сохранены в {output.resolve()}")


def write_preview(preview, frame, width, height, stride):
    """One RGB pixel per GR/BG block, using the high eight bits of packed RAW10."""
    preview.write(f"P6\n{width // 2} {height // 2}\n255\n".encode("ascii"))
    row_bytes = width * 5 // 4
    for y in range(0, height, 2):
        top = bytearray(frame[y * stride:y * stride + row_bytes])
        bottom = bytearray(frame[(y + 1) * stride:(y + 1) * stride + row_bytes])
        del top[4::5]
        del bottom[4::5]
        rgb = bytearray(width // 2 * 3)
        rgb[0::3] = top[1::2]
        rgb[1::3] = bytes((a + b) // 2 for a, b in zip(top[::2], bottom[1::2]))
        rgb[2::3] = bottom[::2]
        preview.write(rgb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=str.lower, choices=PORTS, default="cam2",
                        help="разъём Q6A (по умолчанию cam2/J16)")
    args = parser.parse_args()
    try:
        capture(args.port)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        sys.exit(str(error))
