import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "src" / "Ploan_skill.py"
SPEC = importlib.util.spec_from_file_location("ploan_skill", MODULE_PATH)
PLOAN_SKILL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLOAN_SKILL)


def scene(subject, lines, **overrides):
    data = {
        "subject": subject,
        "style": "classic-ascii-gallery-inspired volumetric-shaded-ascii",
        "composition": "single-object",
        "focal_strength": "high",
        "background_width": 80,
        "background_height": len(lines),
        "lines": [line.ljust(80) for line in lines],
    }
    data.update(overrides)
    return data


GOOD_MOON = [
    "        .                 *                 .",
    "",
    "                         .-\"\"\"\"\"\"\"\"\"-.",
    "                      .-'   ::.  .:   '-.",
    "                    .'   :  o   :  :  .  '.",
    "                   /  .::  .--.  :  o     \\",
    "                  |  :   (    )  ::  .--.   |",
    "                  |  : o  (  )   :  (    )  |",
    "                  |  ::    '--' ::  (  )    |",
    "                   \\ :  .--.   :    '--'  /",
    "                    '. :: (  )  :::  o   .'",
    "                      '-.  '--'  :: .-'",
    "                         '-..__..-'",
    "",
    "       *                    .                  *",
    "",
]


BAD_RAMP_MOON = [
    "       .                                           .",
    "                                           .-=========-.",
    "                                      .-==+++++*****++=-.",
    "                                  .-=++***####%%%%###*+=.",
    "                                .-+**###%%88888888%%##*+=.",
    "                               /+*##%%8888@@@8888%%##*+\\",
    "                              |+*#%%888@@@888000888%#*|",
    "                              |+*#%88@@@88ooOO00888%#*|",
    "                              |+*#%88@@8o..,,o0888%#*|",
    "                              |+*#%888@8o,  .:o0888%#*|",
    "                              |+*#%88888O:   ,o0888%#*|",
    "                              |+*#%%88880o::oO8888%#*|",
    "                              |+**##%%8880008888%%#*+|",
    "                               \\+**##%%%888888%%%#*+/",
    "                                \\-=+**###%%%%###**+=/",
    "                                  `--==++*****++==--`",
    "                                    `---=======---`",
    "",
]


BAD_O_MOON = [
    "",
    "",
    "",
    "",
    "                                         .--:oOOOOOOo:--.",
    "                                      .:oOOOOOOO888OOOOOOo:.",
    "                                    .oOOOOoo:..  ..:oO888OOOo.",
    "                                  .oOOOoo.   .oo.    .:O888OOo.",
    "                                  oOOOo   . (o..o) .    O888OOo",
    "                                 oOOO:  .oo.  ::  .oo.  :O88OOO",
    "                                 OOOO  (O88)  ..  (oO)   O88OOO",
    "                                 OOOO:  :oo. .--.  ..   :888OOO",
    "                                  OOOOo.    (o88o)    .o888OOo",
    "                                  .oOOOOo:.   ::   .:o888OOOo.",
    "                                    .oOOOOOOo::::oO888OOOOo.",
    "                                      .:oOOOOOO888OOOOOo:.",
    "                                         .--:oOOOOOOo:--.",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]


GOOD_CRESCENT = [
    "",
    "",
    "                         _..------.._",
    "                      .-' M8: .LCG0 `-.",
    "                    .' NW .--. G08@LC `.",
    "                   / M8 (    ) C0@8N  .'",
    "                  / NW: '--' G08  .'",
    "                 | M8 .: o  C0  .'",
    "                 | NW ( ) :G8  /",
    "                 | M8 .-.  C0  \\",
    "                 | NW ( ) :G08  `.",
    "                  \\ M8 '--' LC0@  `.",
    "                   \\ NW: .LCG088MN  `.",
    "                    `. M8LCG08@NWM8 .'",
    "                      `-. NWG08M .-'",
    "                         `--......--'",
    "",
    "",
]


BAD_CLOSED_CRESCENT = [
    "                _..-\"\"\"\"\"-.._",
    "             .-' MMMMMMMMMMMMM `-.",
    "           .' MMMMMM8888MMMMMMM   `.",
    "          / MMMMM88888888MMMMM      \\",
    "         | MMMM8888@@@888MMMM       |",
    "         | MMM8888@@@@88MMMM       /",
    "         | MMMM8888@@88MMMM     .-'",
    "          \\ MMMMM8888MMMM    .-'",
    "           `. MMMMMMMMMM   _.-'",
    "             `-. MMMM _..-'",
    "                `----'",
]


BAD_STIPPLED_EDGE_CRESCENT = [
    "                                                                 .",
    "                                                            *",
    "                                                                   _..---.._",
    "                                                                .-'  .:::::. `-.",
    "                                                              .'   .:::::::::.  `.",
    "                                                             /   .:::::::::::'    \\",
    "                                                            /   :::::::::::'       |",
    "                                                           |   ::::::::::'        /",
    "                                                           |  .:::::::::'       .'",
    "                                                           |  :::::::::.      .'",
    "                                                            \\  `:::::::::.      `.",
    "                                                             `.   `::::::::.      \\",
    "                                                               `-.   `:::::::.    |",
    "                                                                  `-.   `::::'    /",
    "                                                                       `--..__..-'",
    "",
]


GOOD_SATURN = [
    "",
    "                 _.oo.",
    "             _.u[[/;:,.         .odMMMMMM'",
    "          .o888UU[[[/;:-.   .o@P^    MMM^",
    "         oN88888UU[[[/;::-.       dP^",
    "        dNMMNN888UU[[[/;:--.  .o@P^",
    "       ,MMMMMMN888UU[[/;::-.o@^",
    "       NNMMMNN888UU[[[/~.o@P^",
    "       888888888UU[[[/o@^-..",
    "      oI8888UU[[[/o@P^:--..",
    "   .@^  YUU[[[/o@^;::---..",
    "   oMP     ^/o@P^;:::---..",
    "   .dMMM    .o@^  ^;::---...",
    "   dMMMMMMM@^`       `^^^^",
    "   YMMMUP^",
    "   ^^",
    "",
    "",
]


BAD_SCREEN_WIDE_SATURN = [""] * 22 + [
    "                                                                                             _..------.._",
    "                                                                                        _.-~::,,......,,::~-.",
    "                                                         __..----~~~~                 .~.,:;i11tttt11i;:,.  ~.          ~~~~----..__",
    "                                               __..---~~~                            /.,;itfLCGGGCLft1i;:,.  \\                       ~~~-",
    "                                       _..---~~                                      /,:tfCG008880GCLti;:,. \\",
    "                                  _.-~~                                              |.;fCG08888880GCL1;:,. |",
    "                               .-~                                                   |:tG0888@@@@8880GLi;:,.|",
    "                              /                                                      |;L088@@@@@@@8880Cf:,.|",
    "                             /                                                       |iG0888@@@@@8880Gt;:,.|",
    "                            ;                                                         \\tC0888@@@88880L1:,./",
    "                            |                                                          \\;fCG0888880Cti:,/",
    "                            ;          __..----~~~~~~~----..__                          ~-;itLCCCLt1;.-~",
    "                             \\__..--~~~                       ~~~---..__                    ~--....--~",
    "                        _..--~                                        ~~~---...___                     ___...---~~~",
    "                   _.--~                                                         ~~~~-----.._________..-----~~~~",
    "               .-~~                                                                 .,:;i1tfLCG00880GCLft1i;:,.",
    "                 ~~---..___                                              ___...---~~~--==++**######**++==--~~~---...___",
    "                           ~~~~----....._________________________.....----~~~~             ~~~~~~~~             ~~~~----.....________....",
] + [""] * 9


BAD_REPETITIVE_CRESCENT = [
    "           _..--------.._",
    "        .-' MMMMMMMMMMMMM `-.",
    "      .' MMMMM88888MMMMMMMM  `.",
    "     / MMMMM8888888MMMMM   _.-'",
    "    / MMMM8888@@88MMM   .-'",
    "   | MMM8888@@@@8MM  .-'",
    "   | MM8888@@@@8M  .'",
    "   | MM8888@@@@8M  \\",
    "   | MMM8888@@88MM  `.",
    "    \\ MMMM8888@@8MMM   `-.",
    "     \\ MMMMM888888MMMMM    `-.",
    "      `. MMMMM8888MMMMMMMMM   `.",
    "        `-. MMMMMMMMMMMMMMMMM .'",
    "           `--..__________..--'",
]


def two_object_canvas(left, right):
    def compact(lines):
        lines = [line.rstrip() for line in lines if line.strip()]
        indent = min(len(line) - len(line.lstrip()) for line in lines)
        return [line[indent:] for line in lines]

    left = compact(left)
    right = compact(right)
    rows = [""]
    for index in range(max(len(left), len(right))):
        left_line = left[index] if index < len(left) else ""
        right_line = right[index] if index < len(right) else ""
        rows.append((" " * 5 + left_line).ljust(70) + right_line)
    return rows + [""] * (49 - len(rows))


class SceneQualityTest(unittest.TestCase):
    def test_rejects_procedural_filled_moon(self):
        result = PLOAN_SKILL.analyze_scene_quality(scene("moon on the right", BAD_RAMP_MOON))

        self.assertFalse(result["passed"])
        self.assertLess(result["score"], 100)
        self.assertIn("filled_planet_blob", result["issues"])

    def test_accepts_cratered_moon(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "cratered moon",
                GOOD_MOON,
                composition="single-centered-object",
                background_width=64,
            )
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("moon_not_recognizable", result["issues"])
        self.assertNotIn("filled_planet_blob", result["issues"])
        self.assertNotIn("weak_visual_weight", result["issues"])

    def test_rejects_o_character_moon_blob(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "single centered cratered moon",
                BAD_O_MOON,
                composition="single-centered-object",
                background_width=96,
            )
        )

        self.assertFalse(result["passed"])
        self.assertIn("filled_planet_blob", result["issues"])

    def test_rejects_block_glyph_moon(self):
        lines = [
            "                         ▄▄▟▛",
            "                     ▄▟████▛",
            "                  ▄█████▀ ▐▌",
            "               ▄▟████▀    ▝▌",
            "             ◂███▛░       ▐",
            "            ◂██▛          ▐",
            "             ◂██▄         ▟",
            "               ▀███▄     ▟▌",
            "                  ▀████▄▟▛",
            "                     ▀███▀",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene("single moon", lines, composition="single-centered-object")
        )

        self.assertFalse(result["passed"])
        self.assertIn("pixel_art_moon", result["issues"])

    def test_accepts_asymmetric_crescent(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "crescent moon on the left",
                GOOD_CRESCENT,
                composition="single-object on left",
                background_width=136,
            )
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("moon_not_recognizable", result["issues"])
        self.assertNotIn("crescent_not_recognizable", result["issues"])
        self.assertNotIn("weak_visual_weight", result["issues"])

    def test_rejects_closed_disc_disguised_as_crescent(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene("crescent moon on the left", BAD_CLOSED_CRESCENT, composition="single-object on left")
        )

        self.assertFalse(result["passed"])
        self.assertIn("weak_crescent_cutout", result["issues"])

    def test_rejects_stippled_edge_hugging_crescent(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "crescent moon with stars",
                BAD_STIPPLED_EDGE_CRESCENT,
                composition="single-object on right",
                background_width=80,
            )
        )

        self.assertFalse(result["passed"])
        self.assertIn("stippled_crescent", result["issues"])
        self.assertIn("subject_clipped_or_edge_hugging", result["issues"])

    def test_preserves_letter_shaded_moon(self):
        lines = [
            "",
            "                    .-aaaaaaaaaaaa-.",
            "                 .-aaaaoooOO00Oooaaaa-.",
            "                /aaaao..,:;i1tO88Oaaaa\\",
            "               /aaaao. (  ) tfL0888Oaaaa\\",
            "              |aaaao:  '--' CG08888Oaaaa|",
            "              |aaaao; .--.  G088888Oaaaa|",
            "              |aaaao: (  ) L0088888Oaaaa|",
            "               \\aaaao. '--' O88888Oaaaa/",
            "                \\aaaaoooOO00888Oaaaa/",
            "                 '-aaaaaOOOaaaaaa-'",
            "                    '-aaaaaaaa-'",
            "",
            "",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene("letter-shaded moon", lines, composition="single-centered-object", background_width=64)
        )

        self.assertNotIn("moon_not_recognizable", result["issues"])
        self.assertNotIn("filled_planet_blob", result["issues"])

    def test_accepts_tilted_ring_saturn(self):
        result = PLOAN_SKILL.analyze_scene_quality(scene("saturn", GOOD_SATURN))

        self.assertTrue(result["passed"], result)
        self.assertNotIn("saturn_not_recognizable", result["issues"])

    def test_rejects_screen_wide_saturn_behind_opencode_ui(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "saturn with stars around it",
                BAD_SCREEN_WIDE_SATURN,
                composition="single-centered-object",
                background_width=136,
                background_height=49,
            ),
            target="opencode",
        )

        self.assertFalse(result["passed"])
        self.assertIn("saturn_not_recognizable", result["issues"])
        self.assertEqual(result["metrics"]["focal_width"], 0)

    def test_accepts_distinct_saturn_and_crescent(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "beautiful detailed Saturn and crescent moon with stars",
                two_object_canvas(GOOD_CRESCENT, GOOD_SATURN),
                composition="two compact objects in upper corners",
                background_width=136,
                background_height=49,
            ),
            target="opencode",
        )

        self.assertTrue(result["passed"], result)
        self.assertGreaterEqual(result["metrics"]["compact_subject_count"], 2)

    def test_rejects_repetitive_crescent_beside_valid_saturn(self):
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "beautiful detailed Saturn and crescent moon with stars",
                two_object_canvas(BAD_REPETITIVE_CRESCENT, GOOD_SATURN),
                composition="two compact objects in upper corners",
                background_width=136,
                background_height=49,
            ),
            target="opencode",
        )

        self.assertFalse(result["passed"])
        self.assertIn("repetitive_crescent_fill", result["issues"])

    def test_rejects_single_line_saturn_ring(self):
        lines = [
            "",
            "                         .------.",
            "                      .-'  oO0   '-.",
            "                     /   oO000O     \\",
            "          ===========|  O00000O  |===========",
            "                     \\   oO000O     /",
            "                      '-.  oO0  .-'",
            "                         '------'",
            "",
            "",
            "",
            "",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(scene("saturn", lines))

        self.assertFalse(result["passed"])
        self.assertIn("saturn_not_recognizable", result["issues"])

    def test_accepts_five_row_codex_house_footer(self):
        lines = [""] * 15 + [
            "                         /\\____/\\",
            "              __________/  []   \\__________",
            "             |  []  ##  |  __   |  ##  []  |",
            "             |__________|_|__|__|___________|",
            "        ~~~~~~~..,,____/          \\____,,..~~~~~~~",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "cool modern house",
                lines,
                composition="codex-footer-strip",
                safe_zone="codex-footer-3-5-rows",
            ),
            target="codex",
        )

        self.assertTrue(result["passed"], result)
        self.assertEqual(result["metrics"]["non_empty_rows"], 5)
        self.assertNotIn("subject_not_grounded", result["issues"])
        self.assertNotIn("subject_not_lower", result["issues"])

    def test_accepts_wide_three_row_codex_saturn(self):
        lines = [
            "",
            "",
            "                      _..:,,,,,,,,,,::;--------;:,,,,,,,,,,,:.._",
            "             ~~~--~~-=~' oO0GCLi1tf  8@@@@@8@  tf1iLCG0Oo '~=-~~--~~",
            "                  `--==::,,::::::::::::::::::::,,,,,,,,,,::==--'",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "wide Saturn for footer strip",
                lines,
                composition="codex-footer-strip",
                background_height=5,
                background_width=100,
            ),
            target="codex",
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("saturn_not_recognizable", result["issues"])
        self.assertNotIn("codex_width_underused", result["issues"])

    def test_accepts_two_row_codex_moon_strip(self):
        lines = [
            "        ,,,,,,,,,,:;ii1tfLCG08@@@@@@@@########%@@@@80GCLft1ii;:,,,,,,,,,,",
            "  ~~~~~~-------....__    `-.  oO0#@@@@88@@@@0o  .-'     __....-------~~~~~~",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "low wide moon over fog",
                lines,
                composition="codex-footer-strip",
                background_height=2,
                background_width=90,
            ),
            target="codex",
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("moon_not_recognizable", result["issues"])
        self.assertNotIn("codex_width_underused", result["issues"])

    def test_rejects_narrow_codex_footer_art(self):
        lines = [
            "",
            "",
            "",
            "                              .--.",
            "                             ( oO )",
            "                              '--'",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "small moon",
                lines,
                composition="codex-footer-strip",
                background_height=6,
            ),
            target="codex",
        )

        self.assertFalse(result["passed"])
        self.assertIn("codex_width_underused", result["issues"])

    def test_rejects_codex_art_not_on_last_row(self):
        lines = [
            "",
            "        ~~~~--==  oO08@@0Oo  ==--~~~~",
            "          `--==__________==--'",
            "",
            "",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "footer moon",
                lines,
                composition="codex-footer-strip",
                background_height=5,
                background_width=100,
            ),
            target="codex",
        )

        self.assertFalse(result["passed"])
        self.assertIn("subject_not_lower", result["issues"])

    def test_accepts_one_row_right_side_house(self):
        line = "_.,;:__~~--__,,..░▒" * 6 + "_.,;:__~~--___░░▒▒▓▓▄▄▄▄/\\▄▄/\\▄[##]▐▣▣▌▐██▌▄▓▓▒▒░░"
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "small house on the right with shaded ground",
                [line],
                composition="codex-footer-strip",
                safe_zone="codex-footer-strip",
                style="detailed-ascii-wallpaper",
                rendering_mode="volumetric-shaded-ascii",
                background_height=1,
                background_width=164,
            ),
            target="codex",
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("subject_not_grounded", result["issues"])
        self.assertNotIn("house_not_prominent", result["issues"])
        self.assertNotIn("codex_width_underused", result["issues"])

    def test_rejects_one_row_ground_blob_without_house(self):
        line = "~~--__,,..░▒▓█▓▒░.,,..__--~~" * 5
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "small house on the right",
                [line],
                composition="codex-footer-strip",
                background_height=1,
                background_width=150,
            ),
            target="codex",
        )

        self.assertFalse(result["passed"])
        self.assertIn("house_not_prominent", result["issues"])

    def test_accepts_two_row_house_with_ground_row(self):
        lines = [
            "                          /\\____/\\",
            "   ~~..,,::;;░▒▓______o____|__[##]__|____o______▓▒░;;::,,..~~",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "small house with path",
                lines,
                composition="codex-footer-strip",
                background_height=2,
                background_width=110,
            ),
            target="codex",
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("house_not_prominent", result["issues"])
        self.assertNotIn("subject_not_grounded", result["issues"])

    def test_accepts_one_row_moon_strip(self):
        line = "~~--__,,.._~-.oO0#@@#0Oo.-~_,,..,__--~~"
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "low moon over fog",
                [line],
                composition="codex-footer-strip",
                background_height=1,
                background_width=70,
            ),
            target="codex",
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("moon_not_recognizable", result["issues"])

    def test_accepts_grounded_opencode_house(self):
        lines = [""] * 17 + [
            "                              /\\________/\\",
            "                     ________/..\\..__../88\\________",
            "                    /..::::./____\\/  \\/8888\\.MM::.\\",
            "                   /_______/| [] | __ | [] |\\8888___\\",
            "                   |  [] ::||LCG8||  ||8888||:: []  |",
            "                   |_______||____||__||____||_______|",
            "                ~~~^~~..,,____/          \\____,,..~~^~~~",
        ]
        result = PLOAN_SKILL.analyze_scene_quality(
            scene(
                "single centered modern house",
                lines,
                composition="single-centered-object landscape",
                background_height=24,
            )
        )

        self.assertTrue(result["passed"], result)
        self.assertNotIn("house_not_prominent", result["issues"])
        self.assertNotIn("subject_not_grounded", result["issues"])

    def test_bottom_aligns_short_codex_art(self):
        art = [
            "                         /\\____/\\",
            "              __________/  []   \\__________",
            "             |  []  ##  |  __   |  ##  []  |",
            "             |__________|_|__|__|___________|",
            "        ~~~~~~~..,,____/          \\____,,..~~~~~~~",
        ]
        rendered = PLOAN_SKILL.render_opencode_background(
            scene("cool modern house", art, background_height=20, full_width=True),
            target="codex",
        ).splitlines()

        self.assertEqual(len(rendered), 20)
        self.assertTrue(all(not line.strip() for line in rendered[:15]))
        self.assertEqual([line.rstrip() for line in rendered[-5:]], art)

    def test_accepts_explicit_ascii_typography(self):
        lines = [""] * 14 + [
            "I'M A VIBECODER",
            " __     __ ___ ____  _____",
            " \\ \\   / /|_ _| __ )| ____|",
            "  \\ \\ / /  | ||  _ \\|  _|",
            "   \\ V /   | || |_) | |___",
            "    \\_/   |___|____/|_____|"]
        typography = scene(
            "I'M A VIBECODER",
            lines,
            composition="codex-footer-strip ascii-typography",
            include_text=True,
            no_text=False,
        )

        result = PLOAN_SKILL.analyze_scene_quality(typography, target="codex")
        rendered = PLOAN_SKILL.render_opencode_background(typography, target="codex")

        self.assertTrue(result["passed"], result)
        self.assertNotIn("contains_readable_text", result["issues"])
        self.assertNotIn("PLOAN /", rendered)
        self.assertNotIn("Palette:", rendered)

    def test_sparse_opencode_art_has_no_generated_ambient_pattern(self):
        rendered = PLOAN_SKILL.render_opencode_background(
            scene(
                "small moon",
                ["  .-.  ", " ( o ) ", "  '-'  "],
                background_width=80,
                background_height=20,
                full_width=False,
            ),
            target="opencode",
        )

        self.assertNotIn("·", rendered)
        self.assertNotIn("░", rendered)
        self.assertNotIn("▒", rendered)


if __name__ == "__main__":
    unittest.main()
