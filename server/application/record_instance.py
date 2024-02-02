class RecordInstance:

    def __init__(self, **kwargs):
        self.fieldInstances = {}
        self.resourceType = "com.bmc.arsys.rx.services.record.domain.RecordInstance"
        self.permittedGroupsBySecurityLabels = {}
        self.permittedUsersBySecurityLabels = {}
        self.permittedRolesBySecurityLabels = {}
        self.id = kwargs.get('id', None)
        self.displayId = kwargs.get('displayId', None)
        self.recordDefinitionName = kwargs.get('recordDefinitionName', None)

    def set_field_instances(self, field_instances):
        self.fieldInstances = {}
        for fieldInstance in field_instances:
            self.fieldInstances[fieldInstance.id] = FieldInstance.to_json(fieldInstance)

    def to_json(self):
        result = {'resourceType': "com.bmc.arsys.rx.services.record.domain.RecordInstance",
                  'recordDefinitionName': self.recordDefinitionName, 'id': self.id, 'displayId': self.displayId,
                  'permittedGroupsBySecurityLabels': self.permittedGroupsBySecurityLabels,
                  'permittedUsersBySecurityLabels': self.permittedUsersBySecurityLabels,
                  'permittedRolesBySecurityLabels': self.permittedRolesBySecurityLabels,
                  'fieldInstances': self.fieldInstances}
        return result


class FieldInstance:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.value = kwargs.get('value', None)
        self.permissionType = kwargs.get('permissionType', "CHANGE")
        self.resourceType = "com.bmc.arsys.rx.services.record.domain.FieldInstance"

    @staticmethod
    def to_json(field_instance):
        return {'id': field_instance.id, 'value': field_instance.value, 'permissionType': field_instance.permissionType,
                'resourceType': "com.bmc.arsys.rx.services.record.domain.FieldInstance"}


class Attachment:
    def __init__(self, **kwargs):
        self.fieldId = kwargs['fieldId']
        self.fileName = kwargs.get('fileName')
        self.data = kwargs.get('data')

    def set_data(self, data):
        self.data = data
