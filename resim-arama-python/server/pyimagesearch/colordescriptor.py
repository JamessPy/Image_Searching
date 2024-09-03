# coding=utf-8
# gerekli paketleri içe aktarın
import numpy as np
import cv2
import imutils


class ColorDescriptor:
    def __init__(self, bins):
        # 3B histogram için kutu sayısını saklama
        self.bins = bins

    def describe(self, image):
        # görüntüyü HSV renk uzayına dönüştür ve başlat
        # görüntüyü ölçmek için kullanılan özellikler
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        # boyutları yakalayın ve görüntünün merkezini hesapla
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))
        # görüntüyü dört dikdörtgen / segmente ayırın (sol üst, sağ üst, sağ alt, sol alt)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
                    (0, cX, cY, h)]
        # merkezini temsil eden eliptik bir maske oluştur
        # Resim
        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
        # segmentler üzerinde döngü
        for (startX, endX, startY, endY) in segments:
            # görüntünün her köşesi için bir maske oluştur,
            # ondan eliptik merkez
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)
            # Resimden bir renk histogramı çıkar, ardından
            # özellik vektörü
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
        # eliptik bölgeden bir renk histogramı ayıklayın ve özellik vektörünü güncelleyin
        hist = self.histogram(image, ellipMask)
        features.extend(hist)
        # özellik vektörünü döndürme
        return features

    def histogram(self, image, mask):
        # 3B renk histogramı
        # Kanal başına verilen kutu sayısını kullanarak
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                            [0, 180, 0, 256, 0, 256])
        # OpenCV 2.4 kullanıyor histogramı normalleştir
        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()
        # aksi takdirde OpenCV 3 için tutma yeri
        else:
            hist = cv2.normalize(hist, hist).flatten()
        # histogramı döndür
        return hist
