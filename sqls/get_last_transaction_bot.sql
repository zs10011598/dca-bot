SELECT *
FROM transaction
WHERE bot_id = '{bot_id}'
ORDER BY id DESC
LIMIT 1