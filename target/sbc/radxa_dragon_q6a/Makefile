CXX ?= g++
CXXFLAGS ?= -std=c++17 -O3 -Wall -Wextra -Werror -pthread
KERNEL ?= $(shell uname -r)
BASE_DTB ?= build/base-q6a.dtb
DEMO_LIBS = $(shell pkg-config --cflags --libs libcamera sdl2 glesv2)

.PHONY: demo driver overlay overlay-check check fetch
demo: build/ar0234-demo

build/ar0234-demo: demo/ar0234-demo.cpp
	mkdir -p build
	$(CXX) $(CXXFLAGS) $< -o $@.new $(DEMO_LIBS)
	mv $@.new $@

fetch:
	python3 tools/fetch-driver.py

driver: fetch
	mkdir -p build/driver
	cp vendor/ar0234.c build/driver/ar0234.c
	printf 'obj-m += ar0234.o\nccflags-y += -Werror\n' > build/driver/Kbuild
	$(MAKE) -C /lib/modules/$(KERNEL)/build M=$(CURDIR)/build/driver -j4 modules

overlay: build/ar0234-cam2.dtbo

build/ar0234-cam2.dtbo: overlay/ar0234-cam2.dts
	mkdir -p build
	dtc -@ -I dts -O dtb -o $@ $<

overlay-check: overlay
	fdtoverlay -i $(BASE_DTB) -o build/q6a-ar0234-cam2-test.dtb build/ar0234-cam2.dtbo
	fdtget build/q6a-ar0234-cam2-test.dtb /soc@0/cci@ac4b000/i2c-bus@0/ar0234@10 compatible
	fdtget build/q6a-ar0234-cam2-test.dtb /soc@0/cci@ac4b000/i2c-bus@0/ar0234@10/port/endpoint data-lanes
	fdtget build/q6a-ar0234-cam2-test.dtb /soc@0/isp@acb3000 status

check: demo
	./build/ar0234-demo --self-test
