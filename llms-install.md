# Установка yandex-market-mcp-ru агентом

Документ для ИИ-агента, который ставит сервер за человека. Человеку удобнее
[README](README.md).

## 1. Проверить uv

```bash
uvx --version || curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Прописать сервер

Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) или `%APPDATA%\Claude\claude_desktop_config.json` (Windows).
Cline: `cline_mcp_settings.json`.

```json
{
  "mcpServers": {
    "ym": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/ilyautov/yandex-market-mcp-ru", "yandex-market-mcp-ru"],
      "env": {
        "YANDEX_MARKET_API_KEY": "<значение>"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## 3. Ключи

| переменная | тип | где взять |
|---|---|---|
| `YANDEX_MARKET_API_KEY` | секрет | API-ключ из кабинета партнёра, раздел Настройки → API. |

Значения спрашиваются у человека и в репозиторий не пишутся. Второй путь, без
переменных окружения: запустить сервер и вызвать `ym_add_cabinet`,
ключи лягут в `~/.marketplace-mcp/cabinets.json` с правами 600.

## 4. Проверить

Перезапустить клиент и вызвать `ym_check_auth`. Ответ «ключей нет»
означает, что сервер поднялся, а ключи не дошли: смотреть шаг 3. Каталог
отвечает `ym_list_sections`, в нём 165 методов.

## Если не поднимается

- `uvx` не найден: шаг 1, потом перезапустить клиент, он читает PATH при старте.
- Пусто в списке инструментов: клиент не перечитал конфигурацию, нужен рестарт.
- Ошибка авторизации при верных ключах: активный кабинет в
  `~/.marketplace-mcp/cabinets.json` имеет приоритет над переменными окружения.
