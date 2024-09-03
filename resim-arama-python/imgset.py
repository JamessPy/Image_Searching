from imgmngr.pyimagesearch.colordescriptor import ColorDescriptor
import glob
import cv2
from data.mongo import Mongo


class ImgSet:
    dataset = ""
    def add(self, statement):
        # Mongodb yeni veri ekleme
        result = Mongo.db.courses.insert_one(statement)
        return result

    def __init__(self, dataset):
        self.dataset = dataset
        #self.index = index

    def Run(self):
        cd = ColorDescriptor((8, 12, 3))
        #output = open(self.index, "w
        # output = open(self.datasetW, "w")
        # görüntü yollarını kapmak ve üzerinde döngü yapmak için glob kullan
        for imagePath in glob.glob(self.dataset + "/*.jpg"):
            # resim kimliğini (yani benzersiz dosya adı) resimden çıkar
            # yol ve görüntünün kendisini yükleme
            imageID = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            feature = cd.describe(image)
            # özellikleri dosyaya yaz

            features = [str(f) for f in feature]
            #output.write("%s,%s\n" % (imageID, ",".join(features)))

            # add metoduna csvde ki verilere gonderme
            if Mongo.db.courses.count({ 'name': imageID }, limit = 1) == 0:
                self.add({
                    "name": imageID,
                    "data": features
                })

        #output.close()

    # db.courses.createIndex({
    #     "about": 'text'
    # })
