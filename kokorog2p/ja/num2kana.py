"""Japanese Number to Kana Converter.

COPIED from https://github.com/Greatdane/Convert-Numbers-to-Japanese/blob/master/Convert-Numbers-to-Japanese.py
Original License: MIT
"""

ROMAJI_DICT = {
    ".": "ten",
    "0": "zero",
    "1": "ichi",
    "2": "ni",
    "3": "san",
    "4": "yon",
    "5": "go",
    "6": "roku",
    "7": "nana",
    "8": "hachi",
    "9": "kyuu",
    "10": "juu",
    "100": "hyaku",
    "1000": "sen",
    "10000": "man",
    "100000000": "oku",
    "300": "sanbyaku",
    "600": "roppyaku",
    "800": "happyaku",
    "3000": "sanzen",
    "8000": "hassen",
    "01000": "issen",
}

KANJI_DICT = {
    ".": "点",
    "0": "零",
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
    "10": "十",
    "100": "百",
    "1000": "千",
    "10000": "万",
    "100000000": "億",
    "300": "三百",
    "600": "六百",
    "800": "八百",
    "3000": "三千",
    "8000": "八千",
    "01000": "一千",
}

HIRAGANA_DICT = {
    ".": "てん",
    "0": "ゼロ",
    "1": "いち",
    "2": "に",
    "3": "さん",
    "4": "よん",
    "5": "ご",
    "6": "ろく",
    "7": "なな",
    "8": "はち",
    "9": "きゅう",
    "10": "じゅう",
    "100": "ひゃく",
    "1000": "せん",
    "10000": "まん",
    "100000000": "おく",
    "300": "さんびゃく",
    "600": "ろっぴゃく",
    "800": "はっぴゃく",
    "3000": "さんぜん",
    "8000": "はっせん",
    "01000": "いっせん",
}

KEY_DICT = {"kanji": KANJI_DICT, "hiragana": HIRAGANA_DICT, "romaji": ROMAJI_DICT}


def len_one(convert_num: str, requested_dict: dict) -> str:
    return requested_dict[convert_num]


def len_two(convert_num: str, requested_dict: dict) -> str:
    if convert_num[0] == "0":
        return len_one(convert_num[1], requested_dict)
    if convert_num == "10":
        return requested_dict["10"]
    if convert_num[0] == "1":
        return requested_dict["10"] + " " + len_one(convert_num[1], requested_dict)
    elif convert_num[1] == "0":
        return len_one(convert_num[0], requested_dict) + " " + requested_dict["10"]
    else:
        num_list = [
            requested_dict[convert_num[0]],
            requested_dict["10"],
            requested_dict[convert_num[1]],
        ]
        return " ".join(num_list)


def len_three(convert_num: str, requested_dict: dict) -> str:
    num_list = []
    if convert_num[0] == "1":
        num_list.append(requested_dict["100"])
    elif convert_num[0] == "3":
        num_list.append(requested_dict["300"])
    elif convert_num[0] == "6":
        num_list.append(requested_dict["600"])
    elif convert_num[0] == "8":
        num_list.append(requested_dict["800"])
    else:
        num_list.append(requested_dict[convert_num[0]])
        num_list.append(requested_dict["100"])
    if convert_num[1:] == "00" and len(convert_num) == 3:
        pass
    else:
        if convert_num[1] == "0":
            num_list.append(requested_dict[convert_num[2]])
        else:
            num_list.append(len_two(convert_num[1:], requested_dict))
    return " ".join(num_list)


def len_four(convert_num: str, requested_dict: dict, stand_alone: bool) -> str:
    num_list = []
    if convert_num == "0000":
        return ""
    while convert_num[0] == "0":
        convert_num = convert_num[1:]
    if len(convert_num) == 1:
        return len_one(convert_num, requested_dict)
    elif len(convert_num) == 2:
        return len_two(convert_num, requested_dict)
    elif len(convert_num) == 3:
        return len_three(convert_num, requested_dict)
    else:
        if convert_num[0] == "1" and stand_alone:
            num_list.append(requested_dict["1000"])
        elif convert_num[0] == "1":
            num_list.append(requested_dict["01000"])
        elif convert_num[0] == "3":
            num_list.append(requested_dict["3000"])
        elif convert_num[0] == "8":
            num_list.append(requested_dict["8000"])
        else:
            num_list.append(requested_dict[convert_num[0]])
            num_list.append(requested_dict["1000"])
        if convert_num[1:] == "000" and len(convert_num) == 4:
            pass
        else:
            if convert_num[1] == "0":
                num_list.append(len_two(convert_num[2:], requested_dict))
            else:
                num_list.append(len_three(convert_num[1:], requested_dict))
        return " ".join(num_list)


def len_x(convert_num: str, requested_dict: dict) -> str:
    num_list = []
    if len(convert_num[0:-4]) == 1:
        num_list.append(requested_dict[convert_num[0:-4]])
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 2:
        num_list.append(len_two(convert_num[0:2], requested_dict))
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 3:
        num_list.append(len_three(convert_num[0:3], requested_dict))
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 4:
        num_list.append(len_four(convert_num[0:4], requested_dict, False))
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 5:
        num_list.append(requested_dict[convert_num[0]])
        num_list.append(requested_dict["100000000"])
        num_list.append(len_four(convert_num[1:5], requested_dict, False))
        if convert_num[1:5] != "0000":
            num_list.append(requested_dict["10000"])
    else:
        raise ValueError("Not yet implemented, please choose a lower number.")
    num_list.append(len_four(convert_num[-4:], requested_dict, False))
    return " ".join(num_list)


def remove_spaces(convert_result: str) -> str:
    return "".join(c for c in convert_result if c != " ")


def do_convert(convert_num: str, requested_dict: dict) -> str:
    if len(convert_num) == 1:
        return len_one(convert_num, requested_dict)
    elif len(convert_num) == 2:
        return len_two(convert_num, requested_dict)
    elif len(convert_num) == 3:
        return len_three(convert_num, requested_dict)
    elif len(convert_num) == 4:
        return len_four(convert_num, requested_dict, True)
    else:
        return len_x(convert_num, requested_dict)


def split_point(split_num: str, dict_choice: str) -> str:
    parts = split_num.split(".")
    split_num_a = parts[0]
    split_num_b = parts[1]
    split_num_b_end = " "
    for x in split_num_b:
        split_num_b_end += len_one(x, KEY_DICT[dict_choice]) + " "
    if split_num_a[-1] == "0" and split_num_a[-2] != "0" and dict_choice == "hiragana":
        small_tsu = Convert(split_num_a, dict_choice)
        small_tsu = small_tsu[0:-1] + "っ"
        return small_tsu + KEY_DICT[dict_choice]["."] + split_num_b_end
    if split_num_a[-1] == "0" and split_num_a[-2] != "0" and dict_choice == "romaji":
        small_tsu = Convert(split_num_a, dict_choice)
        small_tsu = small_tsu[0:-1] + "t"
        return small_tsu + KEY_DICT[dict_choice]["."] + split_num_b_end
    return (
        Convert(split_num_a, dict_choice)
        + " "
        + KEY_DICT[dict_choice]["."]
        + split_num_b_end
    )


def Convert(convert_num: str, dict_choice: str = "hiragana"):
    """Convert a number to Japanese representation.

    Args:
        convert_num: Number to convert (as string).
        dict_choice: Output format ("kanji", "hiragana", or "romaji").

    Returns:
        Japanese representation of the number.
    """
    convert_num = str(convert_num).replace(",", "")
    dict_choice = dict_choice.lower()

    if dict_choice == "all":
        return [Convert(convert_num, x) for x in ("kanji", "hiragana", "romaji")]

    dictionary = KEY_DICT[dict_choice]

    if len(convert_num) > 9:
        return "Number length too long, choose less than 10 digits"

    # Remove any leading zeroes
    while convert_num[0] == "0" and len(convert_num) > 1:
        convert_num = convert_num[1:]

    # Check for decimal places
    if "." in convert_num:
        result = split_point(convert_num, dict_choice)
    else:
        result = do_convert(convert_num, dictionary)

    # Remove spaces for non-romaji output
    if KEY_DICT[dict_choice] != ROMAJI_DICT:
        result = remove_spaces(result)

    return result
