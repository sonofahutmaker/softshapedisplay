import board
import adafruit_dotstar as dotstar

class LEDManager:
    def __init__(self, ledNum):
        self.lednum = ledNum
        self.dots = dotstar.DotStar(board.D6, board.D5, self.lednum, brightness=0.2)

    #convert from row, col (i.e. 0, 0) to dotstar num 0-210
    def rowColConvert(self, row, col):
        if row%2 == 0: #if even num row, goes top to bottom
            num = row*14 + col
        else: #if odd num row, goes bottom to top
            num = row*14 + (13-col)
        return num

    def setLight(self, row, col, dots, brightness):
        dotNum = self.rowColConvert(row, col)
        dots[dotNum].brightness(brightness)