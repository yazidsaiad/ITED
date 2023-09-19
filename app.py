"""
This file allows you to run the project app.
"""
from multipage import MultiPage
from pages import material_series      # import your page modules here
from pages import activities_duration



app = MultiPage()

# Add all your application here
app.add_page("Séries Matérielles", material_series.app)
app.add_page("Temps d'Activité", activities_duration.app)


# The main app
app.run()