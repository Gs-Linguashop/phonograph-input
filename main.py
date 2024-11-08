import subprocess
import sys
from fontTools import ttLib
import copy
import chinese_converter as cvt # used only for morphs

def read_dict(file_name,delim=None):
    d = dict()
    with open(file_name,'r',encoding='utf8') as f: lines = f.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        if delim is None: d[line[0]] = line.split('\t')[0][1:] # [key][val][val]...\t[comment]
        else: # [key][key]#[commented key]...[delim][val][val]...\t[comment]
            for key in line.split(delim)[0].split('#')[0]:
                d[key] = line.split(delim)[1].split('\t')[0]
    return d # {'key':'val'+'val'+..., 'another key':'...', ...}

def mod_dict_keys(d,key_dict):
    for key_from,key_to in key_dict.items():
        chars_in_key_from = d.pop(key_from)
        d.setdefault(key_to,[]).extend(chars_in_key_from)
    return True

def read_morphs(file_name,pre_assigned_dict): # traditional morphs
    morph_dict = dict()
    with open(file_name,'r',encoding='utf8') as f: lines = f.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        morph, chars = line.split('\t')[0], [*line.split('\t')[1]]
        morph_dict[morph] = chars
        for char in chars.copy():
            if char in pre_assigned_dict: chars.remove(char)
        if len(morph_dict[morph]) == 0: morph_dict.pop(morph)
    for char, morph in pre_assigned_dict.items():
        morph_dict.setdefault(morph,[]).append(char)
    return morph_dict

# invert morph_dict to morph_map 
def morph_dict_to_map(morph_dict):
    morph_map = dict()
    for morph, chars in morph_dict.items():
        for char in chars:
            morph_map[char] = morph
    return morph_map

# Main
# 1. read chars with assigned morphs
# 2. read morphs and then modify with pre-assigned chars
# 3. replace unwanted morphs then merge secondary morphs
# 4. modify the font file and sub with desired displayed form
# 5. save font and delete excessive glyphs

file_in_dir = 'luna_pinyin.dict.yaml'
file_header_dir = 'luna_pinyin_header.dict.yaml'
file_out_dir = 'luna_phonograph_pinyin.dict.yaml'
src_dir = 'src/'
file_essay_dir = src_dir + 'essay.txt'
line_number_content_starts = 36 - 1

pre_assigned_dict = read_dict(src_dir + 'exception_chars.txt')
morph_dict = read_morphs(src_dir + 'phonographeme_dict.txt',pre_assigned_dict)
morph_sub_dict = read_dict(src_dir + 'display_mod.txt',delim='\t')
morph_map = morph_dict_to_map(morph_dict)

essay_dict = dict() # [essay entry] : freq 
with open(file_essay_dir,'r',encoding='utf8') as f: 
    for line in f.read().splitlines(): 
        if line == '' or line[0] == '#': continue
        essay_dict[line.split('\t')[0]] = int(line.split('\t')[1])

def modify_dictionary_entry(line, essay_dict, processed_entry_dict, freq_floor = 0):
    line_split = line.split('\t')
    if len(line_split) <= 1: return line, -1 # no freq info 
    word = line_split[0]
    word_and_spelling = line_split[0] + '\t' + line_split[1]
    freq = essay_dict.get(word,0)
    if len(line_split) >= 3:
        if '%' in line_split[2]:
            freq = int(freq * float(line_split[2].split('%')[0])/ 100)
        else: 
            freq = int(line_split[2])
    freq = max(freq, freq_floor, processed_entry_dict.get(word_and_spelling,0))
    return word_and_spelling, freq

# read char spellings 
char_entry_dict = dict() # [char]: list([spelling])
with open(file_in_dir,'r',encoding='utf8') as f: 
    for line in f.read().splitlines()[line_number_content_starts:]: 
        if line == '' or line[0] == '#': continue
        line_split = line.split('\t')
        word = line_split[0]
        if len(line_split) <= 1 or len(word) != 1: continue
        if len(line_split) >= 3:
            if '%' in line_split[2]:
                if float(line_split[2].split('%')[0]) < 5: continue
        spelling = line_split[1]
        char_entry_dict.setdefault(word,[]).append(spelling)

def append_spellings(line, char_entry_dict):
    if '\t' in line: return [line] # spelling already exists 
    line_split = line.split('\t')
    spellings = [line + '\t']
    for char in line:
        update_spellings = []
        for char_spelling in char_entry_dict.get(char,[]):
            for spelling in spellings:
                if spelling[-1] == '\t': update_spellings.append(spelling + char_spelling)
                else: update_spellings.append(spelling + ' ' + char_spelling)
        spellings = update_spellings
    return spellings

processed_entry_dict = dict()
char_spelling_dict = dict()
with open(file_in_dir,'r',encoding='utf8') as f: 
    for line_entries in (f.read().splitlines()[line_number_content_starts:], essay_dict.keys()):
        for line_entry in line_entries: 
            if line_entry == '' or line_entry[0] == '#': continue

            for line in append_spellings(line_entry, char_entry_dict):
                line_substituted = ''
                for char in line: line_substituted += morph_map.get(char,char)
                entry, freq = modify_dictionary_entry(line, essay_dict, processed_entry_dict)
                processed_entry_dict[entry] = freq
                if line_substituted != line:
                    entry, freq = modify_dictionary_entry(line_substituted, essay_dict, processed_entry_dict, freq_floor = freq + 1)
                    processed_entry_dict[entry] = freq

lines_out = []
for entry, freq in processed_entry_dict.items():
    if freq == -1: lines_out.append(entry)
    if freq >= 0: lines_out.append(entry + '\t' + str(freq))

with (open(file_header_dir,'r',encoding='utf8') as header, 
      open(file_out_dir,"w",encoding="utf8") as f):
    f.write(header.read() + '\n\n' + '\n'.join(sorted(lines_out)))