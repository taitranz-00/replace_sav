#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAV File Comparator - So sánh 2 file .sav và hiển thị điểm khác nhau
Usage: python compare_sav.py <file1.sav> <file2.sav>
"""

import struct
import sys
from typing import Dict, Any, Tuple


def read_sav_properties(filepath: str) -> Dict[str, Any]:
    """Đọc properties từ file SAV"""
    with open(filepath, 'rb') as f:
        data = bytearray(f.read())

    properties = {}

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


def compare_byte_level(file1: str, file2: str) -> Tuple[int, int, list]:
    """So sánh ở mức byte"""
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    differences = []
    min_len = min(len(data1), len(data2))

    for i in range(min_len):
        if data1[i] != data2[i]:
            differences.append((i, data1[i], data2[i]))

    # Check length difference
    if len(data1) != len(data2):
        differences.append((min_len, None, None))  # Mark length difference

    return len(data1), len(data2), differences


def main():
    if len(sys.argv) < 3:
        print("❌ Thiếu tham số!")
        print("Usage: python compare_sav.py <file1.sav> <file2.sav>")
        print("Ví dụ: python compare_sav.py Active.sav Active_modified.sav")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    print("╔" + "="*78 + "╗")
    print("║" + " "*25 + "SO SÁNH 2 FILE SAV" + " "*35 + "║")
    print("╚" + "="*78 + "╝\n")

    print(f"📄 File 1: {file1}")
    print(f"📄 File 2: {file2}")
    print()

    # So sánh properties
    print("🔍 So sánh Properties...")
    props1 = read_sav_properties(file1)
    props2 = read_sav_properties(file2)

    print(f"   File 1: {len(props1)} properties")
    print(f"   File 2: {len(props2)} properties")
    print()

    # Tìm khác biệt
    all_props = set(props1.keys()) | set(props2.keys())
    differences = []

    for prop in sorted(all_props):
        val1 = props1.get(prop)
        val2 = props2.get(prop)

        if val1 is None:
            differences.append((prop, "Missing", val2['value']))
        elif val2 is None:
            differences.append((prop, val1['value'], "Missing"))
        elif val1['value'] != val2['value']:
            differences.append((prop, val1['value'], val2['value']))

    # Hiển thị kết quả
    if differences:
        print("=" * 80)
        print(f"⚠️  PHÁT HIỆN {len(differences)} ĐIỂM KHÁC NHAU:")
        print("=" * 80)
        print(f"{'Property':<30} {'File 1':<20} {'File 2':<20}")
        print("-" * 80)

        for prop, val1, val2 in differences:
            # Format values
            if isinstance(val1, float):
                val1_str = f"{val1:.4f}"
            elif isinstance(val1, bool):
                val1_str = "BẬT" if val1 else "TẮT"
            else:
                val1_str = str(val1)

            if isinstance(val2, float):
                val2_str = f"{val2:.4f}"
            elif isinstance(val2, bool):
                val2_str = "BẬT" if val2 else "TẮT"
            else:
                val2_str = str(val2)

            print(f"{prop:<30} {val1_str:<20} {val2_str:<20}")

        print("=" * 80)
    else:
        print("✅ KHÔNG CÓ SỰ KHÁC BIỆT trong các properties!")

    # So sánh byte level
    print("\n🔬 So sánh ở mức Byte...")
    size1, size2, byte_diffs = compare_byte_level(file1, file2)

    print(f"   File 1: {size1} bytes")
    print(f"   File 2: {size2} bytes")

    if size1 != size2:
        print(f"   ⚠️  Chênh lệch kích thước: {abs(size1-size2)} bytes")

    if byte_diffs:
        print(f"   ⚠️  Có {len(byte_diffs)} bytes khác nhau")

        # Hiển thị một số bytes khác nhau đầu tiên
        if len(byte_diffs) <= 20:
            print("\n   Chi tiết bytes khác nhau:")
            for offset, b1, b2 in byte_diffs[:20]:
                if b1 is not None and b2 is not None:
                    print(f"      Offset 0x{offset:04X}: 0x{b1:02X} → 0x{b2:02X}")
    else:
        print("   ✅ Hai file giống hệt nhau!")

    print("\n" + "=" * 80)
    print("📊 TỔNG KẾT:")
    print(f"   - Properties khác nhau: {len(differences)}")
    print(f"   - Bytes khác nhau: {len(byte_diffs)}")
    print("=" * 80)


if __name__ == '__main__':
    main()
