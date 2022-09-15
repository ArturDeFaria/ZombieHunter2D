import json

class toJason:
    
    def __init__(self):
        self.list_dicts={}
    
    ####cria um obj jason e da dump para cada __dict__ dentro da lista de objetos
    def list_obj(self,lista,titulo):
        j_obj= json.dumps([o.__dict__ for o in lista])
        ####criar um dict vazio
        
        #####criar um indicie e adicionar o obj json a lista de dicts
        self.list_dicts[titulo] = j_obj
        ####criar um obj jason que vai conter as listas strings de objetos
        j_dicts=json.dumps(self.list_dicts)
        return j_dicts

    def add_to_list(self,j_obj,titulo):
        #####criar um indicie e adicionar o obj json a lista de dicts
        self.list_dicts[titulo] = j_obj
        ####criar um obj jason que vai conter as listas strings de objetos
        j_dicts=json.dumps(self.list_dicts)
        return j_dicts
        
    def clear_list(self):
        self.list_dicts.clear()
        
        
    
    def list_obj_not__dict(self,lista,titulo):
        j_obj= json.dumps([o.get_dictio() for o in lista])
        ####criar um dict vazio
        
        #####criar um indicie e adicionar o obj json a lista de dicts
        self.list_dicts[titulo] = j_obj
        ####criar um obj jason que vai conter as listas strings de objetos
        j_dicts=json.dumps(self.list_dicts)
        return j_dicts
    
    ####converter de json para dict para retornar as lista de objeto 
    def dic_list(self,jason_list,listas):#listaStrings['Carros','Navios','Avioes']
        newList=[]
        dicts=json.loads(jason_list)
        for titulos in range(len(listas)):
            ###Converter a string list do json para uma dict lista 
            newList.append(json.loads(dicts[listas[titulos]]))
        return newList
       
"""
###Exemplo de uso
class carro:
    def __init__(self,marca,cor):
            self.marca=marca
            self.cor=cor
carros=[]
car = carro( "ford","preto")
carros.append(car)
car = carro("fiat","vermelho")
carros.append(car)

class navio:
    def __init__(self,modelo,tamanho):
            self.modelo=modelo
            self.tamanho=tamanho
navios=[]
nav = navio("lancha", 3.50)
navios.append(nav)
nav = navio("iate", 6.0)
navios.append(nav)

toJ = toJason()
stringList=toJ.list_obj(carros,"Carros")
stringList=toJ.list_obj(navios,"Navios")
print(stringList)
lista=toJ.dic_list(stringList,('Carros','Navios'))
carros = lista[0]
navios = lista[1]
print(f"Carro: {carros[0]['marca']} na pos[0]")
for each in navios: print(f"Barco de {each['tamanho']}m")
"""