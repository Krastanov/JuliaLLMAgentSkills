# Color Names Reference

## Named Colors (NamedColor)

9 basic terminal colors. Use directly in markup: `{red}text{/red}`.

| Name | ANSI Code |
|------|-----------|
| `default` | 9 |
| `black` | 0 |
| `red` | 1 |
| `green` | 2 |
| `yellow` | 3 |
| `blue` | 4 |
| `magenta` | 5 |
| `cyan` | 6 |
| `white` | 7 |

## 256-Bit Colors (BitColor)

Use in markup: `{gold3}text{/gold3}`. Prefixed with `on_` for background.

### Bright Variants (8-15)
bright_black, bright_red, bright_green, bright_yellow, bright_blue,
bright_magenta, bright_cyan, bright_white

### Blues (17-33)
navy_blue, dark_blue, blue3, blue1, dodger_blue3, dodger_blue2, dodger_blue1,
deep_sky_blue4, deep_sky_blue3, deep_sky_blue2, deep_sky_blue1

### Greens (22-48)
dark_green, green4, green3, green1, spring_green4, spring_green3,
spring_green2, spring_green1, medium_spring_green, chartreuse4,
chartreuse3, chartreuse2, chartreuse1, dark_olive_green3, dark_olive_green2,
dark_olive_green1, green_yellow

### Cyans/Teals (36-51)
dark_cyan, light_sea_green, dark_turquoise, turquoise4, turquoise2,
cyan3, cyan2, cyan1, pale_turquoise4, pale_turquoise1, dark_slate_gray1,
dark_slate_gray2, dark_slate_gray3, aquamarine3, aquamarine1

### Reds/Pinks (88-218)
dark_red, red3, red1, deep_pink4, deep_pink3, deep_pink2, deep_pink1,
hot_pink3, hot_pink2, hot_pink, light_pink4, light_pink3, light_pink1,
pink3, pink1, pale_violet_red1, medium_violet_red

### Purples (55-141)
purple4, purple3, purple, dark_violet, blue_violet, medium_purple4,
medium_purple3, medium_purple2, medium_purple1, medium_purple, slate_blue3,
slate_blue1, royal_blue1, light_slate_blue, light_slate_grey

### Oranges/Browns (94-215)
orange4, orange3, orange1, dark_orange3, dark_orange, dark_goldenrod,
sandy_brown, indian_red, indian_red1, light_coral, salmon1, light_salmon3,
light_salmon1, orange_red1

### Yellows/Golds (106-228)
yellow4, yellow3, yellow2, yellow1, gold3, gold1, light_goldenrod3,
light_goldenrod2, light_goldenrod1, dark_khaki, khaki3, khaki1, wheat4,
wheat1, navajo_white3, navajo_white1, cornsilk1

### Greens (Olive/Sea) (71-157)
dark_sea_green4, dark_sea_green3, dark_sea_green2, dark_sea_green1,
dark_sea_green, pale_green3, pale_green1, sea_green3, sea_green2,
sea_green1, light_green, cadet_blue

### Orchids/Violets (128-213)
dark_magenta, light_pink4, plum4, plum3, plum2, plum1, orchid, orchid2,
orchid1, medium_orchid3, medium_orchid1, medium_orchid, violet, thistle3,
thistle1

### Greys (232-255)
grey0 through grey100 (also spelled gray0-gray100), plus named stops:
grey3, grey7, grey11, grey15, grey19, grey23, grey27, grey30, grey35,
grey37, grey39, grey42, grey46, grey50, grey53, grey54, grey58, grey62,
grey63, grey66, grey69, grey70, grey74, grey78, grey82, grey84, grey85,
grey89, grey93, grey100

### Steel/Sky Blues (67-189)
steel_blue, steel_blue3, steel_blue1, sky_blue3, sky_blue2, sky_blue1,
light_sky_blue3, light_sky_blue1, light_steel_blue3, light_steel_blue1,
light_steel_blue, cornflower_blue, light_cyan3, light_cyan1

### Misc
misty_rose3, misty_rose1, tan, rosy_brown, honeydew2

## Numeric Access

You can also use numeric strings "1" through "255" for direct 256-color index.

## RGB and Hex Colors (RGBColor)

Not named -- specify directly in markup:
- RGB: `{(255, 100, 50)}text{/(255, 100, 50)}`
- Hex: `{#FF6432}text{/#FF6432}`
