from developer.universal_generator import generator

from developer.game_generator import (
    snake,
    platformer,
    racing,
    shooter
)

from developer.website_generator import (
    portfolio,
    landing_page,
    ecommerce
)

from developer.chatbot_generator import (
    ai_assistant,
    discord_bot,
    telegram_bot,
    whatsapp_bot
)

from developer.app_generator import (
    calculator,
    weather,
    notes,
    media_player
)

from developer.api_generator import (
    flask_api,
    rest_api,
    nitron_api
)

from developer.database_generator import (
    sqlite_database,
    user_database,
    school_database,
    ecommerce_database
)

from developer.desktop_generator import (
    calculator as desktop_calculator,
    notes as desktop_notes,
    music_player,
    file_manager
)

from developer.automation_generator import (
    backup_script,
    file_organizer,
    folder_watcher,
    task_scheduler,
    web_scraper,
    email_sender
)

from developer.ml_generator import (
    prediction_model,
    image_classifier,
    text_classifier,
    recommendation_system,
    chatbot_model
)

generator.register("snake", snake)
generator.register("platformer", platformer)
generator.register("racing", racing)
generator.register("shooter", shooter)

generator.register("portfolio", portfolio)
generator.register("landing page", landing_page)
generator.register("ecommerce", ecommerce)

generator.register("ai assistant", ai_assistant)
generator.register("discord bot", discord_bot)
generator.register("telegram bot", telegram_bot)
generator.register("whatsapp bot", whatsapp_bot)

generator.register("calculator app", calculator)
generator.register("weather app", weather)
generator.register("notes app", notes)
generator.register("media player", media_player)

generator.register("flask api", flask_api)
generator.register("rest api", rest_api)
generator.register("nitron api", nitron_api)

generator.register("sqlite database", sqlite_database)
generator.register("user database", user_database)
generator.register("school database", school_database)
generator.register("ecommerce database", ecommerce_database)

generator.register("desktop calculator", desktop_calculator)
generator.register("desktop notes", desktop_notes)
generator.register("desktop music player", music_player)
generator.register("file manager", file_manager)

generator.register("backup script", backup_script)
generator.register("file organizer", file_organizer)
generator.register("folder watcher", folder_watcher)
generator.register("task scheduler", task_scheduler)
generator.register("web scraper", web_scraper)
generator.register("email sender", email_sender)

generator.register("prediction model", prediction_model)
generator.register("image classifier", image_classifier)
generator.register("text classifier", text_classifier)
generator.register("recommendation system", recommendation_system)
generator.register("chatbot model", chatbot_model)
