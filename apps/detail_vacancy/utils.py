def render_stars_html(rating, max_stars=5):
    """
    Генерирует HTML со звёздами рейтинга.
    4.5 → 4 полные + 1 половинка
    4.4 → 4 полные + 1 пустая
    2.0 → 2 полные + 3 пустые
    """
    full_stars = int(rating)
    remainder = rating - full_stars
    half_star = 1 if remainder >= 0.5 else 0
    empty_stars = max_stars - full_stars - half_star

    html = '<i class="bi bi-star-fill text-warning"></i>' * full_stars
    html += '<i class="bi bi-star-half text-warning"></i>' * half_star
    html += '<i class="bi bi-star text-warning"></i>' * empty_stars

    return html
