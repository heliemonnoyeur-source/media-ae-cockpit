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

## Campagne prete a l'emploi : Media & Ads Industry Day

Si votre objectif est de lancer une campagne de prospection pour le Media & Ads Industry Day, vous pouvez utiliser un jeu de templates dedie :

- `templates/media_ads_industry_day_subject.txt`
- `templates/media_ads_industry_day_body.txt`
- `data/media_ads_industry_day.contacts.example.csv`

### 1. Preparez votre fichier de contacts

```bash
cp data/media_ads_industry_day.contacts.example.csv data/media_ads_industry_day.contacts.csv
```

Colonnes recommandees :

```csv
email,name,company,interest_area,value_prop,status
julie@example.com,Julie,Studio Nova,les partenariats brand content,une prise de parole qualifiee avec des interlocuteurs media et adtech,
```

- `interest_area` : sujet ou angle qui interesse le contact
- `value_prop` : valeur concrete de votre proposition
- `status` : laissez vide pour envoyer, ou mettez `skip` pour exclure la ligne

### 2. Relisez la campagne avant envoi

```bash
python3 campaign_mailer.py preview \
  --contacts data/media_ads_industry_day.contacts.csv \
  --subject-template templates/media_ads_industry_day_subject.txt \
  --body-template templates/media_ads_industry_day_body.txt \
  --context event_name="Media & Ads Industry Day" \
  --context event_date="12 juin 2026" \
  --context event_location="Paris" \
  --context sender_name="Alex Martin" \
  --context sender_role="Partnerships Lead" \
  --context sender_phone="+33 6 00 00 00 00"
```

### 3. Validez le flux d'envoi sans expedier de message

```bash
python3 campaign_mailer.py send \
  --contacts data/media_ads_industry_day.contacts.csv \
  --subject-template templates/media_ads_industry_day_subject.txt \
  --body-template templates/media_ads_industry_day_body.txt \
  --context event_name="Media & Ads Industry Day" \
  --context event_date="12 juin 2026" \
  --context event_location="Paris" \
  --context sender_name="Alex Martin" \
  --context sender_role="Partnerships Lead" \
  --context sender_phone="+33 6 00 00 00 00" \
  --sender alex@votre-domaine.com \
  --dry-run
```

### 4. Lancez la campagne

```bash
python3 campaign_mailer.py send \
  --contacts data/media_ads_industry_day.contacts.csv \
  --subject-template templates/media_ads_industry_day_subject.txt \
  --body-template templates/media_ads_industry_day_body.txt \
  --context event_name="Media & Ads Industry Day" \
  --context event_date="12 juin 2026" \
  --context event_location="Paris" \
  --context sender_name="Alex Martin" \
  --context sender_role="Partnerships Lead" \
  --context sender_phone="+33 6 00 00 00 00" \
  --throttle-seconds 8
```

### Conseil de personnalisation

Pour de meilleurs resultats, adaptez au minimum ces champs :

- `interest_area` avec un angle propre au contact
- `value_prop` avec un benefice concret
- `event_date` et `event_location`
- `sender_name`, `sender_role`, `sender_phone`

Le script ignore automatiquement les contacts deja journalises dans `outbox/sent-log.jsonl`, ainsi que les lignes marquees `skip`.
