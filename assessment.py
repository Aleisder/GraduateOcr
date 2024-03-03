import string
from difflib import Differ
from dash.html import Span
import pandas as pd


class AssessmentService:

    def __init__(self):
        self.punctuations = list(',;:.?!-()\'\"')
        self.specials = list('~+[\\@^{%*|&<`}_=]>#$/')
        self.last_df: pd.DataFrame = pd.DataFrame([0])
        self.differ = Differ()

    def build_from_differ_compare(self, reference: str, hypothesis: str) -> list[Span]:
        diff = self.differ.compare(reference, hypothesis)
        children = []
        for symbol in diff:
            if symbol[0] == '+':
                class_name = 'wrong-symbol'
            elif symbol[0] == '-':
                class_name = 'missed-symbol'
            else:
                class_name = 'correct-symbol'
            children.append(Span(children=symbol[-1], className=class_name))
        return children

    def character_analysis(self, reference: str, hypothesis: str):
        diff = self.differ.compare(reference, hypothesis)
        stats = dict()
        for line in diff:
            char = line[-1]
            if char not in stats:
                if line[0] == '-':
                    stats[char] = [0, 1]
                elif line[0] == '+':
                    stats[char] = [1, 0]
                elif line[0] == ' ':
                    stats[char] = [1, 1]
            else:
                found: int = stats[char][0]
                actually: int = stats[char][1]
                if line[0] == ' ':
                    found += 1
                    actually += 1
                elif line[0] == '-':
                    actually += 1
                elif line[0] == '+':
                    found += 1
                stats[char] = [found, actually]
        arr = []
        for key in stats:
            found: int = stats[key][0]
            actually: int = stats[key][1]
            if actually == 0:
                accuracy = 0
            else:
                accuracy: float = round(found / actually * 100, 1)
            arr.append([key, found, actually, accuracy])

        df = pd.DataFrame(data=arr, columns=['char', 'found', 'actually', 'accuracy']).sort_values('char')
        self.last_df = df.copy()
        return df

    def filter_by_symbol_type(self, option: str):
        match option:
            case 'all':
                return self.last_df
            case 'letters':
                return self.last_df[self.last_df['char'].isin(list(string.ascii_letters))]
            case 'numbers':
                return self.last_df[self.last_df['char'].isin(list(string.digits))]
            case 'punctuations':
                return self.last_df[self.last_df['char'].isin(self.punctuations)]
            case 'specials':
                return self.last_df[self.last_df['char'].isin(self.specials)]



reference = '''
What is Lorem Ipsum?

Lorem Ipsum is simply dummy text of the printing and typesetting
industry. Lorem Ipsum has been the industry's standard dummy
text ever since the 1500s, when an unknown printer took a galley
of type and scrambled it to make a type specimen book. It has
survived not only five centuries, but also the leap into electronic
typesetting, remaining essentially unchanged. It was popularised in
the 1960s with the release of Letraset sheets containing Lorem
Ipsum passages, and more recently with desktop publishing
software like Aldus PageMaker including versions of Lorem Ipsum.

Why do we use it?

It is a long established fact that a reader will be distracted by the
readable content of a page when looking at its layout. The point of
using Lorem Ipsum is that it has a more-or-less normal distribution
of letters, as opposed to using 'Content here, content here',
making it look like readable English. Many desktop publishing
packages and web page editors now use Lorem Ipsum as their
default model text, and a search for 'lorem ipsum' will uncover
many web sites still in their infancy. Various versions have evolved
over the years, sometimes by accident, sometimes on purpose
(injected humour and the like)'''
hypo = '''
What is Lorem Ipsum?

Lorem Ipsum is simply dummy text of the printing and typesetting
industry. Lorem Ipsum has been the industry's standard dummy
text ever since the 1500s, when an unknown printer took a galley
of type and scrambled it to make a type specimen book. It has
survived not only five centuries, but also the leap into electronic
typesetting, remaining essentially unchanged. It was popularised in
the 1960s with the release of Letraset sheets containing Lorem
Ipsum passages, and more recently with desktop publishing
software like Aldus PageMaker including versions of Lorem Ipsum.

Why do we use it?

It is a long established fact that a reader will be distracted by the
readable content of a page when looking at its layout. The point of
using Lorem Ipsum is that it has a more-or-less normal distribution
of letters, as opposed to using ‘Content here, content here’,
making it look like readable English. Many desktop publishing
packages and web page editors now use Lorem Ipsum as their
default model text, and a search for ‘lorem ipsum’ will uncover
many web sites still in their infancy. Various versions have evolved
over the years, sometimes by accident, sometimes on purpose
(injected humour and the like).
'''
