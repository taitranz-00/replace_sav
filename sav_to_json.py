#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAV to JSON Converter - Chuyển file .sav sang .json để edit
Usage: python sav_to_json.py <input.sav> [output.json]
"""

import struct
import json
import sys
from typing import Dict, Any


def read_sav_to_dict(filepath: str) -> Dict[str, Any]:
    """Đọc file SAV và chuyển thành dictionary"""
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())

    properties = {}

    # Danh sách properties cần tìm (với length prefix)
    known_props = [
        (b'\x0f\x00\x00\x00LeftRightShoot\x00', 'LeftRightShoot'),
        (b'\x11\x00\x00\x00IntelligentDrugs\x00', 'IntelligentDrugs'),
        (b'\x0a\x00\x00\x00Gyroscope\x00', 'Gyroscope'),
        (b'\x0b\x00\x00\x00ArtQuality\x00', 'ArtQuality'),
        (b'\x16\x00\x00\x00CameraLensSensibility\x00', 'CameraLensSensibility'),
        (b'\x09\x00\x00\x00FPSLevel\x00', 'FPSLevel'),
        (b'\x0d\x00\x00\x00WallFeedBack\x00', 'WallFeedBack'),
        (b'\x0d\x00\x00\x00LimitBandage\x00', 'LimitBandage'),
        (b'\x0d\x00\x00\x00LimitMedical\x00', 'LimitMedical'),
        (b'\x11\x00\x00\x00LimitFirstAidKit\x00', 'LimitFirstAidKit'),
        (b'\x11\x00\x00\x00BGMVolumSwitcher\x00', 'BGMVolumSwitcher'),
        (b'\x0f\x00\x00\x00MainVolumValue\x00', 'MainVolumValue'),
        (b'\x0c\x00\x00\x00GameVersion\x00', 'GameVersion'),
        (b'\x0c\x00\x00\x00FpViewValue\x00', 'FpViewValue'),
        (b'\x0e\x00\x00\x00RedDotCHColor\x00', 'RedDotCHColor'),
        (b'\x13\x00\x00\x00HolographicCHColor\x00', 'HolographicCHColor'),
    ]

    for prop_pattern, prop_name in known_props:
        pos = data.find(prop_pattern)
        if pos >= 0:
            type_pos = pos + len(prop_pattern)
            type_name_len = struct.unpack('<I', data[type_pos:type_pos+4])[0]
            type_name_start = type_pos + 4
            type_name = data[type_name_start:type_name_start+type_name_len-1].decode('ascii')

            size_pos = type_name_start + type_name_len
            value_start = size_pos + 8 + 1

            if type_name == 'IntProperty':
                value = struct.unpack('<i', data[value_start:value_start+4])[0]
                properties[prop_name] = {'type': 'IntProperty', 'value': value}

            elif type_name == 'FloatProperty':
                value = struct.unpack('<f', data[value_start:value_start+4])[0]
                properties[prop_name] = {'type': 'FloatProperty', 'value': value}

            elif type_name == 'BoolProperty':
                bool_pos = size_pos + 8
                value = bool(data[bool_pos])
                properties[prop_name] = {'type': 'BoolProperty', 'value': value}

            elif type_name == 'StrProperty':
                str_len = struct.unpack('<I', data[value_start:value_start+4])[0]
                if 0 < str_len < 1000:
                    str_value = data[value_start+4:value_start+4+str_len-1].decode('ascii', errors='ignore')
                    properties[prop_name] = {'type': 'StrProperty', 'value': str_value}

    return properties


def main():
    if len(sys.argv) < 2:
        print("❌ Thiếu tham số!")
        print("Usage: python sav_to_json.py <input.sav> [output.json]")
        print("Ví dụ: python sav_to_json.py Active.sav Active_edit.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.sav', '_edit.json')

    print(f"📖 Đọc file: {input_file}")
    properties = read_sav_to_dict(input_file)

    print(f"✓ Tìm thấy {len(properties)} properties")

    # Xuất ra JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(properties, f, indent=2, ensure_ascii=False)

    print(f"✓ Đã tạo file JSON: {output_file}")
    print(f"\n📝 Bây giờ bạn có thể edit file JSON này, sau đó dùng:")
    print(f"   python json_to_sav.py {output_file} Active_new.sav")


if __name__ == '__main__':
    main()
