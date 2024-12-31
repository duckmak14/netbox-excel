import openpyxl
from netbox_excel.models import ExportExcel
from .devices import get_device
import pandas as pd
# from io import StringIO
# import xlsxwriter
from django.http import HttpResponse , HttpResponseRedirect

def export_all():
    
    return 

def export_current_view():
    return