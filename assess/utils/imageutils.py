def prepare_image(img1, img2):
    '''统一为彩色或灰度图像，并统一图片大小'''
    isgrayscale = img1.mode == 'L' or img2.mode == 'L'
    if isgrayscale:
        img1 = img1.convert('L')
        img2 = img2.convert('L')
    newsize = (min(img1.size[0], img2.size[0]), min(img1.size[1], img2.size[1]))
    img1 = img1.resize(newsize)
    img2 = img2.resize(newsize)
    return img1, img2, isgrayscale
