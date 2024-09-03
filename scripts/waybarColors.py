class Color:
    def __init__(self, colorFile):
        self.colors = {}

        file = open(colorFile, "r")

        for line in file.readlines():
            name = line.split(' ')[1]
            color = line.split(' ')[2].strip(';\n')

            if not self.colors.get(name):
                self.colors[name] = color

    def get_colors(self):
        return self.colors


# color = Color("mocha.css").get_colors()

# print(color["crust"])

