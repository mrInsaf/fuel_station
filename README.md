Запуск: uvicorn main:app --reload

# Документация для API

## Описание
Этот бэкенд предоставляет API для получения топливных токенов, обрабатывая запросы на выдачу топлива и взаимодействуя с внешним сервисом для фактического получения данных.

---

## Установленные ограничения
- **Частота запросов:** Один запрос в секунду для каждого `tank_id`.
- **Максимальное количество топлива:** При запросе указывается количество топлива, но API ограничивает запрос до 10 единиц за один раз.

---

## Эндпоинт

### `POST /get_fuel`
Обрабатывает запросы на получение топлива для указанного идентификатора танка (`tank_id`) и количества топлива (`count`).

### Запрос
**Тело запроса:**
```json
{
    "tank_id": <int>, // ID танка
    "count": <int>    // Количество топлива для запроса
}
