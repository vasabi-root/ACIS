from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPalette
from xml.etree import ElementTree


def parse_xml(file_path) -> 'QPalette':
    def generate_brushes(brush_index):

        # required imports
        assert QColor
        assert Qt
        assert QBrush

        brush_style_, *rgba = brushes[brush_index]
        brush_ = eval(f"QBrush(QColor(*{rgba}))")
        brush_.setStyle(eval(f"Qt.{brush_style_}"))
        return brush_

    def check_or_create_brush(brush_style, *color_args):
        if (brush_style, *color_args) in brushes:
            return brushes.index((brush_style, *color_args))
        else:
            brushes.append((brush_style, *color_args))
            return len(brushes) - 1

    tree = ElementTree.parse(file_path)
    root = tree.getroot()

    brushes = []
    qt_brushes = []
    assign_brush_roles = {}

    for activeState in root:
        active_state = activeState.tag
        assign_brush_roles[active_state.title()] = {}

        for colorRole in activeState:
            role = colorRole.attrib['role']  # get the role for the colorRole (ex.: WindowText)

            brush = colorRole[0]  # get the brush element
            brushStyle = brush.attrib['brushstyle']  # get the brush style, solidPattern, ...etc

            color = colorRole[0][0]  # get color element for the brush
            alpha = color.attrib['alpha']  # get the color alpha value
            r, g, b, a = color[0].text, color[1].text, color[2].text, alpha  # get color values for the brush

            index_ = check_or_create_brush(brushStyle, int(r), int(g), int(b),
                                           int(a))  # checks if brush exists, or create a new brush and stores it

            assign_brush_roles[active_state.title()][role] = index_

    for br_index in range(len(brushes)):
        _brush = generate_brushes(br_index)
        qt_brushes.append(_brush)

    # create palette
    palette = QPalette()
    for active_state, role_dict in assign_brush_roles.items():
        for _role, _brush in role_dict.items():
            print(active_state, _role)
            brush_x = qt_brushes[_brush]
            assert brush_x
            eval(f"palette.setBrush(QPalette.{active_state}, QPalette.{_role}, brush_x)")

    return palette
