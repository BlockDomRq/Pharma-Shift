    # pharmacy on duty
url = 'https://www.istanbuleczaciodasi.org.tr/print/nobetciler_print.php?t=b&bid=28&d=0&z=17&map_show=1'

    # pharmacy on duty tomorrow
url2 = 'http://www.istanbuleczaciodasi.org.tr/print/nobetciler_print.php?t=b&bid=28&d=1&z=17&map_show=1'

application_path = os.path.join(os.environ["HOME"], "NöbetUygulaması")

    # Trying to enter google.com to check internet connection

def internet_accessible():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=5)
        return True
    except urllib.error.URLError:
        return False
