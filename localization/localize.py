import gettext
import os
from typing import Callable

dirname = os.path.dirname(__file__)
localedir = os.path.join(dirname, "locales")


def get_equivalent_locale(locale: str) -> str:
    if "zh" in locale and "Hans" not in locale and ("Hant" in locale or "TW" in locale):
        return "zh-Hant"
    if "zh" in locale:
        return "zh-Hans"
    return locale


def use_localize(locale: str) -> Callable[[str], str]:
    languages = ["en"] if locale is None else [get_equivalent_locale(locale), "en"]
    translation = gettext.translation("base", localedir=localedir, languages=languages)
    return translation.gettext
