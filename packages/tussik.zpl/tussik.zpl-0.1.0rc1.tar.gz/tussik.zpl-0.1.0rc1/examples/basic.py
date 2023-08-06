from tussik.zpl import ZplWriter

zpl = ZplWriter()
zpl.font(8)
zpl.text('My Basic Test', 30, 50)
zpl.print("1.1.1.1")
zpl.saveas("basic.pdf")
