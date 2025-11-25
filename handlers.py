import requests
import re
import config

BASE_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"


# ========= ENVOI DE MESSAGE =========
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(BASE_URL, json=payload)


# ========= GESTION DES MESSAGES =========
def handle_message(chat_id, text):

    if text.startswith("/start"):
        send_message(chat_id, config.HELP_MESSAGE)
        return

    if text.startswith("/banque"):
        try:
            montant = float(text.split()[1])
            config.banque = montant
            send_message(chat_id, f"✅ Banque définie à {montant} FCFA")
            check_ready(chat_id)
        except:
            send_message(chat_id, "❌ Exemple : /banque 6000")
        return

    if text.startswith("/mise"):
        try:
            montant = float(text.split()[1])
            config.mise = montant
            send_message(chat_id, f"✅ Mise définie à {montant} FCFA")
            check_ready(chat_id)
        except:
            send_message(chat_id, "❌ Exemple : /mise 500")
        return

    if text.startswith("/cote"):
        try:
            montant = float(text.split()[1])
            config.cote = float(montant)
            send_message(chat_id, f"✅ Côte définie à {montant}")
            check_ready(chat_id)
        except:
            send_message(chat_id, "❌ Exemple : /cote 1.9")
        return

    if text.startswith("/reset"):
        config.banque = 0
        config.mise = 0
        config.cote = 0
        config.etat_du_bot = False

        send_message(chat_id, "🔄 Bot réinitialisé. Redéfinissez /banque /mise /cote")
        return

    # ========== ANALYSE DES STATUTS ==========
    if not config.etat_du_bot:
        return

    # Ignore statut en attente
    if "⏳" in text:
        return

    match = re.search(r"(✅[0-2]️⃣|❌)", text)

    if not match:
        return

    statut = match.group(1)

    b = config.banque
    m = config.mise
    c = config.cote

    if statut == "✅0️⃣":
        gain = m * c
        nb = b - m + gain

        message = f"""
✅ STATUT 0 DÉTECTÉ

🎯 Gain : {gain:.2f} FCFA
💼 Ancienne banque : {b:.2f} FCFA
🏦 Nouvelle banque : {nb:.2f} FCFA
"""

    elif statut == "✅1️⃣":
        gain = m * c * 2
        nb = b - m + gain

        message = f"""
✅ STATUT 1 DÉTECTÉ

🎯 Gain : {gain:.2f} FCFA (x2)
💼 Ancienne banque : {b:.2f} FCFA
🏦 Nouvelle banque : {nb:.2f} FCFA
"""

    elif statut == "✅2️⃣":
        gain = m * 4 * c
        perte = m * 8
        nb = b - perte + gain

        message = f"""
✅ STATUT 2 DÉTECTÉ

🚀 SUPER GAIN : {gain:.2f} FCFA
💸 Perte engagée : {perte:.2f} FCFA
💼 Ancienne banque : {b:.2f} FCFA
🏦 Nouvelle banque : {nb:.2f} FCFA
"""

    elif statut == "❌":
        perte = m * 7
        nb = b - perte

        message = f"""
❌ STATUT PERDANT

💸 Perte : {perte:.2f} FCFA
💼 Ancienne banque : {b:.2f} FCFA
🏦 Nouvelle banque : {nb:.2f} FCFA
"""

    config.banque = nb
    send_message(chat_id, message)


def check_ready(chat_id):
    if config.banque > 0 and config.mise > 0 and config.cote > 0:
        config.etat_du_bot = True

        send_message(chat_id,
            "✅ BOT ACTIVÉ\n\nIl analysera maintenant automatiquement les statuts du canal."
        )
