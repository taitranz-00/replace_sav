#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple SAV Editor - Đọc và chỉnh sửa file GVAS save đơn giản hơn
"""

import struct
import json
import os
import re
from typing import Dict, List, Any


class SimpleSavEditor:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = bytearray()
        self.properties_found = {}

    def read(self):
        """Đọc toàn bộ file vào memory"""
        with open(self.filepath, 'rb') as f:
            self.data = bytearray(f.read())

        print(f"✓ Đã đọc file: {self.filepath} ({len(self.data)} bytes)")
        return self

    def find_properties(self):
        """Tìm và extract các properties có thể đọc được"""
        print("\n📋 Đang quét các properties trong file...")

        # Danh sách các properties thường gặp trong PUBG/UE4 save files
        # Format: (search_pattern, display_name)
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

        # Tìm vị trí của các properties
        for prop_pattern, prop_name in known_props:
            pos = self.data.find(prop_pattern)
            if pos >= 0:  # Changed from > 0 to >= 0
                # Tìm type của property (IntProperty, FloatProperty, BoolProperty, StrProperty)
                # Type name bắt đầu ngay sau property name, cũng có length prefix
                type_pos = pos + len(prop_pattern)

                # Đọc length của type name
                type_name_len = struct.unpack('<I', self.data[type_pos:type_pos+4])[0]
                type_name_start = type_pos + 4
                type_name = self.data[type_name_start:type_name_start+type_name_len-1].decode('ascii')

                # Vị trí của size field (8 bytes)
                size_pos = type_name_start + type_name_len
                prop_size = struct.unpack('<Q', self.data[size_pos:size_pos+8])[0]

                # Vị trí giá trị (sau size + index byte)
                value_start = size_pos + 8 + 1

                # Đọc giá trị dựa theo type
                if type_name == 'IntProperty':
                    if value_start + 4 <= len(self.data):
                        value = struct.unpack('<i', self.data[value_start:value_start+4])[0]
                        self.properties_found[prop_name] = {
                            'type': 'IntProperty',
                            'position': value_start,
                            'value': value
                        }

                elif type_name == 'FloatProperty':
                    if value_start + 4 <= len(self.data):
                        value = struct.unpack('<f', self.data[value_start:value_start+4])[0]
                        self.properties_found[prop_name] = {
                            'type': 'FloatProperty',
                            'position': value_start,
                            'value': value
                        }

                elif type_name == 'BoolProperty':
                    # Bool đặc biệt: value ở ngay trước size (1 byte trước size field)
                    bool_pos = size_pos + 8
                    if bool_pos < len(self.data):
                        value = bool(self.data[bool_pos])
                        self.properties_found[prop_name] = {
                            'type': 'BoolProperty',
                            'position': bool_pos,
                            'value': value
                        }

                elif type_name == 'StrProperty':
                    if value_start + 4 <= len(self.data):
                        str_len = struct.unpack('<I', self.data[value_start:value_start+4])[0]
                        if 0 < str_len < 1000:
                            str_value = self.data[value_start+4:value_start+4+str_len-1].decode('ascii', errors='ignore')
                            self.properties_found[prop_name] = {
                                'type': 'StrProperty',
                                'position': value_start + 4,
                                'length': str_len,
                                'value': str_value
                            }

        print(f"✓ Tìm thấy {len(self.properties_found)} properties có thể chỉnh sửa")
        return self

    def display(self):
        """Hiển thị các properties"""
        print("\n" + "="*80)
        print("📋 CÁC THUỘC TÍNH CÓ THỂ CHỈNH SỬA")
        print("="*80)

        for i, (name, prop) in enumerate(sorted(self.properties_found.items()), 1):
            value = prop['value']
            prop_type = prop['type']

            if prop_type == 'FloatProperty':
                display_value = f"{value:.4f}"
            elif prop_type == 'BoolProperty':
                display_value = "✓ BẬT" if value else "✗ TẮT"
            else:
                display_value = str(value)

            print(f"{i:2d}. [{prop_type:14s}] {name:30s} = {display_value}")

        print("="*80 + "\n")

    def export_json(self, output_file: str = "Active_readable.json"):
        """Export ra JSON để dễ đọc"""
        export_data = {}

        for name, prop in self.properties_found.items():
            export_data[name] = {
                'type': prop['type'],
                'value': prop['value']
            }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Đã xuất dữ liệu ra: {output_file}")
        return output_file

    def edit_property(self, prop_name: str, new_value):
        """Chỉnh sửa một property"""
        if prop_name not in self.properties_found:
            print(f"❌ Không tìm thấy property: {prop_name}")
            available = ', '.join(sorted(self.properties_found.keys()))
            print(f"   Properties có sẵn: {available}")
            return False

        prop = self.properties_found[prop_name]
        old_value = prop['value']
        pos = prop['position']

        try:
            if prop['type'] == 'IntProperty':
                new_value = int(new_value)
                struct.pack_into('<i', self.data, pos, new_value)
                prop['value'] = new_value

            elif prop['type'] == 'FloatProperty':
                new_value = float(new_value)
                struct.pack_into('<f', self.data, pos, new_value)
                prop['value'] = new_value

            elif prop['type'] == 'BoolProperty':
                if isinstance(new_value, str):
                    new_value = new_value.lower() in ['true', '1', 'yes', 'on', 'bật']
                new_value = bool(new_value)
                self.data[pos] = 1 if new_value else 0
                prop['value'] = new_value

            elif prop['type'] == 'StrProperty':
                # String phức tạp hơn, cần cẩn thận với length
                print(f"⚠️  Cảnh báo: Chỉnh sửa string có thể gây lỗi nếu độ dài thay đổi")
                return False

            print(f"✓ Đã thay đổi '{prop_name}': {old_value} → {new_value}")
            return True

        except Exception as e:
            print(f"❌ Lỗi khi chỉnh sửa: {e}")
            return False

    def save(self, output_file: str = None):
        """Lưu file đã chỉnh sửa"""
        if output_file is None:
            # Tạo backup
            backup = self.filepath + '.backup'
            if not os.path.exists(backup):
                import shutil
                shutil.copy2(self.filepath, backup)
                print(f"✓ Đã backup file gốc: {backup}")

            output_file = self.filepath.replace('.sav', '_modified.sav')

        with open(output_file, 'wb') as f:
            f.write(self.data)

        print(f"✓ Đã lưu file mới: {output_file}")
        return output_file

    def batch_edit(self, changes: Dict[str, Any]):
        """Chỉnh sửa nhiều properties cùng lúc"""
        print(f"\n✏️  Đang áp dụng {len(changes)} thay đổi...")
        success = 0

        for prop_name, new_value in changes.items():
            if self.edit_property(prop_name, new_value):
                success += 1

        print(f"✓ Đã áp dụng {success}/{len(changes)} thay đổi thành công")
        return success == len(changes)


def main():
    """Chương trình chính"""
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "SAV FILE EDITOR - Công cụ đơn giản" + " "*24 + "║")
    print("╚" + "="*78 + "╝\n")

    sav_file = "Active.sav"

    if not os.path.exists(sav_file):
        print(f"❌ Không tìm thấy file: {sav_file}")
        return

    # Đọc file
    editor = SimpleSavEditor(sav_file)
    editor.read()

    # Tìm properties
    editor.find_properties()

    # Hiển thị
    editor.display()

    # Export JSON
    editor.export_json()

    # Ví dụ chỉnh sửa
    print("\n" + "="*80)
    print("✏️  VÍ DỤ CHỈNH SỬA - Tối ưu hóa cài đặt game")
    print("="*80)

    example_changes = {
        'Gyroscope': 3,           # Tăng độ nhạy gyroscope
        'ArtQuality': 9,          # Đặt chất lượng đồ họa cao nhất
        'FPSLevel': 10,           # FPS cao nhất
        'LeftRightShoot': True,   # Bật chế độ bắn kép
    }

    editor.batch_edit(example_changes)

    # Cho phép chỉnh sửa thêm
    print("\n" + "="*80)
    while True:
        choice = input("\nBạn muốn chỉnh sửa thêm không? (y/n hoặc tên_property giá_trị): ").strip()

        if choice.lower() in ['n', 'no', 'không', 'k']:
            break
        elif choice.lower() in ['y', 'yes']:
            prop = input("  Tên property: ").strip()
            val = input("  Giá trị mới: ").strip()
            editor.edit_property(prop, val)
        else:
            # Thử parse "property value"
            parts = choice.split(None, 1)
            if len(parts) == 2:
                editor.edit_property(parts[0], parts[1])
            elif choice:
                print("  Sai định dạng! Dùng: property_name giá_trị")

    # Lưu file
    print("\n" + "="*80)
    print("💾 LƯU FILE")
    print("="*80)
    output = editor.save()

    print("\n" + "="*80)
    print("✅ HOÀN TẤT!")
    print(f"   📁 File gốc: {sav_file}")
    print(f"   📁 File backup: {sav_file}.backup")
    print(f"   📁 File JSON: Active_readable.json")
    print(f"   📁 File đã sửa: {output}")
    print("="*80)


if __name__ == '__main__':
    main()
