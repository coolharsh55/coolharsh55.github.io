"""markdown extensions for harshp_com

    - uses markdown library standard extensions
    - provides strings in easy to use namespace"""

ABBREVIATION = 'markdown.extensions.abbr'
FENCED_CODE = 'markdown.extensions.fenced_code'
FOOTNOTES = 'markdown.extensions.footnotes'
NEWLINE = 'markdown.extensions.nl2br'
CODEHILITE = 'markdown.extensions.codehilite'
LISTS = 'markdown.extensions.sane_lists'
SMARTYPANTS = 'markdown.extensions.smarty'
TOC = 'markdown.extensions.toc'

ext_formatting = [ABBREVIATION, FOOTNOTES, NEWLINE, LISTS, TOC]
ext_code = [FENCED_CODE, CODEHILITE]
ext_all = [
    ABBREVIATION, FOOTNOTES, NEWLINE, LISTS, TOC,
    FENCED_CODE, CODEHILITE]
ext_all_without_newline = [
    ABBREVIATION, FOOTNOTES, LISTS, TOC,
    FENCED_CODE, CODEHILITE]
