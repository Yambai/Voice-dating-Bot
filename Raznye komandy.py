await state.reset_state(with_data=True) #Очищает данные в в состоянии

# красиво выводит message и другие json файлы
data = json.loads(f"{message}")
# Красиво форматируем JSON с использованием отступов
pretty_json = json.dumps(data, indent=6, ensure_ascii=False)
text=pretty_json
await bot.send_message(admin_id, text=text)