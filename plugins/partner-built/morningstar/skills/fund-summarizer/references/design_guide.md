# Morningstar Design Guidelines

The template CSS is pre-built. Do not modify it. These rules explain the design rationale so you understand what the template encodes:

**Color System** (CSS custom properties in `:root`, from Morningstar Design System)
- `--color-primary` (#0F3D7C, Blue 70): Headers, accents
- `--color-text` (#3D3B39, Neutral 70): Body text - warm grey, softer than pure black
- `--color-text-light` (#7F7D7A, Neutral 40): Labels, secondary text
- `--color-positive` (#039649, Green 50): Positive returns/deltas
- `--color-negative` (#E42513, Red 50): Negative returns/deltas
- `--color-chart-fund` (#2364B9, Blue 50 / Generic 0): Fund data line
- `--color-chart-bench` (#B2013C, Magenta 50 / Generic 1): Benchmark data line
- `--color-alloc-*`: Donut slices use the Generic data-viz palette (color-blind tested): Blue 50, Magenta 50, Yellow 50, Green 70

**Typography**
- Font stack: `"MORN Intrinsic", "Aptos Light", Aptos, Calibri, Georgia, serif`
- Body: 13px, line-height 1.5
- Use Neutral 70 (#3D3B39) for body text, never Neutral 100 (pure black) - reduces harsh contrast

**Ratings Display**
- Star Rating: Filled ★ characters in #000000. Outlined ☆ for funds with <3 years history (extended performance calculation)
- Medalist Rating: Always written as a word (Gold, Silver, Bronze, Neutral, Negative) - never a numeric code or abbreviation

**Color Restrictions**
- Morningstar Red (#FC0412) is for logos/branded moments only.
- Avoid pure black text on white - use Neutral 90 (#3D3B39) for readability
- Data visualization must use the Generic palette in order (0–9) for color-blind accessibility

# Notes
(these were copied from Morningstar's design page - mostly for internal reference for building the skill)

Interaction States
In addition to the core enabled-state tokens, five interaction states are defined for each mode. Interaction tokens are created by adding a state name to the base token. For example, the hover state for $background becomes $background-hover.

Color interaction
Hover
Hover is triggered when a cursor moves over an interactive element. Hover indicates an element is interactive and clickable. Hover is visible by a change in the element's background color, border, or opacity.

Color hover interaction
Focus
The focus state highlights the active element when navigating with a keyboard or voice. In the Product System, a 2px blue border appears around the element.

Color focus interaction
Active
The active state signals a click, tap, or press on an interactive element. It typically appears when an interactive component is pressed down on or turned on.


Performance
Use to show positive, neutral, or negative performance.

Name
Hex
Accessor
Positive	#039649
Neutral	#ECEBEA
Negative	#E42513

Generic
Use when the data you’re plotting doesn’t have a specific color meaning. Always use the generic colors in their provided order, which has been tested across different color weaknesses to ensure colors are as distinguisable for each other as possible.

Name
Hex
Accessor
0	#2364B9
1	#B2013C
2	#F5C72C
3	#125B2F
4	#72A1E0
5	#6B4EA1
6	#F47206
7	#075F65
8	#039649
9	#E42513

Core Color
Core Color color values
Name
Hex
RGB
Morningstar Red	PMS 185	0, 91, 76, 0	#FC0412	252, 4, 18
Neutral Color
Neutral color values
Name
Hex
RGB
Neutral 0 (White)	#FFFFFF	255, 255, 255
Neutral 5	#F6F5F4	246, 245, 244
Neutral 10	#ECEBEA	236, 235, 234
Neutral 15	#DAD9D8	218, 217, 216
Neutral 20	#BDBCBA	189, 188, 186
Neutral 30	#9E9C9B	158, 156, 155
Neutral 40	#7F7D7A	127, 125, 122
Neutral 50	#64625F	100, 98, 95
Neutral 60	#4E4C4A	78, 76, 74
Neutral 70	#3D3B39	61, 59, 57
Neutral 80	#2C2B2A	44, 43, 42
Neutral 85	#212020	33, 32, 32
Neutral 90	#1A1918	26, 25, 24
Neutral 95	#141313	20, 19, 19
Neutral 100 (Black)	#000000	0, 0, 0
Supporting Colors
Blue
Blue color values
Name
Hex
RGB
Blue 5	#F1F6FD	241, 246, 253
Blue 10	#E0EAF8	224, 234, 248
Blue 15	#C4D6EF	196, 214, 239
Blue 20	#A0BCE4	160, 188, 228
Blue 30	#72A1E0	114, 161, 224
Blue 40	#487FCE	72, 127, 206
Blue 50	#2364B9	35, 100, 185
Blue 60	#1A509B	26, 80, 155
Blue 70	#0F3D7C	15, 61, 124
Blue 80	#0B2D5D	11, 45, 93
Blue 85	#061D42	6, 29, 66
Blue 90	#081830	8, 24, 48
Blue 95	#081326	8, 19, 38
Teal
Teal color values
Name
Hex
RGB
Teal 5	#EEF8F9	238, 248, 249
Teal 10	#D6EDEF	214, 237, 239
Teal 15	#B8DBDE	184, 219, 222
Teal 20	#92C6C9	146, 198, 201
Teal 30	#5EAFB4	94, 175, 180
Teal 40	#24979E	36, 151, 158
Teal 50	#0D7D85	13, 125, 133
Teal 60	#075F65	7, 95, 101
Teal 70	#01464B	1, 70, 75
Teal 80	#073235	7, 50, 53
Teal 85	#062426	6, 36, 38
Teal 90	#071C1D	7, 28, 29
Teal 95	#0B1516	11, 21, 22
Green
Green color values
Name
Hex
RGB
Green 5	#F1F8F1	241, 248, 241
Green 10	#DFF0E0	223, 240, 224
Green 15	#C1E0C5	193, 224, 197
Green 20	#9BD0A6	155, 208, 166
Green 30	#6FBF82	111, 191, 130
Green 40	#3CAE61	60, 174, 97
Green 50	#039649	3, 150, 73
Green 60	#06773B	6, 119, 59
Green 70	#125B2F	18, 91, 47
Green 80	#0C4224	12, 66, 36
Green 85	#072C17	7, 44, 23
Green 90	#081F11	8, 31, 17
Green 95	#09170E	9, 23, 14
Yellow
Yellow color values
Name
Hex
RGB
Yellow 5	#FEF9EA	254, 249, 234
Yellow 10	#FDF4DB	253, 244, 219
Yellow 15	#FFEDC5	255, 237, 197
Yellow 20	#FDE4A7	253, 228, 167
Yellow 30	#FADB8B	250, 219, 139
Yellow 40	#F9D261	249, 210, 97
Yellow 50	#F5C72C	245, 199, 44
Yellow 60	#DBB114	219, 177, 20
Yellow 70	#B0902A	176, 144, 42
Yellow 80	#7C682C	124, 104, 44
Yellow 85	#4A401D	74, 64, 29
Yellow 90	#2A230B	42, 35, 11
Yellow 95	#171205	23, 18, 5
Orange
Orange color values
Name
Hex
RGB
Orange 5	#FFF4EE	255, 244, 238
Orange 10	#FEEAE0	254, 234, 224
Orange 15	#FDDBCA	253, 219, 202
Orange 20	#FEC4A7	254, 196, 167
Orange 30	#FDAF86	253, 175, 134
Orange 40	#FE8F4D	254, 143, 77
Orange 50	#F47206	244, 114, 6
Orange 60	#CC6313	204, 99, 19
Orange 70	#9A4B15	154, 75, 21
Orange 80	#673213	103, 50, 19
Orange 85	#41220E	65, 34, 14
Orange 90	#2B1608	43, 22, 8
Orange 95	#1D0E08	29, 14, 8
Red
Red color values
Name
Hex
RGB
Red 5	#FFF3F1	255, 243, 241
Red 10	#FEE3DF	254, 227, 223
Red 15	#FCC6BE	252, 198, 190
Red 20	#F8A99D	248, 169, 157
Red 30	#FC7F70	252, 127, 112
Red 40	#F84D3F	248, 77, 63
Red 50	#E42513	228, 37, 19
Red 60	#BC1D0C	188, 29, 12
Red 70	#8D2216	141, 34, 22
Red 80	#631D15	99, 29, 21
Red 85	#431813	67, 24, 19
Red 90	#30130E	48, 19, 14
Red 95	#210D09	33, 13, 9
Magenta
Magenta color values
Name
Hex
RGB
Magenta 5	#FEF2F3	254, 242, 243
Magenta 10	#FCE4E6	252, 228, 230
Magenta 15	#F1C6CA	241, 198, 202
Magenta 20	#ECA4AA	236, 164, 170
Magenta 30	#E37684	227, 118, 132
Magenta 40	#D1435E	209, 67, 94
Magenta 50	#B2013C	178, 1, 60
Magenta 60	#8C052D	140, 5, 45
Magenta 70	#690C22	105, 12, 34
Magenta 80	#4E121C	78, 18, 28
Magenta 85	#3B0F15	59, 15, 21
Magenta 90	#2E0E10	46, 14, 16
Magenta 95	#240A0D	36, 10, 13
Purple
Purple color values
Name
Hex
RGB
Purple 5	#F6F5FF	246, 245, 255
Purple 10	#EBE8F4	235, 232, 244
Purple 15	#D5CFE4	213, 207, 228
Purple 20	#BCB4D9	188, 180, 217
Purple 30	#A395C9	163, 149, 201
Purple 40	#856EB2	133, 110, 178
Purple 50	#6B4EA1	107, 78, 161
Purple 60	#593883	89, 56, 131
Purple 70	#442968	68, 41, 104
Purple 80	#341F50	52, 31, 80
Purple 85	#28193B	40, 25, 59
Purple 90	#1D142C	29, 20, 44
Purple 95	#161020	22, 16, 32