import os
import re
import glob
import json5
import xlwings as xw


def sheet_to_json(wb_path, ws_name, out_json, key='key', values=['value',], header_row = 1, eval_list=True, eval_dict=True):
    app = xw.App(visible=True, add_book=False)
    with app.books.open(wb_path) as wb:
        ws = wb.sheets(ws_name)
        headers = ws.range(header_row, 1).expand('right').value
        key_col = headers.index(key) + 1
        keys = ws.range(header_row + 1, key_col).expand('down').value
        ### alert dup keys
        seen = set()
        dupes = [(n+header_row+1, x) for n, x in enumerate(keys) if x in seen or seen.add(x)]
        if dupes:
            print('duplicate keys found')
            for r, k in dupes:
                print('row {0} >>> {1}'.format(r, k))
            return None
        ### end alert dup keys
        data = {}
        for row in range(header_row+1, header_row + len(keys) + 1):
            k = str(ws.range(row, key_col).value)
            if len(values) == 1:
                val_col = headers.index(values[0]) + 1
                v = ws.range(row, val_col).value
                if eval_list and isinstance(v, str) and re.match(r'\[[\s\S]+?\]', v):
                    v = eval(v)
                if eval_dict and isinstance(v, str) and re.match(r'\{[\s\S]+?\}', v):
                    v = eval(v)
                data[k] = v

            if len(values) > 1:
                data[k] = {}
                for v_header in values:
                    val_col = headers.index(v_header) + 1
                    v = ws.range(row, val_col).value
                    if eval_list and isinstance(v, str) and re.match(r'\[[\s\S]+?\]', v):
                        v = eval(v)
                    if eval_dict and isinstance(v, str) and re.match(r'\{[\s\S]+?\}', v):
                        v = eval(v)
                    data[k][v_header] = v
    
    app.quit()
    with open(out_json, 'w', encoding='utf8') as f:
        json5.dump(data, f, quote_keys=True)






def main():
    wb_path = r'D:\GIT\Contents\triplematch3ddata\xlsx\TripleMatch3DData.xlsx'
    ws_name = 'Test'
    out_json = r'D:\GIT\Contents\triplematch3ddata\test.json'
    key = 'key'
    values = ['value', 'value2']
    header_row = 1
    eval_list = True
    eval_dict = True
    sheet_to_json(wb_path, ws_name, out_json, key=key, values=values, header_row=header_row, eval_list=eval_list, eval_dict=eval_dict)


if __name__ == '__main__':
    main()
    




        