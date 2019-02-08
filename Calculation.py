# Python3.5
# グラフィック描画
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from decimal import Decimal


# 符号処理
def sign_change(value):
    result = ''

    # 文字列→配列
    sign = list(value)
    # 負の符号確認
    if '-' == sign[0]:
        # 負→正
        sign.pop(0)
        for text in sign:
            result += text
        return result
    else:
        # 正→負
        result = "{}{}".format('-', value)
        return result


# 割合処理
def ratio_change(value1, value2):
    value = ''
    result = ''

    if value2 =='' or value1 == '':
        return result

    # 文字列→配列
    text = list(value2)

    # 符号の取得
    sign = text.pop()

    # 左辺側の値を文字列化
    for x in text:
        value += x

    ratio = str(eval(value1 + '/100'))
    # 符号別に分岐
    if sign == '+' or sign == '-':
        # Ex)100*(10/100)
        result = str(Decimal(eval(value + '*' + ratio)).to_integral())
    elif sign == '*' or sign == '/':
        result = ratio
    return result


# 小数点処理
def point_change(value):
    result = "{}{}".format(value, '.')
    return result


class Calculator(BoxLayout):
    # 演算子の入力判断フラグ
    global operators_flag
    operators_flag = True
    # 数字の入力判断フラグ
    global equal_flag
    equal_flag = True

    # 数字入力関数
    def numbers(self, number):
        global equal_flag
        global operators_flag

        if equal_flag:
            operators_flag = True
            # 文字列操作
            if self.display1.text == '0':
                result = number
            else:
                result = "{}{}".format(self.display1.text, number)

            self.display1.text = result
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
            operators_flag = True
            self.display1.text = '0'

        if operators_flag:
            operators_flag = False
            equal_flag = True
            result = "{}{}{}".format(self.display2.text, self.display1.text, operator)
            self.display1.text = ""
            self.display2.text = result

    # 入力値の削除
    def delete(self):
        self.display1.text = ""

    # 符号、小数点、百分率
    def calculates(self, calc):
        if calc == '+/-':
            self.display1.text = sign_change(self.display1.text)
        elif calc == '%':
            self.display1.text = ratio_change(self.display1.text, self.display2.text)
        else:
            self.display1.text = point_change(self.display1.text)

    # 計算
    def equal(self, equal):
        global equal_flag
        equal_flag = False
        try:
            text = "{}{}".format(self.display2.text, self.display1.text)
            self.display2.text = ""
            self.display1.text = str(Decimal(eval(text)).to_integral())

        except:
            self.display1.text = ''


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
