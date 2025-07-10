from langchain.tools import Tool
import requests

API_BASE = "https://travelagentbackend.onrender.com/api/"
AUTH = ("rohansreejith05", "Rohan333$")

def _get_packages(_input: str) -> str:
    try:
        response = requests.get(f"{API_BASE}packages/", auth=AUTH, timeout=15)
        response.raise_for_status()
        packages = response.json()

        if not packages:
            return "No travel packages found."

        formatted = "### 🧳 Travel Packages:\n"
        for pkg in packages:
            formatted += (
                f"---\n"
                f"**ID:** {pkg['id']}\n"
                f"**Title:** {pkg['title']}\n"
                f"**Destination:** {pkg['destination']}\n"
                f"**Duration:** {pkg['duration_days']} days\n"
                f"**Price:** ${pkg['price']}\n"
                f"**Description:** {pkg['description']}\n\n"
            )
        return formatted
    except requests.exceptions.RequestException as e:
        return (
            f"❌ Error fetching packages: {e}\n"
            f"Status Code: {getattr(e.response, 'status_code', 'N/A')}\n"
            f"Details: {getattr(e.response, 'text', '')}"
        )

def _create_package(input_str: str) -> str:
    try:
        parts = [p.strip() for p in input_str.split("|")]
        if len(parts) != 5:
            return "❗ Invalid format. Use: title | destination | days | price | description"

        data = {
            "title": parts[0],
            "destination": parts[1],
            "duration_days": int(parts[2]),
            "price": float(parts[3]),
            "description": parts[4],
        }

        response = requests.post(f"{API_BASE}packages/", json=data, auth=AUTH, timeout=10)
        response.raise_for_status()
        created = response.json()

        return (
            f"✅ **Package Created Successfully!**\n\n"
            f"**ID:** {created.get('id')}\n"
            f"**Title:** {created.get('title')}\n"
            f"**Destination:** {created.get('destination')}\n"
            f"**Duration:** {created.get('duration_days')} days\n"
            f"**Price:** ${created.get('price')}\n"
            f"**Description:** {created.get('description')}"
        )
    except Exception as e:
        return f"❌ Error creating package: {str(e)}"

get_packages = Tool(
    name="get_packages",
    func=_get_packages,
    description="Fetches all travel packages. Input is ignored."
)

create_package = Tool(
    name="create_package",
    func=_create_package,
    description="Creates a travel package. Input format: 'title | destination | days | price | description'"
)
