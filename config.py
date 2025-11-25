import os

BOT_TOKEN = "VOTRE_TOKEN_ICI"

PORT = int(os.environ.get("PORT", 10000))

banque = 0
mise = 0
cote = 0

etat_du_bot = False

HELP_MESSAGE = """
🤖 BOT DE RENTABILITÉ (VERSION PRO)

/start → Afficher les commandes
/banque 6000 → Définir banque
/mise 500 → Définir mise
/cote 1.9 → Définir cote
/reset → Réinitialiser bot
"""
