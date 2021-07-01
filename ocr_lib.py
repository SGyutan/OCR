"""
tesseract install
https://gammasoft.jp/blog/tesseract-ocr-install-on-windows/

https://itport.cloud/?p=8326
    
"""
import os
import pyocr
import pyocr.builders
import cv2
from PIL import Image, ImageOps,ImageDraw
import sys
from matplotlib import pyplot as plt

# 1.インストール済みのTesseractのパスを通す
path_tesseract = "C:\Program Files\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

def cv2pil(image):
    '''
     [Pillow ↔ OpenCV 変換](https://qiita.com/derodero24/items/f22c22b22451609908ee)
     OpenCV型 -> PIL型 
     '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def ocr_tool_opencv(file_name,bitwise=True):
    """
     using opencv and Pillow
     
    Args:
        file_name ([type]): file name str
        bitwise (bool, optional): Black and white inversion . Defaults to True.
    """
    #利用可能なOCRツールを取得
    tools = pyocr.get_available_tools()
 
    if len(tools) == 0:
        print("Do not find OCR tools")
        sys.exit(1)
    
    #利用可能なOCRツールはtesseractしか導入していないため、0番目のツールを利用
    tool = tools[0]
    
    np_image = cv2.imread(file_name) 
    np_gray_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)

    # 画像処理
    blue = cv2.GaussianBlur(np_gray_image,(5,5),0)
    # print(blue.dtype, np_gray_image.dtype)　-> uint8
    tho = cv2.adaptiveThreshold(blue,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    # ret , tho = cv2.threshold(blue,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    if bitwise:
        tho = cv2.bitwise_not(tho)
    
    # convert to pillow image　->  pil.Image型にしないとエラーになる
    pil_image = Image.fromarray(tho)
    
    builder_list = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
    builder_text = pyocr.builders.TextBuilder(tesseract_layout=6) 
            # TextBuilder  文字列を認識  
            # WordBoxBuilder  単語単位で文字認識 + BoundingBox  
            # LineBoxBuilder  行単位で文字認識 + BoundingBox  
            # DigitBuilder  数字 / 記号を認識
            # DigitLineBoxBuilder  数字 / 記号を認識 + BoundingBox  
    res = tool.image_to_string(pil_image,lang="eng",builder=builder_list)
    res_txt = tool.image_to_string(pil_image,lang="eng",builder=builder_text)
    
    #取得した文字列を表示
    print(res_txt)
    #　WordBoxBuilderを指定するとリスト型が戻り値
    # print(type(res))
    
    #以下は画像のどの部分を検出し、どう認識したかを分析
    out = cv2.imread(file_name)
    
    for d in res:
        # print(d.content) #どの文字として認識したか
        # print(d.position) #どの位置を検出したか
        # print(d.position[0], d.position[1])
        cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2) #検出した箇所を囲む
        
    #検出結果の画像を表示
    print('quit press key')
    
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img",out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()   

def ocr_tool_pillow(file_name,bitwise=True):
    """
     using Pillow

    Args:
        file_name ([type]): file name str
        bitwise (bool, optional): Black and white inversion . Defaults to True.
    """
    #利用可能なOCRツールを取得
    tools = pyocr.get_available_tools()
 
    if len(tools) == 0:
        print("Do not find OCR tools")
        sys.exit(1)
    
    #利用可能なOCRツールはtesseractしか導入していないため、0番目のツールを利用
    tool = tools[0]
    
   
    pil_image = Image.open(file_name)
    if bitwise:
        npil_image = ImageOps.invert(pil_image.convert('RGB'))

    builder_list = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
    builder_text = pyocr.builders.TextBuilder(tesseract_layout=6)
    res = tool.image_to_string(pil_image,lang="eng",builder=builder_list)
    res_txt = tool.image_to_string(pil_image,lang="eng",builder=builder_text)
    #取得した文字列を表示
    print(res_txt)
    # print(type(res))
    
    #以下は画像のどの部分を検出し、どう認識したかを分析
    out = Image.open(file_name)
    print(out.format, out.size, out.mode)
    draw = ImageDraw.Draw(out)

    for d in res:
        print(d.content) #どの文字として認識したか
        print(d.position) #どの位置を検出したか
        # print(d.position[0], d.position[1])
        draw.rectangle(d.position, outline=(255,0,0) )
    
    #検出結果の画像を表示
    out.show()
    
             
if __name__ == '__main__':
    # file_name ="C:/Users/yagyu/Desktop/Camera Roll/WIN_20210629_08_55_01_Pro.jpg"
    # file_name ="C:/Users/yagyu/Desktop/Camera Roll/WIN_20210629_08_56_53_Pro.jpg"
    # file_name ="C:/Users/yagyu/Desktop/Camera Roll/WIN_20210629_08_57_54_Pro.jpg"
    file_name ="./Laser/WIN_20210527_14_14_04_Pro.png"
 
    # file_name ="./Laser/ocr-test.png"
    
    # ocr_tool_pillow(file_name,bitwise=True)
    ocr_tool_opencv(file_name,bitwise=False)
    

    
