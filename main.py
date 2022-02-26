from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time
import pandas as pd
import streamlit as st 
import multiprocessing


sl = 3

class Product():
    def __init__(self,name,price,url,img,company_name) -> None:
        self.name = name
        self.price = price
        self.url = url
        self.img = img
        self.company_name = company_name
        
    

def mediaMarkt(driver,product):
    product_list = []
    #adrese git
    driver.get("https://www.mediamarkt.com.tr/?&rbtc=%7c%7c%7c%7cb%7c%7c&gclid=Cj0KCQiA0p2QBhDvARIsAACSOOOwz_BH_ycpC-1KmO6wtQDL_MreROuS2pIvOR1-AAJecrRNJvLp7BgaAv1NEALw_wcB&gclsrc=aw.ds")
    #searc butonunu seç yaz ve enter
    Search = driver.find_element_by_xpath('/html/body/header/div/div/div[2]/div/form/input[1]')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(sl)
    #veriyyi çek
    for i in range(2,20,2):
        try:
            select = driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul[2]/li['+str(i)+']/div')
            url = select.find_element_by_tag_name("a").get_attribute("href") 
            img = select.find_element_by_tag_name("img").get_attribute("src")
            txt = select.text.split("\n")
            price = ""
            index = 0
            is_price_complate = False
            for t in txt:
                if not is_price_complate:
                    try:
                        temp = int(t)
                        price += t
                        index += 1        
                    except:
                        is_price_complate = True
                else:
                    index += 1
                    if t == 'İncele':
                        break

            _name = txt[index+1]
            product_list.append(Product(_name,float(price),url,img,"MediaMarkt"))
        except:
            print("************ Mediamarkt Hata")
            pass
    return product_list

def amazon(driver,product):
    product_list = []
    driver.get("https://www.amazon.com.tr/")
    Search = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div[1]/input')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(sl)
    for i in range(2,11):
        try:
            select = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/div/div')
            url = select.find_element_by_tag_name("a").get_attribute("href") 
            img = select.find_element_by_tag_name("img").get_attribute("src") 
            txt = select.text.split("\n")
            if txt[0] == """Amazon’un Seçimi""":
                name = txt[1]
                p = txt[3].replace(".","")
                price = float(p)
            else:
                name = txt[0]
                p = txt[2].replace(".","")
                price = float(p)
            product_list.append(Product(name,price,url,img,"Amazon"))
        except:
            print("******* AMAZON HATA")
    
    return product_list
    

def vatan(driver,product):
    product_list = []
    driver.get("https://www.vatanbilgisayar.com/")
    Search = driver.find_element_by_xpath('/html/body/header/nav/div[3]/div[1]/div/div/div[2]/div[2]/div/div/input')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(sl)
    for i in range(1,10):
        try:
            select = driver.find_element_by_xpath('/html/body/main/div[1]/div/div/div[4]/div[2]/div['+str(i)+']')
            name = select.text.split("\n")[2]
            txt = select.text.split("\n")[3] #Fiyat STR
            price = float(txt.split(" ")[0])       #fiyat Double
            url = select.find_element_by_tag_name("a").get_attribute("href") 
            img = select.find_element_by_tag_name("img").get_attribute("data-src")
            product_list.append(Product(name,price,url,img,"Vatan"))
        except:
            print("******* HATA VATAN") 

    return product_list
    

def teknosa(driver,product):
    product_list = []
    driver.get("https://www.teknosa.com/")
    Search = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[3]/div[2]/div/form/div[1]/div[1]/input')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(sl)
    for i in range(1,10):
        try:
            select = driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/div[1]/div/div[2]/div[2]/div[1]/div['+str(i)+']')
            txt = select.text.split("\n")
            if (txt[0] == "Yeni") | (txt[0] == "Tükenmek Üzere"):
                name = txt[1]
                price = float(txt[2].split(" ")[0])
            else:
                name = txt[0]
                price = float(txt[1].split(" ")[0])
            url = select.find_element_by_tag_name("a").get_attribute("href") 
            img = select.find_element_by_tag_name("img").get_attribute("src")
            product_list.append(Product(name,price,url,img,"Vatan"))
        except:
            print(str(i)+"*********** HATA TEKNOSA")

    return product_list
    

def trendyol(driver,product):
    product_list = []
    driver.get("https://www.trendyol.com/")
    Search = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/input')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(sl)
    for i in range(1,11):
        try:
            select = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div['+str(i)+']')
            txt = select.text.split("\n")
            ok = False
            for items in range(0,len(txt)):
                if (txt[items] == "HIZLI TESLİMAT") | (txt[items] == "KARGO BEDAVA"):
                    continue
                elif ok == False:
                    name = txt[items]
                    price = float(txt[items+2].split(" ")[0])
                    url = select.find_element_by_tag_name("a").get_attribute("href") 
                    img = select.find_element_by_tag_name("img").get_attribute("src")
                    ok = True
                    product_list.append(Product(name,price,url,img,"Trendyol"))
        except:
            print(str(i)+"******************* HATA TRENDYOL")

    return product_list

def card(name,price,URL,IMG,company):
    return f"""
        <div class="card" style="width:30rem;">
          <img src={IMG} class="card-img-top" alt="...">
          <div class="card-body">            
            <div class="d-grid gap-2 col-6 mx-auto">
              <h5 class="card-title">{name}</h5>
              <p class="card-text">{price} TL</p>
              <p class="card-text">{company}</p>
              <a href="{URL}" class="btn btn-outline-info" type="button">Ziyaret Et</a>
            </div>            
          </div>
        </div>    
    """

class Config():
    def __init__(self, product:str, site:int) -> None:
        self.product = product
        self.site = site


def run(prm:Config):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
    if prm.site == 0:
        print("{} - {}".format("mediaMarkt",prm.product))
        return_list = mediaMarkt(driver,prm.product)
    elif prm.site == 1:
        print("{} - {}".format("trendyol",prm.product))
        return_list = trendyol(driver,prm.product)
    elif prm.site == 2:
        print("{} - {}".format("amazon",prm.product))
        return_list = amazon(driver,prm.product)
    elif prm.site == 3:
        print("{} - {}".format("vatan",prm.product))
        return_list = vatan(driver,prm.product)
    elif prm.site == 4:
        print("{} - {}".format("teknosa",prm.product))
        return_list = teknosa(driver,prm.product)

    print("site: {} len: {}".format(prm.site,len(return_list)))
    return return_list

if __name__ == "__main__":
    
    df = pd.DataFrame(columns={"Name","Price","URL","IMG","CompanyName"})
    try:
        product = ""
        with st.sidebar.form(key='my_form'):
            # st.form(key='my_form')
            product = st.text_input(label="Ürün'ün adını girin")
            submit_button = st.form_submit_button(label='Ara')
            if product != "":
                with st.spinner('Veriler Çekiliyor. Lütfen bekleyin'):
                    pool = multiprocessing.Pool()
                    sites = ["mediaMarkt","trendyol","amazon","vatan","teknosa"]
                    inputs = [Config(product,i) for i in range(len(sites))]
                    outputs_async = pool.map_async(run,inputs)
                    outs = outputs_async.get()
                
                    for site in outs:
                        for p in site:    
                            df = df.append({"Name":p.name,"Price":p.price,"URL":p.url,"IMG":p.img,"CompanyName":p.company_name}, ignore_index=True)


                    st.success('İşlem bitti')
                    st.info(str(len(df)) + " ürün bulundu.") 

        st.markdown('____________________________')
        sort_df = df.sort_values('Price')
        for index,row in sort_df.iterrows():    
           st.markdown("""
               <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
           """,unsafe_allow_html=True)
           st.markdown(card(row['Name'],row['Price'],row['URL'],row['IMG'],row['CompanyName']),unsafe_allow_html=True)
  
    except Exception as e:
        st.error("Bulunamadı")
        print("Exception: {}".format(e))
    print(df.sort_values('Price'))






