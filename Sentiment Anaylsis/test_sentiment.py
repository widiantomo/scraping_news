# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:33:44 2024

@author: L
"""
#pip install googletrans==3.1.0a0

import requests
from textblob import TextBlob
from googletrans import Translator

translator = Translator()
textx = """PT Medco Energi Internasional Tbk (MEDC) mengumumkan kinerja keuangan dan operasional selama sembilan bulan tahun ini. Beberapa poin penting di antaranya meliputi laba bersih MEDC yang naik sebesar 12,75% dari US$ 242 juta, menjadi US$ 273 juta atau setara Rp 4,28 triliun dan pembayaran dividen interim sebesar Rp 15,75/saham pada (1/11/2024) dari total dividen yang disebar tahun ini sebesar US$ 70 juta atau ekuivalen Rp 1 triliun.
Direktur Utama Medco Energi Hilmi Panigoro mengaku bersyukur dengan hasil operasional dan keuangan perseroan. “Upaya berkelanjutan MedcoEnergi untuk mendukung masa depan energi yang berkelanjutan, dikombinasikan dengan dedikasi kami untuk mematuhi praktik terbaik ESG internasional, telah mendapatkan pengakuan positif dari para investor dan lembaga pemeringkat,” ujar Hilmi dalam keterangan resminya dikutip, Jumat (1/11/2024).
Untuk AMMN sendiri, Manajemen MedcoEnergi menyebut, anak usahanya itu telah memproduksi tembaga sebanyak 335 Mlbs sampai kuartal III-2024, atau 68% lebih tinggi ketimbang tahun lalu dengan harga tembaga saat ini sebesar US$ 4,2/lbs. Bukan hanya produksi tembaga yang naik, produksi emas AMMN bahkan melonjak sebesar 173% menjadi 708 Koz dibanding tahun lalu.
Kemudian, utang bersih MEDC terhadap Ebitda sebesar 1,7x, serta kas dan setara kas mencapai US$ 672 juta. Adapun, dari sisi produksi minyak dan gas (migas) MEDC sudah berada di atas panduan sebesar 153 mboepd dengan harga minyak rata-rata terealisasi sebesar US$ 80/bbl.
MEDC juga melaporkan keberhasilannya melunasi utang restricted group sebesar US$ 2,8 miliar dengan US$ 107 juta dalam sembilan bulan tahun ini, di mana sebagian diimbangi dengan revaluasi mata uang sebesar US$ 42 juta. Tak kalah penting, Manajemen MEDC juga menyatakan, lembaga pemeringkat kredit, Moody's, telah merevisi outlook menjadi B1 positif mengikuti peningkatan serupa dari S&P dan Fitch Credit Ratings menjadi BB-."""
#blob_object = TextBlob(text) #inisialisasi textblob
#text_indo = blob_object.translate(from_lang='id', to='en')

text_indob = translator.translate(textx, dest='en',src='id')
text_indo = text_indob.text 
textindo = TextBlob(text_indo)
analysis = textindo.sentiment
if analysis.polarity > 0:
   polarity = 'Positive'
elif analysis.polarity < 0:
   polarity = 'Negative'
else:
   polarity = 'Netral'
print( polarity)