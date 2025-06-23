import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from random import choice
from config.user_agents import USER_AGENTS

class FBrefScraper:
    def __init__(self):
        self.base_url = "https://fbref.com"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': choice(USER_AGENTS)})
        
    def get_player_data(self, player_url):
        """Récupère toutes les données d'un joueur"""
        try:
            # 1. Récupération page principale
            soup = self._get_page(player_url)
            
            # 2. Extraction des métadonnées
            metadata = self._extract_metadata(soup)
            
            # 3. Récupération des stats standard
            standard_stats = self._extract_table(soup, 'stats_standard')
            
            # 4. Récupération des stats avancées
            advanced_stats = self._extract_table(soup, 'stats_advanced')
            
            # 5. Calcul des centiles
            centiles = self._calculate_centiles(standard_stats, advanced_stats)
            
            return {
                'metadata': metadata,
                'standard_stats': standard_stats,
                'advanced_stats': advanced_stats,
                'centiles': centiles
            }
            
        except Exception as e:
            print(f"Erreur lors du scraping: {str(e)}")
            return None

    def _get_page(self, url):
        """Gestion des requêtes avec délai aléatoire"""
        time.sleep(1.5 + random.random())  # Respect robots.txt
        response = self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def _extract_metadata(self, soup):
        """Extraction des infos joueur"""
        info_box = soup.find('div', {'id': 'meta'})
        metadata = {}
        if info_box:
            name = info_box.find('h1')
            metadata['name'] = name.get_text(strip=True) if name else ""
        # Ajoute ici l’extraction d’autres métadonnées si besoin
        return metadata

    def _extract_table(self, soup, table_id):
        """Extraction d'une table de stats par id"""
        try:
            table = soup.find("table", {"id": table_id})
            if table:
                df = pd.read_html(str(table))[0]
                return df.to_dict(orient="records")
            return []
        except Exception as e:
            print(f"Erreur d'extraction table {table_id}: {e}")
            return []

    def _calculate_centiles(self, standard_stats, advanced_stats):
        """Dummy : retourne un dict vide (à personnaliser si besoin)"""
        return {}
