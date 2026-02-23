# Wedding SMS Blaster

A simple CLI tool to send customizable SMS blasts to wedding guests via Twilio.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Twilio account

1. Sign up at [twilio.com](https://www.twilio.com/) (free trial works for testing)
2. Get a Twilio phone number from the console
3. Find your **Account SID** and **Auth Token** on the [Twilio Console dashboard](https://console.twilio.com/)

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your Twilio credentials and wedding details:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+15551234567
COUPLE_NAMES=Nick & Partner
RSVP_LINK=https://www.zola.com/wedding/yourwedding/rsvp
```

### 4. Add your guests

Edit `guests.csv` with your guest list. Phone numbers can be in any common US format:

```csv
name,phone
John Smith,+15551234567
Jane Doe,(555) 987-6543
Bob Johnson,555.123.4567
```

## Usage

### List guests

```bash
python main.py list
```

### Preview messages (no SMS sent)

```bash
python main.py preview --template rsvp_reminder
```

### Dry run (simulates sending)

```bash
python main.py send --template rsvp_reminder --dry-run
```

### Send to a single guest (for testing)

```bash
python main.py send --template rsvp_reminder --to "John Smith"
```

### Send to all guests

```bash
python main.py send --template rsvp_reminder
```

You'll be prompted to confirm before any messages are actually sent.

### List available templates

```bash
python main.py templates
```

## Adding new templates

Edit `templates.py` to add new message templates. Available placeholders:

- `{name}` -- the guest's name
- `{couple_names}` -- from your `.env` file
- `{rsvp_link}` -- from your `.env` file

Example:

```python
TEMPLATES = {
    "rsvp_reminder": "Hi {name}! ...",
    "save_the_date": "Hi {name}! Save the date for {couple_names}'s wedding! ...",
}
```

## Notes

- Messages are sent with a 1-second delay between each to avoid Twilio rate limiting (adjustable with `--delay`)
- The `send` command always asks for confirmation before sending
- Use `--dry-run` to safely verify everything looks right before sending
- On a Twilio trial account, you can only send to verified phone numbers
