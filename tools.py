from langchain.tools import Tool
import requests

API_BASE = "https://travelagentbackend.onrender.com/api/"
AUTH = ("rohansreejith05", "Rohan333$")

def _get_packages(_input: str) -> dict:
    try:
        res = requests.get(f"{API_BASE}packages/", auth=AUTH, timeout=10)
        res.raise_for_status()
        packages = res.json()

        if not packages:
            return {"output": "❗ No packages found."}

        msg = "🧳 <b>Available Travel Packages:</b><br><br>"
        for pkg in packages:
            try:
                price = float(pkg.get("price", 0))
                price_str = f"${price:,.2f}"
            except:
                price_str = "N/A"

            msg += (
                f"<div style='margin-bottom:20px;'>"
                f"<b>Title:</b> {pkg.get('title', 'N/A')}<br>"
                f"<b>Destination:</b> {pkg.get('destination', 'N/A')}<br>"
                f"<b>Duration:</b> {pkg.get('duration_days', 'N/A')} days<br>"
                f"<b>Price:</b> {price_str}<br>"
                f"<b>Description:</b> {pkg.get('description', 'N/A')}<br>"
                f"</div>"
            )

        return msg

    except requests.exceptions.RequestException as e:
        return {"output": f"❌ Error fetching packages: {e}"}


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
            f"✅ Package created:<br>"
            f"🆔 ID: {pkg.get('id')}<br>"
            f"🏷️ Title: {pkg.get('title')}<br>"
            f"📍 Destination: {pkg.get('destination')}<br>"
            f"📅 Duration: {pkg.get('duration_days')} days<br>"
            f"💰 Price: ${pkg.get('price'):,.2f}<br>"
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
