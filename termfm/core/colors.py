import curses

from termfm.types import ColorPairs


pairs = {
    "normal": 1,
    "statusline": 2,
    "borders": 3,
    "borders_active": 4,
    "selected": 5,
    "current": 6,
    "icon_folder": 7,
    "icon_file": 8,
    "cursor": 9,
}


def color_pair(key: ColorPairs):
    return curses.color_pair(pairs[key])


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(pairs["normal"], colors.WHITE, colors.GREY0)
    curses.init_pair(pairs["borders"], colors.GREY42, colors.GREY0)
    curses.init_pair(pairs["borders_active"], colors.STEELBLUE, colors.GREY0)
    curses.init_pair(pairs["statusline"], colors.WHITE, colors.STEELBLUE)
    curses.init_pair(pairs["selected"], colors.WHITE, colors.STEELBLUE)
    curses.init_pair(pairs["current"], colors.WHITE, colors.STEELBLUE)
    curses.init_pair(pairs["icon_folder"], colors.LIGHTGOLDENROD5, colors.GREY0)
    curses.init_pair(pairs["icon_file"], colors.WHITE, colors.GREY0)
    curses.init_pair(pairs["cursor"], colors.GREY0, colors.WHITE)


class Colors:
    BLACK = 0
    MAROON = 1
    GREEN = 2
    OLIVE = 3
    NAVY = 4
    PURPLE = 5
    TEAL = 6
    SILVER = 7
    GREY = 8
    RED = 9
    LIME = 10
    YELLOW = 11
    BLUE = 12
    FUSCIA = 13
    AQUA = 14
    WHITE = 15
    GREY0 = 16
    NAVYBLUE = 17
    DARKBLUE = 18
    BLUE3 = 19
    BLUE3 = 20
    BLUE1 = 21
    DARKGREEN = 22
    DEEPSKYBLUE5 = 23
    DEEPSKYBLUE6 = 24
    DEEPSKYBLUE7 = 25
    DODGERBLUE3 = 26
    DODGERBLUE2 = 27
    GREEN4 = 28
    SPRINGGREEN4 = 29
    TURQUOISE4 = 30
    DEEPSKYBLUE4 = 31
    DEEPSKYBLUE3 = 32
    DODGERBLUE1 = 33
    GREEN3 = 34
    SPRINGGREEN3 = 35
    DARKCYAN = 36
    LIGHTSEAGREEN = 37
    DEEPSKYBLUE2 = 38
    DEEPSKYBLUE1 = 39
    GREEN3 = 40
    SPRINGGREEN3 = 41
    SPRINGGREEN4 = 42
    CYAN3 = 43
    DARKTURQUOISE = 44
    TURQUOISE2 = 45
    GREEN1 = 46
    SPRINGGREEN2 = 47
    SPRINGGREEN1 = 48
    MEDIUMSPRINGGREEN = 49
    CYAN2 = 50
    CYAN1 = 51
    DARKRED = 52
    DEEPPINK4 = 53
    PURPLE4 = 54
    PURPLE5 = 55
    PURPLE3 = 56
    BLUEVIOLET = 57
    ORANGE4 = 58
    GREY37 = 59
    MEDIUMPURPLE4 = 60
    SLATEBLUE3 = 61
    SLATEBLUE4 = 62
    ROYALBLUE1 = 63
    CHARTREUSE4 = 64
    DARKSEAGREEN4 = 65
    PALETURQUOISE4 = 66
    STEELBLUE = 67
    STEELBLUE3 = 68
    CORNFLOWERBLUE = 69
    CHARTREUSE3 = 70
    DARKSEAGREEN4 = 71
    CADETBLUE = 72
    CADETBLUE = 73
    SKYBLUE3 = 74
    STEELBLUE1 = 75
    CHARTREUSE3 = 76
    PALEGREEN3 = 77
    SEAGREEN3 = 78
    AQUAMARINE3 = 79
    MEDIUMTURQUOISE = 80
    STEELBLUE1 = 81
    CHARTREUSE2 = 82
    SEAGREEN2 = 83
    SEAGREEN1 = 84
    SEAGREEN4 = 85
    AQUAMARINE1 = 86
    DARKSLATEGRAY2 = 87
    DARKRED = 88
    DEEPPINK4 = 89
    DARKMAGENTA = 90
    DARKMAGENTA = 91
    DARKVIOLET = 92
    PURPLE = 93
    ORANGE4 = 94
    LIGHTPINK4 = 95
    PLUM4 = 96
    MEDIUMPURPLE5 = 97
    MEDIUMPURPLE3 = 98
    SLATEBLUE1 = 99
    YELLOW4 = 100
    WHEAT4 = 101
    GREY53 = 102
    LIGHTSLATEGREY = 103
    MEDIUMPURPLE = 104
    LIGHTSLATEBLUE = 105
    YELLOW4 = 106
    DARKOLIVEGREEN3 = 107
    DARKSEAGREEN = 108
    LIGHTSKYBLUE2 = 109
    LIGHTSKYBLUE3 = 110
    SKYBLUE2 = 111
    CHARTREUSE2 = 112
    DARKOLIVEGREEN3 = 113
    PALEGREEN3 = 114
    DARKSEAGREEN3 = 115
    DARKSLATEGRAY3 = 116
    SKYBLUE1 = 117
    CHARTREUSE1 = 118
    LIGHTGREEN = 119
    LIGHTGREEN2 = 120
    PALEGREEN1 = 121
    AQUAMARINE1 = 122
    DARKSLATEGRAY1 = 123
    RED3 = 124
    DEEPPINK4 = 125
    MEDIUMVIOLETRED = 126
    MAGENTA3 = 127
    DARKVIOLET = 128
    PURPLE = 129
    DARKORANGE3 = 130
    INDIANRED = 131
    HOTPINK3 = 132
    MEDIUMORCHID3 = 133
    MEDIUMORCHID = 134
    MEDIUMPURPLE2 = 135
    DARKGOLDENROD = 136
    LIGHTSALMON3 = 137
    ROSYBROWN = 138
    GREY63 = 139
    MEDIUMPURPLE2 = 140
    MEDIUMPURPLE1 = 141
    GOLD3 = 142
    DARKKHAKI = 143
    NAVAJOWHITE3 = 144
    GREY69 = 145
    LIGHTSTEELBLUE3 = 146
    LIGHTSTEELBLUE = 147
    YELLOW3 = 148
    DARKOLIVEGREEN3 = 149
    DARKSEAGREEN3 = 150
    DARKSEAGREEN2 = 151
    LIGHTCYAN3 = 152
    LIGHTSKYBLUE1 = 153
    GREENYELLOW = 154
    DARKOLIVEGREEN2 = 155
    PALEGREEN1 = 156
    DARKSEAGREEN2 = 157
    DARKSEAGREEN1 = 158
    PALETURQUOISE1 = 159
    RED3 = 160
    DEEPPINK3 = 161
    DEEPPINK5 = 162
    MAGENTA4 = 163
    MAGENTA3 = 164
    MAGENTA2 = 165
    DARKORANGE3 = 166
    INDIANRED = 167
    HOTPINK3 = 168
    HOTPINK2 = 169
    ORCHID = 170
    MEDIUMORCHID1 = 171
    ORANGE3 = 172
    LIGHTSALMON3 = 173
    LIGHTPINK3 = 174
    PINK3 = 175
    PLUM3 = 176
    VIOLET = 177
    GOLD3 = 178
    LIGHTGOLDENROD3 = 179
    TAN = 180
    MISTYROSE3 = 181
    THISTLE3 = 182
    PLUM2 = 183
    YELLOW3 = 184
    KHAKI3 = 185
    LIGHTGOLDENROD2 = 186
    LIGHTYELLOW3 = 187
    GREY84 = 188
    LIGHTSTEELBLUE1 = 189
    YELLOW2 = 190
    DARKOLIVEGREEN4 = 191
    DARKOLIVEGREEN1 = 192
    DARKSEAGREEN1 = 193
    HONEYDEW2 = 194
    LIGHTCYAN1 = 195
    RED1 = 196
    DEEPPINK2 = 197
    DEEPPINK6 = 198
    DEEPPINK1 = 199
    MAGENTA2 = 200
    MAGENTA1 = 201
    ORANGERED1 = 202
    INDIANRED2 = 203
    INDIANRED1 = 204
    HOTPINK4 = 205
    HOTPINK5 = 206
    MEDIUMORCHID1 = 207
    DARKORANGE = 208
    SALMON1 = 209
    LIGHTCORAL = 210
    PALEVIOLETRED1 = 211
    ORCHID2 = 212
    ORCHID1 = 213
    ORANGE1 = 214
    SANDYBROWN = 215
    LIGHTSALMON1 = 216
    LIGHTPINK1 = 217
    PINK1 = 218
    PLUM1 = 219
    GOLD1 = 220
    LIGHTGOLDENROD4 = 221
    LIGHTGOLDENROD5 = 222
    NAVAJOWHITE1 = 223
    MISTYROSE1 = 224
    THISTLE1 = 225
    YELLOW1 = 226
    LIGHTGOLDENROD1 = 227
    KHAKI1 = 228
    WHEAT1 = 229
    CORNSILK1 = 230
    GREY100 = 231
    GREY3 = 232
    GREY7 = 233
    GREY11 = 234
    GREY15 = 235
    GREY19 = 236
    GREY23 = 237
    GREY27 = 238
    GREY30 = 239
    GREY35 = 240
    GREY39 = 241
    GREY42 = 242
    GREY46 = 243
    GREY50 = 244
    GREY54 = 245
    GREY58 = 246
    GREY62 = 247
    GREY66 = 248
    GREY70 = 249
    GREY74 = 250
    GREY78 = 251
    GREY82 = 252
    GREY85 = 253
    GREY89 = 254
    GREY93 = 255


colors = Colors()
