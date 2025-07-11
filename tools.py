from langchain.tools import Tool
import requests

API_BASE = "https://travelagentbackend.onrender.com/api/"
AUTH = ("rohansreejith05", "Rohan333$")

def _get_packages(_input: str) -> str:
    try:
        res = requests.get(f"{API_BASE}packages/", auth=AUTH, timeout=10)
        res.raise_for_status()
        packages = res.json()

        if not packages:
            return "❗ No packages found."

        msg = "🧳 **Available Travel Packages:**\n"
        for pkg in packages:
            try:
                price = float(pkg.get("price", 0))
                price_str = f"${price:,.2f}"
            except:
                price_str = "N/A"

            msg += (
                f"\n---\n"
                f"**ID:** {pkg.get('id', 'N/A')}\n"
                f"**Title:** {pkg.get('title', 'N/A')}\n"
                f"**Destination:** {pkg.get('destination', 'N/A')}\n"
                f"**Duration:** {pkg.get('duration_days', 'N/A')} days\n"
                f"**Price:** {price_str}\n"
                f"**Description:** {pkg.get('description', 'N/A')}\n"
            )
        return msg

    except requests.exceptions.RequestException as e:
        return f"❌ Error fetching packages: {e}"

def _create_package(input_str: str) -> str:
    try:
        parts = [p.strip() for p in input_str.split("|")]
        if len(parts) != 5:
            return "❗ Format: title | destination | days | price | description"

        days = int(parts[2])
        price = float(parts[3])

        payload = {
            "title": parts[0],
            "destination": parts[1],
            "duration_days": days,
            "price": price,
            "description": parts[4]
        }

        res = requests.post(f"{API_BASE}packages/", json=payload, auth=AUTH, timeout=10)
        res.raise_for_status()
        pkg = res.json()

        return (
            f"✅ Package created:\n"
            f"🆔 ID: {pkg.get('id')}\n"
            f"🏷️ Title: {pkg.get('title')}\n"
            f"📍 Destination: {pkg.get('destination')}\n"
            f"📅 Duration: {pkg.get('duration_days')} days\n"
            f"💰 Price: ${pkg.get('price'):,.2f}\n"
            f"📝 Description: {pkg.get('description')}"
        )

    except Exception as e:
        return f"❌ Error creating package: {e}"

get_packages = Tool(
    name="get_packages",
    func=_get_packages,
    description="Fetches all travel packages. Input is ignored.",
    return_direct=True
)

create_package = Tool(
    name="create_package",
    func=_create_package,
    description="Creates a travel package. Format: title | destination | days | price | description",
    return_direct=True
)
