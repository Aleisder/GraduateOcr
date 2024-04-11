import string
from difflib import Differ
from dash.html import Span, Thead, Tr, Th, Td, Tbody, Br
import pandas as pd
import dash_mantine_components as dmc


class AssessmentService:

    def __init__(self):
        self.punctuations = list(',;:.?!-()\'\"')
        self.specials = list('~+[\\@^{%*|&<`}_=]>#$/')
        self.last_df: pd.DataFrame = pd.DataFrame([0])
        self.current_df: pd.DataFrame = pd.DataFrame([0])
        self.differ = Differ()

    def experimental_span_formatted(self, reference: list[list[str]], hypothesis: list[list[str]]) -> list[Span]:
        children = []
        for i in range(len(reference)):
            for j in range(len(reference[i])):
                diff = self.differ.compare(reference[i][j], hypothesis[i][j])
                for symbol in diff:
                    if symbol[0] == '+':
                        class_name = 'wrong-symbol'
                    elif symbol[0] == '-':
                        class_name = 'missed-symbol'
                    else:
                        class_name = 'correct-symbol'
                    children.append(Span(children=symbol[-1], className=class_name))
                children.append(Br())
        return children

    def build_two_columns(self, ref: list[list[str]], exp: list[list[str]]):

        children_ref = []
        children_exp = []

        for i in range(0, len(ref)):
            for j in range(0, len(ref[i])):
                first = ref[i][j]
                second = exp[i][j]
                diff = self.differ.compare(first, second)

                curr_ref_line = []
                curr_exp_line = []

                for line in diff:
                    sign = line[-1]

                    if line[0] == '+':
                        curr_exp_line.append(Span(sign, className='wrong-symbol'))
                    elif line[0] == '-':
                        curr_ref_line.append(Span(sign, className='missed-symbol'))
                    else:
                        curr_char = Span(sign)
                        curr_exp_line.append(curr_char)
                        curr_ref_line.append(curr_char)

                children_ref.append(curr_ref_line)
                children_exp.append(curr_exp_line)

        column_names = ['Оригинальный текст', 'Распознанный текст']

        header = [Thead(Tr([Th(name) for name in column_names]))]

        for i in range(0, len(children_ref)):
            counter = dmc.Kbd(str(i + 1))
            children_ref[i] = [counter] + ['    '] + children_ref[i]
            children_exp[i] = [counter] + ['    '] + children_exp[i]

        rows = []

        for i in range(0, len(children_ref)):

            rows.append(
                Tr(
                    [
                        Td(children_ref[i]),
                        Td(children_exp[i])
                    ]
                )
            )
        body = [Tbody(rows)]
        return header + body

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
        self.current_df = df.copy()
        return df


    def filter_by_symbol_type(self, option: str) -> pd.DataFrame:
        match option:
            case 'all':
                self.current_df = self.last_df.copy()
            case 'letters':
                self.current_df = self.last_df[self.last_df['char'].isin(list(string.ascii_letters))]
            case 'numbers':
                self.current_df = self.last_df[self.last_df['char'].isin(list(string.digits))]
            case 'punctuations':
                self.current_df = self.last_df[self.last_df['char'].isin(self.punctuations)]
            case 'specials':
                self.current_df = self.last_df[self.last_df['char'].isin(self.specials)]
        return self.current_df
