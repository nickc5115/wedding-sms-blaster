TEMPLATES: dict[str, str] = {
    "rsvp_reminder": (
        "Hi {name}! This is a friendly reminder to RSVP for {couple_names}'s wedding. "
        "Please visit {rsvp_link} to let us know if you can make it. "
        "We'd love to celebrate with you!"
    ),
}


def get_template(template_name: str) -> str:
    """Get a message template by name."""
    if template_name not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(
            f"Unknown template: '{template_name}'. Available: {available}"
        )
    return TEMPLATES[template_name]


def render_message(template_name: str, guest_name: str, couple_names: str, rsvp_link: str) -> str:
    """Render a template with the guest's name and wedding details."""
    template = get_template(template_name)
    return template.format(
        name=guest_name,
        couple_names=couple_names,
        rsvp_link=rsvp_link,
    )


def list_templates() -> list[str]:
    """Return all available template names."""
    return list(TEMPLATES.keys())
