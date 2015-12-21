# -*- coding: utf-8 -*-

import xlrd

def excel_to_string(ws,r,c):
    cell=ws.cell(r,c)
    if cell.ctype==xlrd.XL_CELL_BLANK or cell.ctype==xlrd.XL_CELL_EMPTY or cell.ctype==xlrd.XL_CELL_ERROR:
        return ""
    elif cell.ctype==xlrd.XL_CELL_NUMBER:
        try:
            i=int(cell.value)
            return str(i)
        except ValueError:
            return cell.value
    else:
        return cell.value     
    
