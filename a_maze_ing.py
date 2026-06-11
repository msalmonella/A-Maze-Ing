#! /usr/bin/env python3

from config_parser import parse_config
from cell import cell_generator
from config_parser import parse_config
import mlx

if __name__ == "__main__":
    cfg = parse_config("config.txt")
    ma_ze_p: list = cell_generator(cfg["width"], cfg["height"])
    print(ma_ze_p)
