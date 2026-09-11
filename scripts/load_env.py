Import("env")

from pathlib import Path
import os


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
# Load .env manually
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
# Inject variables into C++ compiler
# =====================================

env.Append(
    BUILD_FLAGS=[
        f'-DWIFI_SSID=\\"{variables["WIFI_SSID"]}\\"',
        f'-DWIFI_PASSWORD=\\"{variables["WIFI_PASSWORD"]}\\"',
        f'-DBACKEND_HOST=\\"{variables["BACKEND_HOST"]}\\"',
        f'-DBACKEND_PORT=\\"{variables["BACKEND_PORT"]}\\"',
        f'-DNODE_ID=\\"{variables["NODE_ID"]}\\"',
    ]
)


# =====================================
# Debug output
# =====================================

print("")
print("=====================================")
print("ESP32 .env configuration loaded")
print("=====================================")
print(f"WIFI_SSID     : {variables['WIFI_SSID']}")
print(f"WIFI_PASSWORD : ********")
print(f"BACKEND_HOST  : {variables['BACKEND_HOST']}")
print(f"BACKEND_PORT  : {variables['BACKEND_PORT']}")
print(f"NODE_ID       : {variables['NODE_ID']}")
print("=====================================")
print("")