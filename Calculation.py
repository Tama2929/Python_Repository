# Python3.5
# グラフィック描画
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


# 符号処理
def sign_change(text):
    result = ''
    sign = list(text)
    # 負の符号確認
    if '-' == sign[0]:
        # 負→正
        sign.pop(0)
        for text in sign:
            result += text
        return result
    else:
        # 正→負
        result = "{}{}".format('-', text)
        return result


# 割合処理(未実施)
def ratio_change(text):
    result = 1
    return result


# 小数点処理(未実施)
def point_change(text):
    result = 1
    return result


class Calculator(BoxLayout):
    global operators_flag
    operators_flag = True
    global equal_flag
    equal_flag = True

    # 数字入力関数
    def numbers(self, number):
        global equal_flag

        if equal_flag:
            # 文字列操作
            text = "{}{}".format(self.display1.text, number)
            self.display1.text = text
            global operators_flag
            operators_flag = True
        else:
            equal_flag = True
            self.display1.text = number
            self.display2.text = ""

    # クリア
    def clear(self):
        self.display1.text = ""
        self.display2.text = ""

    # 演算子の入力
    def operators(self, operator):
        global operators_flag
        global equal_flag

        if self.display1.text == "":
            self.display1.text = '0'
            operators_flag = True

        if operators_flag:
            text = "{}{}{}".format(self.display2.text, self.display1.text, operator)
            self.display1.text = ""
            self.display2.text = text
            operators_flag = False
            equal_flag = True

    # 入力値の削除
    def delete(self):
        self.display1.text = ""

    # 符号、小数点(未実施)、百分率(未実施)
    def calculates(self, calc):
        if calc == '+/-':
            self.display1.text = sign_change(self.display1.text)
        elif calc == '%':
            self.display1.text = ratio_change(self.display1.text)
        else:
            self.display1.text = point_change(self.display1.text)

    # 計算
    def equal(self, equal):
        global equal_flag

        text = "{}{}".format(self.display2.text, self.display1.text)
        self.display2.text = ""
        self.display1.text = str(eval(text))
        equal_flag = False


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
