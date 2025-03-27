import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import AnotherServiceOrderForm, AnotherServiceToolForm, CalibrationReportForm, DeliveryChallanForm, DeliveryChallanToolsFormSet, InstrumentFamilyGroupForm, InstrumentForm, InstrumentGroupMasterForm, ServiceTypeForm, ShedDetailsForm, ShedLoginForm, ShedToolsForm, TransportOrderForm, TransportToolsForm, VendorForm, VendorHandlesForm, VendorTypeForm
from .models import InstrumentFamilyGroup, InstrumentGroupMaster, CalibrationReport, DeliveryChallan, DeliveryChallanTools, InstrumentModel,  ServiceOrder, ServiceTools, ServiceType, ShedTools, ShedUser, TransportOrder, ShedDetails, TransportTools, Vendor, VendorHandles, VendorType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CalibrationReportSerializer, DeliveryChallanSerializer, DeliveryChallanToolsSerializer, InstrumentFamilyGroupSerializer, InstrumentGroupMasterSerializer, InstrumentModelSerializer, ServiceOrderSerializer, ServiceToolsSerializer, ServiceTypeSerializer, ShedDetailsSerializer, ShedNoteSerializer, ShedToolsSerializer, SimpleInstrumentModelSerializer, TransportOrderSerializer, TransportToolsSerializer, VendorHandlesSerializer, VendorSerializer, VendorTypeSerializer, VendorUpdateSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.models import User

class VendorTypeView(APIView):
    def get(self, request):
        vendor_types = VendorType.objects.all()
        serializer = VendorTypeSerializer(vendor_types, many=True)
        return Response({'vendor_types': serializer.data})


@method_decorator(csrf_exempt, name='dispatch')
class InstrumentToolsView(APIView):
    def get(self, request):
        instruments = InstrumentModel.objects.all()
        serializer = InstrumentModelSerializer(instruments, many=True)
        return Response({'instrument_models': serializer.data})

class InstrumentServiceToolsView(APIView):
    def get(self, request):
        instruments = InstrumentModel.objects.filter(service_status=True)
        serializer = InstrumentModelSerializer(instruments, many=True)
        return Response({'instrument_models': serializer.data})

class InstrumentFamilyGroupView(APIView):
    def get(self, request):
        instruments = InstrumentFamilyGroup.objects.all()
        serializer = InstrumentFamilyGroupSerializer(instruments, many=True)
        return Response({'instrument_family_groups': serializer.data})

class InstrumentGroupMasterView(APIView):
    def get(self, request):
        instruments = InstrumentGroupMaster.objects.all()
        serializer = InstrumentGroupMasterSerializer(instruments, many=True)
        return Response({'instrument_group_masters': serializer.data})

class VendorView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response({'vendors': serializer.data})

class VendorHandlesView(APIView):
    def get(self, request):
        vendor_handles = VendorHandles.objects.all()
        serializer = VendorHandlesSerializer(vendor_handles, many=True)
        return Response({'vendor_handles': serializer.data})


@method_decorator(csrf_exempt, name='dispatch')
class ShedDetailsView(APIView):
    def get(self, request):
        shed_details = ShedDetails.objects.all()
        serializer = ShedDetailsSerializer(shed_details, many=True)
        return Response({'shed_details': serializer.data})

class ShedToolsView(APIView):
    def get(self, request):
        shed_tools = ShedTools.objects.all()
        serializer = ShedToolsSerializer(shed_tools, many=True)
        return Response({'shed_tools': serializer.data})

class AllTransportOrderView(APIView):
    def get(self, request):
        transport_orders = TransportOrder.objects.all()
        serializer = TransportOrderSerializer(transport_orders, many=True)
        return Response({'transport_orders': serializer.data})

class RecentTransportOrderView(APIView):
    def get(self, request):
        recent_transport_orders = TransportOrder.objects.order_by('-movement_date')[:10]
        serializer = TransportOrderSerializer(recent_transport_orders, many=True)
        return Response({'transport_orders': serializer.data})

class AllServiceOrderView(APIView):
    def get(self, request):
        service_orders = ServiceOrder.objects.all()
        serializer = ServiceOrderSerializer(service_orders, many=True)
        return Response({'service_orders': serializer.data})

class RecentServiceOrderView(APIView):
    def get(self, request):
        recent_service_orders = ServiceOrder.objects.order_by('-date')[:10]
        serializer = ServiceOrderSerializer(recent_service_orders, many=True)
        return Response({'service_orders': serializer.data})

class AllDeliveryChallanView(APIView):
    def get(self, request):
        delivery_challan = DeliveryChallan.objects.all()
        serializer = DeliveryChallanSerializer(delivery_challan, many=True)
        return Response({'delivery_challan': serializer.data})

class RecentDeliveryChallanView(APIView):
    def get(self, request):
        recent_delivery_challan = DeliveryChallan.objects.order_by('-received_date')[:10]
        serializer = DeliveryChallanSerializer(recent_delivery_challan, many=True)
        return Response({'delivery_challan': serializer.data})

class CalibrationReportView(APIView):
    def get(self, request):
        calibration_reports = CalibrationReport.objects.all()
        serializer = CalibrationReportSerializer(calibration_reports, many=True)
        return Response({'calibration_reports': serializer.data})

class ShedDetailAPIView(APIView):
    def get(self, request, shed_id):
        shed = get_object_or_404(ShedDetails, pk=shed_id)
        shed_serializer = ShedDetailsSerializer(shed)
        shed_tools = ShedTools.objects.filter(shed=shed)
        shed_tools_serializer = ShedToolsSerializer(shed_tools, many=True)
        return Response({'shed': shed_serializer.data, 'shed_tools': shed_tools_serializer.data})

class VendorDetailsView1(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vendor_serializer = VendorSerializer(vendor)
        vendor_handles = VendorHandles.objects.filter(vendor=vendor)
        vendor_handles_serializer = VendorHandlesSerializer(vendor_handles, many=True)
        instrument_group_masters = vendor_handles.values_list('tool', flat=True)
        instruments = InstrumentModel.objects.filter(type_of_tool__in=instrument_group_masters)
        instruments_serializer = SimpleInstrumentModelSerializer(instruments, many=True)
        return Response({'vendor': vendor_serializer.data,'vendor_handles': vendor_handles_serializer.data,'instruments': instruments_serializer.data})

class TransportOrderViews(APIView):
    def get(self, request, movement_id):
        transport_order = get_object_or_404(TransportOrder, pk=movement_id)
        transport_order_serializer = TransportOrderSerializer(transport_order)
        transport_tools = TransportTools.objects.filter(transport=transport_order)
        transport_tools_serializer = TransportToolsSerializer(transport_tools, many=True)
        return Response({'transport_order': transport_order_serializer.data, 'transport_tools': transport_tools_serializer.data})

class ServiceOrderViews(APIView):
    def get(self, request, service_id):
        service_order = get_object_or_404(ServiceOrder, pk=service_id)
        service_order_serializer = ServiceOrderSerializer(service_order)
        service_tools = ServiceTools.objects.filter(service=service_order)
        service_tools_serializer = ServiceToolsSerializer(service_tools, many=True)
        return Response({'service_order': service_order_serializer.data, 'service_tools': service_tools_serializer.data})

class DeliveryChallanViews(APIView):
    def get(self, request, deliverychallan_id):
        delivery_challan = get_object_or_404(DeliveryChallan, pk=deliverychallan_id)
        delivery_challan_serializer = DeliveryChallanSerializer(delivery_challan)
        delivery_challan_tools = DeliveryChallanTools.objects.filter(deliverychallan=delivery_challan)
        delivery_challan_tools_serializer = DeliveryChallanToolsSerializer(delivery_challan_tools, many=True)
        return Response({'delivery_challan': delivery_challan_serializer.data, 'delivery_challan_tools': delivery_challan_tools_serializer.data})

class ServiceTypeView(APIView):
    def get(self, request):
        service_types = ServiceType.objects.all()
        serializer = ServiceTypeSerializer(service_types, many=True)
        return Response(serializer.data)

def home(request):
    return render(request, 'app1/home.html')

class TransportOrderView(APIView):
    def get(self, request):
        orders_details = TransportOrder.objects.all()
        orders_serializer = TransportOrderSerializer(orders_details, many=True)

        instrument_models = InstrumentModel.objects.all()
        instrument_serializer = InstrumentModelSerializer(instrument_models, many=True)

        shed_details = ShedDetails.objects.all()
        shed_serializer = ShedDetailsSerializer(shed_details, many=True)

        shed_tools_details = ShedTools.objects.all()
        shed_tools_serializer = ShedToolsSerializer(shed_tools_details, many=True)

        response_data = {
            'transport_orders': orders_serializer.data,
            'instrument_models': instrument_serializer.data,
            'shed_details' : shed_serializer.data,
            'shed_tools_details' : shed_tools_serializer.data,
        }

        return Response(response_data)

    def post(self, request):
        serializer = TransportOrderSerializer(data=request.data)
        if serializer.is_valid():
            movement_date = serializer.validated_data['movement_date']
            source_shed_id = serializer.validated_data['source_shed']
            destination_shed_id = serializer.validated_data['destination_shed']
            tool_count = serializer.validated_data['tool_count']
            acknowledgment = serializer.validated_data.get('acknowledgment', False)
            tools_data = request.data.get('tools', [])

            transport_order = TransportOrder.objects.create(
                movement_date=movement_date,
                source_shed=source_shed_id,
                destination_shed=destination_shed_id,
                tool_count=tool_count,
                acknowledgment=acknowledgment
            )

            for tool_data in tools_data:
                tool_id = tool_data.get('tool')
                tool_movement_remarks = tool_data.get('tool_movement_remarks', 'good')
                tool = get_object_or_404(InstrumentModel, pk=tool_id)
                TransportTools.objects.create(transport=transport_order, tool=tool, tool_movement_remarks=tool_movement_remarks)

            return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class TransportAcknowledgmentView(View):
    def get(self, request, order_id):
        transport_order = get_object_or_404(TransportOrder, pk=order_id)
        return render(request, 'app1/transport_acknowledge.html', {'transport_order': transport_order})

    def post(self, request, order_id):
        transport_order = get_object_or_404(TransportOrder, pk=order_id)
        transport_order.acknowledgment = True

        try:
            with transaction.atomic():
                transport_order.save()

                selected_tools = TransportTools.objects.filter(transport=transport_order)

                source_shed = transport_order.source_shed
                destination_shed = transport_order.destination_shed
                transported_tools = ShedTools.objects.filter(shed=source_shed, using_tool__in=selected_tools.values_list('tool', flat=True))
                transported_tools.update(shed=destination_shed)

                selected_tools.update(acknowledgment=True)

                acknowledged_instruments = selected_tools.values_list('tool', flat=True)
                InstrumentModel.objects.filter(instrument_no__in=acknowledged_instruments).update(current_shed=destination_shed)

                return JsonResponse({'success': True, 'message': 'Transport acknowledgment successful.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class TransportAcknowledgmentToolsView(View):
    def get(self, request, order_id):
        transport_order = get_object_or_404(TransportOrder, pk=order_id)
        return render(request, 'app1/transport_acknowledge_tools.html', {'transport_order': transport_order})

    def post(self, request, order_id):
        transport_order = get_object_or_404(TransportOrder, pk=order_id)

        try:
            data = json.loads(request.body.decode('utf-8'))
            tool_ids = data.get('tool_ids', [])

            tool_ids = [tool_id for tool_id in tool_ids if tool_id]

            with transaction.atomic():
                selected_tools = TransportTools.objects.filter(transport=transport_order, tool_id__in=tool_ids)

                selected_tools.update(acknowledgment=True)

                source_shed = transport_order.source_shed
                destination_shed = transport_order.destination_shed
                transported_tools = ShedTools.objects.filter(shed=source_shed, using_tool__in=selected_tools.values_list('tool', flat=True))
                transported_tools.update(shed=destination_shed)

                acknowledged_instruments = selected_tools.values_list('tool', flat=True)
                InstrumentModel.objects.filter(instrument_no__in=acknowledged_instruments).update(current_shed=destination_shed)

                all_tools_acknowledged = not TransportTools.objects.filter(transport=transport_order, acknowledgment=False).exists()
                transport_order.acknowledgment = all_tools_acknowledged
                transport_order.save()

                return JsonResponse({'success': True, 'message': 'Selected tools acknowledgment updated successfully.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def update_service_status():
    instrument_models = InstrumentModel.objects.all()

    for instrument in instrument_models:
        latest_calibration_report = CalibrationReport.objects.filter(calibration_tool=instrument).order_by('calibration_date').first()

        if latest_calibration_report and latest_calibration_report.notification_date == timezone.now().date():
            instrument.service_status = True
            instrument.save()

            print(f"Instrument tool '{instrument.instrument_name}' has been updated.")

import schedule
import time
from django.utils import timezone
import threading

def start_scheduler():
    schedule.every().minutes.do(update_service_status)
    schedule.every().hour.do(update_service_status)
    schedule.every().day.at("00:15").do(update_service_status)

    while True:
        schedule.run_pending()
        if all(not job.should_run for job in schedule.jobs):
            break
        time.sleep(1)

scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.start()

@method_decorator(csrf_exempt, name='dispatch')
class ServiceOrderView(APIView):
    def get(self, request):
        service_orders = ServiceOrder.objects.all()
        service_order_serializer = ServiceOrderSerializer(service_orders, many=True)

        service_tools = ServiceTools.objects.all()
        service_tools_serializer = ServiceToolsSerializer(service_tools, many=True)

        vendors = Vendor.objects.all()
        vendor_serializer = VendorSerializer(vendors, many=True)

        instrument_models = InstrumentModel.objects.all()
        instrument_serializer = InstrumentModelSerializer(instrument_models, many=True)

        response_data = {
            'service_orders': service_order_serializer.data,
            'service_tools': service_tools_serializer.data,
            'vendors': vendor_serializer.data,
            'instrument_tools': instrument_serializer.data,
        }

        return Response(response_data)

    def post(self, request):
        order_serializer = ServiceOrderSerializer(data=request.data)

        if order_serializer.is_valid():
            service_order = order_serializer.save()

            tools_data = request.data.get('tools', [])
            total_amount = 0

            for tool_data in tools_data:
                tool_id = tool_data.get('tool')
                vendor_id = tool_data.get('vendor')
                service_type_id = tool_data.get('service_type')
                tool = get_object_or_404(InstrumentModel, pk=tool_id)
                vendor = get_object_or_404(Vendor, pk=vendor_id)
                service_type = get_object_or_404(ServiceType, pk=service_type_id)
                service_remarks = tool_data.get('service_remarks', 'good')

                service_tool = ServiceTools.objects.create(service=service_order,tool=tool,vendor=vendor,service_type=service_type,service_remarks=service_remarks)

                if service_tool.service_type.service_type.lower() == 'calibration':
                    # vendor_handles = VendorHandles.objects.filter(tool=tool, vendor=vendor)

                    instrument_group = tool.type_of_tool
                    vendor_handles = VendorHandles.objects.filter(tool=instrument_group, vendor=vendor)

                    for vendor_handle in vendor_handles:
                        total_amount += vendor_handle.cost

            service_order.amount = total_amount
            service_order.save()

            return Response({'success': True, 'serviceorder_id': service_order.service_id, 'total_amount': total_amount}, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateBillView(View):
    def get(self, request, service_order_id):
        service_tools = ServiceTools.objects.filter(service_id=service_order_id)
        bill_items = []
        total_amount = 0

        for service_tool in service_tools:
            tool = service_tool.tool
            service_type = service_tool.service_type.service_type

            if service_type.lower() == 'calibration':
                vendor = service_tool.vendor

                instrument_group = tool.type_of_tool

                vendor_handles = VendorHandles.objects.filter(tool=instrument_group, vendor=vendor)

                if vendor_handles.exists():
                    vendor_handle = vendor_handles.first()
                    cost = vendor_handle.cost
                    amount = 1 * cost
                    total_amount += amount
                    bill_items.append({'tool': tool.instrument_name,'service_type': service_type,'cost': cost,'amount': amount})
                else:
                    bill_items.append({'tool': tool.instrument_name,'service_type': service_type,'cost': 0,'amount': 0})
            else:
                bill_items.append({'tool': tool.instrument_name,'service_type': service_type,'cost': 0,'amount': 0})

        try:
            service_order = ServiceOrder.objects.get(service_id=service_order_id)
            service_order.amount = total_amount
            service_order.save()
        except ServiceOrder.DoesNotExist:
            return JsonResponse({'error': f'Service Order with ID {service_order_id} does not exist'}, status=404)

        data = {'bill_items': bill_items,'total_amount': total_amount}
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class StoreDeliveryChallan(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data

        service_id = data.get('service')
        if not service_id:
            return JsonResponse({'success': False, 'errors': 'Service ID is required'}, status=400)

        try:
            service_order = ServiceOrder.objects.get(pk=service_id)
        except ServiceOrder.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Invalid Service ID'}, status=400)

        vendor = service_order.vendor

        data = data.copy()
        data['vendor'] = vendor.vendor_id

        delivery_challan_form = DeliveryChallanForm(data)
        if delivery_challan_form.is_valid():
            delivery_challan = delivery_challan_form.save()

            tool_data_list = []
            index = 0
            while True:
                tool_data = {
                    'calibration_tool': data.get(f'toolData[{index}][calibration_tool]'),
                    'calibration_date': data.get(f'toolData[{index}][calibration_date]'),
                    'calibration_report_no': data.get(f'toolData[{index}][calibration_report_no]'),
                    'calibration_agency': data.get(f'toolData[{index}][calibration_agency]'),
                    'result': data.get(f'toolData[{index}][result]'),
                    'action': data.get(f'toolData[{index}][action]'),
                    'remark': data.get(f'toolData[{index}][remark]'),
                    'calibration_report_file': request.FILES.get(f'toolData[{index}][calibration_report_file]'),
                    'calibration_report_file2': request.FILES.get(f'toolData[{index}][calibration_report_file2]')
                }
                if not tool_data['calibration_tool']:
                    break
                tool_data_list.append(tool_data)
                index += 1

            errors = []
            for tool_info in tool_data_list:
                calibration_report_form = CalibrationReportForm(tool_info, files={'calibration_report_file': tool_info['calibration_report_file']})
                if calibration_report_form.is_valid():
                    calibration_report = calibration_report_form.save(commit=False)
                    calibration_report.calibration_tool_id = tool_info['calibration_tool']

                    if tool_info['calibration_report_file']:
                        calibration_report.calibration_report_file = tool_info['calibration_report_file']

                    if tool_info['calibration_report_file2']:
                        calibration_report.calibration_report_file2 = tool_info['calibration_report_file2']

                    calibration_frequency = calibration_report.calibration_tool.calibration_frequency
                    calibration_date = calibration_report.calibration_date
                    next_calibration_date = calibration_date + timedelta(days=calibration_frequency)
                    calibration_report.next_calibration_date = next_calibration_date

                    try:
                        vendor_handle = VendorHandles.objects.filter(tool=calibration_report.calibration_tool.type_of_tool, vendor=vendor).first()
                        if not vendor_handle:
                            raise VendorHandles.DoesNotExist

                        turnaround_time = vendor_handle.turnaround_time
                        notification_date = next_calibration_date - timedelta(days=turnaround_time)
                        calibration_report.notification_date = notification_date
                    except VendorHandles.DoesNotExist:
                        errors.append({
                            'tool': tool_info['calibration_tool'],
                            'errors': 'Vendor handle not found for the selected tool.'
                        })
                        continue

                    calibration_report.save()

                    try:
                        instrument = InstrumentModel.objects.get(pk=tool_info['calibration_tool'])
                        instrument.notification_date = notification_date
                        instrument.service_status = False

                        new_shed_id = data.get('shed')
                        if new_shed_id:
                            try:
                                new_shed = ShedDetails.objects.get(pk=new_shed_id)
                                instrument.current_shed = new_shed
                                instrument.save()

                                ShedTools.objects.update_or_create(
                                    using_tool=instrument,
                                    defaults={'shed': new_shed}
                                )

                            except ShedDetails.DoesNotExist:
                                errors.append({
                                    'tool': tool_info['calibration_tool'],
                                    'errors': 'New shed not found.'
                                })
                                continue

                        instrument.save()

                    except InstrumentModel.DoesNotExist:
                        errors.append({
                            'tool': tool_info['calibration_tool'],
                            'errors': 'Instrument not found.'
                        })
                        continue

                    delivery_challan_tool = DeliveryChallanTools(
                        deliverychallan=delivery_challan,
                        tool_id=tool_info['calibration_tool'],
                        calibration_report=calibration_report
                    )
                    delivery_challan_tool.save()

                    ServiceTools.objects.filter(service=service_order, tool_id=tool_info['calibration_tool']).update(service_pending_tool=False)
                else:
                    errors.append({
                        'tool': tool_info['calibration_tool'],
                        'errors': calibration_report_form.errors
                    })

            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            else:
                all_tools_pending = ServiceTools.objects.filter(service=service_order, service_pending_tool=True).exists()
                if not all_tools_pending:
                    service_order.service_pending = False
                    service_order.save()

                return JsonResponse({'success': True, 'message': 'Data saved successfully'})
        else:
            return JsonResponse({'success': False, 'errors': delivery_challan_form.errors}, status=400)

class InstrumentTransportHistoryView(APIView):
    def get(self, request, instrument_id):
        instrument = InstrumentModel.objects.get(pk=instrument_id)
        transport_history = TransportTools.objects.filter(tool=instrument)
        serialized_transport_history = TransportToolsSerializer(transport_history, many=True).data

        movement_ids = [item['transport'] for item in serialized_transport_history]

        transport_orders = TransportOrder.objects.filter(movement_id__in=movement_ids)
        serialized_transport_orders = TransportOrderSerializer(transport_orders, many=True).data

        return Response({
            'instrument': InstrumentModelSerializer(instrument).data,
            'transport_history': serialized_transport_history,
            'transport_orders': serialized_transport_orders
        })

class InstrumentServiceHistoryView(APIView):
    def get(self, request, instrument_id):
        instrument = InstrumentModel.objects.get(pk=instrument_id)
        service_history = ServiceTools.objects.filter(tool=instrument).select_related('service')

        serialized_service_history = []
        for service_tool in service_history:
            service_order_data = {
                'service_id': service_tool.service.service_id,
                'date': service_tool.service.date,
                'amount': service_tool.service.amount,
                'description': service_tool.service.description,
                'tool_count': service_tool.service.tool_count,
                'vendor': service_tool.service.vendor.name if service_tool.service.vendor else None
            }
            serialized_service_history.append(service_order_data)

        return Response({'instrument': InstrumentModelSerializer(instrument).data, 'service_history': serialized_service_history})

class InstrumentCalibrationHistoryView(APIView):
    def get(self, request, instrument_id):
        instrument = get_object_or_404(InstrumentModel, pk=instrument_id)

        calibration_history = CalibrationReport.objects.filter(calibration_tool=instrument)

        serialized_calibration_history = CalibrationReportSerializer(calibration_history, many=True).data

        return Response({'instrument': InstrumentModelSerializer(instrument).data,'calibration_history': serialized_calibration_history})

@method_decorator(csrf_exempt, name='dispatch')
class AddInstrumentModelView1(View):
    def get(self, request):
        instrument_model_form = InstrumentForm()
        return render(request, 'app1/instrument_model_form.html', {'instrument_model_form': instrument_model_form})

    def post(self, request):
        try:
            body_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'errors': 'Invalid JSON data'}, status=400)

        instrument_name = body_data.get('instrument_name')
        manufacturer_name = body_data.get('manufacturer_name')
        year_of_purchase = body_data.get('year_of_purchase')
        gst = body_data.get('gst')
        description = body_data.get('description')
        instrument_range = body_data.get('instrument_range')
        least_count = body_data.get('least_count')
        type_of_tool_id = body_data.get('type_of_tool_id')
        calibration_frequency = body_data.get('calibration_frequency')
        shed_id1 = body_data.get('shed_id')

        if InstrumentModel.objects.filter(instrument_name=instrument_name).exists():
            return JsonResponse({'success': False, 'errors': 'Tool with this name already exists'})

        instrument_data = {
            'instrument_name': instrument_name,
            'manufacturer_name': manufacturer_name,
            'year_of_purchase': year_of_purchase,
            'gst': gst,
            'description': description,
            'instrument_range': instrument_range,
            'least_count': least_count,
            'type_of_tool': type_of_tool_id,
            'calibration_frequency': calibration_frequency,
            # 'current_shed': 1,
            'current_shed': shed_id1,
        }

        form = InstrumentForm(instrument_data)

        if form.is_valid():
            try:
                instrument_instance = form.save()

                ShedTools.objects.create(
                    shed_id=shed_id1,
                    using_tool=instrument_instance
                )

                return JsonResponse({'success': True})
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return JsonResponse({'success': False, 'errors': 'Tool with this name already exists'}, status=400)
                else:
                    return JsonResponse({'success': False, 'errors': 'An error occurred while saving the instrument'}, status=400)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class AddInstrumentGroupMasterView(View):
    def get(self, request):
        instrument_group_master_form = InstrumentGroupMasterForm()
        return render(request, 'app1/instrument_group_master_form.html', {'instrument_group_master_form': instrument_group_master_form})

    def post(self, request):
        body_data = json.loads(request.body)
        tool_group_name = body_data.get('tool_group_name')
        tool_group_code = body_data.get('tool_group_code')
        tool_family_id = body_data.get('tool_family')  # This will be the foreign key to InstrumentFamilyGroup

        try:
            tool_family = InstrumentFamilyGroup.objects.get(pk=tool_family_id)
        except InstrumentFamilyGroup.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Instrument Family Group does not exist'}, status=400)

        instrument_group_master_data = {
            'tool_group_name': tool_group_name,
            'tool_group_code': tool_group_code,
            'tool_family': tool_family.instrument_family_id
        }

        form = InstrumentGroupMasterForm(instrument_group_master_data)

        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True})
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return JsonResponse({'success': False, 'errors': 'Instrument group master with this name or code already exists'}, status=400)
                else:
                    return JsonResponse({'success': False, 'errors': 'An error occurred while saving the instrument group master'}, status=400)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class AddInstrumentFamilyView(View):
    def get(self, request):
        instrument_family_form = InstrumentFamilyGroupForm()
        return render(request, 'app1/instrument_family_form.html', {'instrument_family_form': instrument_family_form})

    def post(self, request):
        body_data = json.loads(request.body)
        instrument_family_name = body_data.get('instrument_family_name')

        instrument_family_data = {
            'instrument_family_name': instrument_family_name,
        }

        form = InstrumentFamilyGroupForm(data=instrument_family_data)

        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True})
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return JsonResponse({'success': False, 'errors': 'Instrument family with this name already exists'}, status=400)
                else:
                    return JsonResponse({'success': False, 'errors': 'An error occurred while saving the instrument family'}, status=400)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class AddVendorView(View):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        form = VendorForm()
        return render(request, 'app1/vendor_form.html', {'form': form})

    def post(self, request):
        if request.content_type.startswith('multipart/form-data'):
            form = VendorForm(request.POST, request.FILES)
        else:
            return JsonResponse({'success': False, 'error': 'Unsupported content type'}, status=400)

        if form.is_valid():
            vendor = form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class AddVendorHandlesView(View):
    def get(self, request):

        form = VendorHandlesForm()
        return render(request, 'app1/vendor_handles_form.html', {'form': form})

    def post(self, request):
        body_data = json.loads(request.body)

        vendor_id = body_data.get('vendor')
        tool_id = body_data.get('tool')
        turnaround_time = body_data.get('turnaround_time')
        cost = body_data.get('cost')

        vendor_handles_data = {'vendor': vendor_id,'tool': tool_id,'turnaround_time': turnaround_time,'cost': cost}

        form = VendorHandlesForm(vendor_handles_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class AddShedDetailsView(View):
    def get(self, request):
        form = ShedDetailsForm()
        return render(request, 'app1/shed_details_form.html', {'form': form})

    def post(self, request):
        if request.content_type == 'application/json':
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        else:
            body_data = request.POST

        name = body_data.get('name')
        location = body_data.get('location')
        address = body_data.get('address')
        phone_number = body_data.get('phone_number')
        password1 = body_data.get('password1')

        shed_details_data = {
            'name': name,
            'location': location,
            'address': address,
            'phone_number': phone_number,
            'password': password1
        }

        form = ShedDetailsForm(shed_details_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class AddServiceTypeView(View):
    def get(self, request):
        form = ServiceTypeForm()
        return render(request, 'app1/service_type_form.html', {'form': form})

    def post(self, request):
        body_data = json.loads(request.body)

        service_type = body_data.get('service_type')

        service_type_data = {'service_type': service_type}

        form = ServiceTypeForm(service_type_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class AddVendorTypeView(View):
    def get(self, request):
        form = VendorTypeForm()
        return render(request, 'app1/vendor_type_form.html', {'form': form})

    def post(self, request):
        body_data = json.loads(request.body)

        vendor_type = body_data.get('vendor_type')

        vendor_type_data = {'vendor_type': vendor_type}

        form = VendorTypeForm(vendor_type_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class AddShedToolsView(View):
    def get(self, request):
        form = ShedToolsForm()
        return render(request, 'app1/shed_tools_form.html', {'form': form})

    def post(self, request):
        body_data = json.loads(request.body)

        shed_id = body_data.get('shed_id')
        tool_id = body_data.get('tool_id')

        shed_tools_data = {'shed': shed_id,'using_tool': tool_id}

        form = ShedToolsForm(shed_tools_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

@method_decorator(csrf_exempt, name='dispatch')
class VendorDeleteView(View):
    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        return render(request, 'app1/delete_vendor.html', {'vendor': vendor})

    def post(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        try:
            vendor.delete()
            return JsonResponse({'success': True, 'message': 'Vendor deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class ShedDeleteView(View):
    def get(self, request, shed_id):
        shed = get_object_or_404(ShedDetails, pk=shed_id)
        return render(request, 'app1/delete_shed.html', {'shed': shed})

    def post(self, request, shed_id):
        shed = get_object_or_404(ShedDetails, pk=shed_id)
        default_shed = get_object_or_404(ShedDetails, pk=1)

        try:
            instruments = InstrumentModel.objects.filter(current_shed=shed)

            for instrument in instruments:
                instrument.current_shed = default_shed
                instrument.save()

            shed.delete()
            return JsonResponse({'success': True, 'message': 'Shed deleted and instruments reassigned successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class TransportOrderDeleteView(View):
    def get(self, request, movement_id):
        transport_order = get_object_or_404(TransportOrder, pk=movement_id)
        return render(request, 'app1/delete_transport_order.html', {'transport_order': transport_order})

    def post(self, request, movement_id):
        transport_order = get_object_or_404(TransportOrder, pk=movement_id)
        try:
            transport_order.delete()
            return JsonResponse({'success': True, 'message': 'Transport order deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class ServiceOrderDeleteView(View):
    def get(self, request, service_id):
        service_order = get_object_or_404(ServiceOrder, pk=service_id)
        return render(request, 'app1/delete_service_order.html', {'service_order': service_order})

    def post(self, request, service_id):
        service_order = get_object_or_404(ServiceOrder, pk=service_id)
        try:
            service_order.delete()
            return JsonResponse({'success': True, 'message': 'Service order deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteDeliveryChallanView(View):
    def get(self, request, delivery_challan_id):
        delivery_challan = get_object_or_404(DeliveryChallan, pk=delivery_challan_id)
        return render(request, 'app1/delete_delivery_challan.html', {'delivery_challan': delivery_challan})

    def post(self, request, delivery_challan_id):
        delivery_challan = get_object_or_404(DeliveryChallan, pk=delivery_challan_id)
        try:
            delivery_challan.delete()
            return JsonResponse({'success': True, 'message': 'Delivery challan deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteCalibrationReportView(View):
    def get(self, request, calibration_report_id):
        calibration_report = get_object_or_404(CalibrationReport, pk=calibration_report_id)
        return render(request, 'app1/delete_calibration_report.html', {'calibration_report': calibration_report})

    def post(self, request, calibration_report_id):
        calibration_report = get_object_or_404(CalibrationReport, pk=calibration_report_id)
        try:
            calibration_report.delete()
            return JsonResponse({'success': True, 'message': 'Calibration report deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteShedToolsView(View):
    def get(self, request, shedtool_id):
        shed_tool = get_object_or_404(ShedTools, pk=shedtool_id)
        return render(request, 'app1/delete_shed_tool.html', {'shed_tool': shed_tool})

    def post(self, request, shedtool_id):
        shed_tool = get_object_or_404(ShedTools, pk=shedtool_id)
        try:
            shed_tool.delete()
            return JsonResponse({'success': True, 'message': 'Shed tool deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteTransportToolsView(View):
    def get(self, request, transporttool_id):
        transport_tool = get_object_or_404(TransportTools, pk=transporttool_id)
        return render(request, 'app1/delete_transport_tool.html', {'transport_tool': transport_tool})

    def post(self, request, transporttool_id):
        transport_tool = get_object_or_404(TransportTools, pk=transporttool_id)
        try:
            transport_tool.delete()
            return JsonResponse({'success': True, 'message': 'Transport tool deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteServiceToolsView(View):
    def get(self, request, servicetool_id):
        service_tool = get_object_or_404(ServiceTools, pk=servicetool_id)
        return render(request, 'app1/delete_service_tool.html', {'service_tool': service_tool})

    def post(self, request, servicetool_id):
        service_tool = get_object_or_404(ServiceTools, pk=servicetool_id)
        try:
            service_tool.delete()
            return JsonResponse({'success': True, 'message': 'Service tool deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteDeliveryChallanToolsView(View):
    def get(self, request, deliverychallantool_id):
        delivery_challan_tool = get_object_or_404(DeliveryChallanTools, pk=deliverychallantool_id)
        return render(request, 'app1/delete_delivery_challan_tool.html', {'delivery_challan_tool': delivery_challan_tool})

    def post(self, request, deliverychallantool_id):
        delivery_challan_tool = get_object_or_404(DeliveryChallanTools, pk=deliverychallantool_id)
        try:
            delivery_challan_tool.delete()
            return JsonResponse({'success': True, 'message': 'Delivery challan tool deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteVendorHandlesView(View):
    def get(self, request, vendorhandle_id):
        vendor_handle = get_object_or_404(VendorHandles, pk=vendorhandle_id)
        return render(request, 'app1/delete_vendor_handles.html', {'vendor_handle': vendor_handle})

    def post(self, request, vendorhandle_id):
        vendor_handle = get_object_or_404(VendorHandles, pk=vendorhandle_id)
        try:
            vendor_handle.delete()
            return JsonResponse({'success': True, 'message': 'Vendor handle deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteInstrumentGroupMasterView(View):
    def get(self, request, tool_group_id):
        instrument_group = get_object_or_404(InstrumentGroupMaster, pk=tool_group_id)
        return render(request, 'app1/delete_instrument_group.html', {'instrument_group': instrument_group})

    def post(self, request, tool_group_id):
        instrument_group = get_object_or_404(InstrumentGroupMaster, pk=tool_group_id)
        try:
            instrument_group.delete()
            return JsonResponse({'success': True, 'message': 'Instrument group deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteInstrumentFamilyGroupView(View):
    def get(self, request, instrument_family_id):
        instrument_family = get_object_or_404(InstrumentFamilyGroup, pk=instrument_family_id)
        return render(request, 'app1/delete_instrument_family_group.html', {'instrument_family': instrument_family})

    def post(self, request, instrument_family_id):
        instrument_family = get_object_or_404(InstrumentFamilyGroup, pk=instrument_family_id)
        try:
            instrument_family.delete()
            return JsonResponse({'success': True, 'message': 'Instrument family group deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteInstrumentModelView(View):
    def get(self, request, instrument_no):
        instrument_model = get_object_or_404(InstrumentModel, pk=instrument_no)
        return render(request, 'app1/delete_instrument_model.html', {'instrument_model': instrument_model})

    def post(self, request, instrument_no):
        instrument_model = get_object_or_404(InstrumentModel, pk=instrument_no)
        try:
            instrument_model.delete()
            return JsonResponse({'success': True, 'message': 'Instrument model deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteServiceTypeView(View):
    def get(self, request, servicetype_id):
        service_type = get_object_or_404(ServiceType, pk=servicetype_id)
        return render(request, 'app1/delete_service_type.html', {'service_type': service_type})

    def post(self, request, servicetype_id):
        service_type = get_object_or_404(ServiceType, pk=servicetype_id)
        try:
            service_type.delete()
            return JsonResponse({'success': True, 'message': 'Service type deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class DeleteVendorTypeView(View):
    def get(self, request, vendortype_id):
        vendor_type = get_object_or_404(VendorType, pk=vendortype_id)
        return render(request, 'app1/delete_vendor_type.html', {'vendor_type': vendor_type})

    def post(self, request, vendortype_id):
        vendor_type = get_object_or_404(VendorType, pk=vendortype_id)
        try:
            vendor_type.delete()
            return JsonResponse({'success': True, 'message': 'Vendor type deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

from datetime import datetime, timedelta
class CountOfObjects(View):
    def get(self, request, month_no):
        vendor_count = Vendor.objects.count()
        shed_count = ShedDetails.objects.count()
        instruments_count = InstrumentModel.objects.count()
        transport_order_count = TransportOrder.objects.count()
        service_order_count = ServiceOrder.objects.count()
        deliverychallan_count = DeliveryChallan.objects.count()

        # Get the current date
        current_date = timezone.now().date()

        try:
            # Calculate the start and end date of the specified month
            year = current_date.year
            if month_no < current_date.month:
                year += 1
            month_start = datetime(year, month_no, 1)
            next_month = month_start.replace(day=28) + timedelta(days=4)
            month_end = next_month - timedelta(days=next_month.day)

            # Filter tools based on the selected month
            tools_to_notify = InstrumentModel.objects.filter(
                notification_date__month=month_no,
                notification_date__year=year
            )

            tools_count = tools_to_notify.count()
            tools_list = []

            for tool in tools_to_notify:
                remaining_days = (tool.notification_date - current_date).days

                calibration_report = CalibrationReport.objects.filter(calibration_tool=tool).first()

                tools_list.append({
                    'instrument_no': tool.instrument_no,
                    'instrument_name': tool.instrument_name,
                    'notification_date': tool.notification_date,
                    'current_shed': tool.current_shed.name if tool.current_shed else None,
                    'remaining_days': remaining_days,
                    'next_calibration_date': calibration_report.next_calibration_date if calibration_report else None
                })

            data = {
                'vendor_count': vendor_count,
                'shed_count': shed_count,
                'instruments_count': instruments_count,
                'transport_order_count': transport_order_count,
                'service_order_count': service_order_count,
                'deliverychallan_count': deliverychallan_count,
                'tools_to_notify_count': tools_count,
                'tools_to_notify': tools_list
            }

            return JsonResponse({'success': True, 'data': data})

        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid month number. Use a valid month number (1-12).'}, status=400)

class UpdateInstrumentShedView(View):
    def get(self, request, *args, **kwargs):
        instruments = InstrumentModel.objects.all()
        sheds = ShedDetails.objects.all()

        updated_count = 0

        for instrument in instruments:
            found_shed = None
            for shed in sheds:
                if self.instrument_in_shed(instrument, shed):
                    found_shed = shed
                    break

            if found_shed:
                instrument.current_shed = found_shed
                instrument.save()
                updated_count += 1
            else:
                instrument.current_shed = None
                instrument.save()

        return JsonResponse({'message': f'Successfully updated {updated_count} instruments.'})

    def instrument_in_shed(self, instrument, shed):
        try:
            ShedTools.objects.get(shed=shed, using_tool=instrument)
            return True
        except ShedTools.DoesNotExist:
            return False

class InstrumentsByFamilyView(APIView):
    def get(self, request, instrument_family_id):
        instrument_family = get_object_or_404(InstrumentFamilyGroup, pk=instrument_family_id)

        tools = InstrumentGroupMaster.objects.filter(tool_family = instrument_family)
        serialized_group_instruments = InstrumentGroupMasterSerializer(tools, many=True).data

        return Response({'tool_family': instrument_family.instrument_family_name, 'tools':serialized_group_instruments})

class InstrumentsByGroupView(APIView):
    def get(self, request, tool_group_id):
        tool_group = get_object_or_404(InstrumentGroupMaster, pk=tool_group_id)

        instruments = InstrumentModel.objects.filter(type_of_tool=tool_group)
        serialized_instruments = InstrumentModelSerializer(instruments, many=True).data

        return Response({'tool_group': tool_group.tool_group_name,'instruments': serialized_instruments})

class PendingServiceOrdersByVendorView(APIView):
    def get(self, request, vendortype_id):
        vendor_type = get_object_or_404(VendorType, pk=vendortype_id)
        vendors = Vendor.objects.filter(vendor_type=vendor_type)

        pending_service_orders_by_vendor = []

        for vendor in vendors:
            pending_service_orders = ServiceOrder.objects.filter(vendor=vendor, service_pending=True)
            serialized_service_orders = ServiceOrderSerializer(pending_service_orders, many=True).data
            pending_service_orders_by_vendor.append({'vendor_id': vendor.vendor_id,'vendor_name': vendor.name,'pending_service_orders': serialized_service_orders})

        return Response(pending_service_orders_by_vendor)

class ServiceOrderPendingToolsView(View):
    def get(self, request, service_order_id):
        service_order = get_object_or_404(ServiceOrder, pk=service_order_id)
        pending_tools = ServiceTools.objects.filter(service=service_order, service_pending_tool=True)

        serializer = ServiceToolsSerializer(pending_tools, many=True)
        return JsonResponse({'success': True, 'data': serializer.data})
    
class TransportOrderPendingToolsView(View):
    def get(self, request, transport_order_id):
        transport_order = get_object_or_404(TransportOrder, pk=transport_order_id)
        pending_tools = TransportTools.objects.filter(transport=transport_order,acknowledgment=False)
        
        serializer = TransportToolsSerializer(pending_tools, many=True)
        return JsonResponse({'success': True, 'data': serializer.data})

# @method_decorator(csrf_exempt, name='dispatch')
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            body_data = json.loads(request.body)
            username = body_data.get('username')
            password = body_data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Logged in successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password'}, status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'app1/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# @method_decorator(csrf_exempt, name='dispatch')
# class UpdateShedDetailsView(View):

#     def get(self, request, shed_id):
#         shed = get_object_or_404(ShedDetails, pk=shed_id)
#         shed_data = {'shed_id': shed.shed_id,'name': shed.name,'location': shed.location,'phone_number': shed.phone_number}
#         return JsonResponse({'success': True, 'data': shed_data})

#     def post(self, request, shed_id):
#         shed = get_object_or_404(ShedDetails, pk=shed_id)
#         body_data = json.loads(request.body)

#         name = body_data.get('name')
#         location = body_data.get('location')
#         phone_number = body_data.get('phone_number')
#         password = body_data.get('password1')

#         updated_fields = {}
#         if name is not None:
#             updated_fields['name'] = name
#         if location is not None:
#             updated_fields['location'] = location
#         if phone_number is not None:
#             updated_fields['phone_number'] = phone_number
#         if password is not None:
#             updated_fields['password'] = password

#         if updated_fields:
#             try:
#                 ShedDetails.objects.filter(pk=shed_id).update(**updated_fields)
                
#                 if 'password' in updated_fields:
#                     try:
#                         user = User.objects.get(username=shed.name)
#                         user.set_password(updated_fields['password'])
#                         user.save()
#                     except User.DoesNotExist:
#                         return JsonResponse({'success': False, 'message': 'User does not exist'}, status=400)

#                 return JsonResponse({'success': True, 'message': 'Shed details updated successfully'})
#             except IntegrityError:
#                 return JsonResponse({'success': False, 'message': 'Shed name already exists'}, status=400)
#         else:
#             return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class UpdateShedDetailsView(View):

    def get(self, request, shed_id):
        shed = get_object_or_404(ShedDetails, pk=shed_id)
        shed_data = {
            'shed_id': shed.shed_id,
            'name': shed.name,
            'location': shed.location,
            'phone_number': shed.phone_number
        }
        return JsonResponse({'success': True, 'data': shed_data})

    def post(self, request, shed_id):
        shed = get_object_or_404(ShedDetails, pk=shed_id)
        if request.content_type == 'application/json':
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        else:
            body_data = request.POST

        name = body_data.get('name')
        location = body_data.get('location')
        phone_number = body_data.get('phone_number')
        password = body_data.get('password1')

        updated_fields = {}
        if name is not None:
            updated_fields['name'] = name
        if location is not None:
            updated_fields['location'] = location
        if phone_number is not None:
            updated_fields['phone_number'] = phone_number
        if password is not None:
            updated_fields['password'] = password

        if updated_fields:
            try:
                ShedDetails.objects.filter(pk=shed_id).update(**updated_fields)
                
                if 'password' in updated_fields:
                    try:
                        user = User.objects.get(username=shed.name)
                        user.set_password(updated_fields['password'])
                        user.save()
                    except User.DoesNotExist:
                        return JsonResponse({'success': False, 'message': 'User does not exist'}, status=400)

                return JsonResponse({'success': True, 'message': 'Shed details updated successfully'})
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'Shed name already exists'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateShedToolsView(View):
    def get(self, request, shedtool_id):
        shed_tool = get_object_or_404(ShedTools, pk=shedtool_id)
        return JsonResponse({'success': True, 'data': {
            'shedtool_id': shed_tool.shedtool_id,
            'shed': shed_tool.shed_id,
            'using_tool': shed_tool.using_tool_id
        }})

    def post(self, request, shedtool_id):
        shed_tool = get_object_or_404(ShedTools, pk=shedtool_id)
        body_data = json.loads(request.body)

        shed_id = body_data.get('shed')
        using_tool_id = body_data.get('using_tool')

        updated_fields = {}
        if shed_id is not None:
            shed = get_object_or_404(ShedDetails, pk=shed_id)
            updated_fields['shed'] = shed
        if using_tool_id is not None:
            using_tool = get_object_or_404(InstrumentModel, pk=using_tool_id)
            updated_fields['using_tool'] = using_tool

        if updated_fields:
            try:
                ShedTools.objects.filter(pk=shedtool_id).update(**updated_fields)
                return JsonResponse({'success': True, 'message': 'Shed tool details updated successfully'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateVendorView(View):

    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vendor_data = {
            'vendor_id': vendor.vendor_id,
            'name': vendor.name,
            'location': vendor.location,
            'address': vendor.address,
            'phone_number': vendor.phone_number,
            'email': vendor.email,
            'nabl_number': vendor.nabl_number,
            'nabl_certificate': vendor.nabl_certificate.url if vendor.nabl_certificate else None,
            'vendor_type': vendor.vendor_type_id
        }
        return JsonResponse({'success': True, 'data': vendor_data})

    def post(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)

        if request.content_type == 'application/json':
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

            name = body_data.get('name')
            location = body_data.get('location')
            address = body_data.get('address')
            phone_number = body_data.get('phone_number')
            email = body_data.get('email')
            nabl_number = body_data.get('nabl_number')
            vendor_type_id = body_data.get('vendor_type')

            updated_fields = {}
            if name is not None:
                updated_fields['name'] = name
            if location is not None:
                updated_fields['location'] = location
            if address is not None:
                updated_fields['address'] = address
            if phone_number is not None:
                updated_fields['phone_number'] = phone_number
            if email is not None:
                updated_fields['email'] = email
            if nabl_number is not None:
                updated_fields['nabl_number'] = nabl_number
            if vendor_type_id is not None:
                try:
                    vendor_type = VendorType.objects.get(pk=vendor_type_id)
                    updated_fields['vendor_type'] = vendor_type
                except VendorType.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Invalid VendorType ID'}, status=400)

            if updated_fields:
                try:
                    Vendor.objects.filter(pk=vendor_id).update(**updated_fields)
                    return JsonResponse({'success': True, 'message': 'Vendor details updated successfully'})
                except IntegrityError as e:
                    if 'UNIQUE constraint failed' in str(e):
                        return JsonResponse({'success': False, 'message': 'Vendor with this data already exists'}, status=400)
                    else:
                        return JsonResponse({'success': False, 'message': 'An error occurred while updating the vendor'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

        else:
            form = VendorForm(request.POST, request.FILES, instance=vendor)
            if form.is_valid():
                try:
                    form.save()
                    return JsonResponse({'success': True, 'message': 'Vendor details updated successfully'})
                except IntegrityError as e:
                    if 'UNIQUE constraint failed' in str(e):
                        return JsonResponse({'success': False, 'message': 'Vendor with this data already exists'}, status=400)
                    else:
                        return JsonResponse({'success': False, 'message': 'An error occurred while updating the vendor'}, status=400)
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'errors': errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateInstrumentGroupMasterView(View):

    def get(self, request, tool_group_id):
        group = get_object_or_404(InstrumentGroupMaster, pk=tool_group_id)
        group_data = {
            'tool_group_id': group.tool_group_id,
            'tool_group_name': group.tool_group_name,
            'tool_group_code': group.tool_group_code
        }
        return JsonResponse({'success': True, 'data': group_data})

    def post(self, request, tool_group_id):
        group = get_object_or_404(InstrumentGroupMaster, pk=tool_group_id)
        body_data = json.loads(request.body)

        tool_group_name = body_data.get('tool_group_name')
        tool_group_code = body_data.get('tool_group_code')

        updated_fields = {}
        if tool_group_name is not None:
            updated_fields['tool_group_name'] = tool_group_name
        if tool_group_code is not None:
            updated_fields['tool_group_code'] = tool_group_code

        if updated_fields:
            try:
                InstrumentGroupMaster.objects.filter(pk=tool_group_id).update(**updated_fields)
                return JsonResponse({'success': True, 'message': 'Instrument group details updated successfully'})
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return JsonResponse({'success': False, 'message': 'Instrument group name or code already exists'}, status=400)
                else:
                    return JsonResponse({'success': False, 'message': 'An error occurred'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateInstrumentFamilyGroupView(View):

    def get(self, request, instrument_family_id):
        family = get_object_or_404(InstrumentFamilyGroup, pk=instrument_family_id)
        family_data = {
            'instrument_family_id': family.instrument_family_id,
            'instrument_family_name': family.instrument_family_name,
            'instrument_group_master': family.instrument_group_master_id
        }
        return JsonResponse({'success': True, 'data': family_data})

    def post(self, request, instrument_family_id):
        family = get_object_or_404(InstrumentFamilyGroup, pk=instrument_family_id)
        body_data = json.loads(request.body)

        instrument_family_name = body_data.get('instrument_family_name')
        instrument_group_master_id = body_data.get('instrument_group_master')

        updated_fields = {}
        if instrument_family_name is not None:
            updated_fields['instrument_family_name'] = instrument_family_name
        if instrument_group_master_id is not None:
            updated_fields['instrument_group_master_id'] = instrument_group_master_id

        if updated_fields:
            if 'instrument_family_name' in updated_fields:
                if InstrumentFamilyGroup.objects.exclude(pk=instrument_family_id).filter(
                    instrument_family_name=updated_fields['instrument_family_name']
                ).exists():
                    return JsonResponse({'success': False, 'message': 'Instrument family name already exists'}, status=400)
            
            try:
                InstrumentFamilyGroup.objects.filter(pk=instrument_family_id).update(**updated_fields)
                return JsonResponse({'success': True, 'message': 'Instrument family group details updated successfully'})
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'An error occurred'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateInstrumentModelView(View):

    def get(self, request, instrument_no):
        instrument = get_object_or_404(InstrumentModel, pk=instrument_no)
        instrument_data = {
            'instrument_no': instrument.instrument_no,
            'instrument_name': instrument.instrument_name,
            'manufacturer_name': instrument.manufacturer_name,
            'year_of_purchase': instrument.year_of_purchase,
            'gst': instrument.gst,
            'description': instrument.description,
            'instrument_range': instrument.instrument_range,
            'least_count': instrument.least_count,
            'type_of_tool': instrument.type_of_tool_id,
            'calibration_frequency': instrument.calibration_frequency,
            'service_status': instrument.service_status,
            'current_shed': instrument.current_shed_id
        }
        return JsonResponse({'success': True, 'data': instrument_data})

    def post(self, request, instrument_no):
        instrument = get_object_or_404(InstrumentModel, pk=instrument_no)
        body_data = json.loads(request.body)

        instrument_name = body_data.get('instrument_name')
        manufacturer_name = body_data.get('manufacturer_name')
        year_of_purchase = body_data.get('year_of_purchase')
        gst = body_data.get('gst')
        description = body_data.get('description')
        instrument_range = body_data.get('instrument_range')
        least_count = body_data.get('least_count')
        type_of_tool_id = body_data.get('type_of_tool_id')
        calibration_frequency = body_data.get('calibration_frequency')
        current_shed = body_data.get('shed_id')

        updated_fields = {}
        if instrument_name is not None:
            updated_fields['instrument_name'] = instrument_name
        if manufacturer_name is not None:
            updated_fields['manufacturer_name'] = manufacturer_name
        if year_of_purchase is not None:
            updated_fields['year_of_purchase'] = year_of_purchase
        if gst is not None:
            updated_fields['gst'] = gst
        if description is not None:
            updated_fields['description'] = description
        if instrument_range is not None:
            updated_fields['instrument_range'] = instrument_range
        if least_count is not None:
            updated_fields['least_count'] = least_count
        if type_of_tool_id is not None:
            updated_fields['type_of_tool_id'] = type_of_tool_id
        if calibration_frequency is not None:
            updated_fields['calibration_frequency'] = calibration_frequency
        if current_shed is not None:
            updated_fields['current_shed'] = current_shed

        if updated_fields:
            try:
                InstrumentModel.objects.filter(pk=instrument_no).update(**updated_fields)

                if current_shed is not None:
                    new_shed = get_object_or_404(ShedDetails, pk=current_shed)
                    ShedTools.objects.update_or_create(
                        using_tool=instrument,
                        defaults={'shed': new_shed}
                    )
                return JsonResponse({'success': True, 'message': 'Instrument details updated successfully'})
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return JsonResponse({'success': False, 'message': 'Instrument name already exists'}, status=400)
                else:
                    return JsonResponse({'success': False, 'message': 'An error occurred while updating the instrument'}, status=500)
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateVendorHandlesView(View):

    def get(self, request, vendorhandle_id):
        vendor_handle = get_object_or_404(VendorHandles, pk=vendorhandle_id)
        vendor_handle_data = {
            'vendorhandle_id': vendor_handle.vendorhandle_id,
            'vendor': vendor_handle.vendor_id,
            'tool': vendor_handle.tool_id,
            'turnaround_time': vendor_handle.turnaround_time,
            'cost': vendor_handle.cost
        }
        return JsonResponse({'success': True, 'data': vendor_handle_data})

    def post(self, request, vendorhandle_id):
        vendor_handle = get_object_or_404(VendorHandles, pk=vendorhandle_id)

        if request.content_type == 'application/json':
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        else:
            body_data = request.POST

        vendor_id = body_data.get('vendor')
        tool_id = body_data.get('tool')
        turnaround_time = body_data.get('turnaround_time')
        cost = body_data.get('cost')

        updated_fields = {}
        if vendor_id is not None:
            vendor = get_object_or_404(Vendor, pk=vendor_id)
            updated_fields['vendor'] = vendor
        if tool_id is not None:
            tool = get_object_or_404(InstrumentGroupMaster, pk=tool_id)
            updated_fields['tool'] = tool
        if turnaround_time is not None:
            updated_fields['turnaround_time'] = turnaround_time
        if cost is not None:
            updated_fields['cost'] = cost

        if updated_fields:
            try:
                VendorHandles.objects.filter(pk=vendorhandle_id).update(**updated_fields)
                return JsonResponse({'success': True, 'message': 'Vendor handle details updated successfully'})
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return JsonResponse({'success': False, 'message': 'Vendor with this data already exists'}, status=400)
                else:
                    return JsonResponse({'success': False, 'message': 'An error occurred while updating the vendor handle'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTransportOrderView(View):

    def get(self, request, movement_id):
        transport_order = get_object_or_404(TransportOrder, pk=movement_id)
        transport_tools = TransportTools.objects.filter(transport=transport_order)

        tools_data = [
            {
                'tool': tool.tool_id,
                'tool_movement_remarks': tool.tool_movement_remarks,
                'acknowledgment': tool.acknowledgment
            }
            for tool in transport_tools
        ]

        transport_order_data = {
            'movement_id': transport_order.movement_id,
            'movement_date': transport_order.movement_date,
            'source_shed': transport_order.source_shed_id,
            'destination_shed': transport_order.destination_shed_id,
            'acknowledgment': transport_order.acknowledgment,
            'tool_count': transport_order.tool_count,
            'tools': tools_data,
            'created_at': transport_order.created_at,
            'updated_at': transport_order.updated_at
        }
        return JsonResponse({'success': True, 'data': transport_order_data})

    @transaction.atomic
    def post(self, request, movement_id):
        transport_order = get_object_or_404(TransportOrder, pk=movement_id)
        body_data = json.loads(request.body)

        movement_date = body_data.get('movement_date')
        source_shed_id = body_data.get('source_shed')
        destination_shed_id = body_data.get('destination_shed')
        acknowledgment = body_data.get('acknowledgment')
        tool_count = body_data.get('tool_count')
        tools_data = body_data.get('tools', [])

        updated_fields = {}
        if movement_date is not None:
            updated_fields['movement_date'] = movement_date
        if source_shed_id is not None:
            updated_fields['source_shed_id'] = source_shed_id
        if destination_shed_id is not None:
            updated_fields['destination_shed_id'] = destination_shed_id
        if acknowledgment is not None:
            updated_fields['acknowledgment'] = acknowledgment
        if tool_count is not None:
            updated_fields['tool_count'] = tool_count

        if updated_fields:
            TransportOrder.objects.filter(pk=movement_id).update(**updated_fields)

        # Update or create transport tools
        tool_ids = []
        for tool_data in tools_data:
            tool_id = tool_data.get('tool')
            tool_movement_remarks = tool_data.get('tool_movement_remarks')

            tool_instance, created = TransportTools.objects.update_or_create(
                transport=transport_order,
                tool_id=tool_id,
                defaults={'tool_movement_remarks': tool_movement_remarks}
            )
            tool_ids.append(tool_instance.transporttool_id)

        # Delete transport tools that are not in the current request
        TransportTools.objects.filter(transport=transport_order).exclude(pk__in=tool_ids).delete()

        return JsonResponse({'success': True, 'message': 'Transport order and tools updated successfully'})

@method_decorator(csrf_exempt, name='dispatch')
class UpdateTransportToolsView(View):

    def get(self, request, transporttool_id):
        transport_tool = get_object_or_404(TransportTools, pk=transporttool_id)
        transport_tool_data = {
            'transporttool_id': transport_tool.transporttool_id,
            'transport': transport_tool.transport_id,
            'tool': transport_tool.tool_id,
            'tool_movement_remarks': transport_tool.tool_movement_remarks,
            'acknowledgment': transport_tool.acknowledgment
        }
        return JsonResponse({'success': True, 'data': transport_tool_data})

    def post(self, request, transporttool_id):
        transport_tool = get_object_or_404(TransportTools, pk=transporttool_id)
        body_data = json.loads(request.body)

        transport = body_data.get('transport')
        tool = body_data.get('tool')
        tool_movement_remarks = body_data.get('tool_movement_remarks')
        acknowledgment = body_data.get('acknowledgment')

        updated_fields = {}
        if transport is not None:
            updated_fields['transport_id'] = transport
        if tool is not None:
            updated_fields['tool_id'] = tool
        if tool_movement_remarks is not None:
            updated_fields['tool_movement_remarks'] = tool_movement_remarks
        if acknowledgment is not None:
            updated_fields['acknowledgment'] = acknowledgment

        if updated_fields:
            TransportTools.objects.filter(pk=transporttool_id).update(**updated_fields)
            return JsonResponse({'success': True, 'message': 'Transport tool details updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateServiceOrderView(View):

    def get(self, request, service_id):
        service_order = get_object_or_404(ServiceOrder, pk=service_id)
        service_tools = ServiceTools.objects.filter(service=service_order)

        tools_data = [
            {
                'tool': tool.tool_id,
                'vendor': tool.vendor_id,
                'service_type': tool.service_type_id,
                'service_remarks': tool.service_remarks,
                'service_pending_tool': tool.service_pending_tool
            }
            for tool in service_tools
        ]

        service_order_data = {
            'service_id': service_order.service_id,
            'date': service_order.date,
            'amount': service_order.amount,
            'description': service_order.description,
            'tool_count': service_order.tool_count,
            'vendor': service_order.vendor_id,
            'service_pending': service_order.service_pending,
            'tools': tools_data,
            'created_at': service_order.created_at,
            'updated_at': service_order.updated_at
        }
        return JsonResponse({'success': True, 'data': service_order_data})

    @transaction.atomic
    def post(self, request, service_id):
        service_order = get_object_or_404(ServiceOrder, pk=service_id)
        body_data = json.loads(request.body)

        date = body_data.get('date')
        amount = body_data.get('amount')
        description = body_data.get('description')
        tool_count = body_data.get('tool_count')
        vendor_id = body_data.get('vendor')
        service_pending = body_data.get('service_pending')
        tools_data = body_data.get('tools', [])

        updated_fields = {}
        if date is not None:
            updated_fields['date'] = date
        if amount is not None:
            updated_fields['amount'] = amount
        if description is not None:
            updated_fields['description'] = description
        if tool_count is not None:
            updated_fields['tool_count'] = tool_count
        if vendor_id is not None:
            vendor = get_object_or_404(Vendor, pk=vendor_id)
            updated_fields['vendor'] = vendor

        if updated_fields:
            ServiceOrder.objects.filter(pk=service_id).update(**updated_fields)

        # Update or create service tools
        tool_ids = []
        for tool_data in tools_data:
            tool_id = tool_data.get('tool')
            vendor_id = tool_data.get('vendor')
            service_type_id = tool_data.get('service_type')
            service_remarks = tool_data.get('service_remarks')

            vendor = get_object_or_404(Vendor, pk=vendor_id)
            service_type = get_object_or_404(ServiceType, pk=service_type_id)
            tool = get_object_or_404(InstrumentModel, pk=tool_id)

            tool_instance, created = ServiceTools.objects.update_or_create(
                service=service_order,
                tool=tool,
                vendor=vendor,
                defaults={
                    'service_type': service_type,
                    'service_remarks': service_remarks,
                }
            )
            tool_ids.append(tool_instance.servicetool_id)

        # Delete service tools that are not in the current request
        ServiceTools.objects.filter(service=service_order).exclude(pk__in=tool_ids).delete()

        return JsonResponse({'success': True, 'message': 'Service order and tools updated successfully'})

@method_decorator(csrf_exempt, name='dispatch')
class UpdateServiceToolsView(View):

    def get(self, request, servicetool_id):
        service_tool = get_object_or_404(ServiceTools, pk=servicetool_id)
        service_tool_data = {
            'servicetool_id': service_tool.servicetool_id,
            'service': service_tool.service_id,
            'tool': service_tool.tool_id,
            'vendor': service_tool.vendor_id,
            'service_type': service_tool.service_type_id,
            'service_remarks': service_tool.service_remarks,
            'service_pending_tool': service_tool.service_pending_tool
        }
        return JsonResponse({'success': True, 'data': service_tool_data})

    def post(self, request, servicetool_id):
        service_tool = get_object_or_404(ServiceTools, pk=servicetool_id)
        body_data = json.loads(request.body)

        service = body_data.get('service')
        tool = body_data.get('tool')
        vendor = body_data.get('vendor')
        service_type = body_data.get('service_type')
        service_remarks = body_data.get('service_remarks')
        service_pending_tool = body_data.get('service_pending_tool')

        updated_fields = {}
        if service is not None:
            updated_fields['service_id'] = service
        if tool is not None:
            updated_fields['tool_id'] = tool
        if vendor is not None:
            updated_fields['vendor_id'] = vendor
        if service_type is not None:
            updated_fields['service_type_id'] = service_type
        if service_remarks is not None:
            updated_fields['service_remarks'] = service_remarks
        if service_pending_tool is not None:
            updated_fields['service_pending_tool'] = service_pending_tool

        if updated_fields:
            ServiceTools.objects.filter(pk=servicetool_id).update(**updated_fields)
            return JsonResponse({'success': True, 'message': 'Service tool details updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateDeliveryChallanView(View):

    def get(self, request, deliverychallan_id):
        delivery_challan = get_object_or_404(DeliveryChallan, pk=deliverychallan_id)
        delivery_challan_data = {
            'deliverychallan_id': delivery_challan.deliverychallan_id,
            'received_date': delivery_challan.received_date,
            'vendor': delivery_challan.vendor_id,
            'shed': delivery_challan.shed_id,
            'service': delivery_challan.service_id,
        }
        return JsonResponse({'success': True, 'data': delivery_challan_data})

    def post(self, request, deliverychallan_id):
        delivery_challan = get_object_or_404(DeliveryChallan, pk=deliverychallan_id)
        body_data = json.loads(request.body)

        received_date = body_data.get('received_date')
        vendor = body_data.get('vendor')
        shed = body_data.get('shed')
        service = body_data.get('service')

        updated_fields = {}
        if received_date is not None:
            updated_fields['received_date'] = received_date
        if vendor is not None:
            updated_fields['vendor_id'] = vendor
        if shed is not None:
            updated_fields['shed_id'] = shed
        if service is not None:
            updated_fields['service_id'] = service

        if updated_fields:
            DeliveryChallan.objects.filter(pk=deliverychallan_id).update(**updated_fields)
            return JsonResponse({'success': True, 'message': 'Delivery challan details updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateCalibrationReportView(View):

    def get(self, request, calibrationtool_id):
        calibration_report = get_object_or_404(CalibrationReport, pk=calibrationtool_id)
        calibration_report_data = {
            'calibrationtool_id': calibration_report.calibrationtool_id,
            'calibration_tool': calibration_report.calibration_tool_id,
            'calibration_date': calibration_report.calibration_date,
            'calibration_report_no': calibration_report.calibration_report_no,
            'calibration_agency': calibration_report.calibration_agency,
            'result': calibration_report.result,
            'action': calibration_report.action,
            'next_calibration_date': calibration_report.next_calibration_date,
            'notification_date': calibration_report.notification_date,
            'remark': calibration_report.remark,
        }
        return JsonResponse({'success': True, 'data': calibration_report_data})

    def post(self, request, calibrationtool_id):
        calibration_report = get_object_or_404(CalibrationReport, pk=calibrationtool_id)
        body_data = json.loads(request.body)

        calibration_tool = body_data.get('calibration_tool')
        calibration_date = body_data.get('calibration_date')
        calibration_report_no = body_data.get('calibration_report_no')
        calibration_agency = body_data.get('calibration_agency')
        result = body_data.get('result')
        action = body_data.get('action')
        next_calibration_date = body_data.get('next_calibration_date')
        notification_date = body_data.get('notification_date')
        remark = body_data.get('remark')

        updated_fields = {}
        if calibration_tool is not None:
            updated_fields['calibration_tool_id'] = calibration_tool
        if calibration_date is not None:
            updated_fields['calibration_date'] = calibration_date
        if calibration_report_no is not None:
            updated_fields['calibration_report_no'] = calibration_report_no
        if calibration_agency is not None:
            updated_fields['calibration_agency'] = calibration_agency
        if result is not None:
            updated_fields['result'] = result
        if action is not None:
            updated_fields['action'] = action
        if next_calibration_date is not None:
            updated_fields['next_calibration_date'] = next_calibration_date
        if notification_date is not None:
            updated_fields['notification_date'] = notification_date
        if remark is not None:
            updated_fields['remark'] = remark

        if updated_fields:
            CalibrationReport.objects.filter(pk=calibrationtool_id).update(**updated_fields)
            return JsonResponse({'success': True, 'message': 'Calibration report details updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateDeliveryChallanToolsView(View):

    def get(self, request, deliverychallantool_id):
        delivery_challan_tool = get_object_or_404(DeliveryChallanTools, pk=deliverychallantool_id)
        delivery_challan_tool_data = {
            'deliverychallantool_id': delivery_challan_tool.deliverychallantool_id,
            'deliverychallan': delivery_challan_tool.deliverychallan_id,
            'tool': delivery_challan_tool.tool_id,
            'calibration_report': delivery_challan_tool.calibration_report_id,
        }
        return JsonResponse({'success': True, 'data': delivery_challan_tool_data})

    def post(self, request, deliverychallantool_id):
        delivery_challan_tool = get_object_or_404(DeliveryChallanTools, pk=deliverychallantool_id)
        body_data = json.loads(request.body)

        deliverychallan = body_data.get('deliverychallan')
        tool = body_data.get('tool')
        calibration_report = body_data.get('calibration_report')

        updated_fields = {}
        if deliverychallan is not None:
            updated_fields['deliverychallan_id'] = deliverychallan
        if tool is not None:
            updated_fields['tool_id'] = tool
        if calibration_report is not None:
            updated_fields['calibration_report_id'] = calibration_report

        if updated_fields:
            DeliveryChallanTools.objects.filter(pk=deliverychallantool_id).update(**updated_fields)
            return JsonResponse({'success': True, 'message': 'Delivery challan tool details updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateAllDeliveryChallanView(View):

    def get(self, request, deliverychallan_id):
        delivery_challan = get_object_or_404(DeliveryChallan, pk=deliverychallan_id)
        delivery_challan_tools = DeliveryChallanTools.objects.filter(deliverychallan=delivery_challan)

        tools_data = [
            {
                'deliverychallantool_id': tool.deliverychallantool_id,
                'tool': tool.tool_id,
                'calibration_report': {
                    'calibrationtool_id': tool.calibration_report.calibrationtool_id,
                    'calibration_tool': tool.calibration_report.calibration_tool_id,
                    'calibration_date': tool.calibration_report.calibration_date,
                    'calibration_report_no': tool.calibration_report.calibration_report_no,
                    'calibration_agency': tool.calibration_report.calibration_agency,
                    'result': tool.calibration_report.result,
                    'action': tool.calibration_report.action,
                    'next_calibration_date': tool.calibration_report.next_calibration_date,
                    'notification_date': tool.calibration_report.notification_date,
                    'remark': tool.calibration_report.remark,
                } if tool.calibration_report else None
            }
            for tool in delivery_challan_tools
        ]

        delivery_challan_data = {
            'deliverychallan_id': delivery_challan.deliverychallan_id,
            'received_date': delivery_challan.received_date,
            'vendor': delivery_challan.vendor_id,
            'shed': delivery_challan.shed_id,
            'service': delivery_challan.service_id,
            'tools': tools_data,
            'created_at': delivery_challan.created_at,
            'updated_at': delivery_challan.updated_at
        }
        return JsonResponse({'success': True, 'data': delivery_challan_data})

    @transaction.atomic
    def post(self, request, deliverychallan_id):
        delivery_challan = get_object_or_404(DeliveryChallan, pk=deliverychallan_id)
        body_data = json.loads(request.body)

        received_date = body_data.get('receivedDate')
        vendor_id = body_data.get('vendor')
        shed_id = body_data.get('shed')
        service_id = body_data.get('service')
        tools_data = body_data.get('tools', [])

        updated_fields = {}
        if received_date is not None:
            updated_fields['received_date'] = received_date
        if vendor_id is not None:
            updated_fields['vendor_id'] = vendor_id
        if shed_id is not None:
            updated_fields['shed_id'] = shed_id
        if service_id is not None:
            updated_fields['service_id'] = service_id

        if updated_fields:
            DeliveryChallan.objects.filter(pk=deliverychallan_id).update(**updated_fields)

        # Update or create delivery challan tools and their calibration reports
        tool_ids = []
        for tool_data in tools_data:
            calibration_date = tool_data.get('calibrationDate')
            calibration_report_no = tool_data.get('calibrationReportNumber')
            calibration_agency = tool_data.get('calibrationAgency')
            result = tool_data.get('result')
            action = tool_data.get('action')
            next_calibration_date = tool_data.get('nextCalibrationDate')
            remark = tool_data.get('remark')

            tool = get_object_or_404(InstrumentModel, instrument_name=tool_data.get('toolName'))

            calibration_report, created = CalibrationReport.objects.update_or_create(
                calibration_tool=tool,
                calibration_date=calibration_date,
                defaults={
                    'calibration_report_no': calibration_report_no,
                    'calibration_agency': calibration_agency,
                    'result': result,
                    'action': action,
                    'next_calibration_date': next_calibration_date,
                    'remark': remark
                }
            )

            delivery_challan_tool, created = DeliveryChallanTools.objects.update_or_create(
                deliverychallan=delivery_challan,
                tool=tool,
                defaults={'calibration_report': calibration_report}
            )

            tool_ids.append(delivery_challan_tool.deliverychallantool_id)

        # Delete delivery challan tools that are not in the current request
        DeliveryChallanTools.objects.filter(deliverychallan=delivery_challan).exclude(pk__in=tool_ids).delete()

        return JsonResponse({'success': True, 'message': 'Delivery challan and tools updated successfully'})

@method_decorator(csrf_exempt, name='dispatch')
class UpdateServiceTypeView(View):

    def get(self, request, servicetype_id):
        service_type = get_object_or_404(ServiceType, pk=servicetype_id)
        service_type_data = {
            'servicetype_id': service_type.servicetype_id,
            'service_type': service_type.service_type,
        }
        return JsonResponse({'success': True, 'data': service_type_data})

    def post(self, request, servicetype_id):
        service_type = get_object_or_404(ServiceType, pk=servicetype_id)
        body_data = json.loads(request.body)

        service_type_value = body_data.get('service_type')

        updated_fields = {}
        if service_type_value is not None:
            updated_fields['service_type'] = service_type_value

        if updated_fields:
            ServiceType.objects.filter(pk=servicetype_id).update(**updated_fields)
            return JsonResponse({'success': True, 'message': 'Service type details updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateVendorTypeView(View):

    def get(self, request, vendortype_id):
        vendor_type = get_object_or_404(VendorType, pk=vendortype_id)
        vendor_type_data = {
            'vendortype_id': vendor_type.vendortype_id,
            'vendor_type': vendor_type.vendor_type,
        }
        return JsonResponse({'success': True, 'data': vendor_type_data})

    def post(self, request, vendortype_id):
        vendor_type = get_object_or_404(VendorType, pk=vendortype_id)
        body_data = json.loads(request.body)

        vendor_type_value = body_data.get('vendor_type')

        updated_fields = {}
        if vendor_type_value is not None:
            updated_fields['vendor_type'] = vendor_type_value

        if updated_fields:
            VendorType.objects.filter(pk=vendortype_id).update(**updated_fields)
            return JsonResponse({'success': True, 'message': 'Vendor type details updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No fields to update'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateShedNoteView(View):
    def patch(self, request, shed_id):
        try:
            shed = ShedDetails.objects.get(shed_id=shed_id)
        except ShedDetails.DoesNotExist:
            return JsonResponse({'error': 'ShedDetails not found'}, status=404)

        body_data = json.loads(request.body.decode('utf-8'))
        shed_note = body_data.get('shed_note')

        if shed_note is not None:
            shed.shed_note = shed_note
            shed.save()
            return JsonResponse({'success': True, 'message': 'Shed note updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No shed note provided'}, status=400)
        
# @method_decorator(csrf_exempt, name='dispatch')
# class UpdateShedNoteView(View):
#     def patch(self, request, shed_id):
#         try:
#             shed = ShedDetails.objects.get(shed_id=shed_id)
#         except ShedDetails.DoesNotExist:
#             return JsonResponse({'error': 'ShedDetails not found'}, status=404)

#         data = json.loads(request.body.decode('utf-8'))
        
#         serializer = ShedNoteSerializer(shed, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({'success': True, 'message': 'Shed note updated successfully'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Invalid data', 'errors': serializer.errors}, status=400)