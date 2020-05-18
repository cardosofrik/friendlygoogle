import csv
import sys
from requests import get as init
from requests import exceptions
# - < https://zenserp.com/ >

# friendlygoogle


class FriendlyGoogle(object):

    def __init__(self,procurar):
        self.procurar = procurar
        self.connecting(procurar)

    def arquivoLer(self, arq):
        print(f"[ read ] - lendo conteudo =:> {arq}")
        try:
            return open(arq)
        except FileNotFoundError:
            print(f"[ create ] - ponto de referencia criado.")
            open("apikey.txt",'a')

    def escreverarquivo(self, arq):
        print("[ write ] - escrevendo...")
        return open(f"{arq}.csv", "a", encoding='UTF-8')


    def connecting(self, consulta):
        contagem =1
        _pesquisas = list()
        headers = {}
        param = dict()

        for apikey in self.arquivoLer("apikey.txt"):
        
            print(f'[ key  ] - {apikey}')
            print("[ ...  ] - %s"%consulta)
        
            headers['apikey'] = apikey.strip()
            param['q'] = consulta
            param['num']="100"
            param["start"]=1
            param['search_engine'] = 'google.com'
        
            try:
                html = init('https://app.zenserp.com/api/v2/search', headers=headers ,params=param).json()
                resp = ''.join(( [i for i in html.keys()]))
                if resp == 'error':
                    print('<?> -Not enough requests.\n<!> - Verifique status da api.')
                elif resp[:5] == 'query':
                    for resultado in html['organic']:
        
                        try:
                            urls= resultado['url']
                            print(f"< {contagem} > {urls}")
                            _pesquisas = _pesquisas + [urls]
                            contagem+=1
        
                        except:
                            continue
                            
            except exceptions.ConnectionError:
                print("[:> net <:] - sem rede")
                break
            except KeyError:
                continue
                
        if len(_pesquisas) != 0:
            print(f"<> total <> - {len(_pesquisas)}")
            for _results in list(set(_pesquisas)):
                salvar = self.escreverarquivo("saida_resultado")
                writer = csv.writer(salvar, delimiter=",", lineterminator="\n")
                writer.writerow([_results])


if __name__ == '__main__':
    try:
        if str(sys.version)[:3] == '3.8':


            FriendlyGoogle("gnu/linux")


        else:
            print("version 3.8++")
    except TypeError:
        pass

