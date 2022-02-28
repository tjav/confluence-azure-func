targetScope = 'resourceGroup'

param location string = resourceGroup().location
param kvname string = 'schaap-confunc-kv'
param storagename string = 'schaapconfuncsta'
param eventgridname string = 'schaap-confunc-grid'
param funcname string = 'confluence-function'
param workspacename string = 'schaap-confunc-law'
param appinsightname string = 'schaap-confunc-apis'
param appservicename string = 'schaap-confunc-applan'

module keyvault 'modules/Microsoft.KeyVault/vaults/deploy.bicep' = {
  name: 'deploy-keyvault'
  params: {
    name: kvname
    location: location
  } 
}
module storage 'modules/Microsoft.Storage/storageAccounts/deploy.bicep' = {
  name: 'deploy-storage'
  params: {
    name: storagename
    location: location
  }
}

module eventgrid 'modules/Microsoft.EventGrid/topics/deploy.bicep' = {
  name: 'deploy-eventgrid'
  params: {
    name: eventgridname
    location: location
  }
}

module logworkspace 'modules/Microsoft.OperationalInsights/workspaces/deploy.bicep' = {
  name: 'deploy-log-analytics'
  params: {
    name: workspacename
    location: location
  }
}
module appsinsights 'modules/Microsoft.Insights/components/deploy.bicep' = {
  name: 'deploy-apps-insights'
  params: {
    name: appinsightname
    location: location
    workspaceResourceId: logworkspace.outputs.logAnalyticsWorkspaceId
  }
}

module  appserviceplan 'modules/Microsoft.Web/serverfarms/deploy.bicep' = {
  name: 'deploy-appservice-plan'
  params: {
    name: appservicename
    location: location
    sku: {
      name: 'S1'
      tier: 'Standard'
      size: 'S1'
      family: 'S'
      capacity: 1
    }
    serverOS: 'Linux'
    
  }
}
module functionapp 'modules/Microsoft.Web/sites/deploy.bicep' = {
  name: 'deploy-function'
  params: {
    location: location
    kind: 'functionapp'
    name: funcname
    functionsWorkerRuntime: 'python'
    storageAccountId: storage.outputs.resourceId
    appInsightId: appsinsights.outputs.resourceId
    systemAssignedIdentity: true
    appServicePlanId: appserviceplan.outputs.resourceId
  }
}

