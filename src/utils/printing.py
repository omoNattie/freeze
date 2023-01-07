from src.utils.color import ColorCodes


def freeze_panic(message: str, wants_colors: bool) -> None:
    if wants_colors:
        print(f"{ColorCodes.RED}:: {message}{ColorCodes.END}")
    else:
        print(message)


def freeze_question(message: str) -> str:
    return f":: {message} [Y/n] "


def freeze_aur(name: str, ids: int, out_of_date: bool) -> str:
    if out_of_date:
        return f"{ColorCodes.RED}aur/{ColorCodes.END}{ColorCodes.GREEN}{name}{ColorCodes.END} {ids} " \
               f"- {ColorCodes.MAGENT}package out of date.{ColorCodes.END}"
    else:
        return f"{ColorCodes.RED}aur/{ColorCodes.END}{ColorCodes.GREEN}{name}{ColorCodes.END} {ids}"


def freeze_info(message: str, wants_colors: bool) -> None:
    if wants_colors:
        print(f"{ColorCodes.BLUE}:: {message} ..{ColorCodes.END} ")
    else:
        print(message)
