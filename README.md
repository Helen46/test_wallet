Напишите приложение, которое по REST принимает запрос вида
POST api/v1/wallets/<WALLET_UUID>/operation
{
operation_type: “DEPOSIT” or “WITHDRAW”,
amount: 1000
}
после выполнять логику по изменению счета в базе данных
также есть возможность получить баланс кошелька
GET api/v1/wallets/{WALLET_UUID}
стек:
FastAPI / Flask / Django
Postgresql

Код должен следовать PEP8.
Должны быть написаны миграции для базы данных.
Обратите особое внимание проблемам при работе в конкурентной среде, параллельные запросы на изменения баланса одного кошелька должны работать корректно.
Приложение должно запускаться в докер контейнере, база данных тоже, вся система должна подниматься с помощью docker-compose
Эндпоинты должны быть покрыты тестами.
Решенное задание залить на гитхаб, предоставить ссылку
Все возникающие вопросы по заданию решать самостоятельно, по своему усмотрению.
