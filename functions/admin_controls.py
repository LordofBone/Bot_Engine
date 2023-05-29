from functions.voice_controller import VoiceControllerAccess


def admin_control(words):
    if words == "train bot":
        VoiceControllerAccess.play_training()
        BotInterface.bot_training()
        return "TRAINING COMPLETE"
    elif words == "erase db":
        # todo: find a voice clip here
        BotInterface.bot_erase_db()
        return "DATABASE ERASED"
    elif words == "fresh db":
        # todo: find a voice clip here
        BotInterface.bot_fresh_db()
        return "DATABASE FORMATTED"
    elif words == "mute":
        VoiceControllerAccess.audio_on = not VoiceControllerAccess.audio_on
        return f"VOICE MUTE: {VoiceControllerAccess.audio_on}"
    elif words == "emotions":
        EmotionEngineInterface.process_emotions = not VoiceControllerAccess.audio_on
        return f"EMOTION PROCESSING: {VoiceControllerAccess.audio_on}"
    elif words == "exit admin mode":
        return "admin_exit"
    else:
        return "INVALID COMMAND"
