import os
def find_images_with_number(directory, number):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                image_files.append(os.path.join(root, file))
    
    return image_files
# Sử dụng hàm để tìm ảnh có chứa mã số ở tên trong thư mục
directory_path = "images"
number = "110120111"
image_list = find_images_with_number(directory_path, number)

# In danh sách các tệp ảnh
for image in image_list:
    print(image)
