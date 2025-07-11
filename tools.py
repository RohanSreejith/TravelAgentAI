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
        
        msg = """
        <div style='color: white; font-family: sans-serif;'>
            <h3>🧳 Available Travel Packages:</h3>
        """

        for pkg in packages:
            try:
                price = float(pkg.get("price", 0))
                price_str = f"${price:,.2f}"
            except:
                price_str = "N/A"

            msg += """
            <div style='background-color:#222; padding:20px; border-radius:10px; margin-bottom:20px;'>
                <p><b>Title:</b> {title}</p>
                <p><b>Destination:</b> {destination}</p>
                <p><b>Duration:</b> {duration} days</p>
                <p><b>Price:</b> {price}</p>
                <p><b>Description:</b> {description}</p>
            """.format(
                title=pkg.get("title", "N/A"),
                destination=pkg.get("destination", "N/A"),
                duration=pkg.get("duration_days", "N/A"),
                price=price_str,
                description=pkg.get("description", "N/A")
            )

            # Media
            media_list = pkg.get("media", [])
            for media in media_list:
                media_url = media.get("file")
                media_type = media.get("media_type")
                if media_type == "image":
                    msg += f'<img src="{media_url}" style="max-width: 100%; margin-top: 10px; border-radius: 8px;"><br>'
                elif media_type == "video":
                    msg += (
                        f'<video width="100%" controls style="margin-top: 10px; border-radius: 8px;">'
                        f'<source src="{media_url}" type="video/mp4">'
                        "Your browser does not support the video tag."
                        "</video><br>"
                    )

            msg += "</div>"  # close individual package container

        msg += "</div>"  # close outer wrapper


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
    description="Use this tool only when the user explicitly asks to list, show, or view available travel packages.",
    return_direct=True
)

create_package = Tool(
    name="create_package",
    func=_create_package,
    description="Creates a travel package. Format: title | destination | days | price | description",
    return_direct=True
)
