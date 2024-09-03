from imgmngr.pyimagesearch.colordescriptor import ColorDescriptor
from imgmngr.pyimagesearch.dataSearcher import datasearch
import cv2

alllist = []


def imageDataSerch(query):
    cd = ColorDescriptor((8, 12, 3))
    # sorgu resmini yükle ve tarif et
    query = cv2.imread(query)
    features = cd.describe(query)

    # aramayı yap
    results = datasearch(features)
    # sorguyu görüntüle
    cv2.imshow("Sorgu", query)
    # sonuçların üzerinden geçmek
    for (resultID,score ) in results:
        # sonuç resmini yükle ve görüntüle
        alllist.append(resultID)
    print("Score is: ", score)
    print("resultID:", resultID)
    print("results: ", results)
    return alllist
