import re
import json 
import xml.etree.ElementTree as ET

TTM_NS = 'http://www.w3.org/ns/ttml#metadata'

# this is unironically the best and shortest method for this and im being 20000% serious
#if u were to do every word ending with 'in', you'd have to add exlucions for words like 'again' or 'fin'
#so then, code that detects every 'in' ended word + an exclusion list actually ends up being longer than this. its js a big mess
OMISSION_INCORRECT = {
    "goin": "goin'",
    "runnin": "runnin'",
    "talkin": "talkin'",
    "walkin": "walkin'",
    "comin": "comin'",
    "livin": "livin'",
    "lovin": "lovin'",
    "drillin": "drillin'",
    "cause": "'cause",
    "nothin": "nothin'",
    "somethin": "somethin'",
    "everythin": "everythin'",
    "anythin": "anythin'",
    "gettin": "gettin'",
    "sayin": "sayin'",
    "makin": "makin'",
    "doin": "doin'",
    "tryin": "tryin'",
    "playin": "playin'",
    "feelin": "feelin'",
    "dealin": "dealin'",
    "chillin": "chillin'",
    "ballin": "ballin'",
    "stuntin": "stuntin'",
    "flexin": "flexin'",
    "shinin": "shinin'",
    "grindin": "grindin'",
    "gunnin": "gunnin'",
    "poppin": "poppin'",
    "droppin": "droppin'",
    "shoppin": "shoppin'",
    "cookin": "cookin'",
    "smokin": "smokin'",
    "rollin": "rollin'",
    "creepin": "creepin'",
    "sleepin": "sleepin'",
    "stackin": "stackin'",
    "countin": "countin'",
    "spendin": "spendin'",
    "actin": "actin'",
    "watchin": "watchin'",
    "lookin": "lookin'",
    "thinkin": "thinkin'",
    "knowin": "knowin'",
    "growin": "growin'",
    "showin": "showin'",
    "blowin": "blowin'",
    "throwin": "throwin'",
    "trippin": "trippin'",
    "slippin": "slippin'",
    "clappin": "clappin'",
    "cappin": "cappin'",
    "flippin": "flippin'",
    "trappin": "trappin'",
    "rappin": "rappin'",
    "singin": "singin'",
    "bringin": "bringin'",
    "swingin": "swingin'",
    "slangin": "slangin'",
    "pushin": "pushin'",
    "rushin": "rushin'",
    "crushin": "crushin'",
    "hustlin": "hustlin'",
    "strugglin": "strugglin'",
    "holdin": "holdin'",
    "findin": "findin'",
    "shootin": "shootin'",
    "movin": "movin'",
    "huggin": "huggin'",
    "laughin": "laughin'",
    "wastin": "wastin'",
    "hatin": "hatin'",
    "waitin": "waitin'",
    "hidin": "hidin'",
    "ridin": "ridin'",
    "slidin": "slidin'",
    "vibin": "vibin'",
    "flyin": "flyin'",
    "dyin": "dyin'",
    "cryin": "cryin'",
    "buyin": "buyin'",
    "frontin": "frontin'",
    "fightin": "fightin'",
    "writin": "writin'",
    "bein": "bein'",
    "havin": "havin'",
    "usin": "usin'",
    "losin": "losin'",
    "choosin": "choosin'",
    "cruisin": "cruisin'",
    "jokin": "jokin'",
    "chokin": "chokin'",
    "hopin": "hopin'",
    "copin": "copin'",
    "fadin": "fadin'",
    "shadin": "shadin'",
    "standin": "standin'",
    "demandin": "demandin'",
    "turnin": "turnin'",
    "learnin": "learnin'",
    "earnin": "earnin'",
    "burnin": "burnin'",
    "returnin": "returnin'",
    "workin": "workin'",
    "rockin": "rockin'",
    "knockin": "knockin'",
    "lockin": "lockin'",
    "blockin": "blockin'",
    "fakin": "fakin'",
    "takin": "takin'",
    "breakin": "breakin'",
    "shakin": "shakin'",
    "bakin": "bakin'",
    "facin": "facin'",
    "racin": "racin'",
    "chasin": "chasin'",
    "changin": "changin'",
    "bangin": "bangin'",
    "hangin": "hangin'",
    "backin": "backin'",
    "packin": "packin'",
    "jackin": "jackin'",
    "crackin": "crackin'",
    "trackin": "trackin'",
    "snappin": "snappin'",
    "fore": "'fore",
    "em": "'em",
    "fuckin": "fuckin'",
    "shittin": "shittin'",
    "motherfuckin": "motherfuckin'",
}

TIL_AMERICAN = re.compile(r"'?\btil\b", re.IGNORECASE)
TIL_BRITISH = re.compile(r"'?\btill\b", re.IGNORECASE)

REGIONAL_SPELLING_PAIRS = {
    "color": "colour",
    "colors": "colours",
    "colored": "coloured",
    "coloring": "colouring",
    "favorite": "favourite",
    "favorites": "favourites",
    "behavior": "behaviour",
    "behaviors": "behaviours",
    "behavioral": "behavioural",
    "honor": "honour",
    "honors": "honours",
    "honored": "honoured",
    "honoring": "honouring",
    "neighbor": "neighbour",
    "neighbors": "neighbours",
    "neighborhood": "neighbourhood",
    "mom": "mum",
    "moms": "mums",
    "mommy": "mummy",
    "realize": "realise",
    "realized": "realised",
    "realizes": "realises",
    "realizing": "realising",
    "organize": "organise",
    "organized": "organised",
    "organizing": "organising",
    "apologize": "apologise",
    "apologized": "apologised",
    "recognize": "recognise",
    "recognized": "recognised",
    "theater": "theatre",
    "theaters": "theatres",
    "center": "centre",
    "centers": "centres",
    "centered": "centred",
    "defense": "defence",
    "license": "licence",
    "licensed": "licenced",
    "traveling": "travelling",
    "traveled": "travelled",
    "traveler": "traveller",
    "jewelry": "jewellery",
    "gray": "grey",
    "aluminum": "aluminium",
    "mold": "mould",
    "molded": "moulded",
    "plow": "plough",
    "tire": "tyre",
    "tires": "tyres",
    "pajamas": "pyjamas",
    "curb": "kerb",
    "fiber": "fibre",
    "fibers": "fibres",
    "liter": "litre",
    "liters": "litres",
    "skeptic": "sceptic",
    "skeptical": "sceptical",
    "till": "til'" #brainrot
}

OMISSION_PATTERNS = [
    (re.compile(r'(?<!\')\b' + re.escape(wrong) + r'\b(?!\')', re.IGNORECASE), correct)
    for wrong, correct in OMISSION_INCORRECT.items()
]

REGIONAL_PATTERNS = []
for american, british in REGIONAL_SPELLING_PAIRS.items():
    REGIONAL_PATTERNS.append((re.compile(r'\b' + re.escape(american) + r'\b', re.IGNORECASE), "American", british))
    REGIONAL_PATTERNS.append((re.compile(r'\b' + re.escape(british) + r'\b', re.IGNORECASE), "British/Commonwealth", american))

CURLY_SINGLE = re.compile('[\u2018\u2019]')
CURLY_DOUBLE = re.compile('[\u201c\u201d]')
CENSORED_PATTERN = re.compile(r'\*{2,}')
WOAH_PATTERN = re.compile(r'\bwoah\b', re.IGNORECASE)

CYRILLIC_LOOKALIKES = {
    '\u0430': 'a', '\u0435': 'e', '\u0455': 's', '\u0456': 'i',
    '\u043e': 'o', '\u0440': 'p', '\u0441': 'c', '\u0443': 'y',
    '\u0445': 'x', '\u043a': 'k', '\u043c': 'm', '\u043d': 'h',
    '\u0432': 'b', '\u0442': 't',
}

FULLWIDTH_TO_ASCII = {}
for i in range(0x21, 0x7f):
    FULLWIDTH_TO_ASCII[chr(i + 0xfee0)] = chr(i)
FULLWIDTH_SPACE = '\u3000'

NON_PROPER_CAP_EXCEPTIONS = {'I', "I'm", "I'll", "I'd", "I've", "I'ma", "I'MMA"}

REPEATED_WORDS_PATTERN = re.compile(r'\b(\w+)\b(?:\s+\1\b){2,}', re.IGNORECASE)


def build_text(spans):
    parts = []
    for i, span in enumerate(spans):
        text = span.text or ''
        tail = span.tail or ''
        parts.append(text)
        has_next = i + 1 < len(spans)
        if has_next:
            if tail != '':
                parts.append(' ' if tail.strip() == '' else tail)
    return ''.join(parts).strip()


def process_p(p):
    children = list(p)
    bg_span = None
    regular_spans = []
    for span in children:
        if span.get(f'{{{TTM_NS}}}role', '') == 'x-bg':
            bg_span = span
        else:
            regular_spans.append(span)
    main_text = build_text(regular_spans)
    bg_text = ''
    if bg_span is not None:
        bg_children = list(bg_span)
        if bg_span.text and bg_span.text.strip():
            bg_text = bg_span.text.strip() + ' ' + build_text(bg_children)
        else:
            bg_text = build_text(bg_children)
        bg_text = bg_text.strip()
        bg_text = bg_text.strip('()').strip()  # fucks up grammar checking on bg vocals if this isn't done
    return main_text, bg_text


def extract_lyrics(ttml_path):
    tree = ET.parse(ttml_path)
    root = tree.getroot()
    all_p = root.findall('.//{*}p')
    lines = []
    line_num = 1
    for p in all_p:
        main_text, bg_text = process_p(p)
        if main_text:
            lines.append(f'L{line_num}: {main_text}')
            line_num += 1
            if bg_text:
                lines.append(f'[BG: {bg_text}]')
        elif bg_text:
            lines.append(f'L{line_num}: [BG: {bg_text}]')
            line_num += 1
    return '\n'.join(lines)


def extract_bg_content(line):
    match = re.search(r"\[BG:\s*(.*?)\]", line)
    if match:
        return match.group(1), line.replace(match.group(0), "").strip()
    return None, line


def fmt_issue(line_num, is_bg, message):
    bg_prefix = '[BG] ' if is_bg else ''
    return f"Line {line_num}: {bg_prefix}{message}"


def check_omissions(text, line_num, is_bg):
    errors = []
    for pattern, correct in OMISSION_PATTERNS:
        for match in pattern.finditer(text):
            matched_word = match.group()
            if correct.startswith("'"):
                corrected = "'" + matched_word
            else:
                corrected = matched_word + "'"
            errors.append(fmt_issue(line_num, is_bg, f"ERROR! Missing/incorrect apostrophe/omission. ('{matched_word}' should be '{corrected}')"))
    return errors


def check_til_variant(text, line_num, is_bg):
    regional = []
    for match in TIL_AMERICAN.finditer(text):
        regional.append(fmt_issue(line_num, is_bg, f'"{match.group()}" is American spelling of "till"'))
    for match in TIL_BRITISH.finditer(text):
        regional.append(fmt_issue(line_num, is_bg, f'"{match.group()}" is British/Commonwealth spelling of "\'til"'))
    return regional


def check_regional_spelling(text, line_num, is_bg):
    regional = []
    for pattern, region_label, alt in REGIONAL_PATTERNS:
        for match in pattern.finditer(text):
            word = match.group()
            regional.append(fmt_issue(line_num, is_bg, f'"{word}" is {region_label} spelling of "{alt}"'))
    return regional


def check_curly_quotes(text, line_num, is_bg):
    errors = []
    if CURLY_SINGLE.search(text):
        errors.append(fmt_issue(line_num, is_bg, "ERROR! Contains curly single quotes (' and '); use straight quotes (')"))
    if CURLY_DOUBLE.search(text):
        errors.append(fmt_issue(line_num, is_bg, 'ERROR! Contains curly double quotes (" and "); use straight quotes (")'))
    return errors


def check_censored(text, line_num, is_bg):
    errors = []
    if CENSORED_PATTERN.search(text):
        errors.append(fmt_issue(line_num, is_bg, "WARNING! Contains censored/asterisked text; replace with actual words if possible"))
    return errors


def check_woah(text, line_num, is_bg):
    regional = []
    for match in WOAH_PATTERN.finditer(text):
        regional.append(fmt_issue(line_num, is_bg, f'"{match.group()}" should be "whoa"'))
    return regional


def check_cyrillic_lookalikes(text, line_num, is_bg):
    errors = []
    for cyrillic_char, latin_char in CYRILLIC_LOOKALIKES.items():
        if cyrillic_char in text:
            idx = text.index(cyrillic_char)
            context = text[max(0, idx - 5):idx + 6]
            errors.append(fmt_issue(line_num, is_bg, f'ERROR! Cyrillic character "{cyrillic_char}" (looks like Latin "{latin_char}") found: "...{context}..."'))
    return errors


def check_fullwidth(text, line_num, is_bg):
    errors = []
    if FULLWIDTH_SPACE in text:
        errors.append(fmt_issue(line_num, is_bg, "ERROR! Contains fullwidth ideographic space; use normal ASCII space"))
    for ch in text:
        if ch in FULLWIDTH_TO_ASCII:
            ascii_version = FULLWIDTH_TO_ASCII[ch]
            errors.append(fmt_issue(line_num, is_bg, f'ERROR! Fullwidth character "{ch}" should be ASCII "{ascii_version}"'))
            break
    return errors


def check_mid_sentence_caps(text, line_num, is_bg):
    errors = []
    tokens = text.split()
    if len(tokens) < 2:
        return errors
    for i in range(1, len(tokens)):
        token = tokens[i]
        if re.match(r'^[A-Z][a-z]', token) and token not in NON_PROPER_CAP_EXCEPTIONS:
            errors.append(fmt_issue(line_num, is_bg, f'WARNING! Unexpected capital mid-sentence: "{token}"'))
            break
    return errors


def check_repeated_words(text, line_num, is_bg):
    errors = []
    for match in REPEATED_WORDS_PATTERN.finditer(text):
        word = match.group(1)
        matched_text = match.group()
        tokens = matched_text.split()
        count = sum(1 for t in tokens if t.lower() == word.lower())
        errors.append(fmt_issue(line_num, is_bg, f'WARNING! Word "{word}" repeated {count} times; should be hyphenated like "{word}-{word}-{word}"'))
    return errors


def check_single_string(text, line_num, is_bg):
    errors = []
    regional = []
    stripped = text.strip()
    if not stripped:
        return errors, regional

    first_char = stripped[0]
    if first_char.isalpha() and not first_char.isupper():
        tokens = stripped.split()
        word = tokens[0] if tokens else ''
        errors.append(fmt_issue(line_num, is_bg, f'ERROR! Starting letter is not capitalized. (line starting with "{word}")'))

    if stripped.endswith(','):
        tokens = stripped.split()
        last = tokens[-1] if tokens else ''
        errors.append(fmt_issue(line_num, is_bg, f'ERROR! Line ends with a comma. (line ending with "{last}")'))
    if stripped.endswith('.'):
        tokens = stripped.split()
        last = tokens[-1] if tokens else ''
        errors.append(fmt_issue(line_num, is_bg, f'ERROR! Line ends with a full stop. (line ending with "{last}")'))

    digits = re.findall(r'\d+', stripped)
    if digits:
        errors.append(fmt_issue(line_num, is_bg, f'WARNING! Contains numbers. Check if it should be words or not depending on context/usage (line with "{", ".join(digits)}")'))

    errors.extend(check_omissions(stripped, line_num, is_bg))
    regional.extend(check_til_variant(stripped, line_num, is_bg))
    regional.extend(check_regional_spelling(stripped, line_num, is_bg))

    errors.extend(check_curly_quotes(stripped, line_num, is_bg))
    errors.extend(check_censored(stripped, line_num, is_bg))
    regional.extend(check_woah(stripped, line_num, is_bg))
    errors.extend(check_cyrillic_lookalikes(stripped, line_num, is_bg))
    errors.extend(check_fullwidth(stripped, line_num, is_bg))
    errors.extend(check_mid_sentence_caps(stripped, line_num, is_bg))
    errors.extend(check_repeated_words(stripped, line_num, is_bg))

    if stripped.endswith('-') and not stripped.endswith('—'):
        tokens = stripped.split()
        last = tokens[-1] if tokens else ''
        errors.append(fmt_issue(line_num, is_bg, f'ERROR! Line ends with hyphen; use em dash (—) for cut-off words. (line ending with "{last}")'))

    # this sometimes doesn't work/matter if a quote stretches beyond one line
    if stripped.count('"') % 2 != 0:
        quote_idx = stripped.find('"')
        snippet_match = re.match(r'\S+', stripped[quote_idx:]) if quote_idx != -1 else None
        snippet = snippet_match.group() if snippet_match else '"'
        errors.append(fmt_issue(line_num, is_bg, f'WARNING! Unbalanced double quotes. (line starting with "{snippet}")'))

    return errors, regional


def check_line(raw_line, line_num, is_bg):
    errors = []
    regional = []

    match = re.match(r"^L\d+:\s*", raw_line)
    content = raw_line[match.end():] if match else raw_line

    bg_content, non_bg_part = extract_bg_content(content)
    if bg_content is not None:
        e, r = check_single_string(bg_content, line_num, is_bg=True)
        errors.extend(e)
        regional.extend(r)
        if non_bg_part and non_bg_part.strip():
            e2, r2 = check_single_string(non_bg_part, line_num, is_bg=False)
            errors.extend(e2)
            regional.extend(r2)
    else:
        e, r = check_single_string(content, line_num, is_bg)
        errors.extend(e)
        regional.extend(r)
    return errors, regional


# feels the aura
def process_lyrics_text(text):
    all_errors = []
    all_regional = []
    for idx, line in enumerate(text.splitlines(), start=1):
        e, r = check_line(line, idx, is_bg=False)
        all_errors.extend(e)
        all_regional.extend(r)
    return all_errors, all_regional