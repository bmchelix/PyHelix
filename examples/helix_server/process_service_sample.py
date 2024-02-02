from commons.connector import Connector
from server.application.process_service import ProcessServiceImpl

host_name = "https://[hostname]"
login = "[login]"
password = "[password]"
connector = Connector(host_name, login, password)
process_service = ProcessServiceImpl(connector)

# Get process definition in user overlay, Process definition has been created in Overlay 1
process_definition = process_service.get_process_definition("bundle_id:process_name")

# Get process definition in Base overlay, Process definition has been created in Overlay 1
# Expected exception
try:
    process_definition = process_service.get_process_definition("bundle_id:process_name", request_overlay_group="0")
except Exception as e:
    print(e)

# Get 10 Process instances in bundle "bundle_id"
process_instances = process_service.get_process_instances("bundle_id", pageSize=10)

# Get 10 Process instances for process definition "bundle_id:process_name"
process_instances = process_service.get_process_instances("bundle_id", procesDefinition="bundle_id:process_name")
