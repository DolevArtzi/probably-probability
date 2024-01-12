from PIL import Image
import os
import ipyplot

class TableDisplay:
    def __init__(self):
        self.m = {}
        s = 'pathto/images'
        suits = ['club','spade','diamond','heart']
        card_names = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']

        for f in os.listdir(s):
            name = f[:-4].split('_') #remove .png
            num, suit = name[0], name[-1]
            self.m[(num,suit)] = Image.open(f'{s}/{f}')

    def get(self,n,s):
        return self.m[(f'{n}'.lower(),s)]
    
    def split_display(self,l):
        ll = []
        for s in l:
            name = s.split()
            num,suit = name[0], name[-1]
            ll.append(self.get(num,suit))
        self.display(ll)

    def display(self,l):
        _ = ipyplot.plot_images(l, max_images=20, img_width=150)
