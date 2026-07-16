targetScope = 'resourceGroup'

@description('Azure region for resources')
param location string = resourceGroup().location

@description('Name prefix for resources')
param namePrefix string = 'helpdesk-ai'

@description('Container image to deploy')
param containerImage string


resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: '${namePrefix}acr'
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {}
}


resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: '${namePrefix}-env'
  location: location

  properties: {}
}


resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${namePrefix}-app'
  location: location

  properties: {
    managedEnvironmentId: containerAppsEnvironment.id

    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        transport: 'http'
      }

      registries: [
        {
          server: '${containerRegistry.name}.azurecr.io'
          identity: 'system'
        }
      ]
    }

    template: {
      containers: [
        {
          name: 'helpdesk-agent'
          image: containerImage

          resources: {
            cpu: 1
            memory: '2Gi'
          }

          env: [
            {
              name: 'ENVIRONMENT'
              value: 'azure'
            }

            {
              name: 'DATABASE_PROVIDER'
              value: 'azure'
            }

            {
              name: 'INITIALIZE_LOCAL_DATA'
              value: 'false'
            }

            {
              name: 'LANGGRAPH_STRICT_MSGPACK'
              value: 'true'
            }
          ]
        }
      ]
    }
  }

  identity: {
    type: 'SystemAssigned'
  }
}


output containerRegistryName string = containerRegistry.name

output containerRegistryLoginServer string = '${containerRegistry.name}.azurecr.io'

output containerAppName string = containerApp.name

output containerAppUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
