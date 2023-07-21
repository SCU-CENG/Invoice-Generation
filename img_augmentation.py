import imgaug.augmenters as iaa
import numpy as np
import cv2
import os
import random
import time
import imgaug.augmenters as iaa

from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from constants import OUT_DIRECTORY, SAVE_IMG_BOX_PATH, SAVE_IMG_BOX


def do_img_aug_v6(image, bbs):
    seq = iaa.Sequential([

        # Grup-1: Blur - bozma
        iaa.Sometimes(
            0.5,
            iaa.OneOf([
                iaa.GaussianBlur(sigma=(0, 1)),  # blur
                iaa.JpegCompression(compression=(0, 90)),  # blur
                iaa.AverageBlur(k=(0, 3)),  # blur
                iaa.AverageBlur(k=((0, 4), (0, 4))),  # blur
                iaa.MotionBlur(k=6),  # blur
                iaa.imgcorruptlike.Pixelate(severity=1),  # blur like
                iaa.ElasticTransformation(alpha=(0.1, 1.4), sigma=(0, 0.9))  # dönüşüm - tırtıklı yapma
            ]),
        ),

        # Grup-2: Noktasal hatalar
        iaa.Sometimes(0.2,
                      iaa.OneOf([
                          iaa.Dropout(p=(0, 0.013)),  # point noise
                          iaa.CoarseDropout(p=(0.0, 0.009), size_percent=(0.7, 1)),  # point noise
                          iaa.ImpulseNoise(p=(0.0, 0.015)),  # point noise
                          iaa.SaltAndPepper((0.0, 0.015)),  # point noise
                          iaa.CoarseSaltAndPepper(p=(0.015, 0.015), size_percent=(0.7, 1)),  # point noise
                          iaa.Salt((0, 0.045)),  # point noise
                          iaa.Pepper((0.0, 0.011)),  # point noise
                      ])
                      ),

        # Grup-3: piksel değiştirme
        iaa.Sometimes(0.3,
                      iaa.OneOf([
                          iaa.Add((-40, 40)),  # piksel + -
                          iaa.MultiplyElementwise((0.8, 1.2)),  # piksel + -
                          iaa.Multiply((0.75, 1.25)),  # piksel + -
                          iaa.AddElementwise((-20, 20)),  # piksel + -
                          iaa.WithBrightnessChannels(iaa.Add((-40, 45))),  # piksel + -
                          iaa.MultiplyBrightness((0.8, 1.3)),  # piksel + -
                          iaa.AddToBrightness((-30, 30)),  # piksel + -
                          iaa.AddToBrightness((-40, 50)),  # piksel + -
                      ])
                      ),

        # Grup-4: Contrast değiştirme
        iaa.Sometimes(0.3,
                      iaa.OneOf([
                          iaa.GammaContrast(gamma=(0.3, 2.7)),  # enhancement
                          iaa.SigmoidContrast(gain=(4, 15), cutoff=(0.4, 0.6)),  # enhancement
                          iaa.LogContrast(gain=(0.8, 1.3)),  # enhancement
                          iaa.LinearContrast((0.6, 1.5)),  # enhancement
                          iaa.BlendAlpha((0.0, 0.5), iaa.AllChannelsHistogramEqualization()),  # enhancement
                          iaa.Sharpen(alpha=(0, 1), lightness=(0.75, 3.5)),  # enhancement
                          iaa.Emboss(alpha=(0, 1), strength=(0.5, 1.5))  # enhancement
                      ])
                      ),

        # Grup-5: Crop işlemi
        iaa.Sometimes(0.15,
                      iaa.Crop(px=(0, 15)),  # crop
                      ),

        # Grup-6: Cortoon işlemi
        iaa.Sometimes(0.1,
                      iaa.Cartoon(blur_ksize=(0.5, 1.5), segmentation_size=1, saturation=(1.5, 2),
                                  edge_prevalence=(0.9, 0.912))
                      )
    ], random_order=True)

    img, bbs1 = seq(images=image, bounding_boxes=bbs)

    return img, bbs1


def do_img_aug_v7(image, bbs):
    seq = iaa.Sequential([

        # Grup-7: Dönüşümler - Scale, Translate
        iaa.Sometimes(0.2,
                      iaa.OneOf([
                          iaa.Affine(scale=(0.75, 1.05), cval=np.median(image)),  # dönüşüm
                          iaa.Affine(scale={"x": (0.75, 1.05), "y": (0.75, 1.05)}, cval=np.median(image)),  # dönüşüm
                          iaa.ScaleX((0.75, 1.05), cval=np.median(image)),  # dönüşüm
                          iaa.ScaleY((0.75, 1.05), cval=np.median(image)),  # dönüşüm
                          iaa.Affine(translate_percent={"x": (-0.03, 0.03), "y": (0.03, 0.03)}, cval=np.median(image)),
                          # dönü
                          iaa.Affine(translate_px={"x": (-50, 50), "y": (-50, 50)}, cval=np.median(image)),  # dönüşüm
                          iaa.ShearX((-2, 2), cval=np.median(image)),  # dönüşüm - x ekseninde genişletme (döndürme)
                          iaa.ShearY((-2, 2), cval=np.median(image)),  # dönüşüm - y ekseninde genişletme (döndürme)
                      ])
                      ),
    ])

    img, bbs1 = seq(images=image, bounding_boxes=bbs)

    return img, bbs1


def do_img_aug_v8(image, bbs):
    seq = iaa.Sequential([

        # Grup-8: Dönüşümler - 2

        iaa.Sometimes(0.13,
                      then_list=iaa.OneOf([
                          iaa.Rotate((-3, 3), cval=np.median(image)),  # dönüşüm
                          # dönüşüm - yamultma
                          iaa.PiecewiseAffine(scale=(0.0, 0.02), nb_rows=2, nb_cols=2, cval=np.median(image)),
                          # dönüşüm - kamera açısıyla oynama gibi
                          iaa.PerspectiveTransform(scale=(0.0, 0.015), fit_output=True, cval=np.median(image))
                      ])
                      ),

        iaa.Sometimes(0.2,
                      iaa.Rotate((-1, 1), cval=np.median(image)),  # dönüşüm
                      ),

    ], random_order=True)

    img, bbs1 = seq(images=image, bounding_boxes=bbs)

    return img, bbs1


def dikey_line_func(image, random_state, parents, hooks):
    mean = np.mean(image) * 0.8

    [_, height, weight, _] = image.shape

    rnd_count = random.randint(0, 9)
    rnd_list = random.sample(range(0, height), rnd_count)
    rnd_list2 = random.sample(range(0, weight), rnd_count)
    rnd_list3 = random.sample(range(0, weight), rnd_count)

    rnd_list2.sort()
    rnd_list3.sort()

    for i, j, k in zip(rnd_list, rnd_list2, rnd_list3):
        rnd_px = random.randint(int(255 - mean), int(mean))
        image[0][min(i, j):max(i, j), i:i + 1, :] = rnd_px
    return image


def do_img_aug_v3(image, bbs):
    seq = iaa.Sequential([
        iaa.Add((80, 120)),

    ])

    # aug = iaa.Lambda(line_func, keypoint_func)

    img, bbs1 = seq(images=image, bounding_boxes=bbs)

    return img, bbs1


def do_img_aug_v4(image, bbs):
    seq = iaa.Sequential([
        iaa.Affine(scale=(0.48, 0.6), cval=np.median(image)),
        iaa.Affine(translate_percent={"x": (-0.23, -0.15), "y": (-0.23, -0.15)}, cval=np.median(image)),
        iaa.Sometimes(0.5,
                      then_list=iaa.OneOf([
                          iaa.GaussianBlur(sigma=(0, 1)),  # blur
                          iaa.JpegCompression(compression=(0, 60)),  # blur
                          iaa.AverageBlur(k=(0, 2)),  # blur
                          iaa.AverageBlur(k=((0, 3), (0, 3))),  # blur
                          iaa.MotionBlur(k=4),  # blur
                      ]),
                      ),
        iaa.Sometimes(0.2,
                      then_list=iaa.OneOf([
                          iaa.Add((-20, 20)),
                          iaa.Sharpen(alpha=(0, 1), lightness=(0.8, 3)),  # enhancement
                          iaa.Emboss(alpha=(0, 1), strength=(0.6, 1.4))  # enhancement
                      ])
                      ),

        iaa.Sometimes(0.1,
                      iaa.Rotate((-1.3, 1.3), cval=np.median(image)),  # dönüşüm
                      )
    ])

    img, bbs1 = seq(images=image, bounding_boxes=bbs)

    return img, bbs1


def do_img_aug_v5(image, bbs):
    seq = iaa.Sequential([

        iaa.Add((80, 120)),

        iaa.Sometimes(0.5,
                      then_list=iaa.OneOf([
                          iaa.GaussianBlur(sigma=(0, 1)),  # blur
                          iaa.JpegCompression(compression=(0, 60)),  # blur
                          iaa.AverageBlur(k=(0, 2)),  # blur
                          iaa.AverageBlur(k=((0, 3), (0, 3))),  # blur
                          iaa.MotionBlur(k=4),  # blur
                      ]),
                      ),
        iaa.Sometimes(0.2,
                      then_list=iaa.OneOf([
                          iaa.Sharpen(alpha=(0, 1), lightness=(0.8, 3)),  # enhancement
                          iaa.Emboss(alpha=(0, 1), strength=(0.6, 1.4))  # enhancement
                      ])
                      ),

        iaa.Sometimes(0.1,
                      iaa.Rotate((-1.3, 1.3), cval=np.median(image)),  # dönüşüm
                      )
    ])

    img, bbs1 = seq(images=image, bounding_boxes=bbs)

    return img, bbs1


def img_oug(pil_image, item_list, file_name):
    start = time.time()
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_GRAY2BGR)

    bbs = []
    labels = []

    for item in item_list:
        bbs.append(BoundingBox(x1=int(item.x1), y1=int(item.y1), x2=int(item.x2), y2=int(item.y2)))
        labels.append(item.item_name)

    bbs_oi = BoundingBoxesOnImage(bbs, shape=image.shape)

    img_list = [image]
    img = np.array(img_list)

    img1, bbs_oi1 = do_img_aug_v6(img, bbs_oi)
    img2, bbs_oi2 = do_img_aug_v7(img1, bbs_oi1)
    img3, bbs_oi3 = do_img_aug_v8(img2, bbs_oi2)

    """img3, bbs_oi3 = do_img_aug_v3(img, bbs_oi)
    img3_box = img3[0].copy()"""

    """img3, bbs_oi3 = do_img_aug_v5(img, bbs_oi)
    img3_box = img3[0].copy()"""

    ln = ''
    for i, b in enumerate(bbs_oi3):
        ln += labels[i] + ' ' + str(b.x1_int) + ' ' + str(b.y1_int) + ' ' + str(b.x2_int) + ' ' + str(
            b.y2_int) + '\n'

    if SAVE_IMG_BOX:
        os.makedirs(SAVE_IMG_BOX_PATH, exist_ok=True)
        img3_box = img3[0].copy()
        for b in bbs_oi3:
            # cv2.rectangle(img[0], (c.x1_int, c.y1_int), (c.x2_int, c.y2_int), (0, 0, 255), 2)
            cv2.rectangle(img3_box, (b.x1_int, b.y1_int), (b.x2_int, b.y2_int), (0, 0, 255), 2)

        # cv2.imwrite(save_img_box_path + '1_' + file, img[0])
        cv2.imwrite(SAVE_IMG_BOX_PATH + file_name + '.jpg', img3_box)

    t = time.time() - start

    # if t < 10:
    cv2.imwrite(OUT_DIRECTORY + file_name + '.jpg', img3[0])
    txt_file = open(OUT_DIRECTORY + file_name + '.txt', 'w')
    txt_file.write(ln)
    txt_file.close()
    """else:
        cv2.imwrite(save_path1 + file, img3[0])
        txt_file = open(save_path1 + name + '.txt', 'w')
        txt_file.write(ln)
        txt_file.close()"""

    print('Image Augmentation complated.  -->  ', f"{t:.3f}", 'sn')
