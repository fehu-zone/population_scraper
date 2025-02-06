from selenium.webdriver.common.by import By

def format_number(number_str):
    try:
        if not number_str:
            return None
            
        cleaned = number_str.strip().replace(',', '')
        
        # Bilimsel gösterim kontrolü (örn: 1.2M)
        if 'M' in cleaned:
            return int(float(cleaned.replace('M', '')) * 1_000_000)
        if 'K' in cleaned:
            return int(float(cleaned.replace('K', '')) * 1_000)
            
        return int(cleaned)
    except Exception as e:
        print(f"Format hatası: {e}")
        return None

def extract_number_from_element(element):
    """
    Extract numeric value from Selenium element containing multiple span elements.
    Example: <span class="rts-nr-int">1</span><span class="rts-nr-int">234</span> → 1234
    """
    try:
        # Find all integer parts
        int_spans = element.find_elements(By.XPATH, ".//span[contains(@class, 'rts-nr-int')]")
        
        # Find decimal parts if needed (örnek: 1.234,56 için)
        # dec_spans = element.find_elements(By.XPATH, ".//span[contains(@class, 'rts-nr-dec')]")
        
        # Combine integer parts
        int_part = "".join([span.text for span in int_spans])
        
        # Combine decimal parts if needed
        # dec_part = "".join([span.text for span in dec_spans])
        # full_number = f"{int_part}.{dec_part}" if dec_part else int_part
        
        return format_number(int_part)
        
    except Exception as e:
        print(f"Elementten sayı çıkarılırken hata: {e}")
        return None