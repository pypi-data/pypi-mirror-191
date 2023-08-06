from PyQt5 import QtWidgets


class line(QtWidgets.QMainWindow):
    def __init__(self):
        pass
    def update_data(self,po,data,num,b,n=30):
            if b:
                data.append(num)
                po.setData(data,)
            else:
                if (len(data)>n):
                    data[:-1] = data[1:]
                    data[-1]=num
                else:
                    data.append(num)
                po.setData(data,)