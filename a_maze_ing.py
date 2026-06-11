#! /usr/bin/env python3

from config_parser import parse_config
import mlx

if __name__ == "__main__":
    cfg = parse_config("config.txt")
    print(cfg);
