from typing import Any
from pathlib import Path

# PlatformIO/SCons provides this at build time
env: Any
Import("env")  # type: ignore[name-defined]


# =====================================
# Find .env
# =====================================

project_dir = Path(env.subst("$PROJECT_DIR"))
env_file = project_dir / ".env"

if not env_file.exists():
    raise RuntimeError(
        f".env file not found at: {env_file}"
    )


# =====================================
# Load .env
# =====================================

variables = {}

with open(env_file, "r") as file:
    for line in file:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip().strip('"').strip("'")

        variables[key] = value


# =====================================
# Required variables
# =====================================

required = [
    "WIFI_SSID",
    "WIFI_PASSWORD",
    "BACKEND_HOST",
    "BACKEND_PORT",
    "NODE_ID",
]

for key in required:
    if key not in variables:
        raise RuntimeError(
            f"{key} is missing from {env_file}"
        )


# =====================================
# Escape values for C++ strings
# =====================================

def cpp_escape(value):
    return (
        value
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )


# =====================================
# Generate C++ configuration header
# =====================================

config_file = project_dir / "include" / "env_config.h"

with open(config_file, "w") as file:
    file.write("// AUTO-GENERATED FILE - DO NOT EDIT\n")
    file.write("// Generated from .env by scripts/load_env.py\n\n")

    file.write("#ifndef ENV_CONFIG_H\n")
    file.write("#define ENV_CONFIG_H\n\n")

    file.write(
        f'#define WIFI_SSID "{cpp_escape(variables["WIFI_SSID"])}"\n'
    )

    file.write(
        f'#define WIFI_PASSWORD "{cpp_escape(variables["WIFI_PASSWORD"])}"\n'
    )

    file.write(
        f'#define BACKEND_HOST "{cpp_escape(variables["BACKEND_HOST"])}"\n'
    )

    file.write(
        f'#define BACKEND_PORT {variables["BACKEND_PORT"]}\n'
    )

    file.write(
        f'#define NODE_ID "{cpp_escape(variables["NODE_ID"])}"\n'
    )

    file.write("\n#endif\n")


# =====================================
# Debug output
# =====================================

print("")
print("=====================================")
print("ESP32 .env configuration loaded")
print("=====================================")
print(f"WIFI_SSID     : {variables['WIFI_SSID']}")
print("WIFI_PASSWORD : ********")
print(f"BACKEND_HOST  : {variables['BACKEND_HOST']}")
print(f"BACKEND_PORT  : {variables['BACKEND_PORT']}")
print(f"NODE_ID       : {variables['NODE_ID']}")
print("-------------------------------------")
print(f"Generated     : {config_file}")
print("=====================================")
print("")