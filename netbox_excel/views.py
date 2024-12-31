from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ImportExcelForm, ExportExcelForm
from netbox_excel.models import ExportExcel
from django.views.decorators.csrf import requires_csrf_token
from netbox_excel.export import get_device, export_all, export_current_view
import openpyxl


@requires_csrf_token
def ImportExcelView(request):
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
    else:
        form = ImportExcelForm()
    return render(request, 'netbox_excel/import_excel_console_log.html', {'form': form})

@requires_csrf_token
def ExportExcelView(request):
    if request.method == 'POST':
        # form = ExportExcelForm(request.POST)
        # quick_search = request.POST.get('quick_search')
        # type = request.POST.get('type')

        # Create a new workbook and select the active worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Data Export"

        # create the headers
        headers = ['Rack', 'Số U','Vị trí bắt đầu','Vị trí kế thúc', 'Tên Thiết bị', 'Chủng loại', 'Quản lý', 'Số HĐ', 'Model', 'SN', 'Thời gian lắp đặt', 'Ghi Chú']
        sheet.append(headers)

        # check form data: 1. export all table
        result = []
        # 1. export all table 

        # get all device
        devices_list = get_device()
        
        for device in devices_list:
            # get data custom feild
            device_owner = ""
            year_of_investment = ""
            contract_number = ""
            custom_fields = device.get_custom_fields_by_group()
            for key, value in custom_fields[''].items():
                if str(key) == 'Device owner' and value != None:
                    device_owner = value
                elif str(key) == 'Year of investment' and value != None:
                    year_of_investment = value
                elif str(key) == 'Contract number' and value != None:
                    contract_number = value
            # Tính start U - end U
            end_u = int(device.position) + int(device.device_type.u_height) - 1
            # create new item export
            item_export = ExportExcel(
                rack = device.rack,
                device_role = device.role,
                device_type = device.device_type,
                device_name = device.name,
                position = int(device.position),
                serial_number = device.serial,
                device_description = device.description,
                owner_device = device_owner,
                year_of_investment = year_of_investment,
                contract_number = contract_number, 
                u_number = int(device.device_type.u_height),
                u_end = end_u,
            )
            
            # append data to result export
            result.append(item_export)

            # create item in sheet
            item_sheet = [
                str(item_export.rack), 
                str(item_export.u_number), 
                str(item_export.position), # U start
                str(item_export.u_end), # U end
                str(item_export.device_name),
                str(item_export.device_role),
                str(item_export.owner_device), 
                str(item_export.contract_number),
                str(item_export.device_type),
                str(item_export.serial_number),
                str(item_export.year_of_investment),
                str(item_export.device_description),
            ]
            sheet.append(item_sheet)

        # add header response
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="device_export_excel.xlsx"'

        workbook.save(response)
        return response
        # return HttpResponseRedirect("/dcim/devices/")
    else:
        # form = ExportExcelForm()
        return HttpResponseRedirect("/dcim/devices/")