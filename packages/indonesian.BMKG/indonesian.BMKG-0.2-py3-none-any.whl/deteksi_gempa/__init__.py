import none as none
import requests as requests
from bs4 import BeautifulSoup

description = "to get latest information of earthquake in indonesian from BMKG.go.id "

def ekstraksi_data():


    try:
        r = requests.get('https://www.bmkg.go.id/')
    except  Exception:
        return None
    if r.status_code == 200 :
        # print(r.text)
        # print(r.status_code)

        soup = BeautifulSoup(r.text,'html.parser')

        result = soup.findChild('ul', {'class':'list-unstyled'})
        result = result.findChildren('li')
        print(f'============ list pencaian : ==============\n')
        j = 0
        mag = None
        dalam = None
        koordinat = None
        lokasi = None
        ket = None

        for i in result:
            # print(j,i)
            if j == 1:
                mag = i.text
            elif j == 2:
                dalam = i.text
            elif j ==3:
                koordinat = i.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif j == 4:
                lokasi = i.text
            elif j ==5:
                ket = i.text


            j = j +1

        title = soup.find('title')
        tanggal = soup.find('span',{'class': 'waktu'})
        waktu = tanggal.text.split(', ')[1]
        # mag = soup.find('ul',{'class': 'list-unstyled'})
        print(title.string)
        print("\n===========================================\n")



        hasil = dict()
        hasil['tanggal'] = tanggal.text
        hasil['waktu'] = waktu
        hasil['mag'] = mag
        hasil['kedalaman'] = dalam
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = ket

        return hasil
        print("=================================")
    else:
        return None


def tampilkan_data(result):
    if result is None :
        print("tidak bisa menemukan data apapun")
        return

    print("gempa berdasarkan bmkg")
    print(f'tanggal \t : {result["tanggal"]}')
    print(f'waktu \t\t : {result["waktu"]}')
    print(f'magnitudo \t : {result["mag"]}')
    print(f'kedalaman \t : {result["kedalaman"]}')
    print(f'koordinat \t : LS : {result["koordinat"]["ls"]}, BT: {result["koordinat"]["bt"]}')
    print(f'lokasi \t\t : {result["lokasi"]}')
    print(f'ket \t\t : {result["dirasakan"]}')

if __name__ == '__main__':
    print(f"\ndeskripsi : {description}\n")
    print("aplikasi utama")
    result = ekstraksi_data()
    tampilkan_data(result)
