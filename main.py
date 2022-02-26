from time import time
from unicodedata import name
from numpy import product
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from soupsieve import select
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import Select
import pandas as pd
import streamlit as st 
# import sqllite3 as sql

# options.set_headless()

df = pd.DataFrame(columns={"Name","Price","URL","IMG","CompanyName"})

def mediaMarkt(driver,product):
    #adrese git
    driver.get("https://www.mediamarkt.com.tr/?&rbtc=%7c%7c%7c%7cb%7c%7c&gclid=Cj0KCQiA0p2QBhDvARIsAACSOOOwz_BH_ycpC-1KmO6wtQDL_MreROuS2pIvOR1-AAJecrRNJvLp7BgaAv1NEALw_wcB&gclsrc=aw.ds")
    #searc butonunu seç yaz ve enter
    Search = driver.find_element_by_xpath('/html/body/header/div/div/div[2]/div/form/input[1]')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(2)
    #veriyyi çek
    for i in range(2,20,2):
        time.sleep(1)
        select = driver.find_element_by_xpath('//*[@id="category"]/ul[2]/li['+str(i)+']/div')
                                        #    //*[@id="category"]/ul[2]/li[4]/div
                                        #    //*[@id="category"]/ul[2]/li[6]/div
        time.sleep(2)
        url = select.find_element_by_tag_name("a").get_attribute("href") 
        img = select.find_element_by_tag_name("img").get_attribute("src") 
        print(img)
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
        compare(_name,float(price),url,img,"MediaMarkt")
    

def amazon(driver,product):
    driver.get("https://www.amazon.com.tr/")
    Search = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(1)
    for i in range(2,11):
        try:
            time.sleep(1)
            select = driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/div/div')
            time.sleep(1)
            url = select.find_element_by_tag_name("a").get_attribute("href") 
            img = select.find_element_by_tag_name("img").get_attribute("src") 
            txt = select.text.split("\n")
            time.sleep(1)
            if txt[0] == """Amazon’un Seçimi""":
                name = txt[1]
                p = txt[3].replace(".","")
                price = float(p)
            else:
                name = txt[0]
                p = txt[2].replace(".","")
                price = float(p)
            time.sleep(1)
            compare(name,price,url,img,"Amazon")
            time.sleep(1)
        except:
            print("******* AMAZON HATA")
    

def vatan(driver,product):
    driver.get("https://www.vatanbilgisayar.com/")
    Search = driver.find_element_by_xpath('//*[@id="navbar-search-input"]')
    Search.send_keys(product,Keys.ENTER)
    for i in range(1,10):
        try:
            time.sleep(1)
            select = driver.find_element_by_xpath('//*[@id="product-list-container"]/div/div/div[4]/div[2]/div['+str(i)+']')
            name = select.text.split("\n")[2]
            txt = select.text.split("\n")[3] #Fiyat STR
            price = float(txt.split(" ")[0])       #fiyat Double
            url = select.find_element_by_tag_name("a").get_attribute("href") 
            img = select.find_element_by_tag_name("img").get_attribute("data-src")
            compare(name,price,url,img,"Vatan")
        except:
            print("******* HATA VATAN") 
    

def teknosa(driver,product):
    driver.get("https://www.teknosa.com/")
    Search = driver.find_element_by_xpath('//*[@id="search-input"]')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(3)
    for i in range(1,10):
        time.sleep(1)
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
            # print(name)
            # print(price)
            # print(url)
            # print(img)
            # print("**************")
            compare(name,price,url,img,"TeknoSA")
        except:
            print(str(i)+"*********** HATA TEKNOSA")
    

def trendyol(driver,product):
    driver.get("https://www.trendyol.com/")
    Search = driver.find_element_by_xpath('//*[@id="auto-complete-app"]/div/div/input')
    Search.send_keys(product,Keys.ENTER)
    time.sleep(1)
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
                    compare(name,price,url,img,"Trendyol")
        except:
            print(str(i)+"******************* HATA TRENDYOL")
    
    



def compare(name,price,url,img,companyName):
    global df
    df = df.append({"Name":name,"Price":price,"URL":url,"IMG":img,"CompanyName":companyName}, ignore_index=True)

def streamlitSearch():
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter your name')
        submit_button = st.form_submit_button(label='Submit')
    return text_input

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


if __name__ == "__main__":
    
    try:
        product = ""
        with st.sidebar.form(key='my_form'):
            # st.form(key='my_form')
            product = st.text_input(label="Ürün'ün adını girin")
            submit_button = st.form_submit_button(label='Ara')
            if product != "":
                with st.spinner('Veriler Çekiliyor. Lütfen bekleyin'):
                    options = webdriver.FirefoxOptions()
                    options.add_argument('--headless')
                    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)            
                    mediaMarkt(driver,product)
                    # trendyol(driver,product)
                    # amazon(driver,product)
                    # vatan(driver,product)
                    # teknosa(driver,product)
                    st.success('İşlem bitti')
                    st.info(str(len(df)) + " ürün bulundu.") 

        st.markdown('____________________________')
        sort_df = df.sort_values('Price')
        for index,row in sort_df.iterrows():
            st.markdown("""
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
            """,unsafe_allow_html=True)
            st.markdown(card(row['Name'],row['Price'],row['URL'],row['IMG'],row['CompanyName']),unsafe_allow_html=True)
    except:
        st.error("Bulunamadı")
    # print("*****************************************")
    # print(df.sort_values('Price'))
    





