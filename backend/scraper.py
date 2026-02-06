import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re


class WikipediaScraper:
    """Scrapes and extracts content from Wikipedia articles"""

    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.raw_html = None

    def scrape(self) -> Dict:
        """
        Main method to scrape Wikipedia article
        Returns: Dictionary with title, summary, sections, and entities
        """
        try:
            # Fetch the page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            
            self.raw_html = response.text
            self.soup = BeautifulSoup(self.raw_html, 'lxml')

            # Extract components
            title = self._extract_title()
            summary = self._extract_summary()
            sections = self._extract_sections()
            key_entities = self._extract_entities()

            return {
                'title': title,
                'summary': summary,
                'sections': sections,
                'key_entities': key_entities,
                'raw_html': self.raw_html,
                'full_text': self._extract_full_text()
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch Wikipedia page: {str(e)}")
        except Exception as e:
            raise Exception(f"Error scraping Wikipedia: {str(e)}")

    def _extract_title(self) -> str:
        """Extract article title"""
        title_elem = self.soup.find('h1', class_='firstHeading')
        if title_elem:
            return title_elem.get_text().strip()
        return "Unknown Title"

    def _extract_summary(self) -> str:
        """Extract the first paragraph as summary"""
        # Find the first paragraph in the content area
        content = self.soup.find('div', class_='mw-parser-output')
        if content:
            # Get first few meaningful paragraphs
            paragraphs = content.find_all('p', recursive=False, limit=3)
            summary_parts = []
            
            for p in paragraphs:
                text = p.get_text().strip()
                # Skip empty paragraphs and coordinate listings
                if text and not text.startswith('Coordinates:'):
                    summary_parts.append(text)
                    if len(' '.join(summary_parts)) > 200:
                        break
            
            return ' '.join(summary_parts)[:500] + '...' if summary_parts else ''
        return ''

    def _extract_sections(self) -> List[str]:
        """Extract all section headings"""
        sections = []
        # Find all heading tags (h2, h3)
        headings = self.soup.find_all(['h2', 'h3'])
        
        for heading in headings:
            headline = heading.find('span', class_='mw-headline')
            if headline:
                section_text = headline.get_text().strip()
                # Filter out common non-content sections
                if section_text not in ['Contents', 'References', 'External links', 
                                       'Notes', 'See also', 'Bibliography']:
                    sections.append(section_text)
        
        return sections[:10]  # Limit to 10 main sections

    def _extract_entities(self) -> Dict[str, List[str]]:
        """
        Extract key entities (people, organizations, locations)
        This is a simple implementation - could be enhanced with NER
        """
        entities = {
            'people': [],
            'organizations': [],
            'locations': []
        }

        # Find all links in the article
        content = self.soup.find('div', class_='mw-parser-output')
        if content:
            links = content.find_all('a', href=True, limit=50)
            
            for link in links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                if '/wiki/' in href and ':' not in href and text:
                    # Simple heuristic: categorize based on common patterns
                    if any(word in text for word in ['University', 'College', 'Institute', 
                                                     'Organization', 'Company', 'Corporation']):
                        if text not in entities['organizations']:
                            entities['organizations'].append(text)
                    elif any(word in text for word in ['Kingdom', 'State', 'City', 
                                                       'Country', 'Park']):
                        if text not in entities['locations']:
                            entities['locations'].append(text)
                    else:
                        # Assume it's a person if it's a proper noun
                        if text[0].isupper() and text not in entities['people']:
                            entities['people'].append(text)

        # Limit each category
        entities['people'] = entities['people'][:10]
        entities['organizations'] = entities['organizations'][:10]
        entities['locations'] = entities['locations'][:10]

        return entities

    def _extract_full_text(self) -> str:
        """Extract full article text for LLM processing"""
        content = self.soup.find('div', class_='mw-parser-output')
        if not content:
            return ''

        # Remove unwanted elements
        for element in content.find_all(['table', 'div.reflist', 'div.navbox', 
                                        'div.infobox', 'sup.reference']):
            element.decompose()

        # Get text from all paragraphs
        paragraphs = content.find_all('p')
        text_parts = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            if text and len(text) > 20:  # Filter very short paragraphs
                text_parts.append(text)

        full_text = '\n\n'.join(text_parts)
        
        # Limit text length for LLM (roughly 8000 words)
        words = full_text.split()
        if len(words) > 8000:
            full_text = ' '.join(words[:8000]) + '...'

        return full_text


def validate_wikipedia_url(url: str) -> bool:
    """Validate if the URL is a Wikipedia article"""
    pattern = r'^https?://(en\.)?wikipedia\.org/wiki/[^:]+$'
    return bool(re.match(pattern, url))
