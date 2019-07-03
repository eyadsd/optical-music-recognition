from music.corefiles import midiutilTest
from music.corefiles.preprocess import *
from music.corefiles.staffline_removal import *

import os
from website.settings import BASE_DIR

class Match:
    def __init__(self, symbol_name, position, template_shape, score):
        self.symbol_name =symbol_name
        self.position = position
        self.template_shape = template_shape
        self.score = score


class Component:
    def __init__(self):
        self.pixels = []
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.matches = []
    def compute_boundaries(self):
        pixels = self.pixels
        self.min_y = min(pixels, key=lambda elem: elem[0])[0]
        self.min_x = min(pixels, key=lambda elem: elem[1])[1]
        self.max_y = max(pixels, key=lambda elem: elem[0])[0]
        self.max_x = max(pixels, key=lambda elem: elem[1])[1]


def get_pixels(image,visited,i,j,pixels):
    queue = []
    queue.append((i, j))
    visited[i][j] = True

    while(queue):
        i, j = queue.pop(0)
        pixels.append((i, j))
        if not visited[i+1][j] and image[i+1][j] == 0:
            queue.append((i+1, j))
            visited[i+1][j] = 1
        if not visited[i][j + 1] and image[i][j + 1] == 0:
            queue.append((i, j+1))
            visited[i][j + 1] = 1
        if not visited[i-1][j] and image[i-1][j] == 0:
            queue.append((i-1, j))
            visited[i-1][j] = 1
        if not visited[i][j-1] and image[i][j-1] == 0:
            queue.append((i, j-1))
            visited[i][j-1] = 1
        # if not visited[i+1][j+1] and image[i+1][j+1] == 0:
        #     queue.append((i+1, j+1))
        #     visited[i+1][j+1] = 1
        # if not visited[i-1][j-1] and image[i-1][j-1] == 0:
        #     queue.append((i-1, j-1))
        #     visited[i-1][j-1] = 1
        # if not visited[i+1][j-1] and image[i+1][j-1] == 0:
        #     queue.append((i+1, j-1))
        #     visited[i + 1][j - 1] = 1
        # if not visited[i-1][j+1] and image[i-1][j+1] == 0:
        #     queue.append((i-1, j+1))
        #     visited[i-1][j+1]

def get_highest_match(matches):
    if len(matches) == 1:
        return matches[0]
    scores = []
    for match in matches:
        score = 0
        if isinstance(match, list):
            maximum = 0
            for element in match:
                if element.symbol_name == "quarter_note":
                    return match
                if element.score > maximum:
                    maximum = score
            scores.append(maximum)
        else:
            if match.symbol_name == "quarter_note":
                return match
            score = match.score
            scores.append(score)
    index = scores.index(max(scores))
    return matches[index]


def get_connected_components(image):
    visited = np.zeros(image.shape)
    components = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if visited[i][j] == 0 and image[i][j] == 0:
                pixels = []
                component = Component()
                get_pixels(image, visited, i, j, pixels)
                component.pixels = pixels
                component.compute_boundaries()
                components.append(component)
    return components

def intersected(bottom_left1, top_right1, bottom_left2, top_right2):
    if top_right1[0] < bottom_left2[0] or bottom_left1[0] > top_right2[0]:
        return 0

    if top_right1[1] < bottom_left2[1] or bottom_left1[1] > top_right2[1]:
        return 0

    return 1
#
#path = "test_scores\\" + os.listdir("test_scores")[3]
def get_midi(path, track_name):
    height = 1914
    width = 1353
    print(path)
    print(track_name)
    image = cv.imread(path, 0)
    print(image.shape)
    ret, image = cv.threshold(image, 245, 255, cv.THRESH_BINARY)
    image = resize(image, height, width)

    image, staff_image = remove_staffline(image)
    #cv.imwrite('no_staff.png', image)
    #cv.imwrite('staff_image.png', staff_image)
    cv.imwrite(os.path.join(os.path.join(BASE_DIR,'no_staff.png')), image)
    #cv.imwrite(os.path.join(os.path.join(BASE_DIR,'staff_image.png')), staff_image)
    staves = get_staves(staff_image)

    print(len(staves))
    components = get_connected_components(image)

    for stave in staves:
        stave.get_components(components)
    #
    # count = 0
    # for component in components:
    #     count+=1
    #     height = component.max_y - component.min_y
    #     width = component.max_x - component.min_x
    #     canvas = image[component.min_y:component.max_y,component.min_x:component.max_x]
    #     cv.imwrite("components/component" + str(count)+ ".png" , canvas)
    #     print(canvas)
    #     print(height, width)
    #     print(canvas.shape)

    templates = {}

    for folder in os.listdir(os.path.join(os.path.join(BASE_DIR,'templatesNote\\'))):
        for file in os.listdir(os.path.join(os.path.join(BASE_DIR,'templatesNote\\')) + folder):
            path = os.path.join(os.path.join(BASE_DIR,'templatesNote\\')) + folder + "\\" + file
            print(file)
            template = cv.imread(path, 0)
            if folder in templates:
                templates[folder].append(template)
            else:
                templates[folder] = []
                templates[folder].append(template)

    image = cv.imread(os.path.join(os.path.join(BASE_DIR,'no_staff.png')), 0)
    # im = cv.imread(path)
    # ret, im = cv.threshold(im, 245, 255, cv.THRESH_BINARY)
    # im = resize(im, height, width)

    colored = cv.cvtColor(image, cv.COLOR_GRAY2RGB)
    count = 0
    for stave in staves:
        print("stave")
        for component in stave.components:
            canvas = image[component.min_y - 3:component.max_y + 3, component.min_x - 3:component.max_x + 3]
            for symbol_name in templates:
                for template in templates[symbol_name]:
                    if symbol_name == "flat":
                        continue
                    w, h = template.shape[::-1]
                    if canvas.shape[0] < template.shape[0] or canvas.shape[1] < template.shape[1]:
                        continue
                    try:

                        res = cv.matchTemplate(canvas, template, cv.TM_CCOEFF_NORMED)
                        threshold = 0.5
                        loc = np.where(res >= threshold)
                        matches = []
                        for pt in zip(*loc[::-1]):
                            intersection = 0
                            if len(matches) != 0:
                                for match in matches:
                                    if intersected(match, (match[0] + w, match[1] + h), pt, (pt[0] + w, pt[1] + h)):
                                        intersection = 1
                                        break
                            if intersection == 0:
                                matches.append(pt)
                        pt = (component.min_x, component.min_y)
                        w, h = canvas.shape[::-1]

                        if len(matches) > 1 and symbol_name == "quarter_note":
                            potential_match = []
                            for match in matches:
                                j, i = (match[0] + component.min_x - 3, match[1] + component.min_y - 3)
                                position = (i + math.ceil(template.shape[0] / 2), j + math.ceil(template.shape[1] / 2))
                                score = res[(match[1], match[0])]
                                m = Match(symbol_name, (j, i), template.shape, score)
                                potential_match.append(m)
                            component.matches.append(potential_match)

                        elif len(matches) == 1:
                            j, i = (match[0] + component.min_x - 3, match[1] + component.min_y - 3)
                            position = (i + math.ceil(template.shape[0] / 2), j + math.ceil(template.shape[1] / 2))
                            score = res[(match[1], match[0])]
                            m = Match(symbol_name, (j, i), template.shape, score)
                            component.matches.append(m)

                    except:
                        pass
            colors = {"quarter_note": (200, 20, 0), "half_note":(50, 200, 10),"eighth_note": (50, 200, 10), "G_clef": (10, 90, 200), "F_clef": (10, 90, 200)}

            if len(component.matches) > 0:
                max_match = get_highest_match(component.matches)
                if(isinstance(max_match, list)):
                    for element in max_match:

                        element.symbol_name = "eighth_note"
                        j, i = element.position
                        stave.symbols.append(Symbol((i + element.template_shape[0]/2, j + element.template_shape[1]/2), element.symbol_name))
                        if element.symbol_name in colors:
                            colored[(
                            i + math.ceil(element.template_shape[0] / 2), j + math.ceil(element.template_shape[1] / 2))] = colors[element.symbol_name]
                            rect = cv.rectangle(colored, (j, i), (j + element.template_shape[1], i + element.template_shape[0]), colors[element.symbol_name], 2)
                        else:
                            rect = cv.rectangle(colored, (j, i), (j + element.template_shape[1], i + element.template_shape[0]), (200, 200, 50), 2)

                else:
                    j, i = max_match.position
                    stave.symbols.append(Symbol((i +math.ceil( max_match.template_shape[0]/2), j + math.ceil(max_match.template_shape[1]/2)), max_match.symbol_name))
                    colored[(i + math.ceil(max_match.template_shape[0] / 2), j + math.ceil(max_match.template_shape[1] / 2))] = [255, 0, 0]

                    if max_match.symbol_name in colors:
                        rect = cv.rectangle(colored, (j, i), (j + max_match.template_shape[1], i + max_match.template_shape[0]), colors[max_match.symbol_name], 2)
                    else:
                        rect = cv.rectangle(colored, (j, i), (j + max_match.template_shape[1], i + max_match.template_shape[0]), (200, 200, 50), 2)


    for stave in staves:
        print("stavee")
        stave.calculate_symbol_positions()
        stave.sort_symbols()
        for symbol in stave.symbols:
            print(symbol.label,symbol.position_in_stave)

    midiutilTest.create_midi_file(staves, track_name)

    cv.imwrite("media/res/result_" + track_name + ".png", colored)
