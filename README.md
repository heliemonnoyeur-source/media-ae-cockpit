# media-ae-cockpit

Automatisation simple d'une campagne media par email depuis un fichier CSV de contacts.

## Ce que fournit ce patch

- import de contacts depuis un CSV
- personnalisation du sujet et du corps via des templates `{{variable}}`
- mode `preview` pour relire les emails avant envoi
- mode `send` via SMTP
- journalisation des envois dans `outbox/sent-log.jsonl`
- prevention des doublons grace au journal d'envoi

## Structure

```text
campaign_mailer.py
data/contacts.example.csv
templates/media_subject.txt
templates/media_body.txt
tests/test_campaign_mailer.py
```

## Format du CSV

Le fichier doit contenir au minimum une colonne `email`.

Exemple :

```csv
email,name,company,angle,sender_name,status
julie@example.com,Julie,Studio Nova,lancement du nouveau format video,Alex,
reda@example.com,Reda,Patch Media,serie d'interviews exclusives,Alex,
```

Les colonnes du CSV sont ensuite disponibles dans les templates avec la syntaxe `{{nom_colonne}}`.

La colonne `status` est optionnelle. Si sa valeur est `sent`, `done`, `skip` ou `skipped`, le contact est ignore.

## Templates

Sujet (`templates/media_subject.txt`) :

```text
Partenariat media pour {{ company }}
```

Corps (`templates/media_body.txt`) :

```text
Bonjour {{ name }},

Je vous contacte au sujet de {{ company }} pour proposer une collaboration media autour de {{ angle }}.

Si le sujet vous interesse, je peux vous envoyer un kit presse, des visuels et quelques disponibilites pour un echange rapide.

Bien a vous,
{{ sender_name }}
```

Vous pouvez aussi injecter des variables communes a toute la campagne avec `--context`, par exemple `--context sender_name=Alex`.

## Apercu avant envoi

```bash
cp data/contacts.example.csv data/contacts.csv
python3 campaign_mailer.py preview \
  --contacts data/contacts.csv \
  --context sender_name=Alex
```

## Envoi reel

Definissez vos variables SMTP :

```bash
export MAIL_SENDER="alex@votre-domaine.com"
export MAIL_REPLY_TO="alex@votre-domaine.com"
export SMTP_HOST="smtp.votre-domaine.com"
export SMTP_PORT="587"
export SMTP_USER="alex@votre-domaine.com"
export SMTP_PASSWORD="mot-de-passe-ou-token"
export SMTP_SECURITY="starttls"
```

Validez d'abord les messages sans envoyer :

```bash
python3 campaign_mailer.py send \
  --contacts data/contacts.csv \
  --context sender_name=Alex \
  --dry-run
```

Puis lancez la campagne :

```bash
python3 campaign_mailer.py send \
  --contacts data/contacts.csv \
  --context sender_name=Alex \
  --throttle-seconds 8
```

## Tests

```bash
python3 -m unittest discover -s tests
```
