# coding=utf-8
# gerekli paketleri içe aktarın
from pyimagesearch.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2


# bağımsız değişken ayrıştırıcısını oluşturma ve bağımsız değişkenleri ayrıştırma
class deneme:

    def test(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dataset", required=True,
                        help="Dizine eklenecek resimleri içeren dizinin yolu")
        ap.add_argument("-i", "--index", required=True,
                        help="Hesaplanan dizinin saklanacağı yol")
        args = vars(ap.parse_args())
        # renk tanımlayıcıyı başlat
        cd = ColorDescriptor((8, 12, 3))
        # çıktı dizini dosyasını yazmak için aç
        output = open(args["index"], "w")
        # görüntü yollarını kapmak ve üzerinde döngü yapmak için glob kullan
        for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
            # resim kimliğini (yani benzersiz dosya adı) resimden çıkar
            # yol ve görüntünün kendisini yükleme
            imageID = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            # resmi tanımla

            features = cd.describe(image)
            # özellikleri dosyaya yaz
            features = [str(f) for f in features]
            output.write("%s,%s\n" % (imageID, ",".join(features)))
        # dizin dosyasını kapat
        output.close()
