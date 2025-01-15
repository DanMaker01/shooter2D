
# rota é uma fila
class Rota:
    def __init__(self):
      
        print("iniciou classe rota")
        self.posicao = []
        self.tempo = []
        self.indice = 0
        pass

    def len_rota(self):
        if len(self.posicao) == len(self.tempo):
            return len(self.posicao)
    
    def rota_add(self,pos,tempo):
        self.posicao.append(pos)
        self.tempo.append(tempo)
    
    def rota_avancar_item(self):
        self.indice+=1
        self.indice = self.indice % len(self.posicao)
        pass
    def rota_get_item_atual(self):
        pos = self.posicao[self.indice] #retira o primeiro item colocado
        tempo = self.tempo[self.indice]
        return pos, tempo
        
