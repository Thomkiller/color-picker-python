from tkinter import GROOVE, Tk
from tkinter import ttk, N, S, E, W
from turtle import width
from PIL import Image, ImageTk, ImageDraw

class SlidingIntValue(ttk.Frame):
    
    def __init__(self, parent, title, range=(0,100), init_value=None, text_width=10):
        super().__init__(parent)
        
        # valider les entrées !?!
        
        if init_value is None:
            self.__value = round(sum(range) / 2)
        else: 
            # if init_value < range[0]:
            #     init_value = range[0]
            # elif init_value > range[1]:
            #     init_value = range[1]
            self.__value = max(range[0], min(init_value, range[1]))
            
        self.__title_widget = ttk.Label(self, text=title, width=text_width)
        self.__scale_widget = ttk.Scale(self, from_=range[0], to=range[1], value=self.__value)
        self.__value_widget = ttk.Label(self, text=str(self.__value), width=text_width, anchor='center')
        
        self.__title_widget.grid(column=0, row=0)
        self.__scale_widget.grid(column=1, row=0, sticky=(E, W))
        self.__value_widget.grid(column=2, row=0)
        
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)
        
        self.__scale_widget['command'] = self._update_value
        
    def _update_value(self, value):
        self.__value = round(float(value))
        self.__value_widget['text'] = str(self.__value)
        self.event_generate('<<ValueChange>>')
        
    @property
    def title(self):
        return self.__title_widget['text']
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, val):
        self.__value = max(self.__scale_widget['from'], min(val, self.__scale_widget['to']))
        

class SlidingIntValueImage(SlidingIntValue):
        
    def __init__(self, parent, title, range=(0,100), init_value=None, text_width=10, image_size=(50,20)):
        super().__init__(parent, title, range, init_value, text_width)

        #validation des intrants !?!
        
        self._image_size = image_size
        self.__image_widget = ttk.Label(self, width=text_width, relief=GROOVE)
        self.__image_widget.grid(column=3, row=0)
        self.columnconfigure(3, weight=0)
        
        self.__photo_image = None
        self.__update_image()
    
    def _update_value(self, value):
        super()._update_value(value)
        self.__update_image()
        
    def __update_image(self):
        image = Image.new(mode='RGB', size=(self._image_size[0], self._image_size[1]), color=(0,0,0))
        image_draw = ImageDraw.Draw(image)
        # dessiner
        self._draw(image_draw)
        #
        self.__photo_image = ImageTk.PhotoImage(image)
        self.__image_widget['image'] = self.__photo_image
    
    def _draw(self, image_draw):
        pass

class SlidingIntValueSolidColor(SlidingIntValueImage):
    
    def __init__(self, parent, title, range=(0,100), init_value=None, text_width=10, image_size=(50,20)):
        super().__init__(parent, title, range, init_value, text_width, image_size)
    
    def _color(self):
        return (self.value, self.value, self.value)
        
    def _draw(self, image_draw):
        image_draw.rectangle([0, 0, self._image_size[0] - 1, self._image_size[1] - 1], fill=self._color(), width=0)


class SlidingRed(SlidingIntValueSolidColor):
    
    def __init__(self, parent, red=128, text_width=10, image_size=(50,20)):
        super().__init__(parent, 'Red', (0, 255), red, text_width, image_size)
    
    def _color(self):
        return (self.value, 0, 0)


class SlidingGreen(SlidingIntValueSolidColor):
    
    def __init__(self, parent, green=128, text_width=10, image_size=(50,20)):
        super().__init__(parent, 'Green', (0, 255), green, text_width, image_size)
    
    def _color(self):
        return (0, self.value, 0)
    
class SlidingBlue(SlidingIntValueSolidColor):
    
    def __init__(self, parent, blue=128, text_width=10, image_size=(50,20)):
        super().__init__(parent, 'Blue', (0, 255), blue, text_width, image_size)
    
    def _color(self):
        return (0, 0, self.value)

class Application(Tk):
    def __init__(self):
        super().__init__()
        
        self.title('RGB Color Shift')
        
        test = SlidingGreen(self)
        test.grid(sticky=(N, S, E, W))
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        

def main():  
    app = Application()
    app.mainloop()
    

if __name__ == '__main__':
    main()