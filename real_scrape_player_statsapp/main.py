import pandas as pd

def load_players(csv_path: str = "players.csv") -> pd.DataFrame:
    """Charge la liste des joueurs depuis un CSV."""
    return pd.read_csv(csv_path)

def find_player_id(player_name: str, players_df: pd.DataFrame) -> str:
    """Trouve l'ID du joueur à partir de son nom."""
    result = players_df[players_df['name'].str.lower() == player_name.lower()]
    if not result.empty:
        return result.iloc[0]['id']
    # Recherche intelligente : similarité partielle
    mask = players_df['name'].str.lower().str.contains(player_name.lower())
    if mask.any():
        return players_df[mask].iloc[0]['id']
    return None

def scrape_player_stats(player_id: str):
    """
    Appelle la fonction de scraping pour obtenir les stats de football.
    Cette fonction s’attend à ce que la vraie fonction de scraping soit dans main.py.
    Elle doit retourner un dictionnaire des stats du joueur, par exemple :
    {
        'name': 'Lionel Messi',
        'id': 'messi_lionel',
        'buts': 25,
        'passes': 15,
        'minutes': 2700,
        'cartons_jaunes': 3,
        ...
    }
    """
    # Import dynamique pour éviter les conflits d'import circulaire
    from app.main import real_scrape_player_stats
    return real_scrape_player_stats(player_id)
