# 🎮 SAV File Editor - Công cụ chỉnh sửa file Active.sav

## 📋 Mô tả

Tool Python để đọc, chỉnh sửa và lưu file GVAS save (Unreal Engine 4) - đặc biệt là file Active.sav từ game PUBG Mobile hoặc tương tự.

## ✨ Tính năng

-   ✅ Đọc file .sav định dạng GVAS (Unreal Engine 4)
-   ✅ Xuất ra JSON để dễ đọc
-   ✅ Chỉnh sửa các properties: Int, Float, Bool
-   ✅ Lưu lại file với thay đổi tối thiểu
-   ✅ Tự động backup file gốc
-   ✅ Chế độ chỉnh sửa tương tác

## 📁 Files được tạo ra

1. **simple_editor.py** - Script chính
2. **Active_readable.json** - File JSON dễ đọc
3. **Active_modified.sav** - File SAV đã chỉnh sửa
4. **Active.sav.backup** - Backup file gốc

## 🚀 Cách sử dụng

### Chạy script cơ bản:

```bash
python simple_editor.py
```

### Các properties có thể chỉnh sửa:

-   **Gyroscope** (Int 0-10): Độ nhạy gyroscope
-   **ArtQuality** (Int 0-9): Chất lượng đồ họa
-   **FPSLevel** (Int 0-10): Giới hạn FPS
-   **CameraLensSensibility** (Int): Độ nhạy camera
-   **LeftRightShoot** (Bool): Chế độ bắn kép
-   **IntelligentDrugs** (Bool): Tự động dùng thuốc
-   **WallFeedBack** (Bool): Phản hồi va chạm tường
-   **LimitBandage** (Int): Giới hạn số băng
-   **LimitMedical** (Int): Giới hạn y tế
-   **LimitFirstAidKit** (Int): Giới hạn bộ cứu thương
-   **MainVolumValue** (Float 0.0-1.0): Âm lượng chính
-   **BGMVolumSwitcher** (Bool): Bật/tắt nhạc nền
-   **GameVersion** (String): Phiên bản game
-   **FpViewValue** (Int): Giá trị FOV
-   **RedDotCHColor** (Int): Màu ngắm Red Dot
-   **HolographicCHColor** (Int): Màu ngắm Holographic

### Ví dụ chỉnh sửa tùy chỉnh:

Khi script hỏi "Bạn muốn chỉnh sửa thêm không?", nhập:

```
Gyroscope 5
ArtQuality 9
LeftRightShoot true
MainVolumValue 0.8
```

## 📝 Ví dụ sử dụng trong code

```python
from simple_editor import SimpleSavEditor

# Đọc file
editor = SimpleSavEditor("Active.sav")
editor.read()
editor.find_properties()

# Xem các properties
editor.display()

# Chỉnh sửa
editor.edit_property('Gyroscope', 5)
editor.edit_property('FPSLevel', 10)
editor.edit_property('LeftRightShoot', True)

# Hoặc chỉnh sửa hàng loạt
editor.batch_edit({
    'Gyroscope': 5,
    'ArtQuality': 9,
    'FPSLevel': 10,
    'MainVolumValue': 0.8
})

# Lưu file
editor.save('Active_custom.sav')

# Xuất JSON
editor.export_json('settings.json')
```

## 🔧 Workflow

```
Active.sav (File gốc)
    ↓
[Đọc file] → Phân tích cấu trúc GVAS
    ↓
[Tìm properties] → Quét và extract các giá trị
    ↓
[Hiển thị] → Show danh sách properties
    ↓
[Xuất JSON] → Tạo Active_readable.json
    ↓
[Chỉnh sửa] → Thay đổi giá trị trong memory
    ↓
[Lưu file] → Ghi ra Active_modified.sav
```

## ⚠️ Lưu ý

-   File gốc được backup tự động thành `Active.sav.backup`
-   Chỉ nên chỉnh sửa các properties được liệt kê
-   String properties không nên chỉnh sửa nếu độ dài thay đổi
-   File SAV phải là định dạng GVAS (Unreal Engine 4)

## 🛠️ Cấu trúc file GVAS

```
[Header: "GVAS" + Version]
[Metadata blob]
[Properties:]
    - Property Name (với length prefix)
    - Property Type (IntProperty, FloatProperty, etc.)
    - Size (8 bytes)
    - Index byte
    - Value
[None terminator]
[Remaining data]
```

## 📊 Ví dụ Output

```
╔════════════════════════════════════════════════════════════════╗
║          SAV FILE EDITOR - Công cụ đơn giản                   ║
╚════════════════════════════════════════════════════════════════╝

✓ Đã đọc file: Active.sav (8979 bytes)
✓ Tìm thấy 16 properties có thể chỉnh sửa

📋 CÁC THUỘC TÍNH CÓ THỂ CHỈNH SỬA
═══════════════════════════════════════════════════════════════
 1. [IntProperty   ] Gyroscope                      = 1
 2. [IntProperty   ] ArtQuality                     = 8
 3. [IntProperty   ] FPSLevel                       = 8
 4. [BoolProperty  ] LeftRightShoot                 = ✓ BẬT
...

✏️  VÍ DỤ CHỈNH SỬA - Tối ưu hóa cài đặt game
═══════════════════════════════════════════════════════════════
✓ Đã thay đổi 'Gyroscope': 1 → 3
✓ Đã thay đổi 'ArtQuality': 8 → 9
✓ Đã thay đổi 'FPSLevel': 8 → 10
✓ Đã áp dụng 3/3 thay đổi thành công

💾 LƯU FILE
✓ Đã backup file gốc: Active.sav.backup
✓ Đã lưu file mới: Active_modified.sav

✅ HOÀN TẤT!
```

## 🎯 Khuyến nghị settings

### Cấu hình Performance cao:

```python
{
    'FPSLevel': 10,          # FPS tối đa
    'ArtQuality': 9,         # Đồ họa tốt nhất
    'Gyroscope': 3,          # Độ nhạy vừa phải
}
```

### Cấu hình Low-end device:

```python
{
    'FPSLevel': 5,           # FPS vừa
    'ArtQuality': 3,         # Đồ họa thấp
    'BGMVolumSwitcher': False  # Tắt nhạc nền
}
```

## 📞 Hỗ trợ

-   File SAV phải đúng định dạng GVAS
-   Tested với PUBG Mobile save files
-   Compatible với Python 3.6+

---

**Made with ❤️ for gamers**
