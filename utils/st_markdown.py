def format_str(
        text,
        font_size=16,
        back_color=(240, 186, 78),
        border_color=(240, 186, 78),
        font_color=(0, 0, 0),
        border_width=1,
        border_radius=0.35,
        line_height=1,
        padding_tb=0.65,
        padding_lr=0.65,
        margin_tb=0.5,
        margin_lr=0.5,
):
    """
    Format a string to be displayed in a Markdown cell.
    :return: formatted string
    """
    return f'''<span style="
    font-size:{font_size}px; 
    background: rgb{back_color};
    color: rgb{font_color}; 
    padding: {padding_tb}em {padding_lr}em; 
    margin: {margin_tb}em {margin_lr}em;
    margin-top: 4%; 
    line-height:{line_height};
    border: {border_width}px solid rgb{border_color}; 
    border-radius: {border_radius}em;
    ">{text}</span>'''
