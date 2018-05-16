import json
import pygame
import sys

def html_to_rgb(arg):
    """Returns tuple with RGB colors from html notation"""
    if len(arg) != 7:
        raise ValueError("HTML color code: \"{}\" has wrong length".format(arg))
    return tuple(int(arg[i:i+2], 16) for i in (1, 3 ,5))

def string_to_tuple(arg):
    """Returns tuple out of string"""
    return tuple(map(lambda x: int(x), arg[1:-1].split(",")))
    
def get_color(arg):
    """Returns tuple with RGB color"""
    if isinstance(arg, tuple):
        if len(arg) != 3:
            raise ValueError("Color tuple: \"{}\" should has length = 3: ".format(arg))
        for i in arg:
            if not isinstance(i, int):
                raise ValueError("Color tuple: \"{}\" should have only numbers".format(arg))
            if i < 0 or i > 255:
               raise ValueError("Color tuple: \"{}\" should have values in range <0, 255>".format(arg))
        return arg
    elif isinstance(arg, str):
        if arg[0] == "#":
            return html_to_rgb(arg)
        elif arg[0] == "(" and arg[-1] == ")":
            return get_color(string_to_tuple(arg))
        else:
            return get_color(palette[arg])
    else:
        raise ValueError("Wrong color code: \"{}\"".format(arg))
        
class Screen:
    """Defines screen parameters"""
    def __init__(self, arg_dict):
        self.fg_color = get_color(arg_dict["fg_color"])
        self.bg_color = get_color(arg_dict["bg_color"])
        if not isinstance(arg_dict["width"], int) and arg_dict["width"] < 0:
            raise ValueError("Screen width should be number > 0")
        self.width = arg_dict["width"]
        if not isinstance(arg_dict["height"], int) and arg_dict["height"] < 0:
            raise ValueError("Screen height should be number > 0")
        self.height = arg_dict["height"]
        
    def prepare(self):
        global win
        win = pygame.display.set_mode((self.width, self.height))
        win.fill(self.bg_color)
        
def check_pos(pos):
    """Checks if argument is integer >= 0"""
    return isinstance(pos, int) and pos >= 0
        
class Figure():
    """Defines figure, has color"""
    def __init__(self, arg_dict):
        if "color" in arg_dict.keys():
            self.color = get_color(arg_dict["color"])
        else:
            self.color = screen.fg_color
            
class OnePosFigure(Figure):
    """Defines figure that has only one position"""
    def __init__(self, arg_dict):
        super().__init__(arg_dict)
        self.pos = []
        if not isinstance(arg_dict["x"], int):
            raise ValueError("x coordinate in: \"{}\" should be number".format(arg_dict["type"]))
        self.pos.append(arg_dict["x"])
        if not isinstance(arg_dict["y"], int):
            raise ValueError("y coordinate in: \"{}\" should be number".format(arg_dict["type"]))
        self.pos.append(arg_dict["y"])

class Circle(OnePosFigure):
    """Defines circle, has raius"""
    def __init__(self, arg_dict):
        super().__init__(arg_dict)
        if not check_pos(arg_dict["radius"]):
            raise ValueError("Radius should be number > 0")
        self.radius = arg_dict["radius"]
    
    def draw(self):
        pygame.draw.circle(win, self.color, self.pos, self.radius, 0)
        
class Point(OnePosFigure):
    """Defines point"""
    def __init__(self, arg_dict):
        super().__init__(arg_dict)
        
    def draw(self):
        pygame.draw.circle(win, self.color, self.pos, 0)
        
class Rectangle(OnePosFigure):
    """Defines rectangle, has width and height"""
    def __init__(self, arg_dict):
        super().__init__(arg_dict)
        if not check_pos(arg_dict["width"]):
            raise ValueError("Rectangle width should be number > 0")
        self.pos.append(arg_dict["width"])
        if not check_pos(arg_dict["height"]):
            raise ValueError("Rectangle height should be number > 0")
        self.pos.append(arg_dict["height"])
        self.pos[0] = self.pos[0] - self.pos[2] // 2
        self.pos[1] = self.pos[1] - self.pos[3] // 2
    
    def draw(self):
        pygame.draw.rect(win, self.color, self.pos)
        
class Square(OnePosFigure):
    """Defines square, has size"""
    def __init__(self, arg_dict):
        super().__init__(arg_dict)
        if "size" in arg_dict.keys() and check_pos(arg_dict["size"]):
            self.pos.append(arg_dict["size"])
            self.pos.append(arg_dict["size"])
        elif "radius" in arg_dict.keys() and check_pos(arg_dict["radius"]):
            self.pos.append(arg_dict["radius"] * 2)
            self.pos.append(arg_dict["radius"] * 2)
        else:
            raise ValueError("Wrong \"size\" or \"radius\" in square")
        self.pos[0] = self.pos[0] - self.pos[2] // 2
        self.pos[1] = self.pos[1] - self.pos[3] // 2
        
    def draw(self):
        pygame.draw.rect(win, self.color, self.pos)
            
class Polygon(Figure):
    """Defines polygon, has list of vertexes"""
    def __init__(self, arg_dict):
        super().__init__(arg_dict)
        if not isinstance(arg_dict["points"], list):
            raise ValueError("Polygon has to has a list of points")
        for point in arg_dict["points"]:
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError("Polygon's list has values : [x,y]")
            for i in point:
                if not isinstance(i, int):
                    raise ValueError("Polygon's list has values : [x,y] where x, y are numbers")
        self.points = arg_dict["points"]
        
    def draw(self):
        pygame.draw.polygon(win, self.color, self.points)

def fill_figures(json_dict):
    """Returns list of figures out of map"""
    figures = []

    if "Figures" in json_dict.keys():
        for fig in json_dict["Figures"]:
            if(fig["type"] == "point"):
                figures.append(Point(fig))
            elif(fig["type"] == "circle"):
                figures.append(Circle(fig))
            elif(fig["type"] == "square"):
                figures.append(Square(fig))
            elif(fig["type"] == "rectangle"):
                figures.append(Rectangle(fig))
            elif(fig["type"] == "polygon"):
                figures.append(Polygon(fig))
            else:
                print("No such thing as: ", fig["type"])
                
    return figures
            
def fill_palette(json_dict):
    """Returns map of colors if Palette is key. If not returns empty list"""
    palette = []
    
    if "Palette" in json_dict.keys():
        palette = json_dict["Palette"]
        
    return palette
    
def print_info():
    """Prints parsed json details"""
    print("Screen: \n", screen.__dict__, "\n")
    
    print("Palette: \n", palette, "\n")
    
    print("Figures: ")
    for fig in figures:
        print(fig.__class__.__name__, ": ", fig.__dict__)
    print()
                    
def main():
    global figures
    global palette
    global screen
    global win
        
    if len(sys.argv) < 2:
        print("Not enough arguments")
        sys.exit(1)
        
    try:
        file = open(sys.argv[1])
    except IOError:
        print("Problem opening file")
    else:
        try:
            file_text = file.read()
            file_json = json.loads(file_text)
            
            palette = fill_palette(file_json)
            screen = Screen(file_json["Screen"])
            figures = fill_figures(file_json)
            
            screen.prepare()
            
            print_info()
            
            for fig in figures:
                fig.draw()
            
            pygame.display.flip()
            
            if len(sys.argv) == 4 and (sys.argv[2] == "-o" or sys.argv[3] == "--output"):
                pygame.image.save(win, sys.argv[3])
                print("file {} has been saved".format(sys.argv[3]))
                    
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
            
        except json.JSONDecodeError:
            print("Invalid JSON file")
        except ValueError as err:
            print("Value error: ", err)
        except KeyError as err:
            print("Key error: ", err)
        finally:
            file.close()
    
if __name__ == "__main__":
    main()