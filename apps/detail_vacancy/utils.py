def render_stars_html(rating: float, max_stars: int = 5) -> str:
    full_stars = int(rating)
    remainder = rating - full_stars
    half_star = 1 if remainder >= 0.5 else 0
    empty_stars = max_stars - full_stars - half_star

    html = '<i class="bi bi-star-fill text-warning"></i>' * full_stars
    html += '<i class="bi bi-star-half text-warning"></i>' * half_star
    html += '<i class="bi bi-star text-warning"></i>' * empty_stars

    return html


def years_declension(
    experience_required: str,
    start: int | None = None,
    end: int | None = None
) -> str:
    """
    Returns a string with the required work experience,
    applying correct English declension of the word 'year'.

    Examples:
        years_declension("with_experience", 1)      -> "1 year"
        years_declension("with_experience", 3)      -> "3 years"
        years_declension("with_experience", 1, 3)   -> "1-3 years"
        years_declension("without_experience")      -> "without_experience"
    """
    if experience_required != "with_experience":
        return experience_required

    def _get_form(n: int) -> str:
        return "year" if n == 1 else "years"

    if start is not None and end is not None:
        return f"{start}-{end} {_get_form(end)}"

    value = start if start is not None else end
    if value is None:
        return experience_required

    return f"{value} {_get_form(value)}"


def split_lines(text: str) -> list[str]:
    """
    Splits a multiline text into a clean list of strings,
    stripping empty lines and extra whitespace.
    """
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]
