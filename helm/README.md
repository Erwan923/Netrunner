# Fûinjutsu Helm Chart

Ce chart Helm permet de déployer l'application Fûinjutsu sur Kubernetes.

## Prérequis

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support dans le cluster pour la persistance des données (si activée)
- Ingress controller (si l'Ingress est activé)

## Installation

```bash
# Ajouter le repo Helm (à adapter selon votre hébergement)
helm repo add fuinjutsu https://exemple.com/helm-charts/

# Mettre à jour les repos
helm repo update

# Installer le chart avec valeurs par défaut
helm install fuinjutsu fuinjutsu/fuinjutsu

# Installer avec un fichier de valeurs personnalisé
helm install fuinjutsu fuinjutsu/fuinjutsu -f values.yaml

# Installation depuis le répertoire local
helm install fuinjutsu ./helm/fuinjutsu
```

## Configuration

Le tableau suivant liste les principaux paramètres configurables du chart Fûinjutsu et leurs valeurs par défaut.

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `global.environment` | Environnement de déploiement | `production` |
| `global.persistence.enabled` | Activer la persistance des données | `true` |
| `image.repository` | Dépôt d'images Docker | `fuinjutsu` |
| `image.tag` | Tag de l'image à utiliser | `latest` |
| `cyberpunk.enabled` | Activer le déploiement Cyberpunk | `true` |
| `cyberpunk.replicaCount` | Nombre de réplicas pour Cyberpunk | `1` |
| `mcp.enabled` | Activer le déploiement MCP | `true` |
| `mcp.replicaCount` | Nombre de réplicas pour MCP | `1` |
| `proxy.enabled` | Activer le proxy Nginx | `true` |
| `apiKeys.existingSecret` | Secret Kubernetes existant contenant les clés API | `""` |
| `apiKeys.create` | Créer un secret pour les clés API | `true` |
| `apiKeys.keys.HUGGINGFACE_API_KEY` | Clé API HuggingFace | `""` |
| `apiKeys.keys.OPENAI_API_KEY` | Clé API OpenAI | `""` |
| `ingress.enabled` | Activer l'Ingress | `true` |
| `ingress.hosts[0].host` | Nom d'hôte pour l'Ingress | `fuinjutsu.local` |
| `persistence.config.size` | Taille du volume pour la configuration | `1Gi` |
| `persistence.data.size` | Taille du volume pour les données | `1Gi` |

### Gestion des clés API

Les clés API peuvent être gérées de deux façons :

1. En utilisant l'interface web de Fûinjutsu (`/mcp/` puis "Gérer les clés API")
2. En les définissant dans le fichier `values.yaml` :

```yaml
apiKeys:
  keys:
    HUGGINGFACE_API_KEY: "hf_xxxxxxxxxxxxxxxxxxxxxxxx"
    OPENAI_API_KEY: "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
    ANTHROPIC_API_KEY: "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx"
```

Pour des raisons de sécurité, il est recommandé d'utiliser un secret Kubernetes existant :

```yaml
apiKeys:
  create: false
  existingSecret: "fuinjutsu-api-keys"
```

## Accès à l'application

Une fois déployée, l'application est accessible via les URLs suivantes :

- `/cyberpunk/` - Interface Cyberpunk
- `/mcp/` - Interface MCP (Model Context Protocol)
- `/cyberpunk-ui/` - Interface Cyberpunk HTML
- `/api/mcp/` - API REST pour les MCPs

Si l'Ingress est activé, ces URLs sont accessibles via l'hôte configuré.

## Personnalisation

Pour personnaliser davantage le déploiement, vous pouvez créer votre propre fichier `values.yaml` :

```yaml
# values.yaml
cyberpunk:
  replicaCount: 2
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi

mcp:
  replicaCount: 2
  
persistence:
  config:
    size: 5Gi
  data:
    size: 10Gi

ingress:
  hosts:
    - host: fuinjutsu.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: fuinjutsu-tls
      hosts:
        - fuinjutsu.example.com
```

Puis installer ou mettre à jour avec :

```bash
helm install fuinjutsu ./helm/fuinjutsu -f values.yaml
# ou
helm upgrade fuinjutsu ./helm/fuinjutsu -f values.yaml
```

## Désinstallation

Pour désinstaller/supprimer le déploiement :

```bash
helm delete fuinjutsu
```

## Persistance des données

Ce chart utilise des Persistent Volume Claims pour stocker les données. Par défaut, les PVC sont créés dynamiquement.

Si vous souhaitez utiliser un Persistent Volume existant, vous pouvez définir :

```yaml
persistence:
  config:
    existingClaim: "mon-claim-config"
  data:
    existingClaim: "mon-claim-data"
```

## Documentation supplémentaire

Pour plus d'informations sur Fûinjutsu, consultez [le README du projet](/README.md).