def parse_config(filepath: str) -> dict:
    config = {}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key] = value
    return {
            "width": int(config["WIDTH"]),
            "height": int(config["HEIGHT"]),
            "entry": tuple(int(x) for x in config["ENTRY"].split(",")),
            "exit": tuple(int(x) for x in config["EXIT"].split(",")),
            "perfect": config["PERFECT"].lower() == "true",
            }
