from import_export import resources,fields
from .models import CalibrationReport, DeliveryChallan, DeliveryChallanTools, InstrumentFamilyGroup, InstrumentGroupMaster, InstrumentModel, ServiceOrder, ServiceTools, ServiceType, ShedDetails, ShedTools, TransportOrder, TransportTools, VendorHandles, VendorType, Vendor

class VendorTypeResource(resources.ModelResource):
    class Meta:
        model = VendorType
        fields = ( 'vendortype_id', 'vendor_type')
        import_id_fields = ('vendor_type',)

class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor
        fields = ('vendor_id', 'name', 'location', 'address', 'phone_number', 'email', 'nabl_number', 'nabl_certificate', 'vendor_type')
        import_id_fields = ('vendor_id',)

class InstrumentGroupMasterResource(resources.ModelResource):
    class Meta:
        model = InstrumentGroupMaster
        fields = ('tool_group_id', 'tool_group_name', 'tool_group_code', 'tool_family')
        import_id_fields = ('tool_group_id',)

class InstrumentFamilyGroupResource(resources.ModelResource):
    class Meta:
        model = InstrumentFamilyGroup
        fields = ('instrument_family_id', 'instrument_family_name')
        import_id_fields = ('instrument_family_id',)

class ShedDetailsResource(resources.ModelResource):
    class Meta:
        model = ShedDetails
        fields = ('shed_id', 'name', 'location', 'phone_number', 'password', 'shed_note')
        import_id_fields = ('shed_id',)        


class InstrumentModelResource(resources.ModelResource):
    class Meta:
        model = InstrumentModel
        fields = ('instrument_no', 'instrument_name', 'manufacturer_name', 'year_of_purchase',
                  'gst', 'description', 'instrument_range', 'least_count', 'type_of_tool',
                  'calibration_frequency', 'service_status', 'current_shed')
        import_id_fields = ('instrument_no',)

class ShedToolsResource(resources.ModelResource):
    class Meta:
        model = ShedTools
        fields = ('shedtool_id', 'shed', 'using_tool')
        import_id_fields = ('shedtool_id',)

class TransportOrderResource(resources.ModelResource):
    class Meta:
        model = TransportOrder
        fields = ('movement_id', 'movement_date', 'source_shed', 'destination_shed', 'acknowledgment', 'tool_count', 'created_at', 'updated_at')
        import_id_fields = ('movement_id',)

class TransportToolsResource(resources.ModelResource):
    class Meta:
        model = TransportTools
        fields = ('transporttool_id', 'transport', 'tool', 'tool_movement_remarks', 'acknowledgment')
        import_id_fields = ('transporttool_id',)

class ServiceTypeResource(resources.ModelResource):
    class Meta:
        model = ServiceType
        fields = ('servicetype_id', 'service_type')
        import_id_fields = ('servicetype_id',)


class ServiceOrderResource(resources.ModelResource):
    class Meta:
        model = ServiceOrder
        fields = ('service_id', 'date', 'amount', 'description', 'tool_count', 'vendor', 'service_pending', 'created_at', 'updated_at')
        import_id_fields = ('service_id',)

class ServiceToolsResource(resources.ModelResource):
   class Meta:
        model = ServiceTools
        fields = ('servicetool_id', 'service', 'tool', 'vendor', 'service_type', 'service_remarks', 'service_pending_tool')
        import_id_fields = ('servicetool_id',)

class VendorHandlesResource(resources.ModelResource):
    class Meta:
        model = VendorHandles
        fields = ('vendorhandle_id', 'vendor', 'tool', 'turnaround_time', 'cost')
        import_id_fields = ('vendorhandle_id',)

class DeliveryChallanResource(resources.ModelResource):
    class Meta:
        model = DeliveryChallan
        fields = ('deliverychallan_id', 'received_date', 'vendor', 'shed', 'service', 'created_at', 'updated_at')
        import_id_fields = ('deliverychallan_id',)

class CalibrationReportResource(resources.ModelResource):
    class Meta:
        model = CalibrationReport
        fields = ('calibrationtool_id', 'calibration_tool', 'calibration_date', 'calibration_report_no',
                  'calibration_agency', 'result', 'action', 'next_calibration_date', 'notification_date',
                  'remark', 'calibration_report_file', 'calibration_report_file2')
        import_id_fields = ('calibrationtool_id',)

      
class DeliveryChallanToolsResource(resources.ModelResource):
    class Meta:
        model = DeliveryChallanTools
        fields = ('deliverychallantool_id', 'deliverychallan', 'tool', 'calibration_report')
        import_id_fields = ('deliverychallantool_id',)  

        