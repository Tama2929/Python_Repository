# グラフィック描画
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class Calculator(BoxLayout):
    # 数字入力関数
    def numbers(self, number):
        # 文字列操作
        text = "{}{}".format(self.display1.text, number)
        self.display1.text = text

    # クリア
    def clear(self):
        self.display1.text = ""
        self.display2.text = ""

    # 演算子の入力
    def operators(self, operator):
        text = "{}{}{}".format(self.display2.text, self.display1.text, operator)
        self.display1.text = ""
        self.display2.text = text

    # 入力値の削除
    def delete(self):
        self.display1.text = ""

    # 符号、小数点
    def calculates(self, calc):
        if '-' in self.display1.text:
            text = self.display1.text.split('-')
            del text[0]
            self.display1.text = text
        else:
            self.display1.text = "{}{}".format('-', self.display1.text)

    # 計算
    def equal(self,equal):
        text = "{}{}".format(self.display2.text, self.display1.text)
        text = text.split('+,-,*,/')
        print(text)


class CalculatorRoot(BoxLayout):
    # コンストラクタ
    def __init__(self, **kwargs):
        super(CalculatorRoot, self).__init__(**kwargs)
    pass


class Calc(App):
    # コンストラクタ
    def __init__(self, **kwargs):
        super(Calc, self).__init__(**kwargs)
        self.title = 'SampleGame'
    pass


if __name__ == '__main__':
    Calc().run()
