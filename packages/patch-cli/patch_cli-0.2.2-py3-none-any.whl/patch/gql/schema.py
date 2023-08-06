from sgqlc.types import Type, Field, Union, list_of, non_null, ArgDict, Input, Enum
from sgqlc.types.datetime import DateTime


class ScalarBoolean(Type):
    boolValue = non_null(bool)


class ScalarInt(Type):
    intValue = non_null(int)


class ScalarString(Type):
    stringValue = non_null(str)


class TableColumnInfoValue(Union):
    __types__ = (ScalarInt, ScalarBoolean, ScalarString)


class TableColumnInfo(Type):
    name = non_null(str)
    value = TableColumnInfoValue


class TableColumnDescription(Type):
    name = non_null(str)
    description = str
    type = non_null(str)
    nullable = non_null(bool)
    index = int
    extra = non_null(list_of(non_null(TableColumnInfo)))


class TableStateEnum(Enum):
    __choices__ = ("INIT", "LOADING", "READY", "ERROR", "DELETING")


class TableDescription(Type):
    id = non_null(str)
    name = non_null(str)
    database = non_null(str)
    schema = non_null(str)
    type = non_null(str)
    description = str
    columns = non_null(list_of(non_null(TableColumnDescription)))
    sizeBytes = int
    rowCount = int


class SourceDescription(Type):
    id = non_null(str)
    namespace = non_null(list_of(non_null(str)))
    tables = non_null(list_of(non_null(TableDescription)))
    quota = int
    quotaUsed = int


class User(Type):
    id = non_null(str)
    login = non_null(str)
    fullName = str
    loggedIn = bool
    tenantId = non_null(str)


class CurrentUser(Type):
    id = non_null(str)
    login = non_null(str)
    fullName = str
    loggedIn = bool
    tenant = non_null('Tenant')


class Tenant(Type):
    id = non_null(str)
    name = non_null(str)
    isMultiTenant = non_null(bool)
    users = non_null(list_of(non_null('User')))
    quota = int
    quotaUsed = int


class Source(Type):
    id = non_null(str)
    name = non_null(str)


class DatasetTableColumn(Type):
    name = non_null(str)

class TableEdgeOnColumns(Type):
    fromColumnName = non_null(str)
    toColumnName = non_null(str)

class TableEdge(Type):
    name = non_null(str)
    fromTableId = non_null(str)
    toTableId = non_null(str)
    onColumns = non_null(list_of(non_null(TableEdgeOnColumns)))
    unique = bool

class DatasetTable(Type):
    id = non_null(str)
    qualifiedTableIdentifier = non_null(str)
    name = non_null(str)
    primaryKey = non_null(list_of(non_null(DatasetTableColumn)))
    tableState = non_null(TableStateEnum)
    lastRowCount = int
    edges = list_of(non_null(TableEdge))
    lastSyncAt = DateTime
    lastCdcSuccessTimeAgo = str 

class Dataset(Type):
    id = non_null(str)
    name = non_null(str)
    tables = non_null(list_of(non_null('DatasetTable')))


class QueryAuth(Type):
    accessToken = non_null(str)


class DataAccessKey(Type):
    id = non_null(str)
    name = non_null(str)
    sourceId = non_null(str)
    datasetName = non_null(str)
    createdAt = non_null(str)
    accessKey = non_null(str)


class RecordInspectionColumn(Type):
    name = non_null(str)
    value = str


class RecordInspectionSpec(Type):
    columns = non_null(list_of(non_null('RecordInspectionColumn')))


class RecordInspection(Type):
    sourceRecordCount = non_null(int)
    sourceRecords = non_null(list_of(non_null(RecordInspectionSpec)))
    cacheRecord = RecordInspectionSpec


class SourceDisconnectInput(Input):
    name = non_null(str)


class CreateDatasetTableIngestModeEnum(Enum):
    __choices__ = ("ONCE", "CONTINUOUS")


class CreateDatasetTableColumnInput(Input):
    columnName = non_null(str)


class CreateObjectStorageTableInput(Input):
    prefix = str
    filePattern = str


class CreateDatasetTableInput(Input):
    tableId = non_null(str)
    primaryKeys = non_null(list_of(non_null(CreateDatasetTableColumnInput)))
    ingestMode = CreateDatasetTableIngestModeEnum
    objectStorage = CreateObjectStorageTableInput


class CreateDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)
    tables = non_null(list_of(non_null(CreateDatasetTableInput)))

class TableEdgeOnColumnsInput(Input):
    fromColumnName = non_null(str)
    toColumnName = non_null(str)

class TableEdgeInput(Input):
    name = non_null(str)
    fromTableId = non_null(str)
    toTableId = non_null(str)
    onColumns = non_null(list_of(non_null(TableEdgeOnColumnsInput)))
    unique = bool

class GetSourceStatusInput(Input):
    name = non_null(str)


class SourceConnectionSnowflakeInput(Input):
    name = non_null(str)
    user = non_null(str)
    password = non_null(str)
    host = non_null(str)
    warehouse = non_null(str)
    database = non_null(str)
    schema = non_null(str)
    stagingDatabase = str


class GetSourceListInput(Input):
    sourceName = str


class SourceConnectionAzureBlobInput(Input):
    name = non_null(str)
    containerName = non_null(str)
    accountName = non_null(str)
    sasToken = str


class SourceConnectionBigQueryInput(Input):
    name = non_null(str)
    credentialsKey = non_null(str)
    projectId = non_null(str)
    location = str
    dataset = str
    stagingProjectId = non_null(str)


class RegisterUserInput(Input):
    phone = non_null(str)
    tenantId = str
    fullName = str
    isMultiTenant = non_null(bool)


class UnregisterUserInput(Input):
    userId = non_null(str)


class UpdateUserInput(Input):
    userId = non_null(str)
    fullName = str


class UpdateTenantInput(Input):
    tenantId = non_null(str)
    name = str
    quota = int


class CreateTenantInput(Input):
    name = str
    quota = int


class DeleteTenantInput(Input):
    tenantId = non_null(str)


class GetTenantsInput(Input):
    pass


class DatasetByNameInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)


class SyncDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = str
    datasetId = str
    tableName = str


class DatasetsInput(Input):
    sourceId = non_null(str)


class DataAccessKeysInput(Input):
    showKey = bool
    sourceId = str
    datasetName = str


class RemoveDatasetInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)


class GenerateQueryAuthFilterInput(Input):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class GenerateQueryAuthInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)
    filters = list_of(non_null(GenerateQueryAuthFilterInput))


class RevokeDataAccessKeyInput(Input):
    dataAccessKeyId = non_null(str)


class GenerateDataAccessKeyFilterInput(Input):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class GenerateDataAccessKeyInput(Input):
    name = non_null(str)
    sourceId = non_null(str)
    datasetName = non_null(str)
    filters = list_of(non_null(GenerateDataAccessKeyFilterInput))


class RecordInspectionColumnInput(Input):
    name = non_null(str)
    value = non_null(str)


class RecordInspectionInput(Input):
    sourceId = non_null(str)
    datasetName = non_null(str)
    tableName = non_null(str)
    primaryKey = non_null(list_of(non_null('RecordInspectionColumnInput')))


class CustomSigningTemplateFilter(Type):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class CustomSigningTemplateJwk(Type):
    kid = non_null(str)


class CustomSigningTemplate(Type):
    id = non_null(str)
    name = non_null(str)
    sourceId = str
    datasetName = str
    jwks = non_null(list_of(non_null(CustomSigningTemplateJwk)))
    filters = non_null(list_of(non_null(CustomSigningTemplateFilter)))


class CustomSigningTemplateFilterInput(Input):
    tableName = non_null(str)
    columnName = non_null(str)
    value = non_null(str)


class CreateCustomSigningTemplateInput(Input):
    name = non_null(str)
    jwk = non_null(str)
    sourceId = str
    datasetName = str
    filters = non_null(list_of(non_null(CustomSigningTemplateFilterInput)))


class DeleteCustomSigningTemplateInput(Input):
    customSigningTemplateId = non_null(str)


class Query(Type):
    getSourceList = Field(non_null(list_of(non_null(Source))), args=ArgDict({
        'input': non_null(GetSourceListInput)
    }))
    getSourceDescription = Field(non_null(SourceDescription), args=ArgDict({
        'id': non_null(str)
    }))
    getSourceStatus = Field(non_null(bool), args=ArgDict({
        'input': non_null(GetSourceStatusInput)
    }))
    getTenants = Field(non_null(list_of(non_null('Tenant'))))

    dataset = Field('Dataset', args=ArgDict({
        'id': non_null(str)
    }))
    datasetByName = Field('Dataset', args=ArgDict({
        'input': 'DatasetByNameInput'
    }))
    datasets = Field(non_null(list_of(non_null('Dataset'))), args=ArgDict({
        'input': 'DatasetsInput'
    }))
    user = Field(non_null('User'), args=ArgDict({
        'id': non_null(str)
    }))
    currentUser = Field(non_null('CurrentUser'))
    recordInspection = Field(non_null('RecordInspection'), args=ArgDict({
        'input': non_null('RecordInspectionInput')
    }))
    dataAccessKeys = Field(non_null(list_of(non_null('DataAccessKey'))), args=ArgDict({
        'input': 'DataAccessKeysInput'
    }))
    dataAccessKey = Field(non_null('DataAccessKey'), args=ArgDict({
        'id': non_null(str)
    }))
    listCustomSigningTemplates = Field(non_null(list_of(non_null('CustomSigningTemplate'))))


class Mutation(Type):
    sourceConnectAzureBlob = Field(non_null(Source), args=ArgDict({
        'input': non_null(SourceConnectionAzureBlobInput)
    }))
    sourceConnectBigQuery = Field(non_null(Source), args=ArgDict({
        'input': non_null(SourceConnectionBigQueryInput)
    }))
    sourceConnectSnowflake = Field(non_null(Source), args=ArgDict({
        'input': non_null(SourceConnectionSnowflakeInput)
    }))
    sourceDisconnect = Field(non_null(bool), args=ArgDict({
        'input': non_null(SourceDisconnectInput)
    }))
    createDataset = Field(non_null(bool), args=ArgDict({
        'input': non_null(CreateDatasetInput)
    }))
    createTableEdge = Field(non_null(bool), args=ArgDict({
        'input': non_null(TableEdgeInput)
    }))
    registerUser = Field(non_null('User'), args=ArgDict({
        'input': non_null('RegisterUserInput')
    }))
    unregisterUser = Field(non_null('User'), args=ArgDict({
        'input': non_null('UnregisterUserInput')
    }))
    updateUser = Field(non_null('User'), args=ArgDict({
        'input': non_null('UpdateUserInput')
    }))
    updateTenant = Field(non_null('Tenant'), args=ArgDict({
        'input': non_null('UpdateTenantInput')
    }))
    removeDataset = Field(non_null(bool), args=ArgDict({
        'input': non_null('RemoveDatasetInput')
    }))
    generateQueryAuth = Field(non_null(QueryAuth), args=ArgDict({
        'input': non_null('GenerateQueryAuthInput')
    }))
    generateDataAccessKey = Field(non_null(DataAccessKey), args=ArgDict({
        'input': non_null('GenerateDataAccessKeyInput')
    }))
    revokeDataAccessKey = Field(non_null(bool), args=ArgDict({
        'input': non_null('RevokeDataAccessKeyInput')
    }))
    syncDataset = Field(non_null(bool), args=ArgDict({
        'input': non_null('SyncDatasetInput')
    }))
    createTenant = Field(non_null('Tenant'), args=ArgDict({
        'input': non_null('CreateTenantInput')
    }))
    deleteTenant = Field(non_null(bool), args=ArgDict({
        'input': non_null('DeleteTenantInput')
    }))
    createCustomSigningTemplate = Field(non_null('CustomSigningTemplate'), args=ArgDict({
        'input': non_null('CreateCustomSigningTemplateInput')
    }))
    deleteCustomSigningTemplate = Field(non_null(bool), args=ArgDict({
        'input': non_null('DeleteCustomSigningTemplateInput')
    }))
