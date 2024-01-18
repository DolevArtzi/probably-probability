from PIL import Image
import os
import ipyplot

class TableDisplay:
    def __init__(self):
        self.m = {}
        s = './images'

        for f in os.listdir(s):
            name = f[:-4].split('_') #remove .png
            num, suit = name[0], name[-1]
            self.m[(num,suit)] = Image.open(f'{s}/{f}')

    def get(self,n,s):
        return self.m[(f'{n}'.lower(),s)]
    
    """
    Takes a string of the form "(Queen of clubs, 10 of diamonds)" and displays the hand
    """
    def displayHand(self,handString,w=90):
        h = handString
        h = list(h)
        h = h[1:]
        h = h[:-1]
        l = ''.join(h).split(',')
        self.split_display(l,w=w)
        
    def split_display(self,l,w=150):
        ll = self._split(l)
        self.display(ll,w=w)

    def _split(self,l):
        ll = []
        for s in l:
            name = s.split()
            num,suit = name[0], name[-1]
            ll.append(self.get(num,suit))
        return ll

    def display_all_hands(self,hands):
        hands = [self._split(h) for h in hands]
        flat_hands = []
        labels = []
        for i in range(len(hands)):
            for x in hands[i]:
                flat_hands.append(x)
                labels.append(i)
        _ = ipyplot.plot_class_tabs(flat_hands,labels=labels,img_width=75)

    def display(self,l,w=150):
        _ = ipyplot.plot_images(l, max_images=20, img_width=w,show_url=False)
