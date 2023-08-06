from collections import OrderedDict
from functools import reduce

import numpy as np
from ecl.eclfile import EclInitFile, EclKW
from ecl.grid import EclGrid
from ecl.summary import EclSum
from ecl.well import WellInfo
from ecl2df import EclFiles

from preprocessing.deck.section import get_includes

SMSPEC_WELL_KEYWORDS = {
    "WOPR",
    "WOPRH",
    "WWPR",
    "WWPRH",
    "WGPR",
    "WWIR",
    "WBHP",
    "WBHPH",
    "WTHP",
    "WGPRH",
    "WTHPH",
    "WWIRH",
}
SMSPEC_FIELD_KEYWORDS = ["FOPR", "FWPR", "FGPR", "FOPRH", "FWPRH", "FGPRH"]


def preprocess(
    data_file_loc,
    egrid_file_loc=None,
    smspec_file_loc=None,
    init_file_loc=None,
    restart_file_loc=None,
    download_func=None,
    allow_missing_files=tuple(),
    base_dir=None,
):
    get_includes(data_file_loc, download_func, allow_missing_files=allow_missing_files, base_dir=base_dir)

    if smspec_file_loc:
        smry = EclSum(str(smspec_file_loc))
        wnames = OrderedDict((wname, {"injector": None, "type": None}) for wname in smry.wells())

        if egrid_file_loc and restart_file_loc:
            grid = EclGrid(str(egrid_file_loc))
            winfo = WellInfo(grid, str(restart_file_loc))

            for wname, wprops in wnames.items():
                if wname in winfo:
                    wtimeline = winfo[wname]
                    wstate = wtimeline and next(iter(wtimeline), None)
                    if wstate:
                        wprops["type"] = str(wstate.wellType().name)
                        wprops["injector"] = "INJECTOR" in wprops["type"].upper()

        available_keywords_by_well = reduce(
            lambda d, p: d.setdefault(p[0], set()).add(p[1]) or d,
            (
                (p[1], p[0])
                for p in (x.split(":") for x in list(smry))
                if len(p) == 2 and p[1] in wnames and p[0] in SMSPEC_WELL_KEYWORDS
            ),
            {},
        )

        extractor_keywords = sorted(
            reduce(
                lambda p, n: p.intersection(n),
                (k for w, k in available_keywords_by_well.items() if wnames[w]["injector"] is False),
                SMSPEC_WELL_KEYWORDS,
            )
        )

        injector_keywords = sorted(
            reduce(
                lambda p, n: p.intersection(n),
                (k for w, k in available_keywords_by_well.items() if wnames[w]["injector"] is True),
                SMSPEC_WELL_KEYWORDS,
            )
        )

        # Discover implicit liquid keywords (_L__..) as a combination of oil and water [(_W__..) and (_O__..)]
        for keyword_set in (extractor_keywords, injector_keywords):
            liquid_keyword_candidates = set(f"{x[0]}_{x[2:]}" for x in extractor_keywords if x[1] in ("W", "O"))
            for liquid_keyword_candidate in liquid_keyword_candidates:
                include_liquid_keyword = (
                    liquid_keyword_candidate.replace("_", "O") in keyword_set
                    and liquid_keyword_candidate.replace("_", "W") in keyword_set
                )
                if include_liquid_keyword:
                    keyword_set.append(liquid_keyword_candidate.replace("_", "L"))

        field_keywords = set(SMSPEC_FIELD_KEYWORDS).intersection(list(smry))

    else:
        wnames = {}
        extractor_keywords = []
        injector_keywords = []
        field_keywords = []

    if data_file_loc:
        data = EclFiles(data_file_loc)
        ecldeck = data.get_ecldeck()
        data_keywords = sorted(set(x.name for x in ecldeck))
    else:
        data_keywords = []

    if egrid_file_loc and init_file_loc:
        grid = EclGrid(str(egrid_file_loc))
        init = EclInitFile(grid, str(init_file_loc))
        init_keywords = sorted(set(x.name for x in init if isinstance(x, EclKW)))
    else:
        init_keywords = []

    return {
        "phases": preprocess_phases(ecldeck),
        "start": preprocess_start(ecldeck),
        "endscale": find_keyword(ecldeck, "ENDSCALE"),
        "multout": find_keyword(ecldeck, "MULTOUT"),
        "dimens": preprocess_dimens(ecldeck),
        "wnames": wnames,
        "wkeywords": {"injector": injector_keywords, "extractor": extractor_keywords},
        "fkeywords": sorted(field_keywords),
        "data_keywords": data_keywords,
        "init_keywords": init_keywords,
    }


def preprocess_start(ecldeck):
    from datetime import datetime

    try:
        start = str(ecldeck["START"][0]).strip(" \n/")
        return datetime.strptime(start, "%d '%b' %Y")
    except Exception:
        return False


def preprocess_phases(ecldeck):
    return {
        "gas": find_keyword(ecldeck, "GAS"),
        "oil": find_keyword(ecldeck, "OIL"),
        "water": find_keyword(ecldeck, "WATER"),
    }


def preprocess_dimens(ecldeck):
    dimens = ecldeck["DIMENS"][0]
    return np.array([dimens[0].value, dimens[1].value, dimens[2].value])


def find_keyword(ecldeck, keyword):
    return hasattr(ecldeck, "__contains__") and keyword in ecldeck
