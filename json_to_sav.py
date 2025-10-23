#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON to SAV Converter - Chuyển file JSON đã edit về .sav
Usage: python json_to_sav.py <input.json> <template.sav> [output.sav]
"""

import struct
import json
import sys
import shutil
from typing import Dict, Any


def apply_json_to_sav(json_file: str, template_sav: str, output_sav: str):
    """Áp dụng các thay đổi từ JSON vào file SAV"""

    # Đọc JSON
    print(f"📖 Đọc file JSON: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        properties = json.load(f)

    print(f"✓ Load được {len(properties)} properties từ JSON")

    # Đọc template SAV
    print(f"📖 Đọc template SAV: {template_sav}")
    with open(template_sav, 'rb') as f:
        data = bytearray(f.read())

    # Map pattern cho mỗi property
    prop_patterns = {
        'LeftRightShoot': b'\x0f\x00\x00\x00LeftRightShoot\x00',
        'IntelligentDrugs': b'\x11\x00\x00\x00IntelligentDrugs\x00',
        'Gyroscope': b'\x0a\x00\x00\x00Gyroscope\x00',
        'ArtQuality': b'\x0b\x00\x00\x00ArtQuality\x00',
        'CameraLensSensibility': b'\x16\x00\x00\x00CameraLensSensibility\x00',
        'FPSLevel': b'\x09\x00\x00\x00FPSLevel\x00',
        'WallFeedBack': b'\x0d\x00\x00\x00WallFeedBack\x00',
        'LimitBandage': b'\x0d\x00\x00\x00LimitBandage\x00',
        'LimitMedical': b'\x0d\x00\x00\x00LimitMedical\x00',
        'LimitFirstAidKit': b'\x11\x00\x00\x00LimitFirstAidKit\x00',
        'BGMVolumSwitcher': b'\x11\x00\x00\x00BGMVolumSwitcher\x00',
        'MainVolumValue': b'\x0f\x00\x00\x00MainVolumValue\x00',
        'GameVersion': b'\x0c\x00\x00\x00GameVersion\x00',
        'FpViewValue': b'\x0c\x00\x00\x00FpViewValue\x00',
        'RedDotCHColor': b'\x0e\x00\x00\x00RedDotCHColor\x00',
        'HolographicCHColor': b'\x13\x00\x00\x00HolographicCHColor\x00',
    }

    changes = 0

    # Áp dụng từng property
    for prop_name, prop_data in properties.items():
        if prop_name not in prop_patterns:
            print(f"⚠️  Bỏ qua property không xác định: {prop_name}")
            continue

        pattern = prop_patterns[prop_name]
        pos = data.find(pattern)

        if pos < 0:
            print(f"❌ Không tìm thấy property: {prop_name}")
            continue

        # Tính toán vị trí giá trị
        type_pos = pos + len(pattern)
        type_name_len = struct.unpack('<I', data[type_pos:type_pos+4])[0]
        type_name_start = type_pos + 4
        size_pos = type_name_start + type_name_len
        value_start = size_pos + 8 + 1

        prop_type = prop_data['type']
        new_value = prop_data['value']

        try:
            if prop_type == 'IntProperty':
                old_value = struct.unpack('<i', data[value_start:value_start+4])[0]
                struct.pack_into('<i', data, value_start, int(new_value))
                print(f"✓ {prop_name}: {old_value} → {new_value}")
                changes += 1

            elif prop_type == 'FloatProperty':
                old_value = struct.unpack('<f', data[value_start:value_start+4])[0]
                struct.pack_into('<f', data, value_start, float(new_value))
                print(f"✓ {prop_name}: {old_value:.4f} → {new_value}")
                changes += 1

            elif prop_type == 'BoolProperty':
                bool_pos = size_pos + 8
                old_value = bool(data[bool_pos])
                data[bool_pos] = 1 if new_value else 0
                print(f"✓ {prop_name}: {old_value} → {new_value}")
                changes += 1

            elif prop_type == 'StrProperty':
                print(f"⚠️  Bỏ qua String property: {prop_name} (không hỗ trợ edit)")

        except Exception as e:
            print(f"❌ Lỗi khi áp dụng {prop_name}: {e}")

    # Lưu file
    print(f"\n💾 Lưu file: {output_sav}")
    with open(output_sav, 'wb') as f:
        f.write(data)

    print(f"✅ Hoàn tất! Đã áp dụng {changes}/{len(properties)} thay đổi")
    print(f"\n🔍 Kiểm tra thay đổi:")
    print(f"   python compare_sav.py {template_sav} {output_sav}")


def main():
    if len(sys.argv) < 3:
        print("❌ Thiếu tham số!")
        print("Usage: python json_to_sav.py <input.json> <template.sav> [output.sav]")
        print("Ví dụ: python json_to_sav.py Active_edit.json Active.sav Active_new.sav")
        sys.exit(1)

    json_file = sys.argv[1]
    template_sav = sys.argv[2]
    output_sav = sys.argv[3] if len(sys.argv) > 3 else 'Active_modified.sav'

    apply_json_to_sav(json_file, template_sav, output_sav)


if __name__ == '__main__':
    main()
