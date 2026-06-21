import requests
from colorama import init, Fore, Style

# initialise colorama
init(autoreset=True)


def mostrar_banner():
    banner = f"""{Fore.RED}
▐▄• ▄  ▄▄▄·      .▄▄ · ▄▄▄ .·▄▄▄▄       ▄▄▄·  ▄▄▄·▪  
 █▌█▌▪▐█ ▄█▪     ▐█ ▀. ▀▄.▀·██▪ ██     ▐█ ▀█ ▐█ ▄███ 
 ·██·  ██▀· ▄█▀▄ ▄▀▀▀█▄▐▀▀▪▄▐█· ▐█▌    ▄█▀▀█  ██▀·▐█·
▪▐█·█▌▐█▪·•▐█▌.▐▌▐█▄▪▐█▐█▄▄▌██. ██     ▐█ ▪▐▌▐█▪·•▐█▌
•▀▀ ▀▀.▀    ▀█▄▀▪ ▀▀▀▀  ▀▀▀ ▀▀▀▀▀•      ▀  ▀ .▀   ▀▀▀
{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}================  Xposed Breach Lookup ================ 
"""
    print(banner)
    print(f"{' ' * 22}{Fore.WHITE}{Style.BRIGHT}Made By: @0xvileness\n")


def consultar_email_breach(email):
    api_url = f"https://api.xposedornot.com/v1/breach-analytics?email={email}"

    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()
        mostrar_resultados(data)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error connecting with the API: {e}")


def mostrar_resultados(data):
    print(f"\n{Fore.CYAN}RESULTS OF THE QUERY {Style.RESET_ALL}")

    # Case: email WITHOUT gaps
    if not data or data.get("ExposedBreaches") is None:
        print(f"\n{Fore.GREEN} No known gaps were found for this email")
        print(f"{Fore.GREEN}Estimated risk: Low  (0/100)")
        return

    breach_metrics = data.get("BreachMetrics") or {}

    # ===== Risk =====
    risk_list = breach_metrics.get("risk") or []
    risk_info = risk_list[0] if risk_list else {}

    risk_label = risk_info.get("risk_label", "Bajo")
    risk_score = risk_info.get("risk_score", 0)

    color = (
        Fore.RED if risk_label == "High"
        else Fore.YELLOW if risk_label == "Medium"
        else Fore.GREEN
    )

    print(f"\n Risk level: {color}{risk_label} ({risk_score}/100)")

    # ===== Summary of Breaches =====
    sites = data.get("BreachesSummary", {}).get("site", "")
    site_list = [s for s in sites.split(";") if s]

    print(f"\n Breaches Found: {Fore.WHITE}{len(site_list)}")
    print(f"Affected sites : {Fore.WHITE}{', '.join(site_list)}")

    # ===== Industries  =====
    industry_list = breach_metrics.get("industry") or []
    if industry_list:
        print(f"\n Breaches For Industry:")
        for industry in industry_list[0]:
            if industry[1] > 0:
                print(f"  {Fore.CYAN}{industry[0]}: {Fore.WHITE}{industry[1]} brecha(s)")

    # ===== Passwords =====
    passwords = breach_metrics.get("passwords_strength") or []
    if passwords:
        pwd = passwords[0]
        print(f"\n Status of exposed passwords:")
        print(f"  {Fore.RED}Easy to crack: {pwd.get('EasyToCrack', 0)}")
        print(f"  {Fore.YELLOW}Plain Text: {pwd.get('PlainText', 0)}")
        print(f"  {Fore.GREEN}Hash Strong: {pwd.get('StrongHash', 0)}")
        print(f"  {Fore.BLUE}Unknown: {pwd.get('Unknown', 0)}")

    # ===== Details Of Breaches =====
    breaches = data.get("ExposedBreaches", {}).get("breaches_details", [])
    if breaches:
        print(f"\n Details Of The Breaches:")
        for breach in breaches:
            print(f"\n{Fore.MAGENTA}➤ {breach.get('breach', 'Desconocido')} ({breach.get('industry', '?')})")
            print(f"   Year: {breach.get('xposed_date', '?')}")
            print(f"   Affected records: {breach.get('xposed_records', '?')}")
            print(f"   Exposed data: {breach.get('xposed_data', '?')}")
            print(f"   Reference: {breach.get('references', '?')}")
            print(f"   Details: {breach.get('details', '')[:1000]}...")


if __name__ == "__main__":
    mostrar_banner()
    print(f"{Fore.CYAN} Verification of security breaches by email")
    email = input(f"{Fore.WHITE}Enter your email address: ")
    consultar_email_breach(email)
