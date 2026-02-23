import os

import click

from config import load_config
from guests import load_guests
from templates import render_message, list_templates
from sms import create_client, send_blast

DEFAULT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guests.csv")


@click.group()
def cli():
    """Wedding SMS Blaster - Send SMS blasts to your wedding guests."""
    pass


@cli.command("list")
@click.option("--csv", "csv_path", default=DEFAULT_CSV, help="Path to guests CSV file.")
def list_guests(csv_path):
    """List all guests loaded from the CSV."""
    try:
        guests = load_guests(csv_path)
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(f"\nGuests ({len(guests)}):")
    click.echo("-" * 40)
    for g in guests:
        click.echo(f"  {g.name:<25} {g.phone}")
    click.echo()


@cli.command()
@click.option("--template", "template_name", required=True, help="Message template to preview.")
@click.option("--csv", "csv_path", default=DEFAULT_CSV, help="Path to guests CSV file.")
def preview(template_name, csv_path):
    """Preview messages that would be sent to each guest."""
    config = load_config()

    try:
        guests = load_guests(csv_path)
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(f"\nTemplate: {template_name}")
    click.echo(f"Recipients: {len(guests)}")
    click.echo("=" * 60)

    for g in guests:
        msg = render_message(template_name, g.name, config.couple_names, config.rsvp_link)
        click.echo(f"\nTo: {g.name} ({g.phone})")
        click.echo(f"Message: {msg}")
        click.echo("-" * 60)

    click.echo()


@cli.command()
@click.option("--template", "template_name", required=True, help="Message template to send.")
@click.option("--csv", "csv_path", default=DEFAULT_CSV, help="Path to guests CSV file.")
@click.option("--dry-run", is_flag=True, default=False, help="Simulate sending without actually sending.")
@click.option("--to", "single_recipient", default=None, help="Send to a single guest by name (for testing).")
@click.option("--delay", default=1.0, help="Seconds between messages (rate limiting).", show_default=True)
def send(template_name, csv_path, dry_run, single_recipient, delay):
    """Send an SMS blast to all guests (or a single guest with --to)."""
    config = load_config()

    try:
        guests = load_guests(csv_path)
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if single_recipient:
        matches = [g for g in guests if g.name.lower() == single_recipient.lower()]
        if not matches:
            click.echo(f"Error: No guest found with name '{single_recipient}'", err=True)
            click.echo("Available guests:")
            for g in guests:
                click.echo(f"  - {g.name}")
            raise SystemExit(1)
        guests = matches

    recipients = []
    for g in guests:
        msg = render_message(template_name, g.name, config.couple_names, config.rsvp_link)
        recipients.append((g.name, g.phone, msg))

    click.echo(f"\nTemplate: {template_name}")
    click.echo(f"Recipients: {len(recipients)}")
    if dry_run:
        click.echo("Mode: DRY RUN (no messages will be sent)")
    click.echo()

    if dry_run:
        for name, phone, body in recipients:
            click.echo(f"  [DRY RUN] Would send to {name} ({phone}): {body}")
        click.echo(f"\nDry run complete. {len(recipients)} message(s) would be sent.")
        return

    if not click.confirm(f"Send {len(recipients)} SMS message(s)?"):
        click.echo("Cancelled.")
        return

    client = create_client(config)

    def on_progress(index, total, name, success, detail):
        status = click.style("SENT", fg="green") if success else click.style("FAILED", fg="red")
        click.echo(f"  [{index}/{total}] {status} - {name}: {detail}")

    click.echo("Sending...\n")
    results = send_blast(client, config.twilio_phone_number, recipients, delay=delay, progress_callback=on_progress)

    succeeded = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])

    click.echo(f"\nDone! {succeeded} sent, {failed} failed.")

    if failed:
        click.echo("\nFailed messages:")
        for r in results:
            if not r["success"]:
                click.echo(f"  - {r['name']} ({r['phone']}): {r['detail']}")


@cli.command()
def templates():
    """List all available message templates."""
    names = list_templates()
    click.echo("\nAvailable templates:")
    for name in names:
        click.echo(f"  - {name}")
    click.echo()


if __name__ == "__main__":
    cli()
