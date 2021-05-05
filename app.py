from load_page_dash import layout as layout_load
from server import app
from navbar import navbar as layout_navbar
app.layout = layout_navbar

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=True)

# 0.883 m3 to MT
