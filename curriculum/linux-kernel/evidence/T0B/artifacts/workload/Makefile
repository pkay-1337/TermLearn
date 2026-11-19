CC ?= gcc
CFLAGS ?= -std=c99 -Wall -Wextra -g -Iinclude

all: app

app: src/main.o src/sensor.o src/bus.o
	$(CC) $(CFLAGS) $^ -o $@

src/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f src/*.o app

.PHONY: all clean
