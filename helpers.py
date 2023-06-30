import requests
from config import DICT_API_KEY, THES_API_KEY
import datetime
import json
import wikipedia
import sqlite3
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_definition(word):
    """Accesses the Marriam webster API to get the definition of a word"""
    base_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    api_key = "?key=" + DICT_API_KEY
	
    print(api_key)
    
    full_api_url = base_url + word + api_key

    try:
        response = requests.get(full_api_url)
        data = json.loads(response.content.decode('utf-8'))[0]
        print(data)
        #Dig through the JSON response to find relevant info
        definition = data['shortdef'][0]
        #Remove text modifiers from raw sentence string
        #print(definition)
        return definition
    except Exception as e:
        print(e)
        return -1

def get_synonyms(word):
    """Accesses the Marriam webster API to get the synonyms of a word"""
    base_url = "https://dictionaryapi.com/api/v3/references/thesaurus/json/"
    api_key = "?key=" + THES_API_KEY
	
    print(api_key)
    
    full_api_url = base_url + word + api_key

    try:
        response = requests.get(full_api_url)
        data = json.loads(response.content.decode('utf-8'))[0]
        #print(data)
        #Dig through the JSON response to find relevant info
        synonyms = data["meta"]["syns"][0] # fix this
        #Remove text modifiers from raw sentence string
        print(synonyms)
        return synonyms
    except Exception as e:
        print(e)
        return -1

def get_info(wikipedia_arg):
    """Uses the wikipedia module to return a summary of the topic"""
    wikipedia_summary = wikipedia.summary(wikipedia_arg, sentences=5, auto_suggest=True, redirect=True)
    return wikipedia_summary

def get_pos_word(pos_acronym):
    """Gets the Part of Speech of a word"""
    return POS_DICTIONARY[pos_acronym]

LANGUAGE_CODES = {
    "afar": "aa",
    "abkhazian": "ab",
    "afrikaans": "af",
    "akan": "ak",
    "amharic": "am",
    "arabic": "ar",
    "aragonese": "an",
    "assamese": "as",
    "avaric": "av",
    "avestan": "ae",
    "aymara": "ay",
    "azerbaijani": "az",
    "bashkir": "ba",
    "bambara": "bm",
    "belarusian": "be",
    "bengali": "bn",
    "bihari": "bh",
    "bislama": "bi",
    "tibetan": "bo",
    "bosnian": "bs",
    "breton": "br",
    "bulgarian": "bg",
    "catalan": "ca",
    "czech": "cs",
    "chamorro": "ch",
    "chechen": "ce",
    "church slavic": "cu",
    "chuvash": "cv",
    "cornish": "kw",
    "corsican": "co",
    "cree": "cr",
    "welsh": "cy",
    "danish": "da",
    "german": "de",
    "divehi": "dv",
    "dzongkha": "dz",
    "greek": "el",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "basque": "eu",
    "ewe": "ee",
    "faroese": "fo",
    "persian": "fa",
    "fijian": "fj",
    "finnish": "fi",
    "french": "fr",
    "western frisian": "fy",
    "fulah": "ff",
    "scottish gaelic": "gd",
    "irish": "ga",
    "galician": "gl",
    "manx": "gv",
    "guaraní": "gn",
    "gujarati": "gu",
    "haitian": "ht",
    "hausa": "ha",
    "serbo-croatian": "sh",
    "herero": "hz",
    "hindi": "hi",
    "hiri motu": "ho",
    "croatian": "hr",
    "hungarian": "hu",
    "igbo": "ig",
    "icelandic": "is",
    "ido": "io",
    "nuosu": "ii",
    "inuktitut": "iu",
    "interlingue": "ie",
    "interlingua": "ia",
    "indonesian": "id",
    "inupiaq": "ik",
    "italian": "it",
    "javanese": "jv",
    "japanese": "ja",
    "kalaallisut": "kl",
    "kannada": "kn",
    "kashmiri": "ks",
    "kanuri": "kr",
    "kazakh": "kk",
    "khmer": "km",
    "kikuyu": "ki",
    "kinyarwanda": "rw",
    "kirghiz": "ky",
    "komi": "kv",
    "kongo": "kg",
    "korean": "ko",
    "kwanyama": "kj",
    "kurdish": "ku",
    "lao": "lo",
    "latin": "la",
    "latvian": "lv",
    "limburgish": "li",
    "lingala": "ln",
    "lithuanian": "lt",
    "luxembourgish": "lb",
    "luba-katanga": "lu",
    "ganda": "lg",
    "marshallese": "mh",
    "malayalam": "ml",
    "marathi": "mr",
    "macedonian": "mk",
    "malagasy": "mg",
    "maltese": "mt",
    "mongolian": "mn",
    "maori": "mi",
    "malay": "ms",
    "burmese": "my",
    "nauru": "na",
    "navajo": "nv",
    "southern ndebele": "nr",
    "northern ndebele": "nd",
    "ndonga": "ng",
    "nepali": "ne",
    "dutch": "nl",
    "norwegian nynorsk": "nn",
    "norwegian bokmål": "nb",
    "norwegian": "no",
    "chichewa": "ny",
    "occitan": "oc",
    "ojibwa": "oj",
    "oriya": "or",
    "oromo": "om",
    "ossetian": "os",
    "panjabi": "pa",
    "pashto": "ps",
    "pāli": "pi",
    "polish": "pl",
    "portuguese": "pt",
    "quechua": "qu",
    "romansh": "rm",
    "romanian": "ro",
    "kirundi": "rn",
    "russian": "ru",
    "sango": "sg",
    "sanskrit": "sa",
    "sinhala": "si",
    "slovak": "sk",
    "slovene": "sl",
    "northern sami": "se",
    "samoan": "sm",
    "shona": "sn",
    "sindhi": "sd",
    "somali": "so",
    "southern sotho": "st",
    "spanish": "es",
    "albanian": "sq",
    "sardinian": "sc",
    "serbian": "sr",
    "swati": "ss",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tahitian": "ty",
    "tamil": "ta",
    "tatar": "tt",
    "telugu": "te",
    "tajik": "tg",
    "tagalog": "tl",
    "thai": "th",
    "tigrinya": "ti",
    "tonga": "to",
    "tswana": "tn",
    "tsonga": "ts",
    "turkmen": "tk",
    "turkish": "tr",
    "twi": "tw",
    "uighur": "ug",
    "ukrainian": "uk",
    "urdu": "ur",
    "uzbek": "uz",
    "venda": "ve",
    "vietnamese": "vi",
    "volapük": "vo",
    "walloon": "wa",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zhuang": "za",
    "zulu": "zu"
}


POS_DICTIONARY = {
    'CC': 'Coordinating conjunction',
    'CD': 'Cardinal number',
    'DT': 'Determiner',
    'EX': 'Existential there',
    'FW': 'Foreign word',
    'IN': 'Preposition or subordinating conjunction',
    'JJ': 'Adjective',
    'JJR': 'Adjective, comparative',
    'JJS': 'Adjective, superlative',
    'LS': 'List item marker',
    'MD': 'Modal',
    'NN': 'Noun, singular or mass',
    'NNS': 'Noun, plural',
    'NNP': 'Proper noun, singular',
    'NNPS': 'Proper noun, plural',
    'PDT': 'Predeterminer',
    'POS': 'Possessive ending',
    'PRP': 'Personal pronoun',
    'PRP$': 'Possessive pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb, comparative',
    'RBS': 'Adverb, superlative',
    'RP': 'Particle',
    'SYM': 'Symbol',
    'TO': 'to',
    'UH': 'Interjection',
    'VB': 'Verb, base form',
    'VBD': 'Verb, past tense',
    'VBG': 'Verb, gerund or present participle',
    'VBN': 'Verb, past participle',
    'VBP': 'Verb, non-3rd person singular present',
    'VBZ': 'Verb, 3rd person singular present',
    'WDT': 'Wh-determiner',
    'WP': 'Wh-pronoun',
    'WP$': 'Possessive wh-pronoun',
    'WRB': 'Wh-adverb'
}
