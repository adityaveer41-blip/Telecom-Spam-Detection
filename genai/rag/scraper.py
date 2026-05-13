# Web Scraper — TRAI + FTC Real Documents
import requests
from bs4 import BeautifulSoup
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# STEP 1 — URLs Define Karo

TRAI_URLS = [
    {
        "id": "trai_web_001",
        "url": "http://trai.gov.in/what-spam-or-ucc",
        "title": "TRAI — What is Spam or UCC"
    },
    {
        "id": "trai_web_002",
        "url": "http://www.trai.gov.in/faqcategory/unsolicited-commercial-communicationsucc",
        "title": "TRAI — UCC FAQ and DND Registry"
    },
    {
        "id": "trai_web_003",
        "url": "http://trai.gov.in/complain-or-report-against-ucc",
        "title": "TRAI — How to Complain Against UCC"
    },
    {
        "id": "trai_web_004",
        "url": "https://trai.gov.in/measures-be-taken-avoid-ucc",
        "title": "TRAI — Measures to Avoid UCC"
    },
    {
        "id": "trai_web_005",
        "url": "https://www.trai.gov.in/sites/default/files/2025-02/Regulation_12022025.pdf",
        "title": "TRAI TCCCPR 2025 Amendment Regulations"
    },
]

# STEP 2 — Scraper Function

def scrape_url(url: str, title: str) -> str:
    """
    URL se text content fetch karo
    Input : URL string
    Output: Clean text content
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        print(f"  Fetching: {url[:60]}...")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"   Failed: Status {response.status_code}")
            return None

        # PDF handle karo alag se
        if url.endswith('.pdf'):
            print(f"   PDF detected — extracting text...")
            return extract_pdf_text(response.content, title)

        # HTML parse karo
        soup = BeautifulSoup(response.text, 'html.parser')

        # Unnecessary tags remove karo
        for tag in soup(['script', 'style', 'nav', 'header',
                         'footer', 'aside', 'form', 'button']):
            tag.decompose()

        # Main content dhundo
        main = (soup.find('main') or
                soup.find('div', class_='content') or
                soup.find('div', class_='main-content') or
                soup.find('article') or
                soup.find('body'))

        if main:
            text = main.get_text(separator=' ', strip=True)
            # Clean up extra whitespace
            text = ' '.join(text.split())
            # First 3000 chars — enough for RAG
            text = text[:3000]
            print(f"  Fetched: {len(text)} characters")
            return text
        else:
            print(f"   No content found")
            return None

    except requests.exceptions.Timeout:
        print(f"   Timeout — skipping")
        return None
    except requests.exceptions.ConnectionError:
        print(f"   Connection error — skipping")
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None


def extract_pdf_text(pdf_content: bytes, title: str) -> str:
    """
    PDF se text extract karo
    """
    try:
        import pypdf
        import io
        reader = pypdf.PdfReader(io.BytesIO(pdf_content))
        text = ""
        # First 5 pages enough
        for i, page in enumerate(reader.pages[:5]):
            text += page.extract_text() or ""
            if len(text) > 3000:
                break
        text = ' '.join(text.split())[:3000]
        print(f"   PDF extracted: {len(text)} characters")
        return text
    except ImportError:
        print("   pypdf not installed — pip install pypdf")
        return None
    except Exception as e:
        print(f"   PDF error: {e}")
        return None


# STEP 3 — Scrape All + Return Documents

def scrape_trai_documents() -> list:
    """
    Saare TRAI URLs scrape karo
    Output: list of document dicts
    """
    print("\n" + "="*50)
    print("WEB SCRAPING — TRAI DOCUMENTS")
    print("="*50)

    scraped_docs = []

    for item in TRAI_URLS:
        print(f"\n {item['title']}")
        content = scrape_url(item['url'], item['title'])

        if content and len(content) > 200:
            scraped_docs.append({
                'id': item['id'],
                'title': item['title'],
                'content': content,
                'source': item['url']
            })
            print(f"  Added to knowledge base")
        else:
            print(f"   Skipped — insufficient content")

        # Polite delay — server pe load mat daalo
        time.sleep(2)

    print(f"\n✅ Successfully scraped: {len(scraped_docs)}/{len(TRAI_URLS)} documents")
    return scraped_docs


# STEP 4 — ChromaDB Mein Store Karo

def update_knowledge_base_with_scraped(scraped_docs: list):
    """
    Scraped documents ChromaDB mein add karo
    """
    if not scraped_docs:
        print("⚠️  No documents to add")
        return

    # Pipeline ka collection import karo
    from pipeline import collection

    print("\nUpdating ChromaDB with scraped documents...")

    for doc in scraped_docs:
        try:
            # Agar already exist karta hai toh update karo
            collection.upsert(
                ids=[doc['id']],
                documents=[doc['content']],
                metadatas=[{
                    'title': doc['title'],
                    'source': doc['source'],
                    'type': 'scraped'
                }]
            )
            print(f"   Added: {doc['title'][:50]}")
        except Exception as e:
            print(f"   Error adding {doc['id']}: {e}")

    total = collection.count()
    print(f"\n Knowledge base updated: {total} total documents")


# STEP 5 — Test Karo

if __name__ == "__main__":
    # Scrape karo
    docs = scrape_trai_documents()

    if docs:
        # ChromaDB mein store karo
        update_knowledge_base_with_scraped(docs)

        # Sample content dikho
        print("\n" + "="*50)
        print("SAMPLE SCRAPED CONTENT")
        print("="*50)
        for doc in docs[:2]:
            print(f"\n📄 {doc['title']}")
            print(f"Content preview: {doc['content'][:300]}...")
    else:
        print("\n No documents scraped")
        print("TRAI website unreachable — using manual knowledge base")
