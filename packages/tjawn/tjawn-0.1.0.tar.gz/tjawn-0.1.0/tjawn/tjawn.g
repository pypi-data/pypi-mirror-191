?start: value | file

?value: "null"i         -> null
    | "true"i           -> true
    | "false"i          -> false
    | number
    | string
    | cname
    | text
    | list
    | set
    | dict

file: _dict_inner

list: "[" [value (_SEP? value)*] _SEP? "]"
set: "{" value (_SEP? value)* _SEP? "}" | "{" "_" _SEP? "}"

_dict_inner: [pair (_SEP? pair)*] _SEP?
dict: "{" _dict_inner "}"

pair: key ":" value
key: STRING | CNAME

_STRING_INNER: /(.|\n)*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\)(\\\\)*?/
TEXT: /\"\"\"/ _STRING_ESC_INNER /\"\"\"/
text: TEXT

STRING: /\"/ _STRING_ESC_INNER /\"/
string: STRING

cname: CNAME

number: SIGNED_NUMBER

_SEP: "," | _EOLN

_EOLN: /\n/

%import common.SIGNED_NUMBER
%import common.CNAME

%import common.WS
%ignore WS
