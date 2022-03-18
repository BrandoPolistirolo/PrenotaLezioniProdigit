from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



####FILE READ

with open('Dati.txt') as f:
    lines = f.readlines()
    matricola = lines[0].split(':')[1].strip()
    password = lines[1].split(':')[1].strip()
    prenotazioni = lines[2:]
print(matricola)
print(password)


#####

#### WEB DRIVER

driver = webdriver.Chrome()
driver.get("https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/home")
driver.implicitly_wait(30)


#accetta cookie
driver.find_element_by_link_text('Accetto').click()

elem = driver.find_element_by_name("Username")
elem2 = driver.find_element_by_name("Password")

elem.clear()
elem2.clear()



elem.send_keys(matricola)
elem2.send_keys(password)

driver.find_element_by_xpath("//input[@type ='submit']").click()
# FINE LOGIN
driver.implicitly_wait(30)

for line in prenotazioni:
    edificio = line.split(':')[0]
    aula = line.split(':')[1]
    giorno = line.split(':')[2]
    ora_iniz = line.split(':')[3]
    ora_fine = line.split(':')[4].strip()
    
    driver.find_element_by_link_text('Prenota il posto in aula').click()

    select_element = driver.find_element(By.ID,'codiceedificio')
    select_object = Select(select_element)
    select_object.select_by_visible_text(edificio)

    select_element = driver.find_element_by_name('aula')
    select_object = Select(select_element)
    select_object.select_by_visible_text(aula)
    
    
    
    table = driver.find_elements_by_xpath ("//table[@class= 'table-striped'][4]/tbody/tr/td[1]")
    giorni = []
    k=1
    for i in table:
        if i.text=='':
            continue
        giorni.append([i.text,k])
        k+=1
    
    #controlla prenotazioni gia fatte
    table = driver.find_elements_by_xpath ("//table[@class= 'table-striped'][4]/tbody/tr/td[5]")
    k=-1
    for j in table:
        if k==-1:
            k+=1
            continue
            
        if j.text != '':
            giorni[k].append('si')
        else:
            giorni[k].append('no')
        k+=1
        
    #print(giorni)
    
    
    for k in giorni:
        if k[0]==giorno and k[2]=='no':
            
            select_element = driver.find_element_by_name('dalleore'+str(k[1]))
            select_object = Select(select_element)
            select_object.select_by_visible_text(ora_iniz+':00')
            select_element = driver.find_element_by_name('alleore'+str(k[1]))
            select_object = Select(select_element)
            select_object.select_by_visible_text(ora_fine+':00')
            
    driver.find_element_by_name('dichiarazione').click()
    driver.find_element_by_id('btnprenota').click()
    driver.implicitly_wait(30)
    driver.find_element_by_xpath("//a[@title='Home Page']").click()
