# 🎮 SAV Editor - 3 Lệnh Đơn Giản

## 📝 WORKFLOW ĐƠN GIẢN

### Bước 1️⃣: SAV → JSON (để edit)

```bash
python sav_to_json.py Active.sav MyEdit.json
```

-   Chuyển file SAV sang JSON
-   File JSON dễ đọc và chỉnh sửa bằng text editor

### Bước 2️⃣: Edit JSON File

Mở `MyEdit.json` và chỉnh sửa giá trị:

```json
{
  "Gyroscope": {
    "type": "IntProperty",
    "value": 5        ← Sửa từ 1 thành 5
  },
  "ArtQuality": {
    "type": "IntProperty",
    "value": 9        ← Sửa từ 8 thành 9
  },
  "FPSLevel": {
    "type": "IntProperty",
    "value": 10       ← Sửa từ 8 thành 10
  }
}
```

### Bước 3️⃣: JSON → SAV (tạo file mới)

```bash
python json_to_sav.py MyEdit.json Active.sav Active_new.sav
```

-   Áp dụng thay đổi từ JSON vào file SAV
-   Tạo file mới `Active_new.sav`

### Bước 4️⃣: So sánh 2 file SAV

```bash
python compare_sav.py Active.sav Active_new.sav
```

-   Hiển thị các properties đã thay đổi
-   Hiển thị số bytes khác nhau
-   Xác nhận thay đổi thành công

---

## 📋 PROPERTIES CÓ THỂ CHỈNH SỬA

| Property                  | Type  | Mô tả               | Giá trị    |
| ------------------------- | ----- | ------------------- | ---------- |
| **Gyroscope**             | Int   | Độ nhạy gyroscope   | 0-10       |
| **ArtQuality**            | Int   | Chất lượng đồ họa   | 0-9        |
| **FPSLevel**              | Int   | Giới hạn FPS        | 0-10       |
| **CameraLensSensibility** | Int   | Độ nhạy camera      | 0-10       |
| **LeftRightShoot**        | Bool  | Bắn kép             | true/false |
| **IntelligentDrugs**      | Bool  | Tự động dùng thuốc  | true/false |
| **WallFeedBack**          | Bool  | Phản hồi va chạm    | true/false |
| **LimitBandage**          | Int   | Giới hạn băng       | 0-10       |
| **LimitMedical**          | Int   | Giới hạn y tế       | 0-10       |
| **LimitFirstAidKit**      | Int   | Giới hạn cứu thương | 0-10       |
| **MainVolumValue**        | Float | Âm lượng            | 0.0-1.0    |
| **BGMVolumSwitcher**      | Bool  | Nhạc nền            | true/false |
| **FpViewValue**           | Int   | FOV góc nhìn        | 60-120     |
| **RedDotCHColor**         | Int   | Màu ngắm            | 0-10       |
| **HolographicCHColor**    | Int   | Màu ngắm Holo       | 0-10       |

---

## 🚀 VÍ DỤ NHANH

```bash
# 1. Tạo JSON từ SAV
python sav_to_json.py Active.sav edit.json

# 2. Edit file edit.json với notepad hoặc VS Code
notepad edit.json

# 3. Tạo SAV mới từ JSON đã edit
python json_to_sav.py edit.json Active.sav Active_modified.sav

# 4. Kiểm tra thay đổi
python compare_sav.py Active.sav Active_modified.sav
```

---

## ⚡ ONE-LINER

Nếu chỉ cần xem nhanh:

```bash
# Xem nội dung SAV dạng JSON
python sav_to_json.py Active.sav temp.json && type temp.json
```

---

## 📊 OUTPUT MẪU

### sav_to_json.py:

```
📖 Đọc file: Active.sav
✓ Tìm thấy 16 properties
✓ Đã tạo file JSON: MyEdit.json
```

### json_to_sav.py:

```
✓ Gyroscope: 1 → 5
✓ ArtQuality: 8 → 9
✓ FPSLevel: 8 → 10
✅ Hoàn tất! Đã áp dụng 15/16 thay đổi
```

### compare_sav.py:

```
⚠️  PHÁT HIỆN 4 ĐIỂM KHÁC NHAU:
Property                  File 1      File 2
-----------------------------------------------
Gyroscope                 1           5
ArtQuality                8           9
FPSLevel                  8           10
CameraLensSensibility     6           8

📊 TỔNG KẾT:
   - Properties khác nhau: 4
   - Bytes khác nhau: 4
```

---

## 💡 TIPS

1. **Backup quan trọng**: Luôn giữ file `Active.sav` gốc
2. **Kiểm tra trước khi dùng**: Chạy `compare_sav.py` để xác nhận
3. **Edit cẩn thận**: Chỉ sửa giá trị, không sửa "type"
4. **String properties**: Không nên edit (có thể gây lỗi)

---

## ⚠️ LƯU Ý

-   File SAV phải là định dạng GVAS (Unreal Engine 4)
-   Chỉ thay đổi giá trị (value), không đổi type
-   String properties bị bỏ qua khi chuyển về SAV
-   Luôn test file mới trước khi dùng trong game

---

**✨ Đơn giản, nhanh, hiệu quả!**
