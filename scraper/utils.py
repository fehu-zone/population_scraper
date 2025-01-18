from selenium.webdriver.common.by import By

def format_number(number_str):
    """String'deki sayıları temizleyip int'e dönüştürür."""
    try:
        return int(number_str.replace(',', '').strip())
    except ValueError:
        return None



def extract_number_from_element(element):
    """
    HTML içindeki birden fazla span yapısından sayıyı birleştirir ve tam sayı olarak döndürür.
    
    Args:
        element (WebElement): Sayıyı içeren HTML elementi.
        
    Returns:
        int: Birleştirilmiş tam sayı.
        None: Hata oluşursa veya sayı bulunamazsa.
    """
    try:
        spans = element.find_elements(By.XPATH, ".//span[contains(@class, 'rts-nr-int')]")
        if not spans:
            print("Elementte sayı bulunamadı.")
            return None
        number_str = "".join([span.text for span in spans])
        return format_number(number_str)
    except Exception as e:
        print(f"Sayı verisi alınırken hata oluştu: {e}")
        return None

