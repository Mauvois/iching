# IChing

Application I Ching en architecture microservices:

- `iching_front` (Dash): UX, tirage, affichage du resultat
- `iching_back` (FastAPI + DuckDB): generation des lignes et resolution des hexagrammes
- `iching_interpreter` (FastAPI + OpenAI): interpretation IA

## Lancer en local avec Docker Compose

### 1) Prerequis

- Docker ou Podman avec plugin Compose
- reseau Docker externe `edge_net` partage avec le conteneur `cloudflared`

Creation du reseau (une seule fois):

```bash
docker network create edge_net
```

### 2) Configuration

Copiez le fichier d'exemple:

```bash
cp .env.example .env
```

Puis renseignez au minimum `OPENAI_API_KEY` dans `.env`.

### 3) Demarrage

```bash
docker compose up --build
```

Ou avec Podman:

```bash
podman compose up --build
```

## Acces

- debug local frontend: `http://localhost:18050` (modifiable avec `PORT_FRONT`)
- acces public via Cloudflare Tunnel sur ton sous-domaine

Les services `iching_back` et `iching_interpreter` ne sont **pas** exposes sur l'hote. Ils communiquent uniquement via le reseau interne Compose.

## Variables d'environnement

- `PORT_FRONT` (defaut `18050`): port host pour debug local du frontend
- `OPENAI_API_KEY`: cle API OpenAI (obligatoire pour `/interpret`)
- `OPENAI_MODEL` (defaut `gpt-4o-mini`)

## Architecture reseau

- `iching_front` appelle:
  - `http://iching_back:8080`
  - `http://iching_interpreter:8080`
- `iching_back` et `iching_interpreter` sont en `expose: 8080` uniquement (interne)
- `iching_front` est attache a:
  - `iching_net` (interne app)
  - `edge_net` (partage avec cloudflared)

## Cloudflared (exemple)

Route le sous-domaine IChing vers le nom de service Docker:

```yaml
ingress:
  - hostname: iching.example.com
    service: http://iching_front:8050
  - service: http_status:404
```

Le conteneur cloudflared doit etre connecte au reseau `edge_net`.

## Smoke tests rapides

Puis faites un parcours UI complet:

1. saisir une question
2. lancer le tirage et completer 6 lignes
3. verifier l'affichage hexagramme
4. cliquer sur interpretation

## Arborescence

- `frontend/front.py`
- `backend/main.py`
- `services/interpreter/app.py`
- `docker-compose.yml`
