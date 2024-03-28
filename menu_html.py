import base64


def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def generate_html_content(gpt_list):
    html_content = "<style>"
    html_content += """
      .avatar-button {
        display: flex;
        align-items: center;
        width: 100%;
        padding: 10px;
        margin: 5px 0;
        border: none;
        border-radius: 5px;
        background-color: #f2f2f2;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
      }
      .avatar-button:hover {
        background-color: #e0e0e0;
      }

      .avatar-button img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
      }

      .avatar-button span {
        font-size: 16px;
      }
    """
    html_content += "</style>"

    for gpt in gpt_list:
        html_content += f"""
        <button class="avatar-button" onclick="stBridges.send('current-gpt', '{gpt['id']}')">
          <img src="data:image/png;base64,{get_image_base64(gpt['image'])}" alt="{gpt['name']}">
          <span>{gpt['name']}</span>
        </button>
        """
    return html_content
