import board
import adafruit_dotstar as dotstar

class LEDManager:
    def __init__(self, ledNum):
        self.lednum = ledNum
        self.dots = dotstar.DotStar(board.D6, board.D5, self.lednum, brightness=0.2)

    #convert from row, col (i.e. 0, 0) to dotstar num 0-210
    def rowColConvert(self, row, col):
        if col%2 == 0:
            num = col*15 + row
        else:
            num = col*15 + (14-row)
        return num

    #brightness is a float between 0 and 1
    def setLight(self, row, col, brightness):
        dotNum = self.rowColConvert(row, col)
        fillnum = 255 * brightness
        self.dots[dotNum].fill(fillnum, fillnum, fillnum)

    def setLight(self, ledIndex, brightness):
        fillnum = 255 * brightness
        self.dots[ledIndex].fill(fillnum, fillnum, fillnum)