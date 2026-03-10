from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


class NoCompanyRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Миксин для представлений, доступных только пользователям БЕЗ компании.

    - Не авторизован         → страница логина
    - Авторизован + есть компания  → страница компании
    - Авторизован + нет компании   → доступ разрешён (главная страница)
    """

    # URL для редиректа если у пользователя уже есть компания
    company_url = reverse_lazy('company_dashboard')  # заменить позже

    def test_func(self):
        """Возвращает True если у пользователя НЕТ компании — доступ разрешён."""
        return not hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        """Вызывается когда test_func() вернул False (компания есть)."""
        from django.shortcuts import redirect

        # Если не авторизован — LoginRequiredMixin сам перенаправит на логин
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        # Если авторизован, но компания есть → на страницу компании
        return redirect(self.company_url)
