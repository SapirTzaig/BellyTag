import os

name1 = "Ultrasound-for-Fetal-Nuchal-Translucency_20250309102726"
name2 = "Ultrasound-for-Fetal-Nuchal-Translucency_20250304102726"
name3 = "Ultrasound-for-Fetal-Nuchal-Translucency_20250309102826"

names = [name1, name2, name3]

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


dir_path = r'C:\Users\galev\OneDrive\Desktop'


def get_updated_file(dir_path, test_name):
    files = [
        f for f in os.listdir(dir_path)
        if f.startswith(test_name) and f.split('.')[-1] in ALLOWED_EXTENSIONS
    ]

    if not files:
        return None  # No matching files found

    # Use max() to get the most updated file based on filename sorting
    return max(files)

if __name__ == "__main__":
    dir_path = r'C:\Users\galev\OneDrive\Desktop'
    test_name = "Ultrasound-for-Fetal-Nuchal-Translucency"
    latest = get_updated_file(dir_path, test_name)
    print(latest)

