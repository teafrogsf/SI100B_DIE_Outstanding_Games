from PIL import Image


def crop_and_save(image_path, output_folder, crop_size):
    # 打开图片
    image = Image.open(image_path)

    # 获取图片大小
    width, height = image.size

    # 确定行列数
    rows = height // crop_size[1]
    cols = width // crop_size[0]

    count = 1  # 初始化编号

    # 循环截取并保存子图
    for row in range(rows):
        for col in range(cols):
            # 计算截取区域的坐标
            left = col * crop_size[0]
            top = row * crop_size[1]
            right = left + crop_size[0]
            bottom = top + crop_size[1]

            # 截取子图
            cropped_image = image.crop((left, top, right, bottom))

            # 保存子图
            output_path = f"{output_folder}/{count}.png"
            cropped_image.save(output_path)

            count += 1


# 输入图片路径、输出文件夹路径和子图大小
image_path = "999.png"
output_folder = "."  # 当前文件夹
crop_size = (100, 100)

# 调用函数进行截取和保存
crop_and_save(image_path, output_folder, crop_size)
