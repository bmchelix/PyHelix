from commons.connector import Connector
from server.application.record_service import RecordServiceImpl

host_name = "https://[hostname]"
login = "[login]"
password = "[password]"
connector = Connector(host_name, login, password)
record_service = RecordServiceImpl(connector)

record_definition_name = "[rd_name]"
date_page_result = record_service.get_record_instances(record_definition_name)
print(date_page_result)

#Retrieve every record from the table, regardless of the quantity, even if it amounts to 100,000.
record_definition_name = "[rd_name]"
date_page_result = record_service.get_record_instances_bulk(record_definition_name)
print(date_page_result)

# Get Record Instances using parameters. Same parameters could be applied to
date_page_result = record_service.get_record_instances(record_definition_name,
                                                       page_size=50,
                                                       startIndex=0,
                                                       propertySelectionFields="1,2,5,379",
                                                       queryExpression="'5'=\"user\"",
                                                       sortByFields="-3"
                                                       )
print(date_page_result)

# Get Record Instance by Id
record_id = "AGGADGG8ECDC1ASIYUCTSIHOCTHUCO"
record_instance = record_service.get_record_instance(record_definition_name, record_id)
