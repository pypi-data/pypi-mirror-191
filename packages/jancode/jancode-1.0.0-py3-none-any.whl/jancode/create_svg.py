def create(binary_number: str, width: str, path: str, number: str, jancode_type: str):
    content = list()
    margin = 8
    standard_guard_bar_point = [0, 1, 2, 45, 46, 47, 48, 49, 92, 93, 94]
    short_guard_bar_point = [0, 1, 2, 31, 32, 33, 34, 35, 64, 65, 66]

    for i, x in enumerate(binary_number, margin):
        if(int(x)):
            if jancode_type == "standard":
                if i in [n + margin for n in standard_guard_bar_point]:
                    content.append(f'<rect x="{i}" y="1" width="1" height="90%" fill="#000000" />')
                else:
                    content.append(f'<rect x="{i}" y="1" width="1" height="85%" fill="#000000" />')
            else:
                if i in [n + margin for n in short_guard_bar_point]:
                    content.append(f'<rect x="{i}" y="1" width="1" height="90%" fill="#000000" />')
                else:
                    content.append(f'<rect x="{i}" y="1" width="1" height="85%" fill="#000000" />')

    for i in range(len(number)):
        if jancode_type == "standard":
            if i == 0:
                content.append(f'<text x="1" y="98%" font-size="12">{number[i]}</text>')
            elif i < 7:
                content.append(f'<text x="{i * 7 + 4}" y="98%" font-size="12">{number[i]}</text>')
            else:
                content.append(f'<text x="{i * 7 + 9}" y="98%" font-size="12">{number[i]}</text>')
        else:
            if i < 4:
                content.append(f'<text x="{i * 7 + + 12}" y="98%" font-size="12">{number[i]}</text>')
            else:
                content.append(f'<text x="{i * 7 + 16}" y="98%" font-size="12">{number[i]}</text>')

    meta_head = f'<svg version="1.1"\nbaseProfile="full"\nwidth="{margin + width + margin}"\nheight="80"\nxmlns="http://www.w3.org/2000/svg">\n\n' + \
    '<!-- fill background -->\n<rect width="100%" height="100%" fill="white" />\n\n' + \
    '<!-- fill jancode -->\n'
    meta_tail =  "\n\n</svg>"
    data = meta_head + "\n".join(content) + meta_tail

    with open(f"{path}/{number}.svg", "w") as f:
        f.write(data)
