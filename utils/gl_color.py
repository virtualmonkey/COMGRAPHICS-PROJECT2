def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

def decimalToRgb(colors_array):
    return [round(i*255) for i in colors_array]
