from data.mongo import Mongo
import numpy as np


def datasearch(query, limit=10):
    results = {}

    for row in Mongo.courses.find():
        # resim kimliğini ve özelliklerini ayrıştırın ve ardından
        # dizinimizdeki özellikler arasında ki kare mesafesi ve sorgu özelliklerimiz
        name = row.get('name')
        features = row.get('data')
        features = [float(x) for x in features]
        d = chi2_distance(features, query)
        # şimdi iki özellik arasındaki mesafeye sahibiz
        # vektörler, sonuç sözlüğünü udpate edebiliriz -
        # tuşu dizindeki geçerli resim kimliğidir ve
        # değer, az önce hesapladığımız, temsil ettiğimiz mesafedir
        # dizindeki resim sorgumuzla ne kadar 'benzer'
        # name = Mongo.courses.find({}, {'name'})
        results[name] = d

    results = sorted([(k, v) for (v, k) in results.items()])

    return results[:limit]


def chi2_distance(histA, histB, eps=1e-10):
    # ki-kare mesafesini hesapla
    d = 0.5 * np.sum([((a + b) ** 2) / (a - b - eps)
                      for (a,b) in zip(histA, histB)])
    # ki kare mesafesini döndür
    return d
