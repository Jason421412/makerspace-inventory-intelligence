from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from makerspace_inventory.loaders import FIELDNAMES  # noqa: E402


SYNTHETIC_ROWS = [
    ("MC-001", "Arduino Uno R3", "microcontroller", "Cabinet A / Shelf 1", "Parts bin", "Blue", "", "", "recorded", ""),
    ("MC-002", "ESP32 Development Board", "microcontroller", "Cabinet A / Shelf 1", "Parts bin", "Green", "8", "8", "complete", ""),
    ("MC-003", "Raspberry Pi Pico", "microcontroller", "Cabinet A / Shelf 2", "Parts tray", "Green", "", "", "recorded", ""),
    ("MC-004", "Microcontroller Starter Kit", "microcontroller", "Cabinet A / Shelf 2", "Kit box", "Blue", "6", "5", "complete", "one cable replaced"),
    ("SN-001", "Ultrasonic Distance Sensor", "sensor", "Cabinet B / Shelf 1", "Sensor drawer", "Yellow", "12", "12", "complete", ""),
    ("SN-002", "Soil Moisture Sensor", "sensor", "Cabinet B / Shelf 1", "Sensor drawer", "Yellow", "", "", "recorded", ""),
    ("SN-003", "DHT Temperature Humidity Sensor", "sensor", "Cabinet B / Shelf 1", "Sensor drawer", "Yellow", "10", "8", "missing", "two units unavailable"),
    ("SN-004", "PIR Motion Sensor", "sensor", "Cabinet B / Shelf 2", "Sensor drawer", "Orange", "", "", "recorded", ""),
    ("SN-005", "RFID Reader Module", "sensor", "Cabinet B / Shelf 2", "Small parts case", "Orange", "5", "5", "complete", ""),
    ("PW-001", "Rechargeable Battery Pack", "power", "Cabinet C / Shelf 1", "Battery case", "Red", "10", "9", "missing", "one pack unavailable"),
    ("PW-002", "Power Supply Module", "power", "Cabinet C / Shelf 1", "Parts bin", "Red", "", "", "recorded", ""),
    ("PW-003", "USB Power Adapter", "power", "Cabinet C / Shelf 2", "Cable box", "Red", "15", "15", "complete", ""),
    ("PW-004", "Solar Charger Module", "power", "Cabinet C / Shelf 2", "Parts tray", "Red", "", "", "recorded", ""),
    ("RB-001", "Robot Chassis Kit", "robotics", "Cabinet D / Shelf 1", "Kit box", "Purple", "4", "4", "complete", ""),
    ("RB-002", "Servo Motor Pack", "robotics", "Cabinet D / Shelf 1", "Motor bin", "Purple", "20", "18", "unknown", "count needs verification"),
    ("RB-003", "DC Gear Motor", "robotics", "Cabinet D / Shelf 2", "Motor bin", "Purple", "", "", "recorded", ""),
    ("RB-004", "Wheel Set", "robotics", "Cabinet D / Shelf 2", "Parts bin", "Purple", "16", "14", "mixed", "two wheel sizes mixed"),
    ("RB-005", "Linear Actuator Demo Unit", "robotics", "Cabinet D / Shelf 3", "Demo box", "Purple", "", "", "recorded", ""),
    ("FB-001", "3D Printer Filament PLA", "fabrication", "Rack E / Shelf 1", "Filament rack", "White", "9", "9", "complete", ""),
    ("FB-002", "3D Printer Filament PLA Roll", "fabrication", "Rack E / Shelf 1", "Filament rack", "White", "", "", "recorded", "possible duplicate naming"),
    ("FB-003", "Acrylic Sheet Pack", "fabrication", "Rack E / Shelf 2", "Flat storage", "Clear", "", "", "recorded", ""),
    ("FB-004", "Laser-Safe Test Material Pack", "fabrication", "Rack E / Shelf 2", "Flat storage", "Clear", "6", "6", "complete", ""),
    ("CM-001", "LoRa Gateway Module", "communication", "Cabinet F / Shelf 1", "Network kit", "Gray", "2", "2", "complete", ""),
    ("CM-002", "WiFi Antenna Set", "communication", "Cabinet F / Shelf 1", "Network kit", "Gray", "", "", "recorded", ""),
    ("CM-003", "Bluetooth Serial Module", "communication", "Cabinet F / Shelf 2", "Parts tray", "Gray", "7", "6", "unknown", "count needs verification"),
    ("DP-001", "LCD Display Module", "display", "Cabinet G / Shelf 1", "Display drawer", "Teal", "", "", "recorded", ""),
    ("DP-002", "OLED Display Module", "display", "Cabinet G / Shelf 1", "Display drawer", "Teal", "8", "8", "complete", ""),
    ("DP-003", "RGB LED Strip", "display", "Cabinet G / Shelf 2", "Lighting box", "Teal", "5", "4", "unknown", "count needs verification"),
    ("TL-001", "Jumper Wire Bundle", "tooling", "Cabinet H / Shelf 1", "Cable box", "Black", "", "", "recorded", ""),
    ("TL-002", "Screwdriver Set", "tooling", "Cabinet H / Shelf 1", "Tool roll", "Black", "", "", "recorded", ""),
    ("TL-003", "Label Maker Cartridge", "tooling", "Cabinet H / Shelf 2", "Label box", "Black", "4", "4", "recorded", ""),
    ("TL-004", "Assorted Connector Kit", "tooling", "Cabinet H / Shelf 2", "Connector case", "Black", "", "", "no_label", "label needs replacement"),
    ("TL-005", "Portable Soldering Kit", "tooling", "Cabinet H / Shelf 3", "Tool case", "Black", "3", "3", "recorded", ""),
    ("SG-001", "Mini Water Pump", "smart_garden", "Cabinet I / Shelf 1", "Garden kit", "Green", "6", "5", "unknown", "count needs verification"),
    ("SG-002", "Grow Light Strip", "smart_garden", "Cabinet I / Shelf 1", "Garden kit", "Green", "", "", "recorded", ""),
    ("SG-003", "Plant Sensor Cable Set", "smart_garden", "Cabinet I / Shelf 2", "Cable pouch", "Green", "10", "10", "no_label", "label needs replacement"),
]


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SYNTHETIC_ROWS:
        asset_id, name, category, location, container, tag_color, expected_qty, actual_qty, status, notes = row
        rows.append(
            {
                "asset_id": asset_id,
                "name": name,
                "category": category,
                "location": location,
                "container": container,
                "tag_color": tag_color,
                "expected_qty": expected_qty,
                "actual_qty": actual_qty,
                "status": status,
                "notes": notes,
                "source": "synthetic_demo",
            }
        )
    return rows


def write_rows(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the synthetic sample inventory CSV.")
    parser.add_argument("--output", default=str(PROJECT_ROOT / "data" / "sample_inventory.csv"))
    args = parser.parse_args()

    rows = build_rows()
    write_rows(rows, Path(args.output))
    print(f"Wrote {len(rows)} synthetic rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
