from bs4 import BeautifulSoup

def parse_case_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Get the row in the result table
        row = soup.select_one('#caseTable tbody tr')
        if not row:
            return { "error": "No case data found." }

        # Extract cells (tds)
        cells = row.find_all('td')
        if len(cells) < 4:
            return { "error": "Unexpected table structure." }

        case_no = cells[1].get_text(strip=True, separator=' ')
        parties = cells[2].get_text(strip=True, separator=' ')
        listing_info = cells[3].get_text(strip=True, separator=' ')
        
        # Extract hearing dates and court no
        next_hearing = ""
        last_hearing = ""
        court_no = ""
        for line in listing_info.splitlines():
            if "NEXT DATE" in line:
                next_hearing = line.replace("NEXT DATE:", "").strip()
            elif "Last Date" in line:
                last_hearing = line.replace("Last Date:", "").strip()
            elif "COURT NO" in line:
                court_no = line.replace("COURT NO:", "").strip()
        
        # Extract order PDF link
        pdf_link = None
        link_tag = cells[1].find('a', string="Orders")
        if link_tag and link_tag.has_attr('href'):
            pdf_link = link_tag['href']

        return {
            "case_no": case_no,
            "parties": parties,
            "next_hearing": next_hearing,
            "last_hearing": last_hearing,
            "court_no": court_no,
            "pdf_link": pdf_link
        }

    except Exception as e:
        return { "error": "Failed to parse HTML", "details": str(e) }
