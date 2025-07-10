from langchain.tools import Tool
import requests

API_BASE = "http://localhost:8000/api/"
AUTH = ("rohansreejith05", "Rohan333$")

def _get_packages(_input: str) -> str:
    try:
        response = requests.get(f"{API_BASE}packages/", auth=AUTH, timeout=10)
        response.raise_for_status()
        packages = response.json()

        if not packages:
            return "❗ No travel packages found."

        result = "🧳 **Available Travel Packages:**\n"
        for pkg in packages:
            result += (
                f"\n---\n"
                f"**ID:** {pkg.get('id', 'N/A')}\n"
                f"**Title:** {pkg.get('title', 'N/A')}\n"
                f"**Destination:** {pkg.get('destination', 'N/A')}\n"
                f"**Duration:** {pkg.get('duration_days', 'N/A')} days\n"
                f"**Price:** ${pkg.get('price', 0):,.2f}\n"
                f"**Description:** {pkg.get('description', 'N/A')}\n"
            )
        return result

    except requests.exceptions.RequestException as e:
        return f"❌ Error fetching packages: {e}"

def _create_package(input_str: str) -> str:
    try:
        parts = [p.strip() for p in input_str.split("|")]
        if len(parts) != 5:
            return "❗ Format: title | destination | days | price | description"

        try:
            days = int(parts[2])
        except ValueError:
            return "❗ 'days' must be an integer."

        try:
            price = float(parts[3])
        except ValueError:
            return "❗ 'price' must be a number."

        data = {
            "title": parts[0],
            "destination": parts[1],
            "duration_days": days,
            "price": price,
            "description": parts[4],
        }

        response = requests.post(f"{API_BASE}packages/", json=data, auth=AUTH, timeout=10)
        response.raise_for_status()
        created = response.json()

        return (
            f"✅ **Package Created Successfully!**\n"
            f"**ID:** {created.get('id')}\n"
            f"**Title:** {created.get('title')}\n"
            f"**Destination:** {created.get('destination')}\n"
            f"**Duration:** {created.get('duration_days')} days\n"
            f"**Price:** ${created.get('price'):,.2f}\n"
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
    description="Creates a package. Input: 'title | destination | days | price | description'"
)
