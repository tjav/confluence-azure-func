targetScope = 'resourceGroup'

param location string = resourceGroup().location
param kvname string = 'schaap-confunc-kv'
param storagename string = 'schaapconfuncsta'
param eventgridname string = 'schaap-confunc-grid'
param funcname string = 'schaap-confunc-function'
param workspacename string = 'schaap-confunc-law'
param appinsightname string = 'schaap-confunc-apis'
param appservicename string = 'schaap-confunc-applan'
param manageidname string = 'schaap-confunc-man-id'

module managedidentity 'modules/Microsoft.ManagedIdentity/userAssignedIdentities/deploy.bicep' = {
  name: 'deploy-managedidentity'
  params:{
    location:location
    name: manageidname
  }
}
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
    workspaceResourceId: logworkspace.outputs.resourceId
  }
}

module  appserviceplan 'modules/Microsoft.Web/serverfarms/deploy.bicep' = {
  name: 'deploy-appservice-plan'
  params: {
    name: appservicename
    location: location
    sku: {
      name: 'B1'
      tier: 'Basic'
      size: 'B1'
      family: 'B'
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
    userAssignedIdentities: {
      '${managedidentity.outputs.resourceId}': {}
    }
    appServicePlanId: appserviceplan.outputs.resourceId
  }
}

