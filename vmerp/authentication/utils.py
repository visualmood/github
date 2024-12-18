# 这个utils.py是用来生产一个随机的图片验证码的。验证码是四个随机的字母或者数字组成的。
# 利用PIL库生成验证码图片，并将图片中数字转换成小写的字母保存到cookies。然后在登录和注册界面调用本函数生成验证码图片。
# 验证码图片的有效期为5分钟。防止恶意登录及注册及爬虫。
import random
import io
import string
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter    # 导入PIL库

# 生成验证码图片函数，返回验证码verify_code和图片buf
def generate_verify_code():                     # 生成验证码图片函数
    background = (                              # 验证码图片的背景颜色
        random.randrange(200, 250),             # 随机生成背景颜色
        random.randrange(200, 250),             # 随机生成背景颜色
        random.randrange(200, 250)              # 随机生成背景颜色
    )
    outline = ImageColor.getrgb("Grey")         # 验证码图片的边框颜色
    line_color = (                              # 验证码图片的干扰线颜色    
        random.randrange(1, 255),               # 随机生成干扰线颜色
        random.randrange(1, 255),               # 随机生成干扰线颜色
        random.randrange(1, 255)                # 随机生成干扰线颜色
    )
    img_width = 200                              # 验证码图片的宽度
    img_height = 80                              # 验证码图片的高度
    font_color = (                               # 验证码图片的字体颜色 
        random.randrange(100, 160),
        random.randrange(100, 160),
        random.randrange(100, 160)
    )
    font = ImageFont.load_default(img_height - 4)                           # 验证码图片的字体

    canvas = Image.new('RGB', (img_width, img_height))                      # 创建一个空白的图片
    code = random.sample(string.ascii_letters + string.digits, 4)           # 随机生成四个字母或者数字
    draw = ImageDraw.Draw(canvas)                                           # 创建一个画笔
    # background
    box = (0, 0, img_width, img_height)                                     # 画布的大小    
    draw.rectangle(box, fill=background, outline=outline)                   # 画背景

    yawp_rate = 0.07                                                        # 干扰线的数量
    area = int(yawp_rate * img_height * img_width)                          # 干扰线的数量
    for x in range(area):                                                   # 随机生成干扰线  
        y = random.randrange(0, img_height - 1)                                          
        x = random.randrange(0, img_width - 1)
        draw.point((x, y), fill=(0, 0, 0))                                  # 画干扰线                    



    # noise lines
    for i in range(random.randrange(3, 23)):                                # 随机生成干扰线    
        x = random.randrange(0, img_width - 1)
        y = random.randrange(0, img_height - 1)
        xl = random.randrange(0, 6)
        yl = random.randrange(0, 12)
        draw.line((x, y, x + xl + 40, y + yl + 20), fill=line_color, width=1)

    # print the verify code
    x = 5
    for i in code:
        y = random.randrange(-10, 10)
        draw.text((x, y), i, font=font, fill=random.choice(font_color))
        x += 45


    verify_code = ''.join(code).lower()                                     # 将验证码转换成小写字母
    im = canvas.filter(ImageFilter.SMOOTH_MORE)                             # 图片模糊化
    buf = io.BytesIO()                                                      # 将图片保存到内存中  
    im.save(buf, 'gif')                                                     # 保存图片到内存中    
    buf.seek(0)                                                             # 将指针移动到开头   

    return verify_code, buf                                                 # 返回验证码和图片



# 获取客户端IP地址函数,返回客户端IP地址
def get_client_ip(request):                                            # 获取客户端IP地址  
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")         # 获取HTTP_X_FORWARDED_FOR的值
    if x_forwarded_for:                                                # 如果HTTP_X_FORWARDED_FOR存在，则取第一个值作为客户端IP 
        ip = x_forwarded_for.split(",")[0]                             # 否则取REMOTE_ADDR的值作为客户端IP
    else:                                                              # 如果HTTP_X_FORWARDED_FOR不存在，则取REMOTE_ADDR的值作为客户端IP
        ip = request.META.get("REMOTE_ADDR")                           # 否则
    return ip                                                          # 返回客户端IP地址


