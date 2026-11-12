"""Pluggable integrations (solution design, section 7.2).

The core never imports anything from this package to do its work. It writes
rows to the outgoing event log (`OutboxEvent`); `dispatcher.dispatch_pending()`
hands them to the integrations that are switched on, with retries.

`CATALOG` lists every integration shown on the "Integrations" page, including
the ones that are only planned, so the page shows honestly what is implemented,
what is simulated and what is planned.
"""

CATALOG = [
    {
        "code": "telegram", "name": "Telegram: уведомления", "kind": "Канал уведомлений", "mode": "real",
        "enabled": False, "sort": 10,
        "description": "Бот отправляет номер обращения, статус и ссылку. Текст обращения и имена в Telegram не передаются. "
                       "Сотрудник привязывает аккаунт одноразовой ссылкой из профиля.",
        "when_off": "Уведомление уходит в следующий включённый канал и всегда видно в системе.",
    },
    {
        "code": "bitrix24_notify", "name": "Битрикс24: уведомления", "kind": "Канал уведомлений", "mode": "simulator",
        "enabled": True, "sort": 20,
        "description": "Имитация: вместо отправки записывается точный REST-запрос im.notify.system.add, "
                       "который ушёл бы на портал. Для реального подключения нужен вебхук заказчика.",
        "when_off": "Уведомления остаются в системе и в Telegram.",
    },
    {
        "code": "bitrix24_directory", "name": "Битрикс24: сотрудники и оргструктура", "kind": "Справочник сотрудников",
        "mode": "simulator", "enabled": True, "sort": 30,
        "description": "Справочник загружается из JSON-файла в формате ответов department.get и user.get. "
                       "Тот же импорт будет работать с реальным API.",
        "when_off": "Остаётся последний загруженный справочник; его можно править вручную в настройках.",
    },
    {
        "code": "bitrix24_login", "name": "Битрикс24: вход (OAuth 2.0)", "kind": "Вход", "mode": "planned",
        "enabled": False, "sort": 40,
        "description": "Вход без отдельного пароля через портал заказчика.",
        "when_off": "Собственный вход (в демо — переключатель ролей).",
    },
    {
        "code": "bitrix24_tasks", "name": "Битрикс24: задачи из решений", "kind": "Задачи", "mode": "planned",
        "enabled": False, "sort": 50,
        "description": "Принятое решение создаёт задачу (tasks.task.add); ход задачи возвращается в обращение.",
        "when_off": "Ответственный сам отчитывается о ходе реализации.",
    },
    {
        "code": "bitrix24_embed", "name": "Битрикс24: приложение в левом меню", "kind": "Встраивание", "mode": "planned",
        "enabled": False, "sort": 60,
        "description": "Система открывается внутри портала во фрейме.",
        "when_off": "Система открывается по своей ссылке.",
    },
    {
        "code": "email", "name": "Почта: уведомления и приём писем", "kind": "Канал уведомлений", "mode": "planned",
        "enabled": False, "sort": 70,
        "description": "Запасной канал уведомлений; письмо на общий адрес становится обращением.",
        "when_off": "Обращения подаются через форму; уведомления — в системе.",
    },
    {
        "code": "onec", "name": "1С:УТ: номер документа", "kind": "Контекст", "mode": "planned",
        "enabled": False, "sort": 80,
        "description": "Ссылка на заказ или поступление в обращениях закупок и продаж (только чтение).",
        "when_off": "Номер документа вводится вручную.",
    },
    {
        "code": "ai", "name": "ИИ-подсказки", "kind": "Подсказки", "mode": "planned",
        "enabled": False, "sort": 90,
        "description": "Подсказка категории, поиск дубликатов, сводка тем. Модель размещается в Казахстане; "
                       "ИИ предлагает — человек подтверждает.",
        "when_off": "Категория подсказывается по ключевым словам, похожие обращения — по совпадению слов.",
    },
]


def ensure_catalog() -> None:
    """Create the integration rows that are missing. Existing switches are left alone."""
    from ..models import Integration

    for item in CATALOG:
        Integration.objects.get_or_create(code=item["code"], defaults={k: v for k, v in item.items() if k != "code"})
